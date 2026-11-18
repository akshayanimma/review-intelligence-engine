import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("Loading raw reviews...")
df=pd.read_csv("raw_reviews.csv")

#Data Cleaning
print("Cleaning data")
df=df.dropna(subset=['content'])
df=df.drop_duplicates(subset=['reviewId'])
df=df.drop_duplicates(subset=['content'])
df['clean_content']= df['content'].astype(str).str.lower()

#Sentiment analysis
print("Running sentiment analysis...")
analyzer= SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return analyzer.polarity_scores(text)['compound']

df['sentiment_score']=df['clean_content'].apply(get_sentiment_score)

def classify_sentiment(score):
    if score>=0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

df['sentiment_category']=df['sentiment_score'].apply(classify_sentiment)

#Root cause keyword tagging
print("Tagging root cause...")
def assign_root_cause(text):
    text=str(text)
    if any(word in text for word in ['delivery', 'late', 'rider', 'driver', 'arrived', 'time', 'delay', 'otp']):
        return 'Delivery & Logistics'
    elif any(word in text for word in ['pay', 'refund', 'money', 'charged', 'upi', 'payment', 'coupon', 'offer', 'wallet']):
        return 'Payment and Refunds'
    elif any(word in text for word in['crash', 'bug', 'slow', 'hang', 'update', 'glitch', 'open', 'loading']):
        return 'App Performance & Bugs'
    elif any(word in text for word in['food', 'taste', 'cold', 'quality', 'quantity', 'item', 'missing', 'packaging', 'price', 'expensive']):
        return 'Food Quality & Pricing'
    else:
        return 'Customer Support & Other'
df['root_cause']=df['clean_content'].apply(assign_root_cause)

#Export cleaned dataset
output_file="cleaned_reviews.csv"
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\nSuccess! Cleaned and tagged {len(df)} reviews.")
print("Breakdown of root causes:")
print(df['root_cause'].value_counts())
print("\nSample preview:")
print(df[['content', 'sentiment_category', 'root_cause']].head(3))
        
    
    