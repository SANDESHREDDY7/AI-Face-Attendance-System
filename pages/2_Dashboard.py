import streamlit as st
import pandas as pd
import plotly.express as px

from attendance.service import AttendanceService

st.set_page_config(
    page_title="Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# DATA
# ==========================================================

total_students = AttendanceService.get_total_students()
present_today = AttendanceService.get_total_present()
absent_today = AttendanceService.get_total_absent()

attendance_percentage = 0

if total_students > 0:
    attendance_percentage = (
        present_today / total_students
    ) * 100

attendance = AttendanceService.get_today_attendance()

# ==========================================================
# HEADER
# ==========================================================

st.title("🎓 AI Face Attendance System")
st.caption(
    "Real-time face detection and automated student attendance tracking"
)

st.markdown("")

# ==========================================================
# TOP CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )

with col2:

    st.metric(
        "✅ Present Today",
        present_today
    )

with col3:

    st.metric(
        "📈 Attendance Rate",
        f"{attendance_percentage:.1f}%"
    )

with col4:

    st.metric(
        "📅 Absent Today",
        absent_today
    )

st.divider()

# ==========================================================
# CHART + RECENT ACTIVITY
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.subheader("📊 Attendance Overview")

    chart_data = pd.DataFrame(
        {
            "Status": [
                "Present",
                "Absent"
            ],
            "Students": [
                present_today,
                absent_today
            ]
        }
    )

    fig = px.bar(
        chart_data,
        x="Status",
        y="Students",
        text="Students"
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    st.subheader("🕒 Recent Activity")

    if attendance:

        recent = attendance[-5:]

        for row in reversed(recent):

            st.success(
                f"""
**Student ID:** {row['student_id']}

🕒 {row['attendance_time']}

✅ {row['status']}
"""
            )

    else:

        st.info(
            "No attendance recorded today."
        )

st.divider()

# ==========================================================
# TODAY'S ATTENDANCE
# ==========================================================

st.subheader("📋 Today's Attendance")

if attendance:

    df = pd.DataFrame(attendance)

    hide_columns = [
        "id",
        "created_at"
    ]

    df = df.drop(
        columns=[
            c for c in hide_columns
            if c in df.columns
        ]
    )

    df.columns = [
        col.replace(
            "_",
            " "
        ).title()
        for col in df.columns
    ]

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No attendance recorded today."
    )

st.divider()

st.caption(
    "Built with Python • Streamlit • OpenCV • face_recognition • Supabase"
)