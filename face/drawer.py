import cv2


class FaceDrawer:

    @staticmethod
    def draw_faces(image, attendance):

        for person in attendance:

            top, right, bottom, left = person["location"]

            if person["student"] is None:
                color = (0, 0, 255)
                name = "Unknown"
            else:
                color = (0, 255, 0)
                name = person["student"]["student_name"]

            cv2.rectangle(
                image,
                (left, top),
                (right, bottom),
                color,
                2
            )

            cv2.rectangle(
                image,
                (left, bottom - 30),
                (right, bottom),
                color,
                cv2.FILLED
            )

            cv2.putText(
                image,
                name,
                (left + 6, bottom - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )

        return image