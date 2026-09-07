import json


def build_record(candidate):
    """
    Build a deterministic record from a discovered web result.

    Only information returned by the genuine web search is used.
    """

    record = {
        "title": candidate.get("title", ""),
        "source": candidate.get("source", ""),
        "page_url": candidate.get("link", ""),
        "image_url": candidate.get("image", "")
    }

    return record


def save_record(record, filename="discovered_record.json"):
    """
    Save the discovered record in a stable JSON format.
    """

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            record,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True
        )

    print(
        f"\n✓ Record saved to: {filename}"
    )


if __name__ == "__main__":

    import json

    # Load the results produced by web_search.py
    with open(
        "lens_results.json",
        "r",
        encoding="utf-8"
    ) as file:

        lens_data = json.load(file)

    candidates = lens_data.get(
        "visual_matches",
        []
    )

    if not candidates:

        print(
            "\n❌ No visual matches available."
        )

        raise SystemExit(1)

    # For now use the strongest candidate returned
    # by the search. Later, app.py will use the
    # SFace-verified candidate instead.
    candidate = candidates[0]

    record = build_record(
        candidate
    )

    print("\n==========================================")
    print("          DISCOVERED WEB RECORD")
    print("==========================================")

    print(
        json.dumps(
            record,
            indent=2,
            ensure_ascii=False
        )
    )

    save_record(
        record
    )

    print(
        "\n=========================================="
    )