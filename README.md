
# Career Progression and Promotion Gap Analysis for Retention Optimization

## Files
- `Palo Alto Networks.csv` – original supplied dataset
- `Palo_Alto_Networks_clean.csv` – cleaned copy
- `PowerBI_DAX_Measures.txt` – DAX measures
- `app.py` – Streamlit deployment-ready dashboard
- `requirements.txt` – Streamlit dependencies
- `Research_Paper_Career_Progression.docx` – research paper
- `Research_Paper_Career_Progression.pdf` – PDF research paper

## Power BI build
1. Open Power BI Desktop → Get Data → Text/CSV.
2. Load `Palo Alto Networks.csv`.
3. In Power Query, confirm numeric fields are numeric and `Attrition` is whole number (0/1).
4. Create the DAX measures from `PowerBI_DAX_Measures.txt`.
5. Create 3 report pages:
   - Executive Overview: cards for employees, attritions, attrition rate, average years at company, average years since promotion; charts by department and role.
   - Promotion Gap Analysis: YearsSinceLastPromotion by JobLevel/JobRole, promotion-gap bands, attrition rate.
   - Retention Drivers: overtime, satisfaction, work-life balance, income and tenure.
6. Add slicers for Department, JobRole, JobLevel, OverTime and Promotion Gap Band.
7. Publish to Power BI Service if you have a Power BI account.

## Suggested project statement
This project analyzes career progression indicators and promotion gaps to identify workforce segments associated with higher attrition. The dashboard combines promotion timing, job level, tenure, role, overtime and employee-experience indicators to support evidence-based retention monitoring.

## Important dataset note
The supplied file contains 1,470 rows and 31 columns and resembles the widely used IBM HR Analytics-style attrition dataset. The analysis should not be presented as verified internal Palo Alto Networks employee data unless the dataset's provenance has been independently established.
