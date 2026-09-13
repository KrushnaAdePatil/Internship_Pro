# 🎥 Netflix AI & Retention Dashboard

This project is a professional data analysis pipeline and interactive web dashboard for Netflix viewer retention and AI-based content recommendations.

## Project Structure
- `code.py`: The Machine Learning engine and data processing script. Calculates retention scores and generates next-watch recommendations using NLP (TF-IDF Cosine Similarity). Output is saved to `Netflix_with_Retention.csv`.
- `app.py`: A Streamlit dashboard that visualizes the AI recommendations, retention metrics, and segments users based on watch history.
- `Netflix_dashboard_dataset.csv`: The raw input data.
- `Netfix app dashboard.pbix`: A Power BI dashboard file for additional business intelligence reporting. 

## How to Run Locally

### 1. Install Dependencies
Make sure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Generate the Machine Learning Dataset
Run the data pipeline script to compute recommendations, fix edge-cases (like divide by zero), and calculate retention segments. This will generate the `Netflix_with_Retention.csv` file.
```bash
python code.py
```

### 3. Launch the Dashboard
Run the Streamlit application to view the interactive web dashboard.
```bash
streamlit run app.py
```
This will automatically open the dashboard in your default web browser (typically at `http://localhost:8501`).
