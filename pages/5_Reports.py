from io import BytesIO

import pandas as pd
import streamlit as st

from attendance.repository import AttendanceRepository

st.title("📋 Attendance Reports")
st.caption("View, Search and Export Attendance Records")

st.divider()

response = AttendanceRepository.get_all_records()

records = response.data

if records:

    processed_records = []

    for record in records:

        student = record.get("students", {})

        processed_records.append(
            {
                "Student Name": student.get("student_name", ""),
                "Roll Number": student.get("roll_number", ""),
                "Class": student.get("class", ""),
                "Section": student.get("section", ""),
                "Attendance Date": record.get("attendance_date"),
                "Attendance Time": record.get("attendance_time"),
                "Status": record.get("status"),
                "Confidence (%)": round(
                    float(record.get("confidence", 0)),
                    2
                )
            }
        )

    df = pd.DataFrame(processed_records)

    # ---------------------------------
    # Search Student
    # ---------------------------------

    search = st.text_input(
        "🔍 Search Student"
    )

    if search:

        df = df[
            df["Student Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # ---------------------------------
    # Filters
    # ---------------------------------

    col1, col2 = st.columns(2)

    with col1:

        status = st.selectbox(
            "Status",
            ["All"] + list(df["Status"].unique())
        )

        if status != "All":

            df = df[
                df["Status"] == status
            ]

    with col2:

        dates = sorted(
            df["Attendance Date"]
            .astype(str)
            .unique()
        )

        selected_date = st.selectbox(
            "Attendance Date",
            ["All"] + dates
        )

        if selected_date != "All":

            df = df[
                df["Attendance Date"].astype(str)
                == selected_date
            ]

    st.divider()

    # ---------------------------------
    # Summary
    # ---------------------------------

    total_records = len(df)

    present = len(
        df[df["Status"] == "Present"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 Total Records",
            total_records
        )

    with col2:

        st.metric(
            "✅ Present",
            present
        )

    st.divider()

    # ---------------------------------
    # Table
    # ---------------------------------

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # ---------------------------------
    # Export
    # ---------------------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Attendance Report"
        )

    excel_data = excel_buffer.getvalue()

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📊 Download Excel",
            excel_data,
            "attendance_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:

        st.download_button(
            "📄 Download CSV",
            csv_data,
            "attendance_report.csv",
            "text/csv"
        )

else:

    st.info("No attendance records found.")