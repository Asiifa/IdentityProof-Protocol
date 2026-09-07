import os
import cv2

from face_reco import load_models, detect_faces


def create_face_crop(input_path, output_path):
    """
    Detect the strongest face and save a cropped version.
    """

    image = cv2.imread(input_path)

    if image is None:
        raise ValueError(
            f"Could not read image: {input_path}"
        )

    detector, _ = load_models()

    faces = detect_faces(
        image,
        detector
    )

    if len(faces) == 0:
        raise ValueError(
            "No face detected."
        )

    # Strongest detected face
    best_face = max(
        faces,
        key=lambda face: float(face[-1])
    )

    x, y, w, h = [
        int(value)
        for value in best_face[:4]
    ]

    height, width = image.shape[:2]

    # Add some padding around the face
    padding_x = int(w * 0.35)
    padding_y = int(h * 0.45)

    x1 = max(
        0,
        x - padding_x
    )

    y1 = max(
        0,
        y - padding_y
    )

    x2 = min(
        width,
        x + w + padding_x
    )

    y2 = min(
        height,
        y + h + padding_y
    )

    crop = image[
        y1:y2,
        x1:x2
    ]

    if crop.size == 0:
        raise ValueError(
            "Face crop is empty."
        )

    # Make sure output folder exists
    output_dir = os.path.dirname(
        os.path.abspath(output_path)
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    success = cv2.imwrite(
        output_path,
        crop
    )

    if not success:
        raise RuntimeError(
            "Could not save face crop."
        )

    print("\n==========================================")
    print("             FACE CROP")
    print("==========================================")

    print(
        f"\nOriginal : {input_path}"
    )

    print(
        f"Cropped  : {output_path}"
    )

    print(
        f"Face box : "
        f"x={x}, y={y}, w={w}, h={h}"
    )

    print(
        "\n✓ Face crop created"
    )

    print("==========================================")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Create a face-focused search image"
    )

    parser.add_argument(
        "--image",
        required=True
    )

    parser.add_argument(
        "--output",
        default="face_search_crop.jpg"
    )

    args = parser.parse_args()

    create_face_crop(
        args.image,
        args.output
    )