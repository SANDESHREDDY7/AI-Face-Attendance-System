import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------
# Home Page
# ---------------------------------------------------

st.title("🎓 AI Face Attendance System")

st.markdown(
    """
## Welcome 👋

An AI-powered attendance system that recognizes students
from group photographs and automatically marks attendance.

---

### 🚀 Features

- 👨‍🎓 Student Management
- 😊 Face Registration
- 📸 Multi Face Recognition
- ✅ Automatic Attendance
- 📊 Dashboard
- 📋 Attendance Reports
- 📥 Excel Export
- 📄 CSV Export

---

### 📌 Workflow

1. Add Student
2. Upload 3 Face Photos
3. Generate Face Encoding
4. Upload Group Photo
5. Recognize Students
6. Mark Attendance
7. View Dashboard
8. Download Reports

---

Use the **sidebar** to navigate through the application.
"""
)

st.success("🚀 System Ready")

st.info(
    "Upload a group photo from the Attendance page to recognize students automatically."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👨‍🎓 Students", "∞")

with col2:
    st.metric("📸 Recognition", "AI Powered")

with col3:
    st.metric("💾 Database", "Supabase")

st.divider()

st.caption(
    "Developed using Python • Streamlit • OpenCV • face_recognition • Supabase"
)