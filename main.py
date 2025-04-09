import os
import requests
from bs4 import BeautifulSoup
from notion_client import Client
import openai
from datetime import datetime

# Environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup clients
notion = Client(auth=NOTION_TOKEN)
openai.api_key = OPENAI_API_KEY

# News source URLs (can be expanded later)
NEWS_SOURCES = {
    "Economic Times": "https://economictimes.indiatimes.com/news/economy",
    "Mint": "https://www.livemint.com/economy",
    "Business Standard": "https://www.business-standard.com/economy-policy",
    "The Hindu Business Line": "https://www.thehindubusinessline.com/economy/",
    "Moneycontrol": "https://www.moneycontrol.com/news/business/"
}

def fetch_article_links(source_url):
    try:
        res = requests.get(source_url, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        links = list({a.get("href") for a in soup.find_all("a", href=True)})
        return [link for link in links if link and link.startswith("http")]
    except Exception as e:
        print(f"Error fetching links from {source_url}: {e}")
        return []

def is_fundamental(text):
    keywords = [
        "policy", "inflation", "FDI", "GDP", "fiscal", "reform", "infrastructure",
        "investment", "budget", "disinvestment", "manufacturing", "macroeconomic"
    ]
    return any(word in text.lower() for word in keywords)

def summarize_article(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this news article in simple English with deep reasoning on its long-term impact."},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return None

def extract_content(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text.strip()
    except Exception as e:
        print(f"Failed to extract content from {url}: {e}")
        return None

def create_notion_entry(title, source, summary, reasoning, sector="General", impact="Neutral"):
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Date": {"date": {"start": datetime.utcnow().isoformat()}},
                "Title": {"title": [{"text": {"content": title}}]},
                "Source": {"rich_text": [{"text": {"content": source}}]},
                "Long Summary": {"rich_text": [{"text": {"content": summary}}]},
                "Sector": {"select": {"name": sector}},
                "Impact": {"select": {"name": impact}},
                "Reasoning": {"rich_text": [{"text": {"content": reasoning}}]},
                "Added By": {"rich_text": [{"text": {"content": "Automated Script"}}]},
            }
        )
        print(f"✅ Added: {title}")
    except Exception as e:
        print(f"Failed to add entry to Notion: {e}")

def run_news_pipeline():
    for source, url in NEWS_SOURCES.items():
        links = fetch_article_links(url)[:5]
        for link in links:
            content = extract_content(link)
            if not content or not is_fundamental(content):
                continue
            summary = summarize_article(content)
            if not summary:
                continue
            reasoning = f"This news is likely to impact the Indian economy or businesses in the long term because it touches on key policy or macroeconomic factors."
            create_notion_entry(title=link.split("/")[-1][:80], source=source, summary=summary, reasoning=reasoning)

if __name__ == "__main__":
    run_news_pipeline()
