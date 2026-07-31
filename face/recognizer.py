import numpy as np
import face_recognition

from face.detector import FaceDetector
from students.service import StudentService

MATCH_THRESHOLD = 0.45


class FaceRecognizer:

    @staticmethod
    def recognize(group_image_path, known_faces):

        image, face_locations, face_encodings = FaceDetector.detect_faces(
            group_image_path
        )

        print("\n====================================")
        print(f"Faces Detected: {len(face_locations)}")

        # -----------------------------------------
        # Group encodings by student
        # -----------------------------------------

        students = {}

        for record in known_faces:

            sid = record["student_id"]

            if sid not in students:
                students[sid] = []

            students[sid].append(
                np.array(record["encoding"])
            )

        attendance = []

        # -----------------------------------------
        # Recognize each detected face
        # -----------------------------------------

        for face_number, (location, face_encoding) in enumerate(
            zip(face_locations, face_encodings),
            start=1
        ):

            best_student = None
            best_distance = 1.0

            for student_id, encodings in students.items():

                distances = face_recognition.face_distance(
                    encodings,
                    np.array(face_encoding)
                )

                student_best = float(np.min(distances))

                if student_best < best_distance:

                    best_distance = student_best
                    best_student = StudentService.get_student(student_id)

            print("\n====================================")
            print(f"Detected Face #{face_number}")

            if (
                best_student is not None
                and best_distance < MATCH_THRESHOLD
            ):

                confidence = round((1 - best_distance) * 100, 2)

                print(f"✅ MATCH -> {best_student['student_name']}")
                print(f"Distance   : {best_distance:.4f}")
                print(f"Confidence : {confidence:.2f}%")

                attendance.append(
                    {
                        "location": location,
                        "student": best_student,
                        "distance": best_distance,
                        "confidence": confidence
                    }
                )

            else:

                print("❌ UNKNOWN")

                attendance.append(
                    {
                        "location": location,
                        "student": None,
                        "distance": None,
                        "confidence": 0
                    }
                )

        print("\n====================================")
        print("Recognition Complete")
        print("====================================\n")

        return {
            "image": image,
            "attendance": attendance,
            "students": attendance
        }