# Employee Attrition Analysis

A Streamlit dashboard for exploring employee attrition patterns and training a baseline Random Forest classifier.

## Dataset
- 1,470 records and 31 columns in the supplied CSV.
- `Attrition`: 0 = stayed, 1 = left.
- Dataset stored in `data/employee_attrition.csv`.

## Run locally
1. Install Python 3.10+.
2. Run `pip install -r requirements.txt`.
3. Run `streamlit run app.py`.

## Deploy on Streamlit Community Cloud
1. Upload this complete folder to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Select the repository, branch and `app.py`.
4. Deploy and test the generated `https://....streamlit.app` link in a private browser window.

## Files
- `app.py`: Streamlit dashboard
- `analysis.py`: validation and descriptive analysis
- `model.py`: preprocessing and Random Forest evaluation
- `data/employee_attrition.csv`: supplied dataset
- `research_paper/Employee_Attrition_Research_Paper.pdf`: project report

## Limitations
The source, sampling method and provenance of the dataset were not provided. Do not claim it represents Palo Alto Networks employees unless independently verified. Model metrics are dataset-dependent. Do not use predictions as the sole basis for employment decisions.
