import sys
from hashlib import sha256

from httpx import Client


def description():
    print("Generating SHA256 hash")
    print("-" * 80)
    print("Usage:")
    print("python generate_sha256.py <strength>")
    print(
        "<strength> - is an integer value that specifies words count that will be encoded"
    )
    print("-" * 80)


def encode(word_count: int = 10):
    with Client() as client:
        response = client.get(
            f"https://random-word-api.herokuapp.com/word?number={word_count}"
        )

        print(sha256(response.text.encode("utf-8")).hexdigest())


def main():
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            word_count = int(sys.argv[1])
            return encode(word_count)
        else:
            return description()

    return encode()


if "__main__" == __name__:
    main()
