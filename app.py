import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Employee Attrition Analytics", page_icon="📊", layout="wide")
st.title("📊 Employee Attrition Analytics")
st.caption("Interactive HR analytics dashboard • Descriptive analysis, not an individual-level prediction or employment decision tool")

@st.cache_data
def load_data():
    path = Path(__file__).parent / "employee_attrition_data.csv"
    df = pd.read_csv(path)
    if "AttritionLabel" not in df.columns:
        df["AttritionLabel"] = df["Attrition"].map({1: "Yes", 0: "No"})
    return df

df = load_data()
with st.sidebar:
    st.header("Filters")
    departments = st.multiselect("Department", sorted(df["Department"].dropna().unique()), default=sorted(df["Department"].dropna().unique()))
    roles = st.multiselect("Job role", sorted(df["JobRole"].dropna().unique()), default=sorted(df["JobRole"].dropna().unique()))
    overtime = st.multiselect("Overtime", sorted(df["OverTime"].dropna().unique()), default=sorted(df["OverTime"].dropna().unique()))
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))
    show_data = st.checkbox("Show filtered records", value=False)

filtered = df[
    df["Department"].isin(departments) &
    df["JobRole"].isin(roles) &
    df["OverTime"].isin(overtime) &
    df["Age"].between(age_range[0], age_range[1])
].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

n = len(filtered)
leavers = int((filtered["Attrition"] == 1).sum())
rate = leavers / n * 100
a, b, c, d = st.columns(4)
a.metric("Employees in view", f"{n:,}")
b.metric("Employees marked as left", f"{leavers:,}")
c.metric("Attrition rate", f"{rate:.1f}%")
d.metric("Overtime rate", f"{(filtered['OverTime'].eq('Yes').mean()*100):.1f}%")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Departments & roles", "Work patterns", "Data & notes"])
with tab1:
    left, right = st.columns(2)
    with left:
        counts = filtered["AttritionLabel"].value_counts().rename_axis("Attrition").reset_index(name="Employees")
        st.plotly_chart(px.bar(counts, x="Attrition", y="Employees", color="Attrition", title="Employees by attrition status", text_auto=True), use_container_width=True)
    with right:
        age = filtered.groupby("AttritionLabel", as_index=False)["Age"].mean()
        st.plotly_chart(px.bar(age, x="AttritionLabel", y="Age", title="Average age by attrition status", labels={"AttritionLabel":"Attrition status","Age":"Average age"}, text_auto=".1f"), use_container_width=True)
    tenure = filtered.groupby("AttritionLabel", as_index=False)["YearsAtCompany"].mean()
    st.plotly_chart(px.bar(tenure, x="AttritionLabel", y="YearsAtCompany", title="Average years at company by attrition status", labels={"AttritionLabel":"Attrition status","YearsAtCompany":"Average years"}, text_auto=".1f"), use_container_width=True)

with tab2:
    dep = filtered.groupby("Department", as_index=False).agg(Employees=("Attrition","size"), Leavers=("Attrition","sum"))
    dep["Attrition rate (%)"] = dep["Leavers"] / dep["Employees"] * 100
    role = filtered.groupby("JobRole", as_index=False).agg(Employees=("Attrition","size"), Leavers=("Attrition","sum"))
    role["Attrition rate (%)"] = role["Leavers"] / role["Employees"] * 100
    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.bar(dep.sort_values("Attrition rate (%)", ascending=False), x="Department", y="Attrition rate (%)", hover_data=["Employees","Leavers"], title="Attrition rate by department", text_auto=".1f"), use_container_width=True)
        st.dataframe(dep.sort_values("Attrition rate (%)", ascending=False).style.format({"Attrition rate (%)":"{:.1f}%"}), use_container_width=True, hide_index=True)
    with right:
        st.plotly_chart(px.bar(role.sort_values("Attrition rate (%)", ascending=False), x="Attrition rate (%)", y="JobRole", orientation="h", hover_data=["Employees","Leavers"], title="Attrition rate by job role", text_auto=".1f"), use_container_width=True)
        st.dataframe(role.sort_values("Attrition rate (%)", ascending=False).style.format({"Attrition rate (%)":"{:.1f}%"}), use_container_width=True, hide_index=True)

with tab3:
    overtime_table = filtered.groupby("OverTime", as_index=False).agg(Employees=("Attrition","size"), Leavers=("Attrition","sum"))
    overtime_table["Attrition rate (%)"] = overtime_table["Leavers"] / overtime_table["Employees"] * 100
    left, right = st.columns(2)
    with left:
        st.plotly_chart(px.bar(overtime_table, x="OverTime", y="Attrition rate (%)", title="Attrition rate by overtime status", text_auto=".1f", hover_data=["Employees","Leavers"]), use_container_width=True)
        st.dataframe(overtime_table.style.format({"Attrition rate (%)":"{:.1f}%"}), use_container_width=True, hide_index=True)
    with right:
        satisfaction = filtered.groupby("JobSatisfaction", as_index=False).agg(Employees=("Attrition","size"), Leavers=("Attrition","sum"))
        satisfaction["Attrition rate (%)"] = satisfaction["Leavers"] / satisfaction["Employees"] * 100
        st.plotly_chart(px.line(satisfaction, x="JobSatisfaction", y="Attrition rate (%)", markers=True, title="Attrition rate by job satisfaction score", hover_data=["Employees","Leavers"]), use_container_width=True)
    st.info("These are descriptive associations in the supplied dataset. They do not establish that overtime, satisfaction, or role caused an employee to leave.")

with tab4:
    st.markdown("""
    **Dataset:** Employee-level HR table supplied with this project (1,470 records, 32 columns).

    **Target:** `Attrition` (`1` = Yes/left, `0` = No/stayed); `AttritionLabel` is a readable label.

    **How rates are calculated:** number of records marked as attrition divided by all records in the selected group, multiplied by 100.

    **Limitations:** this is a historical dataset; categories may not generalize to another organization or time period. Missing values, collection practices, class imbalance, and possible proxy variables can affect interpretation. Use aggregated results to support human review, not to rank, discipline, or make automated employment decisions.
    """)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_employee_attrition.csv", "text/csv")
    st.download_button("Download complete dataset", df.to_csv(index=False).encode("utf-8"), "employee_attrition_data.csv", "text/csv")
    if show_data:
        st.dataframe(filtered, use_container_width=True, hide_index=True)

st.divider()
st.caption("Project demo • Verify data definitions and privacy permissions before using with real employee records.")
