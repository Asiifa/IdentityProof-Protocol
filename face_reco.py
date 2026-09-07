import os
from typing import Dict, Any

import cv2
import numpy as np


# --------------------------------------------------
# MODEL PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

YUNET_MODEL = os.path.join(
    MODEL_DIR,
    "face_detection_yunet_2023mar.onnx"
)

SFACE_MODEL = os.path.join(
    MODEL_DIR,
    "face_recognition_sface_2021dec.onnx"
)


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

def load_models():
    if not os.path.exists(YUNET_MODEL):
        raise FileNotFoundError(
            f"YuNet model not found:\n{YUNET_MODEL}"
        )

    if not os.path.exists(SFACE_MODEL):
        raise FileNotFoundError(
            f"SFace model not found:\n{SFACE_MODEL}"
        )

    detector = cv2.FaceDetectorYN.create(
        YUNET_MODEL,
        "",
        (320, 320),
        0.6,
        0.3,
        5000
    )

    recognizer = cv2.FaceRecognizerSF.create(
        SFACE_MODEL,
        ""
    )

    return detector, recognizer


# --------------------------------------------------
# DETECT FACE
# --------------------------------------------------

def detect_faces(image: np.ndarray, detector) -> np.ndarray:

    height, width = image.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(image)

    if faces is None or len(faces) == 0:
        raise ValueError("No face detected in the image.")

    return faces


# --------------------------------------------------
# EXTRACT FACE EMBEDDING
# --------------------------------------------------

def extract_face_embedding(
    image: np.ndarray,
    face: np.ndarray,
    recognizer
) -> np.ndarray:

    aligned_face = recognizer.alignCrop(
        image,
        face
    )

    embedding = recognizer.feature(
        aligned_face
    )

    return embedding.flatten()


# --------------------------------------------------
# COMPLETE FACE PROCESSING
# --------------------------------------------------

def extract_facial_signature(image_path: str) -> Dict[str, Any]:

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image does not exist: {image_path}"
        )

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Could not read image: {image_path}"
        )

    detector, recognizer = load_models()

    faces = detect_faces(
        image,
        detector
    )

    # Use the strongest detected face
    best_face = max(
        faces,
        key=lambda face: float(face[-1])
    )

    x, y, w, h = best_face[:4]

    confidence = float(best_face[-1])

    embedding = extract_face_embedding(
        image,
        best_face,
        recognizer
    )

    return {
        "face_detected": True,

        "bounding_box": {
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        },

        "confidence_score": round(
            confidence,
            4
        ),

        "embedding_dimension": int(
            embedding.shape[0]
        ),

        "embedding": embedding.tolist()
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Face detection and SFace embedding"
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to input image"
    )

    args = parser.parse_args()

    result = extract_facial_signature(
        args.image
    )

    print("\n==========================================")
    print("       FACE IDENTIFICATION RESULT")
    print("==========================================")

    print(
        f"Face detected        : "
        f"{result['face_detected']}"
    )

    print(
        f"Confidence           : "
        f"{result['confidence_score']}"
    )

    print(
        f"Bounding box         : "
        f"{result['bounding_box']}"
    )

    print(
        f"Embedding dimension  : "
        f"{result['embedding_dimension']}"
    )

    print(
        "\nEmbedding generated  : ✓"
    )

    print(
        "\nFirst 10 embedding values:"
    )

    print(
        result["embedding"][:10]
    )

    print("==========================================")