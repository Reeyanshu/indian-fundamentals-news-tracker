import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary_and_reasoning(article_text):
    prompt = f"""
You are an expert financial analyst. Read the article below and provide:
1. A long, clear summary in simple English (200-300 words).
2. Whether this news is fundamentally significant in the long term. If yes, explain why.
3. Sector involved and impact (Positive, Negative, Neutral).

Article:
{article_text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error summarizing:", e)
        return None
