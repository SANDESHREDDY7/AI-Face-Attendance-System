import face_recognition


class FaceDetector:

    @staticmethod
    def detect_faces(image_path):

        image = face_recognition.load_image_file(image_path)

        locations = face_recognition.face_locations(image)

        encodings = face_recognition.face_encodings(
            image,
            locations
        )

        return image, locations, encodings