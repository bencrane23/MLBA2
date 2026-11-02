import os

import pandas as pd
import plotly.express as px
import streamlit as st

from labeler import label_comment

# ---- Settings ----------------------------------------------------------
TITLE = "Mystery Meat Market"
ICON = "🍖"
LOW_RATING = 2                      # 2 stars or fewer is low
CSV_FILE = "feedback.csv"
VENDORS = ["Sketchy Sausage Shack", "Dumpling Roulette", "Fry Day Fryers", "Gloomy Pies"]
COLORS = {"safety": "#B3261E", "food quality": "#B34700", "service and wait": "#C98A00",
          "cleanliness and space": "#4A7FB5", "praise": "#2BB38A", "other": "#A0A0A0",
          "unclear": "#D0D0D0"}
# ------------------------------------------------------------------------

st.set_page_config(page_title=TITLE, page_icon=ICON, layout="wide")
st.title(f"{ICON} {TITLE}")
st.caption("Customers leave feedback. The app labels it and saves it. The manager reviews it later.")

# Load the saved feedback, or start with an empty table
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE).fillna({"vendor": "", "comment": "", "label": ""})
    df["rating"] = pd.to_numeric(df["rating"]).astype("Int64")
else:
    df = pd.DataFrame(columns=["vendor", "comment", "rating", "label"])

tab_customer, tab_owner = st.tabs(["Customer: leave feedback", "Manager: review the feedback"])

# ---- Customer tab: pick a stall, type feedback, pick stars, get a label, save --
with tab_customer:
    st.subheader("Tell us about your visit")
    with st.form("feedback_form", clear_on_submit=True):
        vendor = st.selectbox("Which stall?", VENDORS, index=None, placeholder="Choose a stall")
        comment = st.text_area("Your comment (optional)")
        stars = st.feedback("stars")          # nothing until clicked, then 0 to 4
        submitted = st.form_submit_button("Send feedback")

    if submitted:
        if vendor is None:
            st.error("Please choose a stall.")
        elif not comment.strip() and stars is None:
            st.error("Please type a comment, choose a star rating, or both.")
        else:
            label = ""                        # a rating with no comment has no label
            if comment.strip():
                try:
                    label = label_comment(comment.strip())
                except Exception:             # API down, rate limit, bad key: keep the comment
                    label = "unclear"
            rating = None if stars is None else stars + 1
            new_row = pd.DataFrame([{"vendor": vendor, "comment": comment.strip(), "rating": rating, "label": label}])
            pd.concat([df, new_row], ignore_index=True).to_csv(CSV_FILE, index=False)
            st.success("Thank you for your feedback!")
            if label:
                st.caption(f"Behind the scenes, the app labeled it: {label}")
            df = pd.read_csv(CSV_FILE).fillna({"vendor": "", "comment": "", "label": ""})
            df["rating"] = pd.to_numeric(df["rating"]).astype("Int64")

# ---- Manager tab: review the feedback ---------------------------------------
with tab_owner:
    if df.empty:
        st.info("No feedback yet. Switch to the customer tab and add the first comment.")
    else:
        stall = st.selectbox("Which stall?", ["All stalls"] + VENDORS)
        view = df if stall == "All stalls" else df[df["vendor"] == stall]
        if view.empty:
            st.info("No feedback for this stall yet.")
            st.stop()

        labeled = view[view["label"] != ""]   # only comments the model labeled

                # Comments to read now: safety, food quality, an unclear label, or praise with a low rating
        flag = (view["label"] == "safety") \
             | (view["label"] == "food quality") \
             | (view["label"] == "unclear") \
             | ((view["label"] == "praise") & (view["rating"] <= LOW_RATING))
        flag = flag.fillna(False)

        st.subheader("What are customers saying?")
        m1, m2, m3 = st.columns(3)
        m1.metric("Comments received", len(view))
        m2.metric("Average stars", f"{view['rating'].mean():.1f}" if view["rating"].notna().any() else "n/a")
        m3.metric("Read these now", int(flag.sum()))

        col1, col2 = st.columns(2)

        with col1:
            st.caption("Number of comments by label")
            counts = labeled["label"].value_counts().rename_axis("label").reset_index(name="count")
            fig = px.bar(counts, x="label", y="count", color="label", text="count",
                         color_discrete_map=COLORS)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Comments")
            st.plotly_chart(fig, width="stretch")

        with col2:
            st.caption("Average stars by label")
            avg = labeled.dropna(subset=["rating"]).groupby("label")["rating"].mean().round(1).reset_index()
            fig = px.bar(avg, x="label", y="rating", color="label", text="rating",
                         color_discrete_map=COLORS, range_y=[0, 5])
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Average stars")
            st.plotly_chart(fig, width="stretch")

        st.subheader("Read these now")
        st.caption("Labeled safety or food quality, labeled unclear, or labeled praise with a low rating (1 or 2 stars).")
        st.table(view[flag].reset_index(drop=True))

        with st.expander("All feedback"):
            st.dataframe(view, hide_index=True, width="stretch")
        st.download_button("Download CSV", df.to_csv(index=False), file_name="feedback.csv")
        st.caption("On the free Streamlit Cloud, the saved file can disappear when the app restarts. "
                   "Download your CSV to keep it.")
