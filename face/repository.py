from database.supabase_client import supabase


class FaceRepository:

    @staticmethod
    def save_encoding(student_id, photo_number, image_path, encoding):

        try:

            response = (
                supabase
                .table("face_encodings")
                .insert({
                    "student_id": student_id,
                    "photo_number": photo_number,
                    "encoding": encoding
                })
                .execute()
            )

            print("✅ Encoding Saved:", response)

        except Exception as e:

            print("❌ ERROR SAVING ENCODING")
            print(e)
            raise

    @staticmethod
    def get_all_encodings():

        response = (
            supabase
            .table("face_encodings")
            .select("*")
            .execute()
        )

        return response.data