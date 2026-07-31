import streamlit as st
import pandas as pd

from students.service import StudentService
from face.service import FaceService

st.title("🎓 Student Management")

tab1, tab2 = st.tabs(["➕ Add Student", "📋 View Students"])

# ============================================================
# ADD STUDENT
# ============================================================

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        roll_number = st.text_input("Roll Number")
        admission_number = st.text_input("Admission Number")
        student_name = st.text_input("Student Name")
        student_class = st.text_input("Class")

    with col2:
        section = st.text_input("Section")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        phone = st.text_input("Phone")
        email = st.text_input("Email")

    st.divider()

    st.subheader("Student Photos")

    photo1 = st.file_uploader(
        "Photo 1",
        type=["jpg", "jpeg", "png"],
        key="photo1"
    )

    photo2 = st.file_uploader(
        "Photo 2",
        type=["jpg", "jpeg", "png"],
        key="photo2"
    )

    photo3 = st.file_uploader(
        "Photo 3",
        type=["jpg", "jpeg", "png"],
        key="photo3"
    )

    st.divider()

    if st.button("💾 Save Student", key="save_student"):

        student = {
            "roll_number": roll_number,
            "admission_number": admission_number,
            "student_name": student_name,
            "class": student_class,
            "section": section,
            "gender": gender,
            "phone": phone,
            "email": email
        }

        success, message, saved_student = StudentService.add_student(student)

        if success:

            try:

                registered = FaceService.register_face(
                    student_id=saved_student["id"],
                    roll_number=roll_number,
                    uploaded_files=[photo1, photo2, photo3]
                )

                st.success(message)
                st.success(f"✅ {registered} face encodings registered.")

            except Exception as e:

                st.error(f"Face Registration Failed:\n\n{e}")

        else:

            st.error(message)

# ============================================================
# VIEW STUDENTS
# ============================================================

with tab2:

    students = StudentService.get_students()

    if students:

        df = pd.DataFrame(students)

        columns_to_hide = [
            "id",
            "created_at",
            "photo1",
            "photo2",
            "photo3"
        ]

        df = df.drop(
            columns=[c for c in columns_to_hide if c in df.columns]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No students found.")