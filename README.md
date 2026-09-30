# 📱 TellCo Telecommunication User Analytics & Interactive Web App

[![CI/CD Pipeline](https://github.com/tellco/telecom-user-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/tellco/telecom-user-analytics/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.60.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end data science, machine learning, and business analytics application developed for an investment due diligence evaluation of **TellCo**, a mobile service provider in the **Republic of Pefkakia**.

---

## 🎬 Live Interactive App Preview (Animation / Recording)

![TellCo Dashboard Recording](artifacts/dashboard_demo.webp)

> **Note:** The animated recording above demonstrates live user navigation across all 6 analytical modules of the Streamlit web app, including SQL query execution on the exported database table.

---

## 🚀 How to Run the App (Step-by-Step)

### Option 1: Direct Local Execution (Recommended)

1. **Clone the Repository & Navigate to Folder:**
   ```bash
   git clone https://github.com/tellco/telecom-user-analytics.git
   cd telecom-user-analytics
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

### Option 2: Docker Container Execution

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
│   ├── mlops_tracking/
│   └── TellCo_Executive_Report_and_Slides.md # 20-Slide Presentation Deck
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
