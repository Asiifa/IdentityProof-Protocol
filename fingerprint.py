import hashlib
import json


def fingerprint_file(filename):
    """
    Create a SHA-256 fingerprint from a JSON record.
    """

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    # Deterministic serialization
    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    sha256_hash = hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()

    return canonical_data, sha256_hash


if __name__ == "__main__":

    filename = "discovered_record.json"

    canonical_data, fingerprint = (
        fingerprint_file(filename)
    )

    print("\n==========================================")
    print("          CONTENT FINGERPRINT")
    print("==========================================")

    print("\nCanonical data:")
    print(canonical_data)

    print("\nSHA-256:")
    print(fingerprint)

    print(
        "\nHash length:",
        len(fingerprint)
    )

    print("\n==========================================")