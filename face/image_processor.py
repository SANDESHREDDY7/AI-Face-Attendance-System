import os
from PIL import Image


class ImageProcessor:

    @staticmethod
    def save_student_images(roll_number, uploaded_files):

        folder = os.path.join(
            "uploads",
            "students",
            str(roll_number)
        )

        os.makedirs(folder, exist_ok=True)

        saved_paths = []

        for index, uploaded_file in enumerate(uploaded_files, start=1):

            if uploaded_file is None:
                continue

            filename = f"photo{index}.jpg"
            filepath = os.path.join(folder, filename)

            image = Image.open(uploaded_file.file)

            # Convert to RGB (required for JPEG)
            if image.mode != "RGB":
                image = image.convert("RGB")

            image.save(filepath, "JPEG", quality=95)

            saved_paths.append(filepath)

        return saved_paths

    @staticmethod
    def save_group_image(uploaded_file):

        folder = os.path.join(
            "uploads",
            "attendance"
        )

        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(
            folder,
            "group_photo.jpg"
        )

        image = Image.open(uploaded_file.file)

        # Convert to RGB (required for JPEG)
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(filepath, "JPEG", quality=95)

        return filepath