import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_mint():
    url = "https://www.livemint.com/news/india"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = []

    for item in soup.select("a.card-wrap"):
        title = item.get("title")
        link = "https://www.livemint.com" + item.get("href")
        date = datetime.now().strftime("%Y-%m-%d")
        articles.append({
            "title": title,
            "url": link,
            "source": "Mint",
            "date": date
        })

    return articles

def scrape_all_sources():
    all_articles = []
    try:
        all_articles.extend(scrape_mint())
        # TODO: Add other websites here
    except Exception as e:
        print(f"❌ Error scraping source: {e}")
    return all_articles
