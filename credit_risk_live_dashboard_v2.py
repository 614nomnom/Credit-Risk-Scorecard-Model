"""
Improved Credit Risk Scorecard Live Dashboard (v2)
More interactive version with better filters and visuals
Run: streamlit run credit_risk_live_dashboard_v2.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="Credit Risk Scorecard | Kartik Rao",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0.3rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1F4E79 0%, #1565C0 100%);
        padding: 1.3rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0.2rem 0;
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🏦 Credit Risk Scorecard Dashboard</p>', unsafe_allow_html=True)
st.caption("MBA Finance Portfolio Project | Prepared by Kartik Rao | April 2026")

# ==================== DATA GENERATION ====================
np.random.seed(42)

def generate_data(n=80):
    data = []
    for i in range(n):
        income = np.random.choice([
            np.random.randint(18000, 45000),
            np.random.randint(45000, 85000),
            np.random.randint(85000, 180000)
        ], p=[0.4, 0.4, 0.2])
        
        emi = int(income * np.random.uniform(0.05, 0.28))
        loan_amount = int(income * np.random.uniform(10, 32))
        
        credit_history = np.random.choice(['Good', 'Average', 'Poor'], p=[0.55, 0.30, 0.15])
        employment = np.random.choice(['Salaried', 'Self-Employed'], p=[0.65, 0.35])
        
        # Simple scoring
        income_score = min(35, max(5, (income - 15000) // 2000))
        dti = (emi / income) * 100 if income > 0 else 0
        dti_score = 30 if dti < 15 else 20 if dti < 25 else 10 if dti < 35 else 5
        ch_score = 25 if credit_history == 'Good' else 12 if credit_history == 'Average' else 3
        emp_score = 10 if employment == 'Salaried' else 5
        
        total_score = income_score + dti_score + ch_score + emp_score
        
        if total_score >= 75:
            risk = 'Low Risk'
        elif total_score >= 55:
            risk = 'Medium Risk'
        else:
            risk = 'High Risk'
            
        data.append({
            'Applicant_ID': f'APP{str(i+1).zfill(3)}',
            'Monthly_Income': income,
            'Existing_EMI': emi,
            'Loan_Amount': loan_amount,
            'DTI_Ratio': round(dti, 1),
            'Credit_History': credit_history,
            'Employment_Type': employment,
            'Credit_Score': total_score,
            'Risk_Category': risk
        })
    return pd.DataFrame(data)

df = generate_data(80)

# ==================== SIDEBAR FILTERS ====================
st.sidebar.header("🔍 Filters")

# Income Range
income_min, income_max = st.sidebar.slider(
    "Monthly Income Range (₹)",
    min_value=15000,
    max_value=200000,
    value=(20000, 120000),
    step=5000
)

# Risk Category
risk_options = ['Low Risk', 'Medium Risk', 'High Risk']
selected_risk = st.sidebar.multiselect(
    "Risk Category",
    options=risk_options,
    default=risk_options
)

# Employment Type
emp_options = ['Salaried', 'Self-Employed']
selected_emp = st.sidebar.multiselect(
    "Employment Type",
    options=emp_options,
    default=emp_options
)

# Credit History
ch_options = ['Good', 'Average', 'Poor']
selected_ch = st.sidebar.multiselect(
    "Credit History",
    options=ch_options,
    default=ch_options
)

# Apply filters
filtered_df = df[
    (df['Monthly_Income'] >= income_min) &
    (df['Monthly_Income'] <= income_max) &
    (df['Risk_Category'].isin(selected_risk)) &
    (df['Employment_Type'].isin(selected_emp)) &
    (df['Credit_History'].isin(selected_ch))
]

# ==================== KPI CARDS ====================
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-label">Total Applicants</div>
        <div class="metric-value">{len(filtered_df)}</div>
        <div style="font-size:0.75rem; opacity:0.8;">Filtered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    approval_rate = round(len(filtered_df[filtered_df['Risk_Category'] == 'Low Risk']) / len(filtered_df) * 100, 1) if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card" style="background: linear-gradient(135deg, #2E7D32, #388E3C);">
        <div class="metric-label">Approval Rate</div>
        <div class="metric-value">{approval_rate}%</div>
        <div style="font-size:0.75rem; opacity:0.85;">Low Risk</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    high_risk_pct = round(len(filtered_df[filtered_df['Risk_Category'] == 'High Risk']) / len(filtered_df) * 100, 1) if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card" style="background: linear-gradient(135deg, #C00000, #B71C1C);">
        <div class="metric-label">High Risk %</div>
        <div class="metric-value">{high_risk_pct}%</div>
        <div style="font-size:0.75rem; opacity:0.85;">Monitor Closely</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_score = round(filtered_df['Credit_Score'].mean(), 1) if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="kpi-card" style="background: linear-gradient(135deg, #FF6B35, #E64A19);">
        <div class="metric-label">Avg Credit Score</div>
        <div class="metric-value">{avg_score}</div>
        <div style="font-size:0.75rem; opacity:0.85;">Out of 100</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["📊 Risk Distribution", "📈 Income vs Score", "⚠️ Scenario Impact"])

with tab1:
    st.subheader("Risk Category Distribution")
    
    if len(filtered_df) > 0:
        risk_counts = filtered_df['Risk_Category'].value_counts().reindex(['Low Risk', 'Medium Risk', 'High Risk']).fillna(0)
        
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color=risk_counts.index,
            color_discrete_map={
                'Low Risk': '#2E7D32',
                'Medium Risk': '#FF6B35',
                'High Risk': '#C00000'
            },
            hole=0.4
        )
        fig_pie.update_traces(textinfo='label+percent+value')
        fig_pie.update_layout(showlegend=True, height=450)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available for selected filters.")

with tab2:
    st.subheader("Income vs Credit Score Analysis")
    
    if len(filtered_df) > 0:
        fig_scatter = px.scatter(
            filtered_df,
            x='Monthly_Income',
            y='Credit_Score',
            color='Risk_Category',
            color_discrete_map={
                'Low Risk': '#2E7D32',
                'Medium Risk': '#FF6B35',
                'High Risk': '#C00000'
            },
            size='DTI_Ratio',
            hover_data=['Applicant_ID', 'Employment_Type', 'Credit_History'],
            title="Higher Income generally leads to Higher Credit Score"
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.caption("Bubble size represents DTI Ratio. Larger bubble = Higher existing debt burden.")
    else:
        st.warning("No data available for selected filters.")

with tab3:
    st.subheader("Scenario Impact: 20% Income Drop")
    
    # Simulate income drop impact
    scenario_df = filtered_df[['Applicant_ID', 'Credit_Score', 'Risk_Category']].copy()
    scenario_df['New_Score'] = (scenario_df['Credit_Score'] - np.random.randint(8, 18, len(scenario_df))).clip(30, 100)
    
    def get_new_risk(score):
        if score >= 75:
            return 'Low Risk'
        elif score >= 55:
            return 'Medium Risk'
        else:
            return 'High Risk'
    
    scenario_df['New_Risk'] = scenario_df['New_Score'].apply(get_new_risk)
    scenario_df['Risk_Change'] = scenario_df.apply(
        lambda x: '↑ Risk Increased' if x['New_Risk'] != x['Risk_Category'] else 'No Change', axis=1
    )
    
    # Show summary
    increased = len(scenario_df[scenario_df['Risk_Change'] == '↑ Risk Increased'])
    st.metric("Applicants whose Risk Increased", f"{increased} out of {len(scenario_df)}")
    
    st.dataframe(
        scenario_df[['Applicant_ID', 'Credit_Score', 'New_Score', 'Risk_Category', 'New_Risk', 'Risk_Change']].head(15),
        use_container_width=True,
        hide_index=True
    )
    
    st.warning("**Key Insight**: Even a moderate income drop can significantly increase risk levels for many applicants. This is why stress testing is critical in credit risk management.")

st.divider()

# Footer
st.caption("This is an improved interactive demo version. Real model built in Excel + Power BI with 80 applicant records.")