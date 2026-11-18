import sqlite3
import pandas as pd

print("Loading cleaned reviews...")
df=pd.read_csv("cleaned_reviews.csv")

conn=sqlite3.connect("review_engine.db")

df.to_sql("reviews", conn, if_exists="replace", index=False)
print("Data loaded into SQLite database successfully!\n")

#Root cause breakdown by sentiment
print("===Root Cause Breakdown by Sentiment===")
query_1="""
SELECT root_cause, sentiment_category, COUNT(*) as review_count
FROM reviews
GROUP BY root_cause, sentiment_category
ORDER BY review_count DESC;
"""
df_q1= pd.read_sql(query_1, conn)
print(df_q1.to_string(index=False))

print("\n==2. TOP DRIVERS OF NEGATIVE REVIEWS==")
query_2="""
SELECT root_cause, COUNT(*) as negative_count
FROM reviews
WHERE sentiment_category= 'Negative'
GROUP BY root_cause
ORDER BY negative_count DESC;
"""
df_q2=pd.read_sql(query_2, conn)
print(df_q2.to_string(index=False))

print("===3.TOP HELPFUL REVIEWS FLAGGED FOR CHURN RISK===")
query_3="""
SELECT score, thumbsUPCount, content, root_cause
FROM reviews
WHERE sentiment_category='Negative'
ORDER BY thumbsUpCount DESC
LIMIT 5;
"""
df_q3=pd.read_sql(query_3, conn)
print(df_q3.to_string(index=False))

print("\n===4.AVERAGE RATING & SENTIMENT BY CATEGORY===")
query_4="""
SELECT
    root_cause,
    COUNT(*) as total_reviews,
    ROUND(AVG(score), 2) as avg_star_rating,
    ROUND(AVG(sentiment_score), 3) as avg_sentiment_score
FROM reviews
GROUP BY root_cause
ORDER BY avg_star_rating ASC;
"""
df_q4=pd.read_sql(query_4, conn)
print(df_q4.to_string(index=False))

conn.close()
print("\nStep 3 Analysis complete!")
