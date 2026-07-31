from datetime import datetime

from attendance.repository import AttendanceRepository
from students.service import StudentService


class AttendanceService:

    @staticmethod
    def mark_attendance(student_id, confidence):

        now = datetime.now()

        record = {
            "student_id": student_id,
            "attendance_date": now.date().isoformat(),
            "attendance_time": now.strftime("%H:%M:%S"),
            "status": "Present",
            "confidence": confidence
        }

        print("\n==============================")
        print("Attendance Record:")
        print(record)

        try:

            response = AttendanceRepository.mark_attendance(record)

            if response is None:

                print("⚠ Attendance already marked today.")

                return {
                    "success": False,
                    "message": "Attendance already marked today."
                }

            print("✅ INSERT SUCCESS")
            print(response)

            return {
                "success": True,
                "message": "Attendance marked successfully."
            }

        except Exception as e:

            print("❌ INSERT FAILED")
            print(str(e))

            return {
                "success": False,
                "message": str(e)
            }

    @staticmethod
    def get_total_students():

        return len(StudentService.get_students())

    @staticmethod
    def get_total_present():

        return AttendanceRepository.get_total_present_today()

    @staticmethod
    def get_total_absent():

        return (
            AttendanceService.get_total_students()
            - AttendanceService.get_total_present()
        )

    @staticmethod
    def get_today_attendance():

        return AttendanceRepository.get_today_attendance().data

    @staticmethod
    def get_all_attendance():

        return AttendanceRepository.get_all_records().data