import os
import tempfile

import cv2
import streamlit as st

from attendance.service import AttendanceService
from face.drawer import FaceDrawer
from face.recognizer import FaceRecognizer
from face.repository import FaceRepository

st.title("📸 Attendance")

# -----------------------------
# Session State
# -----------------------------
if "recognition_result" not in st.session_state:
    st.session_state.recognition_result = None

if "temp_image_path" not in st.session_state:
    st.session_state.temp_image_path = None

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Group Photo",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(uploaded_file, width="stretch")

    if st.button("🚀 Recognize Faces"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp:

            temp.write(uploaded_file.getbuffer())
            image_path = temp.name

        known_faces = FaceRepository.get_all_encodings()

        result = FaceRecognizer.recognize(
            image_path,
            known_faces
        )

        st.session_state.recognition_result = result
        st.session_state.temp_image_path = image_path

# -----------------------------
# Show Recognition Result
# -----------------------------
if st.session_state.recognition_result is not None:

    result = st.session_state.recognition_result

    output_image = FaceDrawer.draw_faces(
        result["image"],
        result["attendance"]
    )

    st.divider()

    st.subheader("Recognition Result")

    st.image(
        cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB),
        width="stretch"
    )

    recognized = len(result["students"])
    total_faces = len(result["attendance"])
    unknown_faces = total_faces - recognized

    st.success(
        f"Recognized {recognized} student(s)"
    )

    # -----------------------------
    # Attendance Summary
    # -----------------------------
    st.divider()

    st.subheader("📊 Attendance Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Faces Detected", total_faces)

    with col2:
        st.metric("✅ Registered", recognized)

    with col3:
        st.metric("❓ Unknown", unknown_faces)

    # -----------------------------
    # Recognized Students
    # -----------------------------
    st.divider()

    st.subheader("✅ Recognized Students")

    if recognized == 0:

        st.warning("No registered students found.")

    else:

        for person in result["attendance"]:

            if person["student"] is None:
                continue

            student = person["student"]

            confidence = (
                1 - person["distance"]
            ) * 100

            st.success(
                f"""
### 👤 {student['student_name']}

**Roll Number:** {student['roll_number']}

**Class:** {student['class']}

**Section:** {student['section']}

**Confidence:** {confidence:.2f}%
"""
            )

    # -----------------------------
    # Unknown Faces
    # -----------------------------
    st.divider()

    st.subheader("❓ Unknown Faces")

    unknown_count = 0

    for person in result["attendance"]:

        if person["student"] is None:

            unknown_count += 1

            st.info(
                f"Unknown Person #{unknown_count}"
            )

    if unknown_count == 0:

        st.success("🎉 No unknown faces detected.")

    # -----------------------------
    # Mark Attendance
    # -----------------------------
    st.divider()

    if st.button("✅ Mark Attendance"):

        inserted = 0
        skipped = 0

        for person in result["attendance"]:

            if person["student"] is None:
                continue

            try:

                response = AttendanceService.mark_attendance(
                    student_id=person["student"]["id"],
                    confidence=(1 - person["distance"]) * 100
                )

                if response["success"]:
                    inserted += 1
                else:
                    skipped += 1

            except Exception as e:

                st.error(
                    f"Failed to mark attendance for "
                    f"{person['student']['student_name']}: {e}"
                )

        if inserted > 0:

            st.success(
                f"✅ Attendance marked for {inserted} student(s)."
            )

        if skipped > 0:

            st.warning(
                f"⚠ {skipped} student(s) were already marked today."
            )

        # Remove temporary image
        if (
            st.session_state.temp_image_path
            and os.path.exists(st.session_state.temp_image_path)
        ):
            os.remove(st.session_state.temp_image_path)

        # Clear session
        st.session_state.recognition_result = None
        st.session_state.temp_image_path = None

        st.rerun()