import streamlit as st
import pandas as pd
import json
import time
import os
from collections import Counter

st.set_page_config(page_title="Internet Pulse Dashboard", layout="wide")

LATEST_FILE = os.path.expanduser("~/internet-pulse-platform/data_lake/latest_news.json")


def load_latest_news():
    if not os.path.exists(LATEST_FILE):
        return pd.DataFrame()

    try:
        with open(LATEST_FILE, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        st.error(f"Error reading JSON: {e}")
        return pd.DataFrame()


st.title("🌐 Internet Pulse Dashboard")

tab1, tab2 = st.tabs(["Latest News", "Metrics"])

news_df = load_latest_news()

# -------------------------
# TAB 1 : Latest News
# -------------------------
with tab1:

    st.subheader("Latest News (100 Buffer)")

    if news_df.empty:
        st.warning("No news yet")
    else:
        st.dataframe(news_df.tail(100).reset_index(drop=True).rename_axis(None).set_axis(range(1,101)), use_container_width=True)


# -------------------------
# TAB 2 : Metrics
# -------------------------
# -------------------------
# TAB 2 : Metrics
# -------------------------
with tab2:
    st.subheader("Analytics")

    if news_df.empty:
        st.warning("No data available for metrics")
    else:
        col1, col2 = st.columns(2)

        # -------------------------
        # TOP AUTHORS TABLE
        # -------------------------
        with col1:
            st.write("### Top Authors")

            if "author" in news_df.columns:
                # Fill missing values and count occurrences
                authors = news_df["author"].fillna("Unknown")
                top_authors = Counter(authors).most_common(10)

                # Create the DataFrame
                authors_df = pd.DataFrame(
                    top_authors, columns=["Author", "Article Count"]
                )

                # Insert S.No column at the start
                authors_df.insert(0, "S.No", range(1, len(authors_df) + 1))

                # Display the table without the default pandas index
                st.table(authors_df) # Streamlit versions 1.35+ support hide_index=True here

        # -------------------------
        # HOURLY ARTICLE TIMELINE
        # -------------------------
        with col2:
            st.write("### Articles Published Per Hour")

            if "published" in news_df.columns:
                timeline_df = news_df.copy()
                timeline_df["published"] = pd.to_datetime(
                    timeline_df["published"], errors="coerce"
                )
                
                # Drop rows where date conversion failed
                timeline_df = timeline_df.dropna(subset=["published"])

                timeline_df["hour"] = timeline_df["published"].dt.floor("H")

                hourly_counts = (
                    timeline_df.groupby("hour")
                    .size()
                    .reset_index(name="articles")
                    .sort_values("hour")
                )

                st.line_chart(hourly_counts.set_index("hour"))

st.markdown("---")
st.caption("Dashboard updates automatically every 5 seconds")

time.sleep(5)
st.rerun()