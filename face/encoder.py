import face_recognition
import numpy as np


class FaceEncoder:

    @staticmethod
    def generate_encoding(image_path):

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            # If default HOG didn't find face, try once with upsample=1
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1)
            if len(face_locations) > 0:
                encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)

        if len(encodings) == 0:
            return None

        return encodings[0].tolist()

    @staticmethod
    def generate_multiple_encodings(image_paths):

        all_encodings = []

        for index, image_path in enumerate(image_paths, start=1):

            encoding = FaceEncoder.generate_encoding(image_path)

            if encoding is not None:
                all_encodings.append(encoding)
            else:
                print(f"Warning: No face detected in photo #{index} ({image_path})")

        return all_encodings
