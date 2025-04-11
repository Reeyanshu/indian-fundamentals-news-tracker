import requests
import datetime

def push_to_notion(token, database_id, article):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": { "database_id": database_id },
        "properties": {
            "Title": { "title": [{ "text": { "content": article["title"] } }] },
            "Source": { "rich_text": [{ "text": { "content": article["source"] } }] },
            "Date": { "date": { "start": article["date"] } },
            "Long Summary": { "rich_text": [{ "text": { "content": article["summary"] } }] },
            "Reasoning": { "rich_text": [{ "text": { "content": article["reasoning"] } }] },
            "Sector": { "select": { "name": article["sector"] } },
            "Impact": { "select": { "name": article["impact"] } },
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Notion API error: {response.text}")
