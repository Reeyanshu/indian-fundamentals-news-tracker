import requests
from bs4 import BeautifulSoup

def scrape_news():
    headlines = []

    sources = {
        "Economic Times": "https://economictimes.indiatimes.com/news/economy",
        "Business Standard": "https://www.business-standard.com/economy",
        "Moneycontrol": "https://www.moneycontrol.com/news/business/",
        "Mint": "https://www.livemint.com/economy",
        "The Hindu Business Line": "https://www.thehindubusinessline.com/economy/"
    }

    for source, url in sources.items():
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all("a", href=True):
                title = link.text.strip()
                href = link['href']
                if title and href.startswith("http"):
                    headlines.append({"title": title, "url": href, "source": source})
        except Exception as e:
            print(f"Error scraping {source}: {e}")

    return headlines
