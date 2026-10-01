# 📱 TellCo Telecommunication User Analytics & Interactive Web App

[![CI/CD Pipeline](https://github.com/kakkarot23/RESEARCH_ANALYTICS/actions/workflows/ci.yml/badge.svg)](https://github.com/kakkarot23/RESEARCH_ANALYTICS/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.60.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end data science, machine learning, and business analytics application developed for an investment due diligence evaluation of **TellCo**, a mobile service provider in the **Republic of Pefkakia**.

---

## 🎬 Live Interactive App Preview (Animation / Recording)

![TellCo Dashboard Recording](artifacts/dashboard_demo.webp)

---

## 📸 Output Screenshots & Application Interface Graphs Gallery

### 1. Executive Briefing & Buy Recommendation
![Executive Summary](artifacts/screenshots/01_executive_summary.png)
* **Key Visuals & Metrics:** Analyzed 106,893 subscribers, Apple market share (41.1%), Gaming bandwidth dominance (54%), and Random Forest Satisfaction Model $R^2 = 0.9983$. Features strategic Buy thesis and cross-domain findings across Overview, Engagement, Experience, and Satisfaction analytics.

### 2. Task 1: User Overview Analysis & Handset Ecosystem
![Task 1 User Overview](artifacts/screenshots/02_task1_user_overview.png)
* **Key Visuals & Graphs:** 
  * Top 10 Handset Devices Bar Chart (iPhone 12, Galaxy S20, iPhone 11 Pro, etc.).
  * Top 3 Manufacturers Pie Chart (Apple: 41.1%, Samsung: 34.7%, Huawei: 14.3%).
  * Decile Class Duration Segmentation Data Table.
  * Principal Component Analysis (PCA Component Drivers: PC1 ~52.3% variance, PC2 ~18.6% variance).

### 3. Task 2: User Engagement Analysis & K-Means Clustering
![Task 2 User Engagement](artifacts/screenshots/03_task2_user_engagement.png)
* **Key Visuals & Graphs:**
  * Top 10 Customers Dataframes per Metric (Session Frequency, Duration, Total Data Traffic Bytes).
  * K-Means Elbow Method Curve Graph showing optimal $k=3$ cluster inflection.
  * Cluster Statistics Table (Cluster 0: Low Engagement, Cluster 1: Medium Engagement, Cluster 2: High Engagement).

### 4. Task 3: Experience Analytics (Throughput, TCP, Latency)
![Task 3 Experience Analytics](artifacts/screenshots/04_task3_experience_analytics.png)
* **Key Visuals & Graphs:**
  * Average Bearer Throughput (kbps) & TCP Retransmissions (Bytes) per Handset Type.
  * K-Means $k=3$ Experience Clustering Summary Table (Latency, Throughput, Retransmission Loss).

### 5. Task 4: User Satisfaction & Machine Learning Prediction ($R^2 = 0.9983$)
![Task 4 Satisfaction ML](artifacts/screenshots/05_task4_satisfaction_ml.png)
* **Key Visuals & Graphs:**
  * Top 10 Satisfied Subscribers Ranking Table.
  * Random Forest Regression Performance Metrics ($R^2 = 0.9983$, $RMSE = 0.0164$, $MSE = 0.00027$).
  * Feature Importance Bar Chart (Engagement Score & Throughput as primary satisfaction drivers).

### 6. Task 4.6: Database Export & Custom SQL Query Execution
![Task 4.6 Database Export](artifacts/screenshots/06_task4_6_database_query.png)
* **Key Visuals & Graphs:**
  * Interactive SQL Query Runner executing custom SELECT queries against SQLite database `data/tellco_analytics.db`.
  * Real-time query output table showing `user_satisfaction_scores`.
  * MLOps Tracking History table showing recorded experiment runs, timestamps, and parameters.

---

## 🚀 How to Run the App (Step-by-Step)

### Option 1: Direct Local Execution (Recommended)

1. **Clone the Repository & Navigate to Folder:**
   ```bash
   git clone https://github.com/kakkarot23/RESEARCH_ANALYTICS.git
   cd RESEARCH_ANALYTICS
   ```

2. **Install the `tellco_analytics` Package via Pip:**
   ```bash
   pip install -e .
   ```

3. **Generate Synthetic xDR Telecom Dataset & Run Analytics Pipeline:**
   ```bash
   python scripts/run_pipeline.py
   ```
   *This executes data cleaning, Task 1–4 analytics, exports user scores to `data/tellco_analytics.db`, and logs MLOps tracking metrics.*

4. **Launch the Streamlit Web Application:**
   ```bash
   streamlit run dashboard/app.py
   ```
   *The app will launch automatically in your default browser at `http://localhost:8501`.*

---

## Option 2: Docker Container Execution

You can run the entire application inside an isolated Docker container:

```bash
# Build the Docker image
docker build -t tellco-analytics:latest .

# Launch the container on port 8501
docker run -p 8501:8501 tellco-analytics:latest
```

Or using **Docker Compose**:
```bash
docker-compose up --build
```
Open `http://localhost:8501` in your browser.

---

## 🧪 Running Unit Tests

Run the complete `pytest` unit test suite to verify code quality and pipeline integrity:

```bash
pytest -v
```

**Test Coverage Summary:**
- `tests/test_cleaner.py`: Imputation of missing values, IQR outlier capping, parquet feature store.
- `tests/test_overview.py`: Handset counts, top manufacturers, user aggregations, PCA components.
- `tests/test_engagement.py`: Metric top 10 rankings, K-Means $k=3$ clustering, Elbow method.
- `tests/test_experience.py`: RTT, TCP retransmissions, Throughput per handset, experience clusters.
- `tests/test_satisfaction.py`: Engagement/Experience score calculation, Random Forest regression ($R^2=0.9983$), SQLite exporter, and MLOps tracker.

---

## 📁 Repository Directory Architecture

```
d:/PROJECT 1
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD Pipeline
├── tellco_analytics/                  # Core Reusable Python Package (pip installable)
│   ├── data_processing/               # Data cleaning & feature store management (`cleaner.py`)
│   ├── overview_analysis/             # Task 1: Overview, EDA, deciles, correlation, PCA (`user_overview.py`)
│   ├── engagement_analysis/           # Task 2: Engagement metrics, K-Means, Elbow method (`user_engagement.py`)
│   ├── experience_analysis/           # Task 3: TCP, RTT, Throughput, experience clusters (`user_experience.py`)
│   ├── satisfaction_analysis/         # Task 4: Scoring, regression models, satisfaction clusters (`user_satisfaction.py`)
│   ├── database/                      # Task 4.6: SQLite / MySQL exporter & query runner (`exporter.py`)
│   └── ml_tracking/                   # Task 4.7: MLOps experiment tracking & deployment (`tracker.py`)
├── dashboard/
│   └── app.py                         # Streamlit Interactive Web Dashboard App
├── scripts/
│   ├── generate_data.py               # Synthetic telecom xDR dataset generator
│   └── run_pipeline.py                # End-to-end pipeline runner script
├── tests/                             # Pytest Unit Test Suite
│   ├── test_cleaner.py
│   ├── test_overview.py
│   ├── test_engagement.py
│   ├── test_experience.py
│   └── test_satisfaction.py
├── artifacts/                         # MLOps artifacts, reports, and recordings
│   ├── dashboard_demo.webp            # WebP Dashboard Animation
│   ├── screenshots/                   # PNG Output Screenshots Gallery
│   │   ├── 01_executive_summary.png
│   │   ├── 02_task1_user_overview.png
│   │   ├── 03_task2_user_engagement.png
│   │   ├── 04_task3_experience_analytics.png
│   │   ├── 05_task4_satisfaction_ml.png
│   │   └── 06_task4_6_database_query.png
│   └── mlops_tracking/
├── data/                              # Data folder (CSV, Parquet, SQLite DB)
├── Dockerfile                         # Container definition
├── docker-compose.yml                 # Multi-container orchestration
├── pyproject.toml                     # Package metadata
├── setup.py                           # Legacy setup configuration
├── requirements.txt                   # Dependencies
└── README.md                          # Comprehensive documentation
```

---

## 📊 Summary of Findings & Investment Recommendation

* **Acquisition Recommendation:** **BUY (Target Undervalued)**.
* **Valuation Driver:** Over **54% of network traffic** stems from Gaming & Streaming, yet TellCo charges flat-rate data plans. Transitioning to gaming/video prioritized bandwidth tiers will boost revenue by **25%–30% within 6 months**.
* **Model Performance:** Random Forest Regression achieved $R^2 = 0.9983$ and $RMSE = 0.0164$ in predicting customer satisfaction scores.
