import streamlit as st
import pandas as pd

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# LOGINde
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if not st.session_state.logged_in:

    st.title("🎓 Student Performance Analytics Dashboard")
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Select Role",
        ["Trainer", "Admin", "Student"]
    )

    if st.button("Login"):

        if username == "trainer" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.role = "Trainer"
            st.rerun()

        elif username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.rerun()

        elif username == "student" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.role = "Student"
            st.rerun()

        else:
            st.error("❌ Invalid username or password")

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Student Performance Analytics Dashboard")

st.write(
    "Data-driven dashboard for monitoring student performance."
)

st.write(
    f"Logged in as: **{st.session_state.role}**"
)

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()

st.divider()


# ============================================================
# CSV UPLOAD
# ============================================================

st.subheader("📂 Upload Student Performance CSV")

uploaded_file = st.file_uploader(
    "Upload student_data.csv",
    type=["csv"]
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is None:

    st.info("👆 Please upload student_data.csv to start.")

else:

    # --------------------------------------------------------
    # READ CSV
    # --------------------------------------------------------

    try:

        df = pd.read_csv(uploaded_file)

    except Exception as error:

        st.error("❌ Unable to read the CSV file.")
        st.error(str(error))
        st.stop()


    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    df.columns = df.columns.str.strip()


    # --------------------------------------------------------
    # REQUIRED COLUMNS
    # --------------------------------------------------------

    required_columns = [
        "Name",
        "Batch",
        "Topic",
        "Average",
        "Attendance",
        "Assignments"
    ]

    missing_columns = []

    for column in required_columns:

        if column not in df.columns:
            missing_columns.append(column)


    if len(missing_columns) > 0:

        st.error(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

        st.info(
            "Your CSV must contain: "
            + ", ".join(required_columns)
        )

        st.stop()


    # --------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # --------------------------------------------------------

    df["Average"] = pd.to_numeric(
        df["Average"],
        errors="coerce"
    )

    df["Attendance"] = pd.to_numeric(
        df["Attendance"],
        errors="coerce"
    )

    df["Assignments"] = pd.to_numeric(
        df["Assignments"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # REMOVE EMPTY DATA
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "Name",
            "Batch",
            "Topic",
            "Average",
            "Attendance",
            "Assignments"
        ]
    )


    # ========================================================
    # STATUS / RISK CALCULATION
    # ========================================================

    def calculate_status(row):

        if (
            row["Average"] < 60
            or row["Attendance"] < 75
            or row["Assignments"] < 60
        ):

            return "🔴 At Risk"

        elif (
            row["Average"] < 70
            or row["Attendance"] < 80
            or row["Assignments"] < 70
        ):

            return "🟡 Needs Improvement"

        else:

            return "🟢 Good"


    df["Status"] = df.apply(
        calculate_status,
        axis=1
    )


    # ========================================================
    # CREATE RISK REASON
    # ========================================================

    def get_reason(row):

        reasons = []

        if row["Average"] < 60:
            reasons.append("Low average score")

        if row["Attendance"] < 75:
            reasons.append("Low attendance")

        if row["Assignments"] < 60:
            reasons.append("Low assignment score")

        if len(reasons) == 0:
            return "No major issue"

        return ", ".join(reasons)


    df["Risk Reason"] = df.apply(
        get_reason,
        axis=1
    )


    # ========================================================
    # KPI SECTION
    # ========================================================

    st.subheader("📊 Key Performance Indicators")

    total_students = df["Name"].nunique()

    class_average = df["Average"].mean()

    top_performer_row = df.loc[
        df["Average"].idxmax()
    ]

    top_performer = top_performer_row["Name"]

    at_risk_count = len(
        df[df["Status"] == "🔴 At Risk"]
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:

        st.metric(
            "📊 Class Average",
            f"{class_average:.2f}"
        )

    with col3:

        st.metric(
            "🏆 Top Performer",
            top_performer
        )

    with col4:

        st.metric(
            "⚠️ At-Risk Students",
            at_risk_count
        )


    st.divider()


    # ========================================================
    # FILTERS
    # ========================================================

    st.subheader("🔎 Filters")

    col1, col2 = st.columns(2)

    with col1:

        topics = ["All"] + sorted(
            df["Topic"].unique().tolist()
        )

        selected_topic = st.selectbox(
            "Select Topic",
            topics
        )

    with col2:

        statuses = [
            "All",
            "🟢 Good",
            "🟡 Needs Improvement",
            "🔴 At Risk"
        ]

        selected_status = st.selectbox(
            "Select Status",
            statuses
        )


    filtered_df = df.copy()


    if selected_topic != "All":

        filtered_df = filtered_df[
            filtered_df["Topic"] == selected_topic
        ]


    if selected_status != "All":

        filtered_df = filtered_df[
            filtered_df["Status"] == selected_status
        ]


    # ========================================================
    # STUDENT PERFORMANCE TABLE
    # ========================================================

    st.subheader("👨‍🎓 Student Performance")

    st.dataframe(
        filtered_df[
            [
                "Name",
                "Batch",
                "Topic",
                "Average",
                "Attendance",
                "Assignments",
                "Status",
                "Risk Reason"
            ]
        ],
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # PERFORMANCE CHARTS
    # ========================================================

    st.subheader("📈 Performance Analytics")

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # TOPIC AVERAGE
    # --------------------------------------------------------

    with col1:

        st.write("### 📚 Topic-wise Average")

        topic_average = (
            df.groupby("Topic")["Average"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(topic_average)


    # --------------------------------------------------------
    # TOPIC ATTENDANCE
    # --------------------------------------------------------

    with col2:

        st.write("### 🕒 Topic-wise Attendance")

        topic_attendance = (
            df.groupby("Topic")["Attendance"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(topic_attendance)


    # ========================================================
    # ATTENDANCE VS PERFORMANCE
    # ========================================================

    st.write("### 📊 Attendance vs Performance")

    chart_data = df[
        ["Name", "Attendance", "Average"]
    ].set_index("Name")

    st.line_chart(chart_data)


    st.divider()


    # ========================================================
    # AT-RISK STUDENTS
    # ========================================================

    st.subheader("🚨 At-Risk Students & Reasons")

    risk_df = df[
        df["Status"] == "🔴 At Risk"
    ]


    if len(risk_df) > 0:

        st.warning(
            f"{len(risk_df)} student(s) need immediate attention."
        )


        st.dataframe(
            risk_df[
                [
                    "Name",
                    "Topic",
                    "Average",
                    "Attendance",
                    "Assignments",
                    "Status",
                    "Risk Reason"
                ]
            ],
            use_container_width=True
        )


        st.write("### 💡 Trainer Recommendations")


        for _, student in risk_df.iterrows():

            st.write(
                f"**👤 {student['Name']}**"
            )

            if student["Average"] < 60:

                st.info(
                    f"{student['Name']}: "
                    "Provide additional academic support."
                )

            if student["Attendance"] < 75:

                st.info(
                    f"{student['Name']}: "
                    "Contact student regarding attendance."
                )

            if student["Assignments"] < 60:

                st.info(
                    f"{student['Name']}: "
                    "Follow up on assignment completion."
                )


    else:

        st.success(
            "🎉 No students are currently at high risk."
        )


    st.divider()


    # ========================================================
    # TOP PERFORMERS
    # ========================================================

    st.subheader("🏆 Top Performing Students")

    top_students = df.sort_values(
        by="Average",
        ascending=False
    ).head(5)


    st.dataframe(
        top_students[
            [
                "Name",
                "Topic",
                "Average",
                "Attendance",
                "Assignments"
            ]
        ],
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # WEAK TOPICS
    # ========================================================

    st.subheader("📚 Topic-wise Weak Areas")

    weak_topics = (
        df.groupby("Topic")["Average"]
        .mean()
        .sort_values()
    )


    weak_topics_df = (
        weak_topics
        .reset_index()
        .rename(
            columns={
                "Average": "Average Score"
            }
        )
    )


    st.dataframe(
        weak_topics_df,
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # INDIVIDUAL STUDENT REPORT
    # ========================================================

    st.subheader("👤 Individual Student Report")

    student_names = sorted(
        df["Name"].unique().tolist()
    )


    selected_student = st.selectbox(
        "Select a student",
        student_names
    )


    student_data = df[
        df["Name"] == selected_student
    ]


    st.dataframe(
        student_data[
            [
                "Name",
                "Batch",
                "Topic",
                "Average",
                "Attendance",
                "Assignments",
                "Status",
                "Risk Reason"
            ]
        ],
        use_container_width=True
    )


    # --------------------------------------------------------
    # INDIVIDUAL STUDENT KPIs
    # --------------------------------------------------------

    student_average = student_data["Average"].mean()

    student_attendance = student_data["Attendance"].mean()

    student_assignments = student_data["Assignments"].mean()


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Score",
            f"{student_average:.2f}"
        )


    with col2:

        st.metric(
            "Attendance",
            f"{student_attendance:.2f}%"
        )


    with col3:

        st.metric(
            "Assignment Score",
            f"{student_assignments:.2f}"
        )


    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    st.divider()

    st.success(
        "✅ Student Performance Dashboard loaded successfully!"
    )