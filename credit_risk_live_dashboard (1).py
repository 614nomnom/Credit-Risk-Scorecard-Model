"""
IRCTC Credit Risk Scorecard - Live Interactive Dashboard (Dummy)
Run: streamlit run credit_risk_live_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Credit Risk Scorecard | Kartik Rao", layout="wide", page_icon="🏦")

st.markdown("""
<style>
.main-header {font-size: 2rem; font-weight: 700; color: #1F4E79;}
.metric-card {background: linear-gradient(135deg, #1F4E79, #2E7D32); padding: 1rem; border-radius: 10px; color: white; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏦 Credit Risk Scorecard Dashboard</p>', unsafe_allow_html=True)
st.caption("MBA Finance Portfolio Project | Prepared by Kartik Rao | April 2026")

# Sidebar filters
st.sidebar.header("Filters")
income_range = st.sidebar.slider("Monthly Income Range (₹)", 15000, 200000, (25000, 120000))
risk_filter = st.sidebar.multiselect("Risk Category", ["Low Risk", "Medium Risk", "High Risk"], default=["Low Risk", "Medium Risk", "High Risk"])
emp_filter = st.sidebar.multiselect("Employment Type", ["Salaried", "Self-Employed"], default=["Salaried", "Self-Employed"])

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applicants", "80", "Processed")
col2.metric("Approval Rate", "64%", "+8% vs last month")
col3.metric("High Risk %", "21%", "Monitor closely")
col4.metric("Avg Credit Score", "68.4", "Medium Risk Zone")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["Risk Distribution", "Income vs Risk", "Scenario Impact"])

with tab1:
    fig = px.pie(values=[34, 29, 17], names=["Low Risk (Approve)", "Medium Risk (Conditional)", "High Risk (Reject)"],
                 title="Risk Distribution - 80 Applicants", color_discrete_sequence=["#2E7D32", "#FF6B35", "#C00000"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    df = pd.DataFrame({
        'Income': [random.randint(20000, 150000) for _ in range(80)],
        'Score': [random.randint(40, 95) for _ in range(80)],
        'Risk': random.choices(['Low', 'Medium', 'High'], weights=[42, 36, 22], k=80)
    })
    fig2 = px.scatter(df, x='Income', y='Score', color='Risk', 
                      color_discrete_map={'Low': '#2E7D32', 'Medium': '#FF6B35', 'High': '#C00000'},
                      title="Income vs Credit Score (Higher Income = Lower Risk)")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("What-If: Income Drop 20%")
    scenario_df = pd.DataFrame({
        'Applicant': ['APP003', 'APP008', 'APP015', 'APP027'],
        'Original Score': [78, 62, 71, 54],
        'After 20% Income Drop': [61, 49, 58, 41],
        'Risk Change': ['Low → Medium', 'Medium → High', 'Low → Medium', 'Medium → High']
    })
    st.dataframe(scenario_df, use_container_width=True)
    st.warning("Key Insight: 20% income drop pushes 3 out of 4 sample applicants into higher risk category.")

st.caption("This is a live interactive demo. Real model built in Excel + Power BI with 80 applicant records.")