# Employee Attrition Analytics — Research + App

## Contents
- `Employee_Attrition_Research_Paper.docx` — research-style project paper.
- `app.py` — interactive Streamlit dashboard.
- `employee_attrition_data.csv` — cleaned table extracted from the supplied workbook.
- `requirements.txt` — Python dependencies.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open the local URL printed by Streamlit.

## Publish online with Streamlit Community Cloud
1. Create a GitHub repository and upload all files in this folder.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
4. Deploy. Streamlit will install dependencies from `requirements.txt`.
5. Share the generated app URL.

This package is deployment-ready but has **not** been published to a public hosting account by this assistant. A public URL can only be created after deployment through an account you control.

## Responsible use
The dashboard is descriptive and does not produce individual risk scores. Do not use it as the sole basis for employment decisions. Only upload data you are authorized to process; anonymize data where possible.
