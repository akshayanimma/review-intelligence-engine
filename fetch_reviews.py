import time
import pandas as pd
from google_play_scraper import reviews, Sort

# Configuration
APP_ID = "in.swiggy.android" 
TARGET_COUNT = 30000
BATCH_SIZE = 200

print(f"Starting ingestion for {APP_ID} (Target: {TARGET_COUNT} reviews)...")

all_reviews = []
continuation_token = None

while len(all_reviews) < TARGET_COUNT:
    try:
        batch, continuation_token = reviews(
            APP_ID,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=BATCH_SIZE,
            continuation_token=continuation_token
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        break
    
    if not batch:
        print("No more reviews returned by Play Store.")
        break
        
    all_reviews.extend(batch)
    
    if len(all_reviews) % 2000 == 0:
        print(f"Fetched {len(all_reviews)} / {TARGET_COUNT} reviews...")
        
    if continuation_token is None:
        break
        
    time.sleep(0.3)

# Convert to a DataFrame
df = pd.DataFrame(all_reviews)

if not df.empty:
    cols_to_keep = [
        "reviewId", "userName", "content", "score", 
        "thumbsUpCount", "reviewCreatedVersion", "at"
    ]
    df = df[[c for c in cols_to_keep if c in df.columns]]
    df.to_csv("raw_reviews.csv", index=False, encoding="utf-8")
    print(f"\nSuccess! Saved {len(df)} rows to raw_reviews.csv")
    print(df.head(3))
else:
    print("DataFrame is empty. Please check connection or app ID.")