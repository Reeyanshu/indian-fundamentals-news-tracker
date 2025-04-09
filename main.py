from news_scraper import scrape_news
from summarizer import generate_summary_and_reasoning
from notion_uploader import upload_to_notion
import datetime
import requests

def fetch_article_text(url):
    try:
        res = requests.get(url, timeout=10)
        return res.text if res.status_code == 200 else None
    except:
        return None

def parse_summary_response(response):
    # Assume response is well-formatted with newline sections
    lines = response.split("\n")
    summary = []
    reasoning = []
    sector = "General"
    impact = "Neutral"

    collecting_summary = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "2." in line:
            collecting_summary = False
            continue
        if "3." in line:
            continue

        if collecting_summary:
            summary.append(line)
        else:
            reasoning.append(line)
            if "sector" in line.lower():
                sector = line.split(":")[-1].strip().title()
            if "impact" in line.lower():
                impact = line.split(":")[-1].strip().title()

    return {
        "summary": " ".join(summary),
        "reasoning": " ".join(reasoning),
        "sector": sector if sector else "General",
        "impact": impact if impact in ["Positive", "Negative", "Neutral"] else "Neutral"
    }

def main():
    print("🚀 Starting News Tracker...")
    articles = scrape_news()

    for article in articles[:5]:  # Limit to first 5 for safety
        print(f"🔍 Processing: {article['title']}")
        article_text = fetch_article_text(article['url'])
        if not article_text:
            print("❌ Failed to fetch article text.")
            continue

        summary_response = generate_summary_and_reasoning(article_text)
        if not summary_response:
            print("❌ Failed to summarize.")
            continue

        parsed = parse_summary_response(summary_response)

        article_data = {
            "title": article["title"],
            "source": article["source"],
            "summary": parsed["summary"],
            "reasoning": parsed["reasoning"],
            "sector": parsed["sector"],
            "impact": parsed["impact"],
            "date": datetime.date.today().isoformat()
        }

        upload_to_notion(article_data)

    print("✅ All Done!")

if __name__ == "__main__":
    main()
