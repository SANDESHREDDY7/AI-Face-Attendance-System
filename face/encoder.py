import face_recognition
import numpy as np


class FaceEncoder:

    @staticmethod
    def generate_encoding(image_path):

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            return None

        return encodings[0].tolist()

    @staticmethod
    def generate_multiple_encodings(image_paths):

        all_encodings = []

        for image_path in image_paths:

            encoding = FaceEncoder.generate_encoding(image_path)

            if encoding is not None:
                all_encodings.append(encoding)

        return all_encodings