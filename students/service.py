from students.repository import StudentRepository
from students.validator import StudentValidator
from face.repository import FaceRepository


class StudentService:

    @staticmethod
    def add_student(student):

        valid, message = StudentValidator.validate(student)

        if not valid:
            return False, message, None

        try:

            saved_student = StudentRepository.insert_student(student)

            student_data = saved_student.data[0]
            student_data["is_encoded"] = False
            student_data["encodings_count"] = 0

            return (
                True,
                "✅ Student added successfully.",
                student_data,
            )

        except Exception as e:

            error = str(e).lower()

            if "duplicate key" in error or "unique constraint" in error:
                return (
                    False,
                    "❌ Roll Number already exists.",
                    None,
                )

            return False, str(e), None

    @staticmethod
    def get_students():

        students = StudentRepository.get_all_students().data or []

        try:
            encodings = FaceRepository.get_all_encodings() or []
            encoded_counts = {}
            for enc in encodings:
                sid = enc.get("student_id")
                if sid is not None:
                    encoded_counts[sid] = encoded_counts.get(sid, 0) + 1

            for s in students:
                count = encoded_counts.get(s["id"], 0)
                s["encodings_count"] = count
                s["is_encoded"] = count > 0

        except Exception as e:
            print("Error checking face encodings:", e)
            for s in students:
                s["encodings_count"] = 0
                s["is_encoded"] = False

        return students

    @staticmethod
    def get_student(student_id):

        return StudentRepository.get_student_by_id(student_id)

    @staticmethod
    def delete_student(student_id):

        return StudentRepository.delete_student(student_id)
