import os
import requests

NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

def upload_to_notion(article):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": article['title']}}]
            },
            "Source": {
                "rich_text": [{"text": {"content": article['source']}}]
            },
            "Date": {
                "date": {"start": article['date']}
            },
            "Long Summary": {
                "rich_text": [{"text": {"content": article['summary'][:2000]}}]
            },
            "Sector": {
                "select": {"name": article['sector']}
            },
            "Impact": {
                "select": {"name": article['impact']}
            },
            "Reasoning": {
                "rich_text": [{"text": {"content": article['reasoning'][:2000]}}]
            },
            "Added By": {
                "rich_text": [{"text": {"content": "Automated Bot"}}]
            }
        }
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        print("Failed to upload to Notion:", res.text)
    else:
        print("Uploaded to Notion:", article['title'])
