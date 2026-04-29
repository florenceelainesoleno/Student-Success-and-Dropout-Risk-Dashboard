import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# =========================================================
# COLOR THEME CONSTANTS
# =========================================================
BG = "#0B132B"
SURFACE = "#111C3A"
SURFACE_2 = "#1C2541"
TEXT = "#F8FAFC"
MUTED = "#A9B4C2"
SUCCESS = "#2EC4B6"
DROPOUT = "#FF5A6A"
INFO = "#4CC9F0"
WARNING = "#FFBE0B"
PURPLE = "#8338EC"

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Student Dropout Risk Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.markdown('<div class="top-spacer"></div>', unsafe_allow_html=True)

image = Image.open("banner.png")
st.image(image, caption="", use_container_width=True)

st.markdown('<div class="banner-bottom-spacer"></div>', unsafe_allow_html=True)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            

header { display: none !important; }

[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

:root {
    --bg: #0B132B;
    --surface: #111C3A;
    --surface-2: #1C2541;
    --border: #3A506B;
    --text: #F8FAFC;
    --muted: #A9B4C2;
    --success: #2EC4B6;
    --danger: #FF5A6A;
    --info: #4CC9F0;
    --blue: #3A86FF;
    --warning: #FFBE0B;
    --purple: #8338EC;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}

.stApp {
    background: radial-gradient(circle at top left, rgba(76,201,240,0.18), transparent 32%),
                linear-gradient(135deg, #070D1F 0%, #0B132B 48%, #111C3A 100%);
    color: var(--text);
}

.main, .block-container { background: transparent !important; }
.block-container { 
    padding-top: 0rem; 
    padding-left: 3rem; 
    padding-right: 3rem; 
}

.top-spacer { height: 55px; }
.banner-bottom-spacer { height: 25px; }

[data-testid="stImage"] {
    border-radius: 26px;
    overflow: hidden;
    box-shadow: 0 20px 44px rgba(0,0,0,0.38);
    border: 1px solid rgba(76,201,240,0.25);
}

[data-testid="stImage"] img { border-radius: 26px; }

h1,h2,h3,h4,h5,h6,p,li,label {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}

.section-card {
    background: linear-gradient(135deg, rgba(36,56,95,0.98), rgba(22,36,71,0.98));
    color: var(--text);
    padding: 26px 30px;
    border-radius: 22px;
    border: 1px solid rgba(144,219,244,0.36);
    box-shadow: 0 20px 44px rgba(0,0,0,0.46), inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 20px;
}

.section-card h2, .section-title {
    color: var(--info) !important;
    font-weight: 800 !important;
}

.section-card p, .section-card li {
    color: #DDE7F3;
    font-size: 16px;
    line-height: 1.65;
}

.info-box {
    background: linear-gradient(135deg, rgba(36,56,95,0.98), rgba(58,134,255,0.22));
    color: var(--text);
    padding: 22px 26px;
    border-radius: 20px;
    border: 1px solid rgba(144,219,244,0.42);
    border-left: 8px solid var(--info);
    margin-bottom: 20px;
    box-shadow: 0 18px 38px rgba(0,0,0,0.42), inset 0 1px 0 rgba(255,255,255,0.05);
}

.info-box h3 {
    color: var(--info) !important;
    font-weight: 800 !important;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(36,56,95,0.98), rgba(22,36,71,0.98)) !important;
    padding: 24px 20px;
    border-radius: 24px !important;
    border: 1px solid rgba(144,219,244,0.40) !important;
    box-shadow: 0 18px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    text-align: center;
    min-height: 138px;
}

.kpi-card:hover {
    transform: translateY(-2px);
    transition: 0.25s ease;
    border-color: rgba(46,196,182,0.60) !important;
}

.kpi-label {
    color: #FFFFF;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 10px;
    letter-spacing: 0.2px;
}

.kpi-value {
    color: var(--text);
    font-size: 38px;
    font-weight: 800;
    line-height: 1.1;
}

.kpi-note {
    color:#FFFFF;
    font-size: 12px;
    margin-top: 8px;
}

.insight-box {
    background: linear-gradient(135deg, rgba(55,64,101,0.98), rgba(255,190,11,0.20));
    color: var(--text);
    padding: 24px 28px;
    border-radius: 22px;
    border: 1px solid rgba(255,190,11,0.35);
    border-left: 8px solid var(--warning);
    margin: 25px 0;
    box-shadow: 0 14px 30px rgba(0,0,0,0.28);
}

.insight-box h3 {
    color: var(--warning) !important;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
}

.insight-box p {
    color: #F8FAFC;
    font-size: 17px;
    line-height: 1.6;
}

.chart-card {
    background: linear-gradient(135deg, rgba(36,56,95,0.98), rgba(22,36,71,0.98));
    border-radius: 22px;
    padding: 18px 18px 10px 18px;
    border: 1px solid rgba(144,219,244,0.36);
    box-shadow: 0 18px 40px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 20px;
}

.explorer-box {
    background: linear-gradient(135deg, rgba(36,56,95,0.98), rgba(46,196,182,0.18));
    color: var(--text);
    padding: 22px 24px;
    border-radius: 22px;
    border: 1px solid rgba(144,219,244,0.40);
    box-shadow: 0 18px 40px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);
    margin: 18px 0 24px 0;
}

.small-note {
    color: #FFFFF;
    font-size: 14px;
    line-height: 1.5;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    padding: 25px 10px;
    border-top: 1px solid rgba(76,201,240,0.26);
    margin-top: 30px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081126 0%, #0B132B 48%, #111C3A 100%);
    border-right: 1px solid rgba(76,201,240,0.20);
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(36,56,95,0.96);
    color: #F8FAFC;
    border-radius: 12px 12px 0 0;
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    background: rgba(76,201,240,0.20) !important;
    color: var(--info) !important;
}

div[data-baseweb="select"] > div {
    background-color: #162447 !important;
    color: #F8FAFC !important;
    border-color: rgba(76,201,240,0.35) !important;
}


div[data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

.stMarkdown, .stMarkdown p, .stCaption, .stAlert, .stTextInput label,
.stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label {
    color: #F8FAFC !important;
}
            
div[role="radiogroup"] * {
    color: #FFFFFF !important;
}


span[data-testid="stIconMaterial"],
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
}

[data-testid="stPlotlyChart"] {
    background: #162447 !important;
    border: 1px solid rgba(200, 230, 255, 0.45) !important;
    border-radius: 28px !important;
    padding: 14px !important;
    box-shadow: 0 18px 40px rgba(0,0,0,0.42) !important;
    overflow: hidden !important;
}

/* ROUND THE ACTUAL PLOT AREA */
[data-testid="stPlotlyChart"] > div {
    border-radius: 24px !important;
    overflow: hidden !important;
}    

.marquee-container {
    margin-top: 40px;
    overflow: hidden;
    border-radius: 16px;
    background: linear-gradient(90deg, #1C2541, #24385F);
    border: 1px solid rgba(144,219,244,0.35);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    padding: 10px 0;
}

.marquee {
    display: flex;
    width: max-content;
    animation: scroll-left 25s linear infinite;
}

.marquee span {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #4CC9F0;
    letter-spacing: 1px;
    padding-right: 60px;
    text-shadow: 0 0 8px rgba(76,201,240,0.6);
}

@keyframes scroll-left {
    0% {
        transform: translateX(0%);
    }
    100% {
        transform: translateX(-50%);
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset file not found. Make sure cleaned_data.csv is in the same folder as this app.py file.")
    st.stop()

# =========================================================
# IMPORTANT COLUMNS
# =========================================================
TARGET_COL = "Target"
COURSE_COL = "Course"
GENDER_COL = "Gender"
SCHOLAR_COL = "Scholarship holder"
TUITION_COL = "Tuition fees up to date"
DEBTOR_COL = "Debtor"
AGE_COL = "Age at enrollment"
ADMISSION_COL = "Admission grade"
APPROVED_1ST = "Curricular units 1st sem (approved)"
APPROVED_2ND = "Curricular units 2nd sem (approved)"

# Create combined approved curricular units for clearer analysis
if APPROVED_1ST in df.columns and APPROVED_2ND in df.columns:
    df["Total approved curricular units"] = df[APPROVED_1ST] + df[APPROVED_2ND]
else:
    df["Total approved curricular units"] = 0

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.markdown("Use these filters to explore student groups and update all visuals automatically.")

outcome_options = sorted(df[TARGET_COL].dropna().unique().tolist())
selected_outcomes = st.sidebar.multiselect("Student Outcome", outcome_options, default=outcome_options)

course_options = sorted(df[COURSE_COL].dropna().unique().tolist())
selected_courses = st.sidebar.multiselect("Course", course_options, default=course_options)

gender_options = sorted(df[GENDER_COL].dropna().unique().tolist())
selected_genders = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

scholar_options = sorted(df[SCHOLAR_COL].dropna().unique().tolist())
selected_scholar = st.sidebar.multiselect("Scholarship Holder", scholar_options, default=scholar_options)

tuition_options = sorted(df[TUITION_COL].dropna().unique().tolist())
selected_tuition = st.sidebar.multiselect("Tuition Fees Up to Date", tuition_options, default=tuition_options)

debtor_options = sorted(df[DEBTOR_COL].dropna().unique().tolist())
selected_debtor = st.sidebar.multiselect("Debtor Status", debtor_options, default=debtor_options)

min_age = int(df[AGE_COL].min())
max_age = int(df[AGE_COL].max())
age_range = st.sidebar.slider("Age Range", min_value=0, max_value=70, value=(18, 70))

st.sidebar.markdown("---")
st.sidebar.markdown("## 🧭 Explore Controls")
st.sidebar.caption("These controls help users navigate the data without changing the main filters too much.")

# Interactive slider to control how many courses are shown in selected charts
top_n_courses = st.sidebar.slider(
    "Show Top N Courses in Course Charts",
    min_value=3,
    max_value=min(20, max(3, df[COURSE_COL].nunique())),
    value=min(12, max(3, df[COURSE_COL].nunique())),
    step=1
)

# Interactive grade range filter for academic exploration
grade_min = float(df[ADMISSION_COL].min())
grade_max = float(df[ADMISSION_COL].max())
admission_grade_range = st.sidebar.slider(
    "Admission Grade Range",
    min_value=float(round(grade_min, 1)),
    max_value=float(round(grade_max, 1)),
    value=(float(round(grade_min, 1)), float(round(grade_max, 1))),
    step=0.5
)

# Interactive metric selector used later in the custom explorer chart
metric_options = {
    "Dropout Rate (%)": "dropout_rate",
    "Graduation Rate (%)": "graduation_rate",
    "Average Admission Grade": "avg_admission",
    "Average Approved Units": "avg_units",
    "Student Count": "student_count"
}
selected_metric_label = st.sidebar.selectbox(
    "Metric to Explore by Course",
    list(metric_options.keys()),
    index=0
)
selected_metric = metric_options[selected_metric_label]

filtered_df = df[
    (df[TARGET_COL].isin(selected_outcomes)) &
    (df[COURSE_COL].isin(selected_courses)) &
    (df[GENDER_COL].isin(selected_genders)) &
    (df[SCHOLAR_COL].isin(selected_scholar)) &
    (df[TUITION_COL].isin(selected_tuition)) &
    (df[DEBTOR_COL].isin(selected_debtor)) &
    (df[AGE_COL].between(age_range[0], age_range[1])) &
    (df[ADMISSION_COL].between(admission_grade_range[0], admission_grade_range[1]))
].copy()

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def safe_rate(data, column, value):
    if len(data) == 0:
        return 0
    return (data[column].eq(value).mean() * 100)

def plotly_layout(fig, height=430):
    fig.update_layout(
        height=height,
        margin=dict(l=30, r=30, t=70, b=90),
        paper_bgcolor="#162447",
        plot_bgcolor="#162447",
        font=dict(family="Inter, Segoe UI, Arial", size=13, color="#F8FAFC"),
        title_font=dict(size=21, color="#4CC9F0", family="Inter, Segoe UI, Arial"),
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.18,
            xanchor="center",
            yanchor="top",
            font=dict(color="#F8FAFC", size=12)
        ),
        legend_title_text="",
        coloraxis_colorbar=dict(tickfont=dict(color="#F8FAFC"))
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(169,180,194,0.18)",
        zeroline=False,
        tickfont=dict(color="#DDE7F3"),
        title_font=dict(color="#F8FAFC")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(169,180,194,0.18)",
        zeroline=False,
        tickfont=dict(color="#DDE7F3"),
        title_font=dict(color="#F8FAFC")
    )

    return fig

# =========================================================
# INTRODUCTION AND DATASET INFO
# =========================================================
st.markdown("""
<div class="section-card">
<h2 style="color:#4CC9F0; font-weight:800;">📌 Dashboard Overview</h2>
<p>Behind every student record is a story shaped by academic performance, financial capacity, and personal circumstances.</p>

<p>This dashboard uses the <i><b style="color:#4CC9F0;">Predict Students’ Dropout and Academic Success</b></i> dataset, designed to identify at-risk students early using academic, demographic, and socio-economic data. Funded by the <b style="color:#FFBE0B;">SATDAP program in Portugal</b>, the dataset classifies students as <b>Dropout</b>, <b>Enrolled</b>, or <b>Graduate</b>, providing insights to support better student retention strategies.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<h3 style="color:#4CC9F0;font-weight:800;">📁 Data Overview</h3>
<b>Dataset Used:</b> Predict Students’ Dropout and Academic Success<br>
<b>Source:</b> Kaggle open dataset<br>
<b>Type of Data:</b> Student demographic, academic, social, and economic data<br>
<b>Purpose:</b> To analyze factors related to student dropout, graduation, and enrollment status
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# KPI CARDS
# =========================================================
total_students = len(filtered_df)
dropout_rate = safe_rate(filtered_df, TARGET_COL, "Dropout")
graduation_rate = safe_rate(filtered_df, TARGET_COL, "Graduate")
avg_admission = filtered_df[ADMISSION_COL].mean() if total_students else 0
scholar_rate = safe_rate(filtered_df, SCHOLAR_COL, "Yes")
tuition_rate = safe_rate(filtered_df, TUITION_COL, "Yes")

st.markdown(
    "<h2 style='color:#4CC9F0; font-weight:800;'>📊 Key Performance Indicators</h2>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

kpi_cols = st.columns(3)
with kpi_cols[0]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Total Students</div>
    <div class="kpi-value">{total_students:,}</div>
    <div class="kpi-note">Filtered student records</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Dropout Rate</div>
    <div class="kpi-value" style="color:#FF5A6A;">{dropout_rate:.1f}%</div>
    <div class="kpi-note">Main risk indicator</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Graduation Rate</div>
    <div class="kpi-value" style="color:#2EC4B6;">{graduation_rate:.1f}%</div>
    <div class="kpi-note">Main success indicator</div>
    </div>""", unsafe_allow_html=True)

st.write("")

kpi_cols2 = st.columns(3)
with kpi_cols2[0]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Average Admission Grade</div>
    <div class="kpi-value" style="color:#4CC9F0;">{avg_admission:.1f}</div>
    <div class="kpi-note">Academic preparedness</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols2[1]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Scholarship Holder Rate</div>
    <div class="kpi-value" style="color:#4CC9F0;">{scholar_rate:.1f}%</div>
    <div class="kpi-note">Financial support measure</div>
    </div>""", unsafe_allow_html=True)

with kpi_cols2[2]:
    st.markdown(f"""<div class="kpi-card" style="border:1px solid rgba(144,219,244,0.42); border-radius:24px; padding:22px; box-shadow:0 18px 38px rgba(0,0,0,0.44), inset 0 1px 0 rgba(255,255,255,0.06);">
    <div class="kpi-label">Tuition Payment Rate</div>
    <div class="kpi-value" style="color:#FFBE0B;">{tuition_rate:.1f}%</div>
    <div class="kpi-note">Financial stability measure</div>
    </div>""", unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# KEY INSIGHT
# =========================================================
st.markdown("""
<div class="insight-box">
<h3>🔎 Key Insight</h3>
<p><b>Students with unpaid tuition fees, no scholarship support, and lower approved curricular units show a higher tendency to drop out.</b> This pattern is evident in the dataset and is consistent with existing research, which highlights that financial constraints and limited academic progress significantly increase the risk of student attrition. Studies further emphasize that dropout is typically influenced by the combined effect of multiple factors rather than a single cause (Tinto, 1993; Bean & Metzner, 1985).</p>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# INTERACTIVE DATA EXPLORER
# =========================================================
st.markdown(
    "<h2 style='color:#4CC9F0; font-weight:800;'>🧭 Interactive Data Explorer</h2>",
    unsafe_allow_html=True
)
st.markdown("""
<div class="explorer-box">
<b>Use this section to ask your own question from the data.</b><br>
<span class="small-note">Choose a grouping variable, select a metric, and adjust the sidebar sliders to see how student outcomes change across groups.</span>
</div>
""", unsafe_allow_html=True)

explore_col1, explore_col2 = st.columns([1, 2])

with explore_col1:
    group_options = [COURSE_COL, GENDER_COL, SCHOLAR_COL, TUITION_COL, DEBTOR_COL]
    selected_group = st.selectbox("Group students by", group_options, index=0)
    sort_order = st.radio("Sort chart", ["Highest first", "Lowest first"], horizontal=True)

# Build dynamic summary table based on chosen group and selected metric
explorer_summary = filtered_df.groupby(selected_group).agg(
    student_count=(TARGET_COL, "count"),
    dropout_count=(TARGET_COL, lambda x: (x == "Dropout").sum()),
    graduate_count=(TARGET_COL, lambda x: (x == "Graduate").sum()),
    avg_admission=(ADMISSION_COL, "mean"),
    avg_units=("Total approved curricular units", "mean")
).reset_index()

explorer_summary["dropout_rate"] = explorer_summary["dropout_count"] / explorer_summary["student_count"] * 100
explorer_summary["graduation_rate"] = explorer_summary["graduate_count"] / explorer_summary["student_count"] * 100
explorer_summary = explorer_summary.sort_values(
    selected_metric,
    ascending=(sort_order == "Lowest first")
).head(top_n_courses)

with explore_col2:
    fig_explorer = px.bar(
        explorer_summary,
        x=selected_group,
        y=selected_metric,
        text=selected_metric,
        title=f"{selected_metric_label} by {selected_group}",
        color_discrete_sequence=["#4CC9F0"],
        hover_data={
            "student_count": True,
            "dropout_count": True,
            "graduate_count": True,
            "avg_admission": ":.1f",
            "avg_units": ":.1f",
            selected_metric: ":.1f"
        }
    )
    fig_explorer.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_explorer.update_xaxes(tickangle=-25)
    st.plotly_chart(plotly_layout(fig_explorer, height=460), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🔍 View the summary table behind this interactive chart"):
    readable_summary = explorer_summary.rename(columns={
        "student_count": "Student Count",
        "dropout_count": "Dropout Count",
        "graduate_count": "Graduate Count",
        "dropout_rate": "Dropout Rate (%)",
        "graduation_rate": "Graduation Rate (%)",
        "avg_admission": "Average Admission Grade",
        "avg_units": "Average Approved Units"
    })
    st.dataframe(readable_summary, use_container_width=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CHARTS
# =========================================================
st.markdown(
    "<h2 style='color:#4CC9F0; font-weight:800;'>📈 Student Success and Dropout Patterns</h2>",
    unsafe_allow_html=True
)

# Color map for consistent interpretation
color_map = {
    "Dropout": "#FF5A6A",
    "Graduate": "#2EC4B6",
    "Enrolled": "#4CC9F0"
}

row1_col1, row1_col2 = st.columns([1, 1])

with row1_col1:
    outcome_counts = filtered_df[TARGET_COL].value_counts().reset_index()
    outcome_counts.columns = [TARGET_COL, "Count"]
    fig_donut = px.pie(
        outcome_counts,
        names=TARGET_COL,
        values="Count",
        hole=0.55,
        title="Student Outcome Distribution",
        color=TARGET_COL,
        color_discrete_map=color_map
    )
    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_donut.update_layout(
    legend=dict(
        x=0.78,   # move left (adjust if needed)
        y=0.95,
        xanchor="left",
        yanchor="top",
        font=dict(color="#F8FAFC")
    )
)
    st.plotly_chart(plotly_layout(fig_donut), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    dropout_by_course = filtered_df[filtered_df[TARGET_COL] == "Dropout"].groupby(COURSE_COL).size().reset_index(name="Dropouts")
    if dropout_by_course.empty:
        st.info("No dropout records available for the selected filters.")
    else:
        fig_tree = px.treemap(
            dropout_by_course,
            path=[COURSE_COL],
            values="Dropouts",
            title="Dropout Contribution by Course",
            color="Dropouts",
            color_continuous_scale=["#111C3A", "#8338EC", "#FF5A6A"]
        )
        fig_tree.update_coloraxes(
            colorbar_title=None
)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(plotly_layout(fig_tree), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Heatmap: Dropout rate by course and gender
heat_data = filtered_df.groupby([COURSE_COL, GENDER_COL]).agg(
    total=(TARGET_COL, "count"),
    dropouts=(TARGET_COL, lambda x: (x == "Dropout").sum())
).reset_index()

heat_data["Dropout Rate (%)"] = (
    heat_data["dropouts"] / heat_data["total"] * 100
).round(1)

# Keep only selected number of top courses to avoid unreadable heatmap
major_courses = filtered_df[COURSE_COL].value_counts().head(top_n_courses).index.tolist()
heat_data = heat_data[heat_data[COURSE_COL].isin(major_courses)]

heat_pivot = heat_data.pivot(
    index=COURSE_COL,
    columns=GENDER_COL,
    values="Dropout Rate (%)"
).fillna(0)

fig_heat = go.Figure(data=go.Heatmap(
    z=heat_pivot.values,
    x=heat_pivot.columns,
    y=heat_pivot.index,
    colorscale=[[0, "#111C3A"], [0.5, "#8338EC"], [1, "#FF5A6A"]],
    text=heat_pivot.values,
    texttemplate="%{text:.1f}%",
    hovertemplate="Course: %{y}<br>Gender: %{x}<br>Dropout Rate: %{z:.1f}%<extra></extra>",
    colorbar=dict(
        x=0.98,
        xanchor="left",
        thickness=16,
        len=0.72,
        tickfont=dict(color="#F8FAFC", size=12)
    )
))

plotly_layout(fig_heat, height=540)

fig_heat.update_layout(
    title=dict(
        text=f"Dropout Rate by Course and Gender — Top {top_n_courses} Courses",
        font=dict(color="#4CC9F0", size=21, family="Inter, Segoe UI, Arial")
    ),
    margin=dict(l=40, r=120, t=70, b=50)
)

fig_heat.update_xaxes(domain=[0.0, 0.90])

fig_heat.update_traces(
    colorbar=dict(
        x=5,
        xanchor="left",
        thickness=16,
        len=0.95,
        tickfont=dict(color="#F8FAFC", size=12)
    )
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig_box = px.box(
        filtered_df,
        x=TARGET_COL,
        y=ADMISSION_COL,
        color=TARGET_COL,
        title="Admission Grade by Student Outcome",
        color_discrete_map=color_map,
        points="outliers"
    )
    fig_box.update_yaxes(range=[0, max(200, filtered_df[ADMISSION_COL].max() + 10)], title="Admission Grade")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(plotly_layout(fig_box), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    fig_violin = px.violin(
        filtered_df,
        x=TARGET_COL,
        y=AGE_COL,
        color=TARGET_COL,
        box=True,
        title="Age Distribution by Student Outcome",
        color_discrete_map=color_map
    )
    fig_violin.update_yaxes(range=[0, 70], title="Age at Enrollment")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(plotly_layout(fig_violin), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    fig_hist = px.histogram(
        filtered_df,
        x="Total approved curricular units",
        color=TARGET_COL,
        marginal="box",
        nbins=25,
        title="Distribution of Approved Curricular Units",
        color_discrete_map=color_map
    )
    fig_hist.update_xaxes(range=[0, max(1, filtered_df["Total approved curricular units"].max() + 2)])
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(plotly_layout(fig_hist), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row3_col2:
    fig_sunburst = px.sunburst(
        filtered_df,
        path=[SCHOLAR_COL, TUITION_COL, TARGET_COL],
        title="Financial Support Pathway to Student Outcome",
        color=TARGET_COL,
        color_discrete_map=color_map
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(plotly_layout(fig_sunburst), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# ADDITIONAL SIMPLE INSIGHTS
# =========================================================
st.markdown(
    "<h2 style='color:#4CC9F0; font-weight:800;'>🧠 Common Observations from the Filtered Data</h2>",
    unsafe_allow_html=True
)

current_dropout = filtered_df[filtered_df[TARGET_COL] == "Dropout"]
if len(current_dropout) > 0:
    top_course = current_dropout[COURSE_COL].value_counts().idxmax()
    no_scholar_dropout_rate = safe_rate(filtered_df[filtered_df[SCHOLAR_COL] == "No"], TARGET_COL, "Dropout")
    unpaid_dropout_rate = safe_rate(filtered_df[filtered_df[TUITION_COL] == "No"], TARGET_COL, "Dropout")
    avg_units_dropout = current_dropout["Total approved curricular units"].mean()
    avg_units_graduate = filtered_df[filtered_df[TARGET_COL] == "Graduate"]["Total approved curricular units"].mean()

    st.markdown(f"""
    <div class="section-card">
    <ul>
        <li><b style="color: #FFFFF;">{top_course}</b> currently contributes the highest number of dropout records within the selected filters.</li>
        <li>Students without scholarship support have a dropout rate of <b style="color: #FFFFF;">{no_scholar_dropout_rate:.1f}%</b>.</li>
        <li>Students with tuition fees not up to date have a dropout rate of <b style="color: #FFFFF;">{unpaid_dropout_rate:.1f}%</b>.</li>
        <li>Dropout students average <b style="color: #FFFFF;">{avg_units_dropout:.1f}</b> approved curricular units, while graduates average <b style="color: #FFFFF;">{avg_units_graduate:.1f}</b>.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("There are no dropout students under the current filter selection.")

    st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# ANALYSIS AND INSIGHTS
# =========================================================
    
# Main Title
st.markdown('<h2 style="color:#4CC9F0;font-weight:800;">📊 Final Analysis & Insights</h2>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)

# CSS shared properties: fixed height ensures alignment regardless of text length
box_height = "520px" 

with col1:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #24385F, #162447);
            padding: 24px;
            border-radius: 22px;
            border: 1px solid rgba(144,219,244,0.32);
            box-shadow: 0 20px 44px rgba(0,0,0,0.46), inset 0 1px 0 rgba(255,255,255,0.06);
            border-top: 5px solid #FF5A6A;
            height: {box_height};
            overflow-y: auto;
        ">
            <div style="color: #FF5A6A; font-size: 24px; font-weight: bold; margin-bottom: 12px;">
                🙎🏼‍♀️ Student Dropout
            </div>
            <div style="color: #DDE7F3; font-size: 16px; line-height: 1.6; font-family: 'Inter', 'Segoe UI', Arial, sans-serif;">
                Student dropout in the dataset reflects a gradual breakdown in academic integration, where students 
                consistently show lower approved units and weaker semester grades compared to graduates. 
                This indicates that dropout develops through repeated academic difficulty rather than a 
                sudden decision. 
                <br><br>
                According to <b>Vincent Tinto (1993)</b>, students who fail to integrate academically are less 
                likely to persist. In the dataset, this is evident in the widening academic gap, 
                confirming that early struggles compound over time. Financial instability intensifies this, 
                as students with unpaid tuition show significantly higher withdrawal rates, aligning with 
                <b>Bean & Metzner (1985)</b>.
                <br><br>
                <span style="color: #FFBE0B; font-weight: bold;">👉 Insight:</span> 
                Dropout is driven by the interaction of declining academic performance and financial pressure, 
                making early support critical.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #24385F, #162447);
            padding: 24px;
            border-radius: 22px;
            border: 1px solid rgba(144,219,244,0.32);
            box-shadow: 0 20px 44px rgba(0,0,0,0.46), inset 0 1px 0 rgba(255,255,255,0.06);
            border-top: 5px solid #2EC4B6;
            height: {box_height};
            overflow-y: auto;
        ">
            <div style="color: #2EC4B6; font-size: 24px; font-weight: bold; margin-bottom: 12px;">
                👩🏼‍🎓 Student Success
            </div>
            <div style="color: #DDE7F3; font-size: 16px; line-height: 1.6; font-family: 'Inter', 'Segoe UI', Arial, sans-serif;">
                Student success in the dataset is characterized by consistent academic progress and financial stability, 
                where graduates maintain higher grades and pass more curricular units across semesters. 
                This reflects sustained academic engagement, which aligns with <b>Tinto (1993)</b>, 
                who argues that strong academic integration increases persistence.
                <br><br>
                Furthermore, the high graduation rates among scholarship holders demonstrate the importance 
                of financial support in enabling students to remain focused and committed. This supports the findings 
                of <b>Bean & Metzner (1985)</b>, who highlight that financial stability reduces external stressors 
                that could otherwise lead to withdrawal.
                <br><br><br>
                <span style="color: #FFBE0B; font-weight: bold;">👉 Insight:</span> 
                Graduation occurs when students experience a reinforcing cycle of academic success and financial support.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# REFERENCES
# =========================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #24385F, #162447);
        border: 1px solid rgba(144, 219, 244, 0.38);
        border-radius: 20px;
        padding: 26px 28px;
        margin-top: 40px;
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.44), inset 0 1px 0 rgba(255,255,255,0.06);
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        ">
            <span style="font-size: 22px;">🔎</span>
            <h3 style="
                margin: 0;
                color: #4CC9F0;
                font-weight: 800;
                font-size: 22px;
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            ">
                References
            </h3>
        </div>
        <div style="
            color: #DDE7F3;
            font-size: 15.5px;
            line-height: 1.7;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        ">
            <p style="margin-bottom: 12px;">
                Tinto, V. (1993). <i>Leaving College: Rethinking the Causes and Cures of Student Attrition</i> (2nd ed.). 
                Chicago, IL: University of Chicago Press.
                <br>
                <span style="color: #4CC9F0;">https://doi.org/10.7208/chicago/9780226922461.001.0001</span>
            </p>
            <p style="margin-bottom: 12px;">
                Bean, J. P., & Metzner, B. S. (1985). A conceptual model of nontraditional undergraduate student attrition.
                <i>Review of Educational Research</i>, 55(4), 485–540.
                <br>
                <span style="color: #4CC9F0;">http://dx.doi.org/10.3102/00346543055004485</span>
            </p>
            <p style="margin-bottom: 12px;">
                Realinho, V., Vieira Martins, J., Machado, J., & Baptista, L. (2021). <i>Predict Students' Dropout and Academic Success</i>. 
                UCI Machine Learning Repository.
                <br>
                <span style="color: #4CC9F0;">https://doi.org/10.24432/C5MC89</span>
            </p>
            <p style="margin-bottom: 0;">
                The Devastator. (2023). <i>Higher Education Predictors of Student Retention</i> [Data set]. 
                Kaggle.
                <br>
                <span style="color: #4CC9F0;">https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention</span>
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
Data Source: <b>Predict Students’ Dropout and Academic Success Dataset</b> from Kaggle.<br>
This dataset is publicly available and used for academic and analytical purposes.<br>
Dashboard created using <b>Python, Streamlit, Pandas, and Plotly</b>.
</div>
""", unsafe_allow_html=True)

# =========================================================
# MARQUEE
# =========================================================
st.markdown("""
<div class="marquee-container">
    <div class="marquee">
        <span>Developed by Balictar, Biñas, and Soleño · Analytics Tools and Techniques · 2026</span>
        <span>🔵</span>
        <span>Developed by Balictar, Biñas, and Soleño · Analytics Tools and Techniques · 2026</span>
        <span>🔵</span>
        <span>Developed by Balictar, Biñas, and Soleño · Analytics Tools and Techniques · 2026</span>
        <span>🔵</span>
        <span>Developed by Balictar, Biñas, and Soleño · Analytics Tools and Techniques · 2026</span>
    </div>
</div>
""", unsafe_allow_html=True)
