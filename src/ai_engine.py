import os
import re
from groq import Groq

# Initialize client using environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------------
# STEP 1: Split notes into blocks
# -------------------------------
def split_notes(notes_text):
    return notes_text.split("\n---\n")


# -------------------------------
# STEP 2: Extract account_id
# -------------------------------
def extract_account_id(note):
    match = re.search(r'\b(10\d{2})\b', note)
    if match:
        return int(match.group(1))
    return None


# -------------------------------
# STEP 3: AI Analysis
# -------------------------------
def analyze_notes(notes_text):
    prompt = f"""
You are a customer success analyst.

Analyze the following customer notes and extract:

1. Overall sentiment (Positive / Neutral / Negative)
2. Key issues mentioned
3. Any churn or risk signals

Notes:
{notes_text}

Return output in this format:
Sentiment:
Issues:
Risk:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return "AI analysis failed"