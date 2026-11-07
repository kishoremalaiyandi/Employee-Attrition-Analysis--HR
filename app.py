
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Career Progression & Promotion Gap Analysis", layout="wide")
st.title("Career Progression and Promotion Gap Analysis")
st.caption("Retention optimization dashboard | Dataset supplied as 'Palo Alto Networks.csv'")

uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("Palo Alto Networks.csv")

# Normalize Attrition to numeric 0/1
if df["Attrition"].dtype == object:
    df["Attrition"] = df["Attrition"].map({"Yes":1,"No":0,"yes":1,"no":0}).fillna(pd.to_numeric(df["Attrition"], errors="coerce"))

st.sidebar.header("Filters")
departments = st.sidebar.multiselect("Department", sorted(df["Department"].dropna().unique()), default=sorted(df["Department"].dropna().unique()))
roles = st.sidebar.multiselect("Job Role", sorted(df["JobRole"].dropna().unique()), default=sorted(df["JobRole"].dropna().unique()))
overtime = st.sidebar.multiselect("Overtime", sorted(df["OverTime"].dropna().unique()), default=sorted(df["OverTime"].dropna().unique()))
view = df[df["Department"].isin(departments) & df["JobRole"].isin(roles) & df["OverTime"].isin(overtime)].copy()

def pct(x): return f"{x:.1%}"

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Employees", f"{len(view):,}")
c2.metric("Attrition", f"{int(view.Attrition.sum()):,}")
c3.metric("Attrition Rate", pct(view.Attrition.mean() if len(view) else 0))
c4.metric("Avg Years at Company", f"{view.YearsAtCompany.mean():.1f}")
c5.metric("Avg Years Since Promotion", f"{view.YearsSinceLastPromotion.mean():.1f}")

tab1,tab2,tab3 = st.tabs(["Overview","Promotion Gap","Retention Drivers"])

with tab1:
    a,b=st.columns(2)
    role = view.groupby("JobRole", as_index=False).agg(Employees=("Attrition","size"),AttritionRate=("Attrition","mean"))
    a.plotly_chart(px.bar(role, x="JobRole", y="AttritionRate", title="Attrition Rate by Job Role", text_auto=".1%"), use_container_width=True)
    dept = view.groupby("Department", as_index=False).agg(Employees=("Attrition","size"),AttritionRate=("Attrition","mean"))
    b.plotly_chart(px.bar(dept, x="Department", y="AttritionRate", title="Attrition Rate by Department", text_auto=".1%"), use_container_width=True)
    a,b=st.columns(2)
    a.plotly_chart(px.histogram(view, x="YearsSinceLastPromotion", color="Attrition", barmode="group", title="Years Since Last Promotion"), use_container_width=True)
    b.plotly_chart(px.box(view, x="Attrition", y="YearsSinceLastPromotion", title="Promotion Gap vs Attrition"), use_container_width=True)

with tab2:
    view["PromotionGapFlag"] = (view["YearsSinceLastPromotion"] >= 3).astype(int)
    gap = view.groupby(["JobLevel","PromotionGapFlag"], as_index=False).agg(Employees=("Attrition","size"),AttritionRate=("Attrition","mean"))
    gap["Promotion Status"] = gap["PromotionGapFlag"].map({0:"0–2 years since promotion",1:"3+ years since promotion"})
    st.plotly_chart(px.bar(gap, x="JobLevel", y="AttritionRate", color="Promotion Status", barmode="group", title="Attrition by Job Level and Promotion Gap", text_auto=".1%"), use_container_width=True)
    role_gap = view.groupby("JobRole", as_index=False).agg(Employees=("Attrition","size"),AvgYearsSincePromotion=("YearsSinceLastPromotion","mean"),AttritionRate=("Attrition","mean"))
    role_gap["Risk Gap Index"] = role_gap["AvgYearsSincePromotion"] * role_gap["AttritionRate"]
    st.dataframe(role_gap.sort_values("Risk Gap Index", ascending=False).style.format({"AvgYearsSincePromotion":"{:.1f}","AttritionRate":"{:.1%}","Risk Gap Index":"{:.2f}"}), use_container_width=True)

with tab3:
    ot = view.groupby("OverTime", as_index=False).agg(Employees=("Attrition","size"),AttritionRate=("Attrition","mean"))
    st.plotly_chart(px.bar(ot, x="OverTime", y="AttritionRate", title="Attrition Rate by Overtime", text_auto=".1%"), use_container_width=True)
    sat_cols = ["JobSatisfaction","EnvironmentSatisfaction","WorkLifeBalance","JobInvolvement"]
    long = view.melt(id_vars=["Attrition"], value_vars=sat_cols, var_name="Factor", value_name="Score")
    summary = long.groupby(["Factor","Score"], as_index=False).agg(AttritionRate=("Attrition","mean"),Employees=("Attrition","size"))
    st.plotly_chart(px.line(summary, x="Score", y="AttritionRate", color="Factor", markers=True, title="Attrition Rate Across Employee Experience Scores"), use_container_width=True)

st.subheader("Management Action View")
st.markdown("""
- Monitor employees with long promotion intervals, especially where attrition is elevated.
- Review career-path clarity, internal mobility, mentoring and promotion eligibility criteria.
- Use overtime, satisfaction and tenure as supporting retention signals rather than treating any single variable as a cause.
- Recheck these indicators periodically; this dashboard describes associations in the supplied dataset and does not establish causation.
""")
