# 📊 Sales & Customer Performance Analytics

A professional Business Analyst portfolio project using **Python, SQL and Streamlit**.

## Business workflow

**Business Problem → Requirements → Data Cleaning → SQL/KPI Analysis → Dashboard → Insights → Recommendations**

## Technology

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- SQL
- Pytest

## Project structure

```text
Business_Analyst_Professional_Project/
├── app.py
├── requirements.txt
├── data/
├── src/
├── sql/
├── reports/
└── tests/
```

## Run in VS Code

### 1. Open this folder in VS Code

### 2. Create/activate a virtual environment (recommended)

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install libraries

```bash
pip install -r requirements.txt
```

### 4. Start dashboard

```bash
streamlit run app.py
```

The browser will open the dashboard automatically.

## CSV format

Required:
- Order Date
- Region
- Category
- Quantity
- Unit Price

Optional:
- Order ID
- Customer ID
- Discount
- Cost
- Revenue
- Profit

## Test the analysis code

```bash
pytest
```

## Portfolio note

The application starts with a synthetic demo dataset so the project can be run immediately. For a real portfolio submission, replace it with a documented public dataset and clearly cite the data source.

## Business Analyst deliverables

- BRD
- Functional requirements
- Acceptance criteria
- KPI definitions
- SQL analysis
- Python data preparation
- Interactive dashboard
- Business insight framework
- Recommendation framework
- Automated tests
