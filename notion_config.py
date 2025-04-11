import os
from notion_client import Client
from dotenv import load_dotenv

# Load the environment variables (your Notion token + database ID)
load_dotenv()

# Create a Notion client
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

# Function to add a news article to Notion
def add_news_to_notion(title, source, summary, sector, impact, reasoning):
    from datetime import datetime
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Title": {"title": [{"text": {"content": title}}]},
            "Source": {"rich_text": [{"text": {"content": source}}]},
            "Date": {"date": {"start": datetime.utcnow().isoformat()}},
            "Summary": {"rich_text": [{"text": {"content": summary}}]},
            "Sector": {"select": {"name": sector}},
            "Impact": {"select": {"name": impact}},
            "Reasoning": {"rich_text": [{"text": {"content": reasoning}}]},
            "Added By": {"rich_text": [{"text": {"content": "Automation"}}]}
        }
    )
