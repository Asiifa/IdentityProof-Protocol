import os
import json
import tempfile
from urllib.parse import urlparse

import cv2
import numpy as np
import requests

from face_reco import (
    load_models,
    detect_faces,
    extract_face_embedding
)


# ============================================================
# SETTINGS
# ============================================================

# Initial SFace cosine similarity threshold.
MATCH_THRESHOLD = 0.363

MAX_CANDIDATES = 100

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


# ============================================================
# TARGET EMBEDDING
# ============================================================

def get_target_embedding(image_path):
    """
    Generate the SFace feature for the target image.
    """

    if not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Target image not found: {image_path}"
        )

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Could not read target image: {image_path}"
        )

    detector, recognizer = load_models()

    faces = detect_faces(
        image,
        detector
    )

    if len(faces) == 0:
        raise ValueError(
            "No face detected in target image."
        )

    # Select the strongest detected face
    best_face = max(
        faces,
        key=lambda face: float(face[-1])
    )

    # Align target face
    aligned_face = recognizer.alignCrop(
        image,
        best_face
    )

    # Generate native SFace feature
    target_feature = recognizer.feature(
        aligned_face
    )

    return target_feature


# ============================================================
# DOWNLOAD CANDIDATE IMAGE
# ============================================================

def download_candidate_image(image_url):
    """
    Download a candidate image to a temporary file.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0 Safari/537.36"
        )
    }

    response = requests.get(
        image_url,
        headers=headers,
        timeout=20,
        stream=True
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if not content_type.startswith("image/"):
        raise ValueError(
            f"URL did not return an image. "
            f"Content-Type: {content_type}"
        )

    content_length = response.headers.get(
        "Content-Length"
    )

    if content_length:

        if int(content_length) > MAX_IMAGE_SIZE:
            raise ValueError(
                "Candidate image exceeds 5 MB."
            )

    parsed_path = urlparse(
        image_url
    ).path

    extension = os.path.splitext(
        parsed_path
    )[1]

    if extension.lower() not in [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]:
        extension = ".jpg"

    temporary_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    )

    total_bytes = 0

    try:

        for chunk in response.iter_content(
            chunk_size=8192
        ):

            if not chunk:
                continue

            total_bytes += len(chunk)

            if total_bytes > MAX_IMAGE_SIZE:
                raise ValueError(
                    "Candidate image exceeded 5 MB."
                )

            temporary_file.write(chunk)

        temporary_file.close()

        return temporary_file.name

    except Exception:

        temporary_file.close()

        if os.path.exists(
            temporary_file.name
        ):
            os.remove(
                temporary_file.name
            )

        raise


# ============================================================
# COMPARE CANDIDATE FACES
# ============================================================

def compare_candidate(
    image_path,
    target_feature,
    detector,
    recognizer
):
    """
    Detect every face in a candidate image and compare
    each one with the target using the native SFace matcher.

    Returns:
        Highest cosine similarity score.
    """

    image = cv2.imread(
        image_path
    )

    if image is None:
        return None

    faces = detect_faces(
        image,
        detector
    )

    if len(faces) == 0:
        return None

    best_score = -1.0

    for face in faces:

        # Align candidate face
        aligned_face = recognizer.alignCrop(
            image,
            face
        )

        # Generate native SFace feature
        candidate_feature = recognizer.feature(
            aligned_face
        )

        # Native OpenCV SFace cosine matching
        score = recognizer.match(
            target_feature,
            candidate_feature,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        score = float(score)

        if score > best_score:
            best_score = score

    return best_score


# ============================================================
# PROCESS ALL CANDIDATES
# ============================================================

def evaluate_candidates(
    target_image,
    candidates
):

    print("\n==========================================")
    print("        CANDIDATE FACE VERIFICATION")
    print("==========================================")

    print(
        "\nGenerating target face embedding..."
    )

    target_feature = get_target_embedding(
        target_image
    )

    detector, recognizer = load_models()

    results = []

    for position, candidate in enumerate(
        candidates,
        start=1
    ):

        title = candidate.get(
            "title",
            "Untitled"
        )

        source = candidate.get(
            "source",
            "Unknown"
        )

        page_url = candidate.get(
            "link",
            ""
        )

        image_url = candidate.get(
            "image",
            ""
        )

        print(
            f"\n[{position}] {title}"
        )

        print(
            f"    Source: {source}"
        )

        # ----------------------------------------------------
        # Check image URL
        # ----------------------------------------------------

        if not image_url:

            print(
                "    ⚠️ No candidate image URL"
            )

            continue

        temporary_path = None

        try:

            print(
                "    Downloading candidate image..."
            )

            temporary_path = (
                download_candidate_image(
                    image_url
                )
            )

            score = compare_candidate(
                temporary_path,
                target_feature,
                detector,
                recognizer
            )

            if score is None:

                print(
                    "    ❌ No usable face found"
                )

                continue

            is_candidate_match = (
                score >= MATCH_THRESHOLD
            )

            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            result = {
                "position": position,
                "title": title,
                "source": source,
                "page_url": page_url,
                "image_url": image_url,
                "cosine_score": round(
                    score,
                    6
                ),
                "passes_threshold":
                    is_candidate_match
            }

            results.append(
                result
            )

            # ------------------------------------------------
            # Display result
            # ------------------------------------------------

            print(
                f"    Cosine score: "
                f"{score:.4f}"
            )

            print(
                f"    Threshold: "
                f"{MATCH_THRESHOLD:.3f}"
            )

            if is_candidate_match:

                print(
                    "    Result: ✅ CANDIDATE MATCH"
                )

            else:

                print(
                    "    Result: ❌ Rejected"
                )

        except Exception as error:

            print(
                f"    ⚠️ Skipped: {error}"
            )

        finally:

            # Remove temporary candidate image
            if (
                temporary_path
                and os.path.exists(
                    temporary_path
                )
            ):

                os.remove(
                    temporary_path
                )

    # Highest score first
    results.sort(
        key=lambda item: item["cosine_score"],
        reverse=True
    )

    return results


# ============================================================
# SAVE RESULTS
# ============================================================

def save_ranked_results(
    results,
    filename="ranked_candidates.json"
):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\n✓ Ranked results saved to: "
        f"{filename}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Verify Google Lens candidates "
            "using SFace"
        )
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target face image"
    )

    parser.add_argument(
        "--results",
        required=True,
        help="Google Lens JSON results"
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Check results file
    # --------------------------------------------------------

    if not os.path.isfile(
        args.results
    ):

        raise FileNotFoundError(
            f"Results file not found: "
            f"{args.results}"
        )

    # --------------------------------------------------------
    # Load Lens results
    # --------------------------------------------------------

    with open(
        args.results,
        "r",
        encoding="utf-8"
    ) as file:

        lens_data = json.load(
            file
        )

    candidates = lens_data.get(
        "visual_matches",
        []
    )

    if not candidates:

        print(
            "\n❌ No visual candidates found."
        )

        raise SystemExit(1)

    # Use all available candidates up to MAX_CANDIDATES
    candidates = candidates[
        :MAX_CANDIDATES
    ]

    print(
        f"\nFound {len(candidates)} "
        f"candidates to evaluate."
    )

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    results = evaluate_candidates(
        args.target,
        candidates
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_ranked_results(
        results
    )

    # --------------------------------------------------------
    # Display ranked results
    # --------------------------------------------------------

    print("\n==========================================")
    print("             RANKED RESULTS")
    print("==========================================")

    if not results:

        print(
            "\n❌ No candidate images could be "
            "successfully analyzed."
        )

    else:

        for rank, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n#{rank}"
            )

            print(
                f"Cosine score : "
                f"{result['cosine_score']:.4f}"
            )

            print(
                f"Source       : "
                f"{result['source']}"
            )

            print(
                f"URL          : "
                f"{result['page_url']}"
            )

            print(
                f"Threshold    : "
                f"{'PASS' if result['passes_threshold'] else 'FAIL'}"
            )

        # ----------------------------------------------------
        # Best candidate
        # ----------------------------------------------------

        best = results[0]

        print("\n==========================================")
        print("           BEST CANDIDATE")
        print("==========================================")

        print(
            f"Cosine score : "
            f"{best['cosine_score']:.4f}"
        )

        print(
            f"Threshold    : "
            f"{MATCH_THRESHOLD:.3f}"
        )

        print(
            f"Source       : "
            f"{best['source']}"
        )

        print(
            f"URL          : "
            f"{best['page_url']}"
        )

        if best["passes_threshold"]:

            print(
                "\n✅ Candidate passed the "
                "initial face-similarity criterion."
            )

        else:

            print(
                "\n❌ No candidate passed the "
                "initial face-similarity criterion."
            )

        print("==========================================")