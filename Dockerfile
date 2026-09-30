# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and setup files
COPY requirements.txt pyproject.toml setup.py /app/

# Install python dependencies and package
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy application files
COPY tellco_analytics /app/tellco_analytics
COPY dashboard /app/dashboard
COPY scripts /app/scripts
COPY tests /app/tests

# Run data pipeline to prepare data and DB
RUN python scripts/run_pipeline.py

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run Streamlit app
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
