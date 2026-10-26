# SalesPulse — Business Intelligence & Sales Analytics

SalesPulse is a beginner-friendly portfolio project that demonstrates a complete retail analytics workflow: data validation, exploratory analysis, SQL business questions, KPI reporting, and an interactive dashboard.

> **Dataset note:** `data/sales_data.csv` is synthetic sample data created for this project. It is not real company data. The results are for demonstrating analytics methods only and should not be presented as real business outcomes.

## Project highlights

- 1,200 synthetic order-line records covering 2023–2024
- Python + Pandas data checks and KPI analysis
- SQL queries for revenue, profit, product, region, and monthly performance
- Streamlit dashboard with KPI cards, filters, and charts
- Reproducible setup and GitHub-friendly project structure

## Dashboard preview

Run the app locally (steps below) and capture a screenshot for this section. Save it to `screenshots/dashboard.png`, then replace this note with:

```markdown
![SalesPulse dashboard](screenshots/dashboard.png)
```

## Key questions answered

1. How are revenue and profit trending over time?
2. Which regions and product categories contribute the most revenue?
3. Which products have the highest sales and profit?
4. How do customer segments compare?
5. Are high discounts associated with weaker profit margins?

## Tech stack

- Python 3.10+
- Pandas and NumPy
- Streamlit
- Plotly
- SQL (SQLite-compatible query examples)

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SalesPulse.git
cd SalesPulse
```

If you are creating the repository directly from this ZIP, extract the ZIP first and open the extracted `SalesPulse` folder in VS Code instead.

### 2. Create a virtual environment

**Windows PowerShell:**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app should open in your browser. If it does not, open the local URL shown in the terminal (usually `http://localhost:8501`).

### 5. Run the data analysis script

In another terminal, from the project root:

```bash
python src/analyze_sales.py
```

The script prints dataset checks and summary tables. It also writes summary CSV files to `reports/`.

## Folder structure

```text
SalesPulse/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── sales_data.csv
├── notebooks/
│   └── analysis_guide.md
├── reports/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
├── sql/
│   └── business_questions.sql
└── src/
    └── analyze_sales.py
```

## Metrics

- **Revenue:** sum of `Revenue`
- **Profit:** sum of `Profit`
- **Profit margin:** total profit / total revenue
- **Orders:** distinct `Order_ID` count
- **Average order value:** total revenue / distinct order count

## SQL practice

Open `sql/business_questions.sql`. The queries use SQLite-compatible SQL and can be adapted to PostgreSQL, MySQL, or SQL Server with small syntax changes.

## Suggested improvements

- Replace the sample data with a properly licensed public dataset.
- Add unit tests and a data dictionary.
- Add customer-level cohort analysis if customer IDs become available.
- Publish a Power BI version (`.pbix`) if you have Power BI Desktop installed.
- Add an executive summary describing verified insights from your own run.

## Important

This is a portfolio starter project, not a production system. The sample data is synthetic, so do not claim that the generated findings represent an actual business.
