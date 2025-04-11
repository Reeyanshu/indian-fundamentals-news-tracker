from transformers import pipeline

# Load the BART summarizer from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    # BART works well with inputs under 1024 tokens
    max_chunk_size = 1000

    if len(text) > max_chunk_size:
        text = text[:max_chunk_size]  # Truncate long articles

    summary = summarizer(text, max_length=300, min_length=100, do_sample=False)
    return summary[0]['summary_text']
