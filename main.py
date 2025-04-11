import os
from dotenv import load_dotenv
from scraper import scrape_all_sources
from summarizer import summarize_article
from notion import push_to_notion

# Load environment variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def main():
    print("🔍 Scraping started...")

    # Step 1: Scrape all news articles
    articles = scrape_all_sources()

    print(f"✅ Scraped {len(articles)} articles")

    for article in articles:
        try:
            # Step 2: Summarize each article
            summary, reasoning, sector, impact = summarize_article(article['url'], article['title'])

            # Step 3: Push to Notion
            push_to_notion(
                NOTION_TOKEN,
                NOTION_DATABASE_ID,
                {
                    "title": article['title'],
                    "source": article['source'],
                    "url": article['url'],
                    "date": article['date'],
                    "summary": summary,
                    "reasoning": reasoning,
                    "sector": sector,
                    "impact": impact
                }
            )

            print(f"✅ Pushed to Notion: {article['title']}")

        except Exception as e:
            print(f"❌ Error processing article: {article['title']} – {e}")

if __name__ == "__main__":
    main()
