from database.supabase_client import supabase


class StudentRepository:

    @staticmethod
    def insert_student(student):

        return (
            supabase.table("students")
            .insert(student)
            .execute()
        )

    @staticmethod
    def get_all_students():

        return (
            supabase.table("students")
            .select("*")
            .order("id", desc=True)
            .execute()
        )

    @staticmethod
    def get_student_by_id(student_id):

        response = (
            supabase.table("students")
            .select("*")
            .eq("id", student_id)
            .single()
            .execute()
        )

        return response.data

    @staticmethod
    def delete_student(student_id):

        return (
            supabase.table("students")
            .delete()
            .eq("id", student_id)
            .execute()
        )