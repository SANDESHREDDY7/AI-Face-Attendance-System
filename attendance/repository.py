from datetime import datetime

from database.supabase_client import supabase


class AttendanceRepository:

    @staticmethod
    def attendance_exists(student_id):

        today = datetime.now().date().isoformat()

        response = (
            supabase.table("attendance_records")
            .select("id")
            .eq("student_id", student_id)
            .eq("attendance_date", today)
            .execute()
        )

        return len(response.data) > 0

    @staticmethod
    def mark_attendance(record):

        if AttendanceRepository.attendance_exists(
            record["student_id"]
        ):

            print(
                f"⚠ Attendance already marked for "
                f"Student ID {record['student_id']}"
            )

            return None

        print(
            f"✅ Marking attendance for "
            f"Student ID {record['student_id']}"
        )

        return (
            supabase.table("attendance_records")
            .insert(record)
            .execute()
        )

    @staticmethod
    def get_today_attendance():

        today = datetime.now().date().isoformat()

        return (
            supabase.table("attendance_records")
            .select(
                """
                attendance_date,
                attendance_time,
                status,
                confidence,
                students(
                    student_name,
                    roll_number,
                    class,
                    section
                )
                """
            )
            .eq("attendance_date", today)
            .order("attendance_time")
            .execute()
        )

    @staticmethod
    def get_total_present_today():

        today = datetime.now().date().isoformat()

        response = (
            supabase.table("attendance_records")
            .select("id")
            .eq("attendance_date", today)
            .execute()
        )

        return len(response.data)

    @staticmethod
    def get_all_records():

        return (
            supabase.table("attendance_records")
            .select(
                """
                attendance_date,
                attendance_time,
                status,
                confidence,
                students(
                    student_name,
                    roll_number,
                    class,
                    section
                )
                """
            )
            .order("attendance_date", desc=True)
            .order("attendance_time", desc=True)
            .execute()
        )