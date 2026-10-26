# Analysis guide

Use this guide as a checklist while exploring the project.

## Questions to investigate
- Which month has the highest revenue?
- Which region has the strongest profit margin?
- Which category generates high revenue but relatively low profit?
- How do customer segments compare in revenue per order?
- Does a higher discount band correspond to lower profit margin?

## Suggested workflow
1. Run `python src/analyze_sales.py`.
2. Inspect the generated CSVs in `reports/`.
3. Open the dashboard with `streamlit run app.py`.
4. Test the filters and compare different slices of the data.
5. Record 3–5 findings supported by actual outputs.
6. Add your findings to the README. Remember that the data is synthetic.
