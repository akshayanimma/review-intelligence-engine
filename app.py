import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Customer Support & Review Intelligence", 
    page_icon="📊",
    layout="wide"
)

# Load data from SQLite database
@st.cache_data
def load_data():
    conn = sqlite3.connect("review_engine.db")
    df = pd.read_sql("SELECT * FROM reviews", conn)
    conn.close()
    if 'at' in df.columns:
        df['at'] = pd.to_datetime(df['at'])
        df['date'] = df['at'].dt.date
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛️ Dashboard Filters")

all_causes = df['root_cause'].unique().tolist()
selected_causes = st.sidebar.multiselect("Filter by Root Cause:", options=all_causes, default=all_causes)

all_sentiments = df['sentiment_category'].unique().tolist()
selected_sentiments = st.sidebar.multiselect("Filter by Sentiment:", options=all_sentiments, default=all_sentiments)

min_star, max_star = st.sidebar.slider("Filter by Star Rating:", min_value=1, max_value=5, value=(1, 5))
search_keyword = st.sidebar.text_input("🔍 Search Review Text (e.g., 'refund', 'late'):", "")

# Apply Filters
filtered_df = df[
    (df['root_cause'].isin(selected_causes)) &
    (df['sentiment_category'].isin(selected_sentiments)) &
    (df['score'].between(min_star, max_star))
]

if search_keyword:
    filtered_df = filtered_df[filtered_df['content'].str.contains(search_keyword, case=False, na=False)]

# --- MAIN HEADER ---
st.title("📊 Customer Support & Review Intelligence Engine")
st.markdown("Use the **left sidebar** to dynamically slice reviews by root cause, sentiment, star rating, or custom keywords.")

# --- DYNAMIC KPI METRICS ---
total_reviews = len(filtered_df)
avg_rating = round(filtered_df['score'].mean(), 2) if total_reviews > 0 else 0
negative_count = len(filtered_df[filtered_df['sentiment_category'] == 'Negative'])
negative_pct = round((negative_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
avg_sentiment = round(filtered_df['sentiment_score'].mean(), 3) if total_reviews > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Filtered Reviews", f"{total_reviews:,}", f"{round((total_reviews/len(df))*100, 1)}% of total")
col2.metric("Average Star Rating", f"{avg_rating} ⭐")
col3.metric("Negative / Churn Risk", f"{negative_pct}%", f"{negative_count:,} reviews", delta_color="inverse")
col4.metric("Avg VADER Sentiment", f"{avg_sentiment}")

st.markdown("---")

if total_reviews == 0:
    st.warning("No reviews match your current filter selection. Try expanding your filters in the sidebar!")
else:
    tab1, tab2, tab3 = st.tabs(["📈 Root Cause & Sentiment", "📅 Trends Over Time", "🚨 High-Risk Review Explorer"])

    with tab1:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Complaint Volume by Root Cause")
            fig_sentiment = px.histogram(
                filtered_df, 
                x="root_cause", 
                color="sentiment_category", 
                barmode="group",
                color_discrete_map={"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"},
                labels={"root_cause": "Root Cause Category", "count": "Review Count"}
            )
            st.plotly_chart(fig_sentiment)

        with col_right:
            st.subheader("Sentiment Proportion Breakdown")
            fig_pie = px.pie(
                filtered_df, 
                names="sentiment_category", 
                hole=0.45,
                color="sentiment_category",
                color_discrete_map={"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"}
            )
            st.plotly_chart(fig_pie)

        st.subheader("Average Star Rating by Business Area")
        avg_ratings = filtered_df.groupby('root_cause')['score'].mean().reset_index().sort_values(by='score')
        fig_rating = px.bar(
            avg_ratings, 
            x="score", 
            y="root_cause", 
            orientation="h",
            color="score",
            color_continuous_scale="RdYlGn",
            range_x=[0, 5],
            labels={"score": "Average Star Rating", "root_cause": "Root Cause"}
        )
        st.plotly_chart(fig_rating)

    with tab2:
        st.subheader("Daily Review Volume & Sentiment Trend")
        if 'date' in filtered_df.columns:
            daily_trends = filtered_df.groupby(['date', 'sentiment_category']).size().reset_index(name='count')
            fig_trend = px.line(
                daily_trends, 
                x="date", 
                y="count", 
                color="sentiment_category",
                color_discrete_map={"Positive": "#2ecc71", "Neutral": "#95a5a6", "Negative": "#e74c3c"},
                labels={"date": "Review Date", "count": "Number of Reviews"}
            )
            st.plotly_chart(fig_trend)
        else:
            st.info("Timestamp column ('at') not available for time-series plotting.")

    with tab3:
        st.subheader("Explore & Export Filtered Reviews")
        sort_by = st.selectbox("Sort reviews by:", ["thumbsUpCount (Most Helpful)", "score (Lowest Rating First)", "sentiment_score (Most Negative First)"])
        
        if "thumbsUpCount" in sort_by:
            display_df = filtered_df.sort_values(by="thumbsUpCount", ascending=False)
        elif "score" in sort_by:
            display_df = filtered_df.sort_values(by="score", ascending=True)
        else:
            display_df = filtered_df.sort_values(by="sentiment_score", ascending=True)

        st.dataframe(
            display_df[['at', 'score', 'thumbsUpCount', 'root_cause', 'sentiment_category', 'content']].head(50),
            use_container_width=True
        )

        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset as CSV",
            data=csv_data,
            file_name="filtered_reviews_export.csv",
            mime="text/csv" # or text/csv
        )