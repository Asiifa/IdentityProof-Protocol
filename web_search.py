import os
import json
import requests
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    raise RuntimeError(
        "SERPAPI_KEY was not found in .env"
    )


# ============================================================
# UPLOAD IMAGE
# ============================================================

def upload_image(image_path):
    """
    Upload a local image to SerpApi Image API.

    Returns:
        image_id (str)
    """

    if not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    print("\n[1] Uploading image...")

    with open(image_path, "rb") as image_file:

        response = requests.post(
            "https://serpapi.com/image",
            files={
                "image": image_file
            },
            data={
                "api_key": SERPAPI_KEY
            },
            timeout=60
        )

    # HTTP error
    response.raise_for_status()

    data = response.json()

    # SerpApi API error
    if "error" in data:
        raise RuntimeError(
            data["error"]
        )

    # Make sure image_id exists
    image_id = data.get("image_id")

    if not image_id:
        raise RuntimeError(
            f"image_id missing from response:\n{data}"
        )

    print("    ✓ Image uploaded")
    print(f"    Image ID: {image_id}")

    return image_id


# ============================================================
# GOOGLE LENS SEARCH
# ============================================================

def search_google_lens(image_id):
    """
    Run one Google Lens search using the uploaded image.
    We use type=all so the search does not fail just because
    there are no exact matches.
    """

    response = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google_lens",
            "image_id": image_id,
            "type": "all",
            "auto_crop": "true",
            "safe": "active",
            "hl": "en",
            "country": "in",
            "api_key": SERPAPI_KEY
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    # SerpApi may return an error when there are no results.
    if "error" in data:
        raise RuntimeError(data["error"])

    return data




# ============================================================
# COMPLETE SEARCH
# ============================================================

def search_image(image_path):
    """
    Complete genuine reverse-image search.

    local image
        ↓
    upload
        ↓
    image_id
        ↓
    Google Lens type=all
        ↓
    visual/exact results
    """

    print("\n==========================================")
    print("          GENUINE WEB SEARCH")
    print("==========================================")

    print(f"\nInput image : {image_path}")

    # ----------------------------------------
    # STEP 1: Upload
    # ----------------------------------------

    image_id = upload_image(image_path)

    # ----------------------------------------
    # STEP 2: Search
    # ----------------------------------------

    print("\n[2] Running Google Lens...")

    results = search_google_lens(image_id)

    print("    ✓ Search completed")

    return results

    # ----------------------------------------
    # STEP 3: Visual matches
    # ----------------------------------------

    print("\n[3] Searching visual matches...")

    visual_data = search_google_lens(
        image_id,
        "visual_matches"
    )

    visual_matches = visual_data.get(
        "visual_matches",
        []
    )

    print(
        f"    ✓ Visual matches returned: "
        f"{len(visual_matches)}"
    )

    # ----------------------------------------
    # Combine results
    # ----------------------------------------

    results = {
        "input_image": image_path,
        "image_id": image_id,
        "exact_matches": exact_matches,
        "visual_matches": visual_matches
    }

    return results


# ============================================================
# DISPLAY RESULTS
# ============================================================
def print_results(results):

    exact_matches = results.get(
        "exact_matches",
        []
    )

    visual_matches = results.get(
        "visual_matches",
        []
    )

    print("\n==========================================")
    print("             SEARCH RESULTS")
    print("==========================================")

    print(
        f"\nExact matches found  : "
        f"{len(exact_matches)}"
    )

    print(
        f"Visual matches found : "
        f"{len(visual_matches)}"
    )

    # ----------------------------------------
    # EXACT MATCHES
    # ----------------------------------------

    if exact_matches:

        print("\n--- EXACT MATCHES ---")

        for index, item in enumerate(
            exact_matches[:10],
            start=1
        ):

            print(f"\n[{index}]")

            print(
                "Title :",
                item.get("title", "N/A")
            )

            print(
                "Source:",
                item.get("source", "N/A")
            )

            print(
                "Page  :",
                item.get("link", "N/A")
            )

    else:

        print(
            "\nNo exact matches found."
        )

    # ----------------------------------------
    # VISUAL MATCHES
    # ----------------------------------------

    if visual_matches:

        print("\n--- VISUAL MATCHES ---")

        for index, item in enumerate(
            visual_matches[:20],
            start=1
        ):

            print(f"\n[{index}]")

            print(
                "Title :",
                item.get("title", "N/A")
            )

            print(
                "Source:",
                item.get("source", "N/A")
            )

            print(
                "Page  :",
                item.get("link", "N/A")
            )

            print(
                "Image :",
                item.get("image", "N/A")
            )

    else:

        print(
            "\nNo visual matches found."
        )

    print("\n==========================================")

# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results, filename="lens_results.json"):

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
        f"\n✓ Full search results saved to: "
        f"{filename}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Genuine Google Lens reverse-image search"
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to local image"
    )

    args = parser.parse_args()

    try:

        results = search_image(
            args.image
        )

        print_results(
            results
        )

        save_results(
            results
        )

    except requests.exceptions.Timeout:

        print(
            "\n❌ Request timed out."
        )

    except requests.exceptions.RequestException as error:

        print(
            f"\n❌ Network/API error:\n{error}"
        )

    except Exception as error:

        print(
            f"\n❌ Search failed:\n{error}"
        )