# Mystery Meat Market: feedback labeling app (Homework 2)

Adapted from the course's Slice Street Pizza starter app (46-887). The business, question, labels, prompt rules, flag rule and demo comments are my own.

**Business:** Mystery Meat Market, a fictional food hall with four vendor stalls (Sketchy Sausage Shack, Dumpling Roulette, Fry Day Fryers, Gloomy Pies) and shared seating.

**Question the labels help answer:** Which safety and food quality problems should the manager follow up on now?

**Labels** (each comment gets exactly one):
- **safety:** illness, an allergen mix-up, a foreign object, or a hygiene concern.
- **food quality:** a problem with the taste, temperature, freshness or portion of the food itself.
- **service and wait:** a problem with long lines, slow orders, staff attitude, or how an issue was handled.
- **cleanliness and space:** a problem with dirty tables, restrooms or trash, or with seating, noise and crowding.
- **praise:** a positive comment with nothing to fix.
- **other:** questions, vague comments like "Fine.", and anything that fits none of the above.

If the model returns anything else, the app records the label as `unclear`.

**Customer tab:** choose a stall, then type a comment, choose stars, or both. The app labels the comment with an LLM (Groq) and saves it to `feedback.csv`.

**Manager tab:** filter by stall; see comments received, average stars, comments by label, average stars by label, and the comments to read now (labeled safety or food quality, labeled unclear, or labeled praise with 1 or 2 stars).

## Files
- `app2.py`: the Streamlit app
- `labeler.py`: asks the LLM for a label
- `demo_comments.csv`: 20 fictional comments with stalls and ratings to type in; not loaded automatically
- `requirements.txt`: packages Streamlit Cloud installs

## Run it online
Public GitHub repo, then share.streamlit.io with main file `app2.py`. Under Advanced settings, add the secret `GROQ_API_KEY = "your key"`. The key is never stored in GitHub.
