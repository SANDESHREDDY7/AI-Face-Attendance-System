class StudentValidator:

    @staticmethod
    def validate(student):
        required_fields = [
            "roll_number",
            "student_name",
            "class",
            "section"
        ]

        for field in required_fields:
            if not student.get(field):
                return False, f"{field.replace('_', ' ').title()} is required."

        return True, "Validation Successful"