import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import prepare_data, attrition_summary, attrition_by_category
from model import train_model, evaluate_model

st.set_page_config(page_title="Employee Attrition Analytics", page_icon="📊", layout="wide")
st.title("Employee Attrition Analytics Dashboard")
st.caption("Explore employee attrition patterns and evaluate a baseline machine-learning model.")

@st.cache_data
def load_data():
    return pd.read_csv("data/employee_attrition.csv")

upload = st.sidebar.file_uploader("Upload another CSV (optional)", type=["csv"])
try:
    data = prepare_data(pd.read_csv(upload) if upload else load_data())
except Exception as e:
    st.error(f"Dataset error: {e}")
    st.stop()

s = attrition_summary(data)
a,b,c,d = st.columns(4)
a.metric("Employees", f"{s['employees']:,}")
b.metric("Employees who left", f"{s['attrition_count']:,}")
c.metric("Attrition rate", f"{s['attrition_rate']:.1%}")
d.metric("Missing cells", f"{s['missing_cells']:,}")

st.subheader("Employee outcomes")
counts = data["Attrition"].map({0:"Stayed",1:"Left"}).value_counts()
fig, ax = plt.subplots()
ax.bar(counts.index, counts.values)
ax.set_ylabel("Employees")
st.pyplot(fig)
plt.close(fig)

categories = [x for x in ["Department","JobRole","BusinessTravel","MaritalStatus","OverTime","EducationField"] if x in data.columns]
if categories:
    choice = st.selectbox("Attrition rate by category", categories)
    rates = attrition_by_category(data, choice).rename("Attrition rate")
    st.dataframe(rates.to_frame().style.format("{:.1%}"), use_container_width=True)

numeric = [x for x in ["Age","MonthlyIncome","TotalWorkingYears","YearsAtCompany","DistanceFromHome"] if x in data.columns]
if numeric:
    choice = st.selectbox("Compare numeric characteristic", numeric)
    fig, ax = plt.subplots()
    for label, value in [("Stayed",0),("Left",1)]:
        ax.hist(data.loc[data.Attrition==value, choice].dropna(), bins=20, alpha=.55, label=label)
    ax.set_xlabel(choice); ax.set_ylabel("Employees"); ax.legend()
    st.pyplot(fig); plt.close(fig)

st.subheader("Machine-learning evaluation")
st.write("Train a Random Forest classifier using a stratified 80/20 holdout split.")
if st.button("Train and evaluate model"):
    with st.spinner("Training..."):
        model, X_test, y_test = train_model(data)
        metrics, report, matrix = evaluate_model(model, X_test, y_test)
    x,y,z = st.columns(3)
    x.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    y.metric("Precision", f"{metrics['precision']:.1%}")
    z.metric("Recall", f"{metrics['recall']:.1%}")
    st.text("Classification report"); st.code(report)
    st.write("Confusion matrix (actual rows × predicted columns)")
    st.dataframe(pd.DataFrame(matrix, index=["Actual stayed","Actual left"],
                              columns=["Predicted stayed","Predicted left"]))
    st.warning("Use predictions only as exploratory decision support. Check fairness and validate on new data before real-world use.")
st.sidebar.caption("Python • Pandas • Scikit-learn • Streamlit")
