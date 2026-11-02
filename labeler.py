import requests
import streamlit as st

# ---- Settings ----------------------------------------------------------
BUSINESS = "Mystery Meat Market, a food hall with several vendor stalls and shared seating"
LABELS = ["safety", "food quality", "service and wait", "cleanliness and space", "praise", "other"]
GUIDE = """Label the comment with exactly one of these labels:
safety: illness, an allergen mix-up, a foreign object, or a hygiene concern.
food quality: a problem with the taste, temperature, freshness or portion of the food itself.
service and wait: a problem with long lines, slow orders, staff attitude, or how an issue was handled.
cleanliness and space: a problem with dirty tables, restrooms or trash, or with seating, noise and crowding.
praise: a positive comment with nothing to fix.
other: questions, vague comments like 'Fine.', and anything that fits none of the above.
Reply with only the label.
If a comment could be safety, label it safety.
Undercooked or spoiled food counts as safety.
An allergen mix-up or illness is safety even if the customer is thankful or the issue was fixed.
If it has praise and a problem, label by the problem.
Sarcasm is labeled by what it complains about."""
MODEL = "openai/gpt-oss-20b"   # if you get a 404, the model was retired: see console.groq.com/docs/models
URL = "https://api.groq.com/openai/v1/chat/completions"
# ------------------------------------------------------------------------


def label_comment(text):
    key = st.secrets["GROQ_API_KEY"]
    prompt = f"You label customer comments for {BUSINESS}.\n{GUIDE}\n\nComment: {text}"
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]
    label = answer.strip().lower()
    return label if label in LABELS else "unclear"
