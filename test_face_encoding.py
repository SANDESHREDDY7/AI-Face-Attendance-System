from face.encoder import FaceEncoder

image_path = "uploads/students/76/photo1.jpeg"

encoding = FaceEncoder.generate_encoding(image_path)

if encoding:
    print("✅ Face Encoding Generated")
    print(f"Encoding Length: {len(encoding)}")
else:
    print("❌ No Face Found")