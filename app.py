import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from report_generator import generate_report
from reportlab.platypus import Image
from datetime import datetime
import io
import base64



def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()
# to save the predicted values
# Database functions
from database import (
    create_database,
    save_prediction,
    get_prediction_history,
    clear_prediction_history
)

create_database()

def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="#F8FBFF",
        plot_bgcolor="#F8FBFF",

        font=dict(
            color="#2C3E50",
            size=14
        ),

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),

        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#DCEBFA")
    )

    return fig

st.markdown("""
<style>

.chart-card{
    background:white;
    border-radius:16px;
    border:1px solid #E3EEF9;
    padding:15px;
    box-shadow:0 4px 12px rgba(21,101,192,0.08);
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

st.write("")

#this shows live data for our app
# from datetime import datetime

# today = datetime.today().strftime("%d %B %Y")

# st.markdown(f"###  {today}")
st.markdown("""
<style>

.main{
    background:#F5F9FF;
}

.section-title{
    color:#1E3A8A;
    font-size:32px;
    font-weight:700;
    margin-top:20px;
}

.section-line{
    height:3px;
    background:#0B5ED7;
    border-radius:10px;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
    border-left:6px solid #0B5ED7;
    margin-bottom:15px;
}

.metric-card{
    background:white;
    padding:18px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
    border-top:5px solid #0B5ED7;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)


# ===========================
# PROFESSIONAL KPI CARDS
# ===========================
st.markdown("""
<style>
.kpi-card{
    background:linear-gradient(135deg,#FAFCFF,#EEF7FF);
    border:1px solid #D9EAFB;
    border-left:5px solid #8EC5FF;
    padding:22px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 4px 12px rgba(74,111,165,0.08);
    transition:all .3s ease;
    margin-bottom:12px;
}

.kpi-card:hover{
    transform:translateY(-4px);
    box-shadow:0 10px 22px rgba(74,111,165,0.12);
}

.kpi-icon{
    font-size:34px;
    color:#5B9BD5;
}

.kpi-title{
    font-size:17px;
    font-weight:600;
    color:#5A6E8C;
    margin-top:8px;
    letter-spacing:0.3px;
}

.kpi-value{
    font-size:42px;
    font-weight:700;
    color:#1F4E79;
    margin-top:8px;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="",
    layout="wide"
)
st.markdown("""
<style>

/* ===== Plotly Chart Cards ===== */

div[data-testid="stPlotlyChart"]{
    background:white;
    border:1px solid #DCEBFA;
    border-radius:18px;
    padding:10px;
    margin-bottom:18px;

    box-shadow:0 4px 12px rgba(21,101,192,0.08);

    transition:0.3s;
}

/* Hover Effect */

div[data-testid="stPlotlyChart"]:hover{
    box-shadow:0 8px 20px rgba(21,101,192,0.15);
}

/* Remove unnecessary top spacing */

div[data-testid="stPlotlyChart"] > div{
    margin-top:0 !important;
}

</style>
""", unsafe_allow_html=True)

# st.title("📊Employee Attrition Dashboard")
# st.subheader("📊 Employee Attrition Dashboard")

df=pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

model = joblib.load("employee_attrition_model.pkl")
# encoder = joblib.load("label_encoder.pkl")
encoders = joblib.load("encoders.pkl")

st.sidebar.image("assets/logo for HR.png", width=80)

st.sidebar.markdown("## HR INSIGHTS ")
# page = st.sidebar.radio(
#     " Navigate To: ",
#     ["Dashboard", "Employee Attrition Prediction"]
# )
page = st.sidebar.radio(
    "Navigate To:",
    [
        " Home",
        " Dashboard",
        " Employee Attrition Prediction"
    ])
if page == " Home":
        
    st.sidebar.markdown("""
    <div style="
    background:#F8FBFF;
    border:1px solid #D8E8FF;
    border-radius:12px;
    padding:18px;
    margin-top:15px;
    ">

    <h3 style="
    color:#1565C0;
    margin-top:0;
    margin-bottom:18px;
    text-align:center;">
    PROJECT DETAILS
    </h3>

    <div style="margin-bottom:16px;">
    <p style="margin:0;color:#7A8FA8;font-size:12px;font-weight:600;">
    PROJECT
    </p>
    <p style="margin:2px 0 0 0;color:#1F3A5F;font-size:16px;font-weight:700;">
    Employee Attrition Prediction
    </p>
    </div>

    <div style="margin-bottom:16px;">
    <p style="margin:0;color:#7A8FA8;font-size:12px;font-weight:600;">
    DOMAIN
    </p>
    <p style="margin:2px 0 0 0;color:#1F3A5F;font-size:16px;font-weight:700;">
    Machine Learning
    </p>
    </div>

    <div style="margin-bottom:16px;">
    <p style="margin:0;color:#7A8FA8;font-size:12px;font-weight:600;">
    MODEL
    </p>
    <p style="margin:2px 0 0 0;color:#1F3A5F;font-size:16px;font-weight:700;">
    Logistic Regression
    </p>
    </div>

    <div style="margin-bottom:16px;">
    <p style="margin:0;color:#7A8FA8;font-size:12px;font-weight:600;">
    DATASET
    </p>
    <p style="margin:2px 0 0 0;color:#1F3A5F;font-size:16px;font-weight:700;">
    IBM HR Analytics
    </p>
    </div>

    <div style="margin-bottom:5px;">
    <p style="margin:0;color:#7A8FA8;font-size:12px;font-weight:600;">
    RECORDS
    </p>
    <p style="margin:2px 0 0 0;color:#1F3A5F;font-size:16px;font-weight:700;">
    1470 Employees
    </p>
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.image("assets/banner.png", width="stretch")
    st.markdown("""
        <style>
        img {
            border-radius:12px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    st.markdown('<div class="section-title">Project Overview</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-line"></div>',unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

    HR Insights is an AI-powered Employee Attrition Prediction Dashboard
    developed to assist HR professionals in identifying employees who are
    at risk of leaving the organization.

    The application combines Machine Learning, Data Analytics and Business
    Intelligence to support data-driven HR decision making.

    </div>
    """,unsafe_allow_html=True)
    st.markdown('<div class="section-title">Quick Statistics</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Employees</div>
            <div class="kpi-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Departments</div>
            <div class="kpi-value">{df["Department"].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Job Roles</div>
            <div class="kpi-value">{df["JobRole"].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Model Accuracy</div>
            <div class="kpi-value">89%</div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown('<div class="section-title">Platform Features</div>',unsafe_allow_html=True)

    st.markdown("---")

    col1,col2=st.columns(2)

    with col1:

        st.info("Interactive HR Dashboard")

        st.info("Employee Attrition Prediction")

        st.info("Professional PDF Report")

        st.info("Prediction History")

    with col2:

        st.info("Prediction History Download")

        st.info("Prediction History Management")

        st.info("Interactive Visualizations")

        st.info("Real-Time Predictions")

    # st.markdown("---")

    st.markdown('<div class="section-title">Technology Stack</div>',unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3=st.columns(3)

    with c1:

        st.markdown("""
        <div class="card">

        <b>Programming</b>

        Python

        Pandas

        NumPy

        </div>
        """,unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card">

        <b>Machine Learning</b>

        Scikit-Learn

        Logistic Regression

        Joblib

        </div>
        """,unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card">

        <b>Application</b>

        Streamlit

        Plotly

        SQLite

        ReportLab

        </div>
        """,unsafe_allow_html=True)

    # st.markdown("---")
    st.markdown('<div class="section-title">Dataset Information</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"""
    <div class="card">

    <b>Dataset</b> : IBM HR Analytics Employee Attrition Dataset
                
    <b>Total Employees</b> : {len(df)}

    <b>Features</b> : {df.shape[1]}

    <b>Target Variable</b> : Attrition

    </div>

    """,unsafe_allow_html=True)

    
    st.markdown('<div class="section-title">Project Objectives</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""

✔ Predict employee attrition using Machine Learning

✔ Assist HR professionals in employee retention

✔ Generate professional PDF reports

✔ Maintain prediction history

✔ Provide interactive business dashboards

✔ Enable data-driven HR decision making

""")
    st.markdown('<div class="section-title">Machine Learning Workflow</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.image("assets/workFlow.png",use_container_width=True)

    st.markdown('<div class="section-title">Developer Information</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div class="card">

    <b>Developer</b><br>
    Dhanya R

    <b>Project</b><br>
    HR Insights – Employee Attrition Prediction Dashboard

    <b>Framework</b><br>
    Streamlit

    <b>Machine Learning Model</b><br>
    Logistic Regression

    <b>Database</b><br>
    SQLite

    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">

    HR INSIGHTS • Employee Attrition Prediction Dashboard

    Version 1.0

    Developed by Dhanya R

    </div>
    """,unsafe_allow_html=True)


elif page == " Dashboard":
    st.markdown("""
<div style="
background:linear-gradient(90deg,#F8FBFF,#EEF6FF);
padding:15px 28px;
border-radius:12px;
border:1px solid #D9EAFB;
box-shadow:0 2px 8px rgba(21,101,192,0.08);
margin-bottom:20px;
">

<h1 style="
margin:0;
font-size:34px;
font-weight:800;
color:#1565C0;
letter-spacing:0.5px;
line-height:1.1;
">
HR INSIGHTS
</h1>

<h2 style="
margin:6px 0 4px 0;
font-size:22px;
font-weight:600;
color:#2F3E4E;
line-height:1.2;
">
Employee Attrition Prediction Dashboard
</h2>

<p style="
margin:0;
font-size:15px;
color:#6E7E91;
line-height:1.3;
">
AI-Powered Human Resource Analytics Platform
</p>

</div>
""", unsafe_allow_html=True)
    Department=df["Department"].unique()
    # lets create an filter 
    selected_department=st.sidebar.selectbox(
        "Select Department",["All"]+list(Department)
    )
    if selected_department!="All":
        df=df[df["Department"]==selected_department]

    #GENDER FILTER
    gender=df["Gender"].unique()
    selected_gender=st.sidebar.selectbox(
        "Select Gender", ["All"]+list(gender)
    )
    if selected_gender!="All":
        df=df[df["Gender"]==selected_gender]

    #JOB ROLE FILTER
    job=df["JobRole"].unique()
    selected_job=st.sidebar.selectbox(
        "Select Job Role", ["All"]+list(job)
    )
    if selected_job!="All":
        df=df[df["JobRole"]==selected_job]

    #EDUCATION FILTER
    Education=df["EducationField"].unique()
    selected_education=st.sidebar.selectbox(
        "Select Education Field", ["All"]+list(Education)
    )
    if selected_education!="All":
        df=df[df["EducationField"]==selected_education]

    total_employees = df.shape[0]
    employees_left = df[df["Attrition"] == "Yes"].shape[0]
    average_age = df["Age"].mean()
    average_income = df["MonthlyIncome"].mean()

    attrition_rate = (employees_left / total_employees) * 100

    df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[18,25,35,45,55,65],
    labels=["18-25","26-35","36-45","46-55","55+"]
)
    age_attrition = (
    df[df["Attrition"] == "Yes"]
    .groupby("AgeGroup")
    .size()
    .reset_index(name="Employees Left")
)
    st.markdown("""
<h2 style="color:#1E3A8A;margin-bottom:5px;">
Employee Statistics
</h2>

<p style="
color:#6B7280;
font-size:16px;
margin-top:0;
margin-bottom:20px;">
Key workforce metrics and employee insights
</p>
""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title"> Total Employees</div>
            <div class="kpi-value">{total_employees}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # st.metric(" Employees Left", employees_left)
        # st.markdown(f"""
        # <div style="
        # background:white;
        # padding:12px;
        # border-radius:15px;
        # box-shadow:0 4px 12px rgba(0,0,0,0.15);
        # text-align:center;
        # ">

        # <h4> Employees Left</h4>

        # <h1 style="color:#1976D2;">{employees_left}</h1>

        # </div>
        # """, unsafe_allow_html=True)
         st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Employees Left</div>
            <div class="kpi-value">{employees_left}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # st.metric(" Attrition Rate", f"{attrition_rate:.2f}%")
        # st.markdown(f"""
        # <div style="
        # background:white;
        # padding:10px;
        # border-radius:15px;
        # box-shadow:0 4px 12px rgba(0,0,0,0.15);
        # text-align:center;
        # ">

        # <h4> Attrition Rate</h4>

        # <h1 style="color:#1976D2;">{attrition_rate:.2f}%</h1>

        # </div>
        # """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Attrition Rate</div>
            <div class="kpi-value">{attrition_rate:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    col4,col5=st.columns(2)
    with col4:
        # st.metric(" Average Salary", f"{average_income:.2f}")
        # st.markdown(f"""
        # <div style="
        # background:white;
        # padding:12px;
        # border-radius:15px;
        # box-shadow:0 4px 12px rgba(0,0,0,0.15);
        # text-align:center;
        # ">

        # <h4> Average Salary</h4>

        # <h1 style="color:#1976D2;">₹{average_income:,.0f}</h1>

        # </div>
        # """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Average Salary</div>
            <div class="kpi-value">₹{average_income:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        # st.metric(" Average Age", f"{average_age:.2f}")
        # st.markdown(f"""
        # <div style="
        # background:white;
        # padding:12px;
        # border-radius:15px;
        # box-shadow:0 4px 12px rgba(0,0,0,0.15);
        # text-align:center;
        # ">

        # <h4> Average Age</h4>

        # <h1 style="color:#1976D2;">{average_age:.2f}</h1>

        # </div>
        # """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-title">Average Age</div>
            <div class="kpi-value">{average_age:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander(" View Dataset"):
        st.dataframe(df)

    with st.expander(" Statistical Summary"):
        st.dataframe(df.describe())

    # CHART 1 - Bar chart for department count
    # col1,col2=st.columns(2)
    # with col1:
    #     department_count=df["Department"].value_counts()
    #     # st.write(department_count)
    #     #creating the chart using Plotly

    #     fig=px.bar(
    #         department_count,
    #         x=department_count.index,
    #         y=department_count.values,
    #         color_discrete_sequence=["#1976D2"],
    #         title=" Employees by Department",
    #         labels={
    #             "X":"Department",
    #             "Y":"Number of Employees"})
    #     fig.update_traces(text=department_count.values,textposition="outside")
    #     fig.update_layout(
    #         xaxis_title="Department",
    #         yaxis_title="Employees"
    #     )
    #     fig.update_layout(height=420)
    #     st.plotly_chart(fig,
    #     use_container_width=True,
    #     config={"displayModeBar": False})
    # with col2:
    #     attrition_count = df["Attrition"].value_counts()
    #     # st.write(attrition_count)

    #     fig = px.pie(
    #         values=attrition_count.values,
    #         names=attrition_count.index,
    #         title=" Attrition Distribution",
    #         color_discrete_sequence=[
    #             "#1976D2",
    #             "#64B5F6"
    #         ]
    #     )
    #     fig.update_traces(
    #         textposition="inside",
    #         textinfo="percent+label"
    #     )
    #     fig.update_layout(
    #     height=420,
    #     title_x=0.5)
    #     fig.update_layout(height=420)
    #     fig.update_layout(showlegend=False)
    #     st.plotly_chart(
    #     fig,
    #     use_container_width=True,
    #     config={"displayModeBar": False})
    col1, col2 = st.columns(2)

# =======================
# Employees by Department
# =======================

    with col1:

        # st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        # st.markdown(
        #     '<div class="chart-title">Employees by Department</div>',
        #     unsafe_allow_html=True
        # )

        department_count = df["Department"].value_counts()

        fig = px.bar(
            department_count,
            x=department_count.index,
            y=department_count.values,
            color_discrete_sequence=["#1976D2"],
            labels={
                "x": "Department",
                "y": "Employees"
            }
        )

        fig.update_traces(
            text=department_count.values,
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Employees",
            height=380,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Employees by Department</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)


    # =======================
    # Attrition Distribution
    # =======================

    with col2:

        # st.markdown(
        #     '<div class="chart-title">Attrition Distribution</div>',
        #     unsafe_allow_html=True
        # )

        attrition_count = df["Attrition"].value_counts()

        fig = px.pie(
            values=attrition_count.values,
            names=attrition_count.index,
            color_discrete_sequence=[
                "#1976D2",
                "#64B5F6"
            ]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            height=380,
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition Distribution
</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # #CHART 3 ATTRITION BY DEPARTMENT

    col1,col2=st.columns(2)
    with col1:
        # st.subheader(" Attrition by Department")

        left_employee = df[df["Attrition"] == "Yes"]

        attrition_department = (
            left_employee.groupby("Department")
            .size()
            .reset_index(name="Employees Left")
        )
        def wrap_text(text):
            return "<br>".join(text.split())

        attrition_department["Department"] = attrition_department["Department"].apply(wrap_text)

        attrition_department = attrition_department.sort_values(
            by="Employees Left",
            ascending=False
        )

        fig = px.bar(
            attrition_department,
            x="Department",
            y="Employees Left",
            color="Department",
            text="Employees Left",
            color_discrete_sequence=[
            "#1976D2",
            "#64B5F6",
            "#26A69A" 
        ])
        fig.update_xaxes(
            showgrid=False
        )

        fig.update_yaxes(
            gridcolor="#E0E0E0"
        )
        

        fig.update_traces(textposition="outside")

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Employees Left"
        )
        fig.update_layout(showlegend=False)
        # st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition by Department
</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)
        st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
        
    

    #CHART 4 ATTRITION BY GENDER
    with col2:
        # st.subheader(" Attrition by Gender")

        gender_attrition = (
            left_employee.groupby("Gender")
            .size()
            .reset_index(name="Employees Left")
        )

        fig = px.bar(
            gender_attrition,
            x="Gender",
            y="Employees Left",
            color="Gender",
            text="Employees Left",
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            xaxis_title="Gender",
            yaxis_title="Employees Left"
        )
        fig.update_layout(showlegend=False)
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition by Gender
</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)
        st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    #CHART 5 AND 6
    #BAR CHART FOR ATTRITION BY JOB ROLE
    # col1,col2=st.columns(2)
    # st.subheader(" Attrition by Job Role")

    jobrole_attrition = (
    left_employee.groupby("JobRole")
    .size()
    .reset_index(name="Employees Left")
    )

    jobrole_attrition = jobrole_attrition.sort_values(
    by="Employees Left",
    ascending=True
    )

    fig = px.bar(
    jobrole_attrition,
    x="Employees Left",
    y="JobRole",
    orientation="h",
    text="Employees Left",
    color="Employees Left",
    # title="Attrition by Job Role",
    color_continuous_scale=[
    "#64B5F6",
    "#1976D2",
    "#26A69A"
    ]
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
    height=500,
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=20, b=20)
    )
    st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition by Job Role
</h4>
""", unsafe_allow_html=True)
    fig = style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([3, 2])

    with col1:

        # st.subheader(" Attrition by Age Group")

        fig_age = px.bar(
            age_attrition,
            x="AgeGroup",
            y="Employees Left",
            text="Employees Left",
            color="AgeGroup",
            color_discrete_sequence=[
                "#1976D2",
                "#64B5F6",
                "#26A69A",
                "#81C784",
                "#90CAF9"
            ],
            # title="Attrition by Age Group"
        )

        fig_age.update_traces(
            textposition="outside",
            marker_line_color="white",
            marker_line_width=1.5
        )

        fig_age.update_layout(
            height=430,
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Age Group",
            yaxis_title="Employees Left",
            font=dict(size=14)
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition by Age Group
</h4>
""", unsafe_allow_html=True)
        fig_age = style_chart(fig_age)

        st.plotly_chart(
            fig_age,
            use_container_width=True,
            config={"displayModeBar": False}
        )
    with col2:

        # st.subheader(" Average Salary by Department")

        salary_department = (
            df.groupby("Department")["MonthlyIncome"]
            .mean()
            .reset_index()
        )

        def wrap_text(text):
            return "<br>".join(text.split())

        salary_department["Department"] = salary_department["Department"].apply(wrap_text)

        fig_salary = px.bar(
            salary_department,
            x="Department",
            y="MonthlyIncome",
            text="MonthlyIncome",
            color="Department",
            # title="Average Salary by Department",
            color_discrete_sequence=[
                "#1976D2",
                "#64B5F6",
                "#26A69A"
            ]
        )

        fig_salary.update_traces(
            texttemplate="₹%{text:.0f}",
            textposition="outside",
            marker_line_color="white",
            marker_line_width=1.5
        )

        fig_salary.update_xaxes(tickangle=0)

        fig_salary.update_layout(
            height=430,
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Department",
            yaxis_title="Average Monthly Income",
            font=dict(size=14)
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Average Salary by Department
</h4>
""", unsafe_allow_html=True)
        fig_salary = style_chart(fig_salary)

        st.plotly_chart(
            fig_salary,
            use_container_width=True,
            config={"displayModeBar": False}
        )
    #CHART 7 AND 8
    #BAR CHART FOR ATTRITION BY JOB ROLE
    col1,col2=st.columns(2)
    with col1:
        # st.subheader(" Attrition by Education Field")

        left_employee = df[df["Attrition"] == "Yes"]

        attrition_education = (
            left_employee.groupby("EducationField")
            .size()
            .reset_index(name="Employees Left")
        )
        def wrap_text(text):
            return "<br>".join(text.split())

        attrition_education["EducationField"] = attrition_education["EducationField"].apply(wrap_text)

        attrition_education = attrition_education.sort_values(
            by="Employees Left",
            ascending=False
        )

        fig = px.bar(
            attrition_education,
            x="EducationField",
            y="Employees Left",
            color="EducationField",
            text="Employees Left",
            color_discrete_sequence=[
                "#1976D2",
                "#64B5F6",
                "#26A69A"
            ],
            # title="Attrition by Education Field"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Education Field",
            yaxis_title="Employees Left",
            showlegend=False,
            height=500
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Attrition by Education Field
</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)

        st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False})
    with col2:
        overtime_attrition = (
            df.groupby(["OverTime", "Attrition"])
            .size()
            .reset_index(name="Employees")
        )

        fig = px.bar(
            overtime_attrition,
            x="OverTime",
            y="Employees",
            color="Attrition",
            barmode="group",
            text="Employees",
            # title="Overtime vs Attrition",
            color_discrete_sequence=[
                "#1976D2",
                "#64B5F6",
                "#26A69A"
            ]
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            xaxis_title="OverTime",
            yaxis_title="Number of Employees",
            height=500
        )
        st.markdown("""
<h4 style="
color:#1E3A8A;
font-weight:700;
margin-bottom:8px;">
Overtime vs Attrition
</h4>
""", unsafe_allow_html=True)
        fig = style_chart(fig)

        st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False})

elif page == " Employee Attrition Prediction":

    # st.header(" Employee Attrition Prediction")
    st.markdown("""
<div style="
background:linear-gradient(90deg,#F8FBFF,#EEF6FF);
padding:15px 28px;
border-radius:12px;
border:1px solid #D9EAFB;
box-shadow:0 2px 8px rgba(21,101,192,0.08);
margin-bottom:20px;
">

<h1 style="
margin:0;
font-size:34px;
font-weight:800;
color:#1565C0;
letter-spacing:0.5px;
line-height:1.1;
">
ATTRITION PREDICTION
</h1>

<h2 style="
margin:6px 0 4px 0;
font-size:22px;
font-weight:600;
color:#2F3E4E;
line-height:1.2;
">
Employee Attrition Prediction Dashboard
</h2>

<p style="
margin:0;
font-size:15px;
color:#6E7E91;
line-height:1.3;
">
AI-Powered Human Resource Analytics Platform
</p>

</div>
""", unsafe_allow_html=True)
    st.write("Fill in the employee details below.")

    # ===========================
    # Personal Information
    # ===========================
    # st.subheader(" Personal Information")
    st.markdown("""
<h3 style="color:#1E3A8A;margin-bottom:5px;">
PERSONAL INFORMATION
</h3>

<p style="
color:#6B7280;
font-size:16px;
margin-top:0;
margin-bottom:20px;">
</p>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 18, 60, 30)

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Divorced"]
        )

        education = st.selectbox(
            "Education Level",
            [1, 2, 3, 4, 5]
        )

        education_field = st.selectbox(
            "Education Field",
            [
                "Life Sciences",
                "Medical",
                "Marketing",
                "Technical Degree",
                "Human Resources",
                "Other"
            ]
        )

    with col2:

        business_travel = st.selectbox(
            "Business Travel",
            [
                "Travel_Rarely",
                "Travel_Frequently",
                "Non-Travel"
            ]
        )

        department = st.selectbox(
            "Department",
            [
                "Research & Development",
                "Sales",
                "Human Resources"
            ]
        )

        job_role = st.selectbox(
            "Job Role",
            [
                "Sales Executive",
                "Research Scientist",
                "Laboratory Technician",
                "Manufacturing Director",
                "Healthcare Representative",
                "Manager",
                "Sales Representative",
                "Research Director",
                "Human Resources"
            ]
        )

        over_time = st.selectbox(
            "Over Time",
            ["No", "Yes"]
        )



    # ===========================
    # Salary & Job Information
    # ===========================

    # st.subheader(" Job Information")
    st.markdown("""
<h3 style="color:#1E3A8A;margin-bottom:5px;">
JOB INFORMATION
</h3>

<p style="
color:#6B7280;
font-size:16px;
margin-top:0;
margin-bottom:20px;">
</p>
""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:

        daily_rate = st.number_input("Daily Rate", value=800)

        hourly_rate = st.number_input("Hourly Rate", value=65)

        monthly_income = st.number_input("Monthly Income", value=5000)

        monthly_rate = st.number_input("Monthly Rate", value=15000)

        percent_salary_hike = st.slider(
            "Percent Salary Hike",
            10,
            30,
            15
        )

        stock_option_level = st.slider(
            "Stock Option Level",
            0,
            3,
            1
        )

    with col4:

        job_level = st.slider(
            "Job Level",
            1,
            5,
            2
        )

        job_involvement = st.slider(
            "Job Involvement",
            1,
            4,
            3
        )

        job_satisfaction = st.slider(
            "Job Satisfaction",
            1,
            4,
            3
        )

        performance_rating = st.slider(
            "Performance Rating",
            1,
            4,
            3
        )

        relationship_satisfaction = st.slider(
            "Relationship Satisfaction",
            1,
            4,
            3
        )

        work_life_balance = st.slider(
            "Work Life Balance",
            1,
            4,
            3
        )

    # st.subheader(" Experience")
    st.markdown("""
<h3 style="color:#1E3A8A;margin-bottom:5px;">
EXPERIENCE
</h3>

<p style="
color:#6B7280;
font-size:16px;
margin-top:0;
margin-bottom:20px;">
</p>
""", unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:

        distance_from_home = st.number_input(
            "Distance From Home",
            value=5
        )

        num_companies_worked = st.number_input(
            "Companies Worked",
            value=2
        )

        total_working_years = st.number_input(
            "Total Working Years",
            value=10
        )

        training_times_last_year = st.number_input(
            "Training Times Last Year",
            value=2
        )

    with col6:

        years_at_company = st.number_input(
            "Years At Company",
            value=5
        )

        years_in_current_role = st.number_input(
            "Years In Current Role",
            value=3
        )

        years_since_last_promotion = st.number_input(
            "Years Since Last Promotion",
            value=1
        )

        years_with_curr_manager = st.number_input(
            "Years With Current Manager",
            value=3
        )



    # ===========================
    # Other Information
    # ===========================

    # st.subheader(" Other Information")
    st.markdown("""
<h3 style="color:#1E3A8A;margin-bottom:5px;">
OTHER INFORMATION
</h3>

<p style="
color:#6B7280;
font-size:16px;
margin-top:0;
margin-bottom:20px;">
</p>
""", unsafe_allow_html=True)

    environment_satisfaction = st.slider(
        "Environment Satisfaction",
        1,
        4,
        3
    )

    # Predict Button

    if st.button(" Predict Attrition"):

    # Encode categorical features
        business_travel_text = business_travel
        department_text = department
        education_field_text = education_field
        gender_text = gender
        job_role_text = job_role
        marital_status_text = marital_status
        over_time_text = over_time

        business_travel = encoders["BusinessTravel"].transform([business_travel])[0]
        department = encoders["Department"].transform([department])[0]
        education_field = encoders["EducationField"].transform([education_field])[0]
        gender = encoders["Gender"].transform([gender])[0]
        job_role = encoders["JobRole"].transform([job_role])[0]
        marital_status = encoders["MaritalStatus"].transform([marital_status])[0]
        over_time = encoders["OverTime"].transform([over_time])[0]


        # Create input data
        input_data = [[
            age,
            business_travel,
            daily_rate,
            department,
            distance_from_home,
            education,
            education_field,
            environment_satisfaction,
            gender,
            hourly_rate,
            job_involvement,
            job_level,
            job_role,
            job_satisfaction,
            marital_status,
            monthly_income,
            monthly_rate,
            num_companies_worked,
            over_time,
            percent_salary_hike,
            performance_rating,
            relationship_satisfaction,
            stock_option_level,
            total_working_years,
            training_times_last_year,
            work_life_balance,
            years_at_company,
            years_in_current_role,
            years_since_last_promotion,
            years_with_curr_manager
        ]]

        # Make Prediction
        prediction = model.predict(input_data)[0]

        # Get Prediction Probability
        probability = model.predict_proba(input_data)

        stay_probability = probability[0][0] * 100
        leave_probability = probability[0][1] * 100

        st.markdown("""
            <div style="
            background:#f8f9fa;
            padding:15px;
            border-radius:10px;
            border-left:6px solid #1E88E5;">
            <h3> Prediction Result</h3>
            </div>
            """, unsafe_allow_html=True)
        
        
        if prediction == 1:
            prediction_text = "Employee is likely to Leave the Company"
            st.error(f" {prediction_text}")
        else:
            prediction_text = "Employee is likely to Stay in the Company"
            st.success(f" {prediction_text}")
        
        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")

        save_prediction(
            date=current_date,
            age=age,
            gender=gender_text,
            department=department_text,
            job_role=job_role_text,
            prediction=prediction_text,
            stay_probability=stay_probability,
            leave_probability=leave_probability
        )


        # Display Probabilities
        col1, col2 = st.columns(2)

        with col1:
            st.metric(" Stay Probability", f"{stay_probability:.2f}%")

        with col2:
            st.metric(" Leave Probability", f"{leave_probability:.2f}%")

        # Progress Bars
        st.write("### Prediction Confidence")

        st.write("Stay Probability")
        st.progress(stay_probability / 100)

        st.write("Leave Probability")
        st.progress(leave_probability / 100)

        st.subheader(" Prediction Summary")

        reasons = []

        if over_time == encoders["OverTime"].transform(["Yes"])[0]:
            reasons.append("• Employee works overtime.")

        if monthly_income < 5000:
            reasons.append("• Monthly income is relatively low.")

        if job_satisfaction <= 2:
            reasons.append("• Job satisfaction is low.")

        if work_life_balance <= 2:
            reasons.append("• Work-life balance is poor.")

        if years_at_company < 2:
            reasons.append("• Employee is relatively new to the company.")

        if environment_satisfaction <= 2:
            reasons.append("• Environment satisfaction is low.")

        if len(reasons) == 0:
            st.success("The employee has good overall workplace indicators.")
        else:
            st.warning("Possible factors influencing the prediction:")
            for reason in reasons:
                st.write(reason)

        st.subheader(" Employee Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Age:** {age}")
            st.write(f"**Gender:** {gender_text}")
            st.write(f"**Department:** {department_text}")
            st.write(f"**Job Role:** {job_role_text}")
            st.write(f"**Education Field:** {education_field_text}")
            st.write(f"**Business Travel:** {business_travel_text}")

        with col2:
            st.write(f"**Monthly Income:** ₹{monthly_income:,}")
            st.write(f"**OverTime:** {over_time_text}")
            st.write(f"**Job Satisfaction:** {job_satisfaction}")
            st.write(f"**Work-Life Balance:** {work_life_balance}")
            st.write(f"**Years at Company:** {years_at_company}")
            st.write(f"**Marital Status:** {marital_status_text}")


        employee_details = {
            "Age": age,
            "Gender": gender_text,
            "Department": department_text,
            "Job Role": job_role_text,
            "Business Travel": business_travel_text,
            "Marital Status": marital_status_text,
            "Education Field": education_field_text,
            "Monthly Income": f"₹{monthly_income:,}",
            "OverTime": over_time_text,
            "Job Satisfaction": job_satisfaction,
            "Work-Life Balance": work_life_balance,
            "Years at Company": years_at_company
        }


        generate_report(
            filename="employee_report.pdf",
            prediction=prediction_text,
            stay_probability=stay_probability,
            leave_probability=leave_probability,
            employee_details=employee_details,
            reasons=reasons
        )
        with open("employee_report.pdf", "rb") as pdf:

            st.download_button(
                label=" Download Report",
                data=pdf,
                file_name="Employee_Attrition_Report.pdf",
                mime="application/pdf"
            )
    st.divider()
    # st.markdown("---")
    # st.subheader("🔍 Prediction History")
    st.markdown("""
<h4 style="color:#1E3A8A;margin-bottom:5px;">
🔍 Prediction History
</h4>

<p style="
color:#6B7280;
font-size:5px;
margin-top:0;
margin-bottom:15px;">
</p>
""", unsafe_allow_html=True)

    history = get_prediction_history()

    if len(history) == 0:
        st.info("No predictions available.")
    else:
        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Date",
                "Age",
                "Gender",
                "Department",
                "Job Role",
                "Prediction",
                "Stay %",
                "Leave %"
            ]
        )

        # Remove ID column
        history_df = history_df.drop(columns=["ID"])

        # Round probabilities
        history_df["Stay %"] = history_df["Stay %"].round(2)
        history_df["Leave %"] = history_df["Leave %"].round(2)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )
        # Convert dataframe to CSV
        csv = history_df.to_csv(index=False).encode("utf-8")

        st.markdown("---")

        st.download_button(
            label=" Download Prediction History",
            data=csv,
            file_name="Prediction_History.csv",
            mime="text/csv"
        )
        if st.button("🗑 Clear Prediction History"):

            clear_prediction_history()

            st.success("Prediction history cleared successfully.")

            st.rerun()