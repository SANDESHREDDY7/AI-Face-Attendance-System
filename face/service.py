from face.image_processor import ImageProcessor
from face.encoder import FaceEncoder
from face.repository import FaceRepository


class FaceService:

    @staticmethod
    def register_face(student_id, roll_number, uploaded_files):

        print("\n========== FACE REGISTRATION ==========")

        # Save Images
        saved_paths = ImageProcessor.save_student_images(
            roll_number,
            uploaded_files
        )

        print("Saved Paths:", saved_paths)

        # Generate Face Encodings
        encodings = FaceEncoder.generate_multiple_encodings(
            saved_paths
        )

        print("Encodings Generated:", len(encodings))

        # Save Encodings to Database
        for index, encoding in enumerate(encodings, start=1):

            print(f"Saving Encoding {index}...")

            FaceRepository.save_encoding(
                student_id=student_id,
                photo_number=index,
                image_path=saved_paths[index - 1],
                encoding=encoding
            )

        print("Face Registration Completed")
        print("=======================================\n")

        return len(encodings)

    @staticmethod
    def get_registered_faces():

        return FaceRepository.get_all_encodings()