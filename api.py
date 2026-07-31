from typing import List

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from students.service import StudentService
from face.service import FaceService
from attendance.service import AttendanceService
from face.recognizer import FaceRecognizer
from face.image_processor import ImageProcessor

app = FastAPI(
    title="AI Face Attendance API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Face Attendance API"
    }


# ----------------------------------------------------
# Students
# ----------------------------------------------------

@app.get("/students")
def get_students():
    return StudentService.get_students()


@app.post("/students")
def add_student(student: dict):

    success, message, data = StudentService.add_student(student)

    return {
        "success": success,
        "message": message,
        "data": data,
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    StudentService.delete_student(student_id)

    return {
        "success": True,
        "message": "Student deleted successfully"
    }


# ----------------------------------------------------
# Face Registration
# ----------------------------------------------------

@app.post("/students/{student_id}/register-face")
async def register_face(
    student_id: int,
    roll_number: str = Form(...),
    photos: List[UploadFile] = File(...)
):
    try:

        total_faces = FaceService.register_face(
            student_id,
            roll_number,
            photos
        )

        return {
            "success": True,
            "message": f"{total_faces} face encodings generated successfully.",
            "faces_registered": total_faces
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ----------------------------------------------------
# Group Attendance
# ----------------------------------------------------

@app.post("/attendance/recognize")
async def recognize_attendance(
    photo: UploadFile = File(...)
):
    try:

        image_path = ImageProcessor.save_group_image(photo)

        known_faces = FaceService.get_registered_faces()

        result = FaceRecognizer.recognize(
            image_path,
            known_faces
        )

        for person in result["attendance"]:

            if person["student"] is None:
                continue

            AttendanceService.mark_attendance(
                person["student"]["id"],
                person["confidence"]
            )

        return {
            "success": True,
            "faces_detected": len(result["attendance"]),
            "students": result["attendance"]
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ----------------------------------------------------
# Attendance Reports
# ----------------------------------------------------

@app.get("/attendance")
def get_attendance():

    return {
        "success": True,
        "data": AttendanceService.get_all_attendance()
    }


@app.get("/attendance/today")
def get_today_attendance():

    return {
        "success": True,
        "data": AttendanceService.get_today_attendance()
    }


@app.get("/attendance/stats")
def attendance_stats():

    total_students = AttendanceService.get_total_students()
    present_today = AttendanceService.get_total_present()
    absent_today = AttendanceService.get_total_absent()

    attendance_rate = 0

    if total_students > 0:
        attendance_rate = round(
            (present_today / total_students) * 100,
            2
        )

    return {
        "success": True,
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
        "attendance_rate": attendance_rate
    }

    return {
        "success": True,
        "total_students": AttendanceService.get_total_students(),
        "present_today": AttendanceService.get_total_present(),
        "absent_today": AttendanceService.get_total_absent(),
    }


# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }