from transformers import pipeline

# Load the summarization model (you can switch to BART, Pegasus, etc.)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_article(url, title):
    text = f"{title} - {url}"  # Replace with actual article text extraction logic
    summary = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']

    reasoning = "This news may have a long-term impact based on government policy/economic indicators."
    sector = "General"
    impact = "Neutral"

    return summary, reasoning, sector, impact
