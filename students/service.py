from students.repository import StudentRepository
from students.validator import StudentValidator


class StudentService:

    @staticmethod
    def add_student(student):

        valid, message = StudentValidator.validate(student)

        if not valid:
            return False, message, None

        try:

            saved_student = StudentRepository.insert_student(student)

            return (
                True,
                "✅ Student added successfully.",
                saved_student.data[0],
            )

        except Exception as e:

            error = str(e).lower()

            if "duplicate key" in error:
                return (
                    False,
                    "❌ Roll Number already exists.",
                    None,
                )

            return False, str(e), None

    @staticmethod
    def get_students():

        return StudentRepository.get_all_students().data

    @staticmethod
    def get_student(student_id):

        return StudentRepository.get_student_by_id(student_id)

    @staticmethod
    def delete_student(student_id):

        return StudentRepository.delete_student(student_id)
    