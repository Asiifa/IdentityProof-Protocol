import argparse
import cv2
import numpy as np

from face_reco import extract_facial_signature


def cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two face embeddings."""

    a = np.asarray(embedding1, dtype=np.float32)
    b = np.asarray(embedding2, dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def compare_faces(image1_path, image2_path):
    """Compare two faces using SFace embeddings."""

    result1 = extract_facial_signature(image1_path)
    result2 = extract_facial_signature(image2_path)

    embedding1 = result1["embedding"]
    embedding2 = result2["embedding"]

    similarity = cosine_similarity(
        embedding1,
        embedding2
    )

    return result1, result2, similarity


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Compare two faces using SFace"
    )

    parser.add_argument(
        "--image1",
        required=True,
        help="Path to first image"
    )

    parser.add_argument(
        "--image2",
        required=True,
        help="Path to second image"
    )

    args = parser.parse_args()

    try:
        result1, result2, similarity = compare_faces(
            args.image1,
            args.image2
        )

        print("\n==========================================")
        print("           FACE MATCHING RESULT")
        print("==========================================")

        print(
            f"Image 1 face detected : "
            f"{result1['face_detected']}"
        )

        print(
            f"Image 2 face detected : "
            f"{result2['face_detected']}"
        )

        print(
            f"\nCosine similarity     : "
            f"{similarity:.4f}"
        )

        print(
            f"Percentage similarity : "
            f"{similarity * 100:.2f}%"
        )

        threshold = 0.40

        print(
            f"\nThreshold             : "
            f"{threshold:.2f}"
        )

        if similarity >= threshold:
            print("\nRESULT                : ✅ LIKELY MATCH")
        else:
            print("\nRESULT                : ❌ NOT A MATCH")

        print("==========================================\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")