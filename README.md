
# Customer Support & Review Intelligence Engine

An end-to-end Data Analytics, NLP, and Business Intelligence pipeline built to ingest, clean, tag, store, and visualize customer reviews (Swiggy Google Play Store dataset) to uncover critical root causes of customer dissatisfaction and churn risk.

**Live Dashboard:** ` https://review-intelligence-engine-kdzbheceffq8wocprpchaf.streamlit.app/` 

## Business Problem & Objective
Customer feedback on app stores contains high-signal operational issues—such as delivery delays, food quality or pricing concerns, payment and refund friction, and app bugs—that are difficult to track manually at scale. This project builds a pipeline and interactive dashboard to:
* Quantify customer sentiment using VADER sentiment analysis (`nltk`).
* Categorize reviews into actionable business root causes.
* Highlight high-risk complaints and trends over time to support data-driven decisions.

## Pipeline Architecture
```text
Google Play Store Reviews (raw_reviews.csv)
        │
        ▼
1. Data Ingestion (fetch_reviews.py)
        │
        ▼
2. Cleaning & NLP Tagging (clean_and_tag.py) ──► clean_reviews.csv
        │
        ▼
3. SQLite Storage & Analysis (analyze_data.py) ──► review_engine.db
        │
        ▼
4. Interactive BI Dashboard (app.py)
```

1. **Data Ingestion (`fetch_reviews.py`)**: Collects Google Play Store reviews and saves the raw dataset to `raw_reviews.csv`.
2. **Cleaning & NLP Tagging (`clean_and_tag.py`)**: Cleans text entries, runs VADER sentiment analysis to classify reviews (*Positive*, *Neutral*, *Negative*), maps feedback to business root causes (*Delivery*, *Food Quality*, *Payments*, *App Performance*, etc.), and outputs `clean_reviews.csv`.
3. **Database Storage & SQL Analysis (`analyze_data.py`)**: Loads processed records into `review_engine.db` (SQLite) and runs SQL queries to analyze root-cause volume, star ratings, and churn-risk indicators.
4. **Interactive BI Dashboard (`app.py`)**: Provides a Streamlit and Plotly dashboard with sidebar filters (root cause, sentiment, star rating, keyword search), KPI summary cards, sentiment and root-cause charts, daily trend views, a sortable review explorer, and filtered CSV export.

## Tech Stack
* **Programming & Data Manipulation**: Python, Pandas
* **Database & Querying**: SQLite (`sqlite3`)
* **NLP**: NLTK (VADER Sentiment Analysis)
* **Visualization & Web App**: Streamlit, Plotly Express
* **Version Control**: Git, GitHub

## Project Structure
```text
review-intelligence-engine/
├── app.py               # Interactive Streamlit BI dashboard
├── fetch_reviews.py     # Data ingestion script
├── clean_and_tag.py     # Cleaning, VADER sentiment & root-cause tagging
├── analyze_data.py      # SQLite loading & analytical queries
├── raw_reviews.csv      # Raw ingested reviews dataset
├── clean_reviews.csv    # Cleaned & tagged reviews dataset
├── review_engine.db     # SQLite database
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## How to Run Locally
1. **Clone the repository**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/review-intelligence-engine.git
   cd review-intelligence-engine
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the pipeline scripts (if rebuilding the database)**
   ```bash
   python fetch_reviews.py
   python clean_and_tag.py
   python analyze_data.py
   ```

5. **Start the Streamlit dashboard**
   ```bash
   streamlit run app.py
   ```

## Resume Highlights
* Engineered an end-to-end NLP and BI pipeline in Python to ingest, clean, and analyze 4,300+ Google Play Store reviews with VADER sentiment analysis and root-cause tagging.
* Stored structured review data in SQLite and wrote SQL queries to evaluate rating distributions, complaint drivers, and high-churn risk feedback.
* Built an interactive Streamlit and Plotly dashboard featuring multi-facet sidebar filters, keyword search, sentiment trend tracking, and CSV export.
