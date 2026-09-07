import cv2

from face_reco import load_models, detect_faces


image_path = "facee.jpg"

image = cv2.imread(image_path)

if image is None:
    raise RuntimeError("Could not read image")


detector, recognizer = load_models()

faces = detect_faces(
    image,
    detector
)

best_face = max(
    faces,
    key=lambda face: float(face[-1])
)

aligned = recognizer.alignCrop(
    image,
    best_face
)

feature1 = recognizer.feature(
    aligned
)

feature2 = recognizer.feature(
    aligned
)

score = recognizer.match(
    feature1,
    feature2,
    cv2.FaceRecognizerSF_FR_COSINE
)

print("\n==========================================")
print("       NATIVE SFACE SANITY TEST")
print("==========================================")

print(
    f"\nCosine score: {score:.6f}"
)

print(
    "\nExpected: very close to 1.0"
)

if score > 0.9:
    print(
        "RESULT: ✅ SFace matcher is working"
    )
else:
    print(
        "RESULT: ❌ Something is wrong"
    )

print("==========================================")