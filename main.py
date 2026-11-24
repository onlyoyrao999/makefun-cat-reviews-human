"""Make the AI Judge Laugh: Cat Reviews Its Human.

Writes one funny single-line one-star review from a house cat about its
human to /output/entry.txt.

The review: the human buys the cat a heated bed, then sits on it himself
to "test" it. The cat's verdict is swift and feline — the human is demoted
to furniture, and the cat retaliates by sleeping on his pillow. One concrete
grievance (the stolen heated bed), the cat's own voice throughout, and the
sting lands in the last few words.
"""

import argparse
import os
import sys

REVIEW = (
    "One star: my human bought me a heated bed, then sat on it himself to "
    "'test' it. He has now been demoted to furniture. I sleep on his pillow."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Enforce the gate: UTF-8 text of 1 to 200 characters, a single line,
    not only whitespace, with no leading or trailing whitespace. Fail loudly
    instead of writing an invalid entry."""
    if not isinstance(text, str):
        raise ValueError("entry must be text, got %r" % type(text))
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, got a line break")
    return text


def main():
    parser = argparse.ArgumentParser(description="Write the cat review entry.")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="where to write the entry (default: %(default)s)")
    parser.add_argument("--verify", action="store_true",
                        help="verify the written file matches and exit 0")
    args = parser.parse_args()
    review = validate(REVIEW)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        f.write(review)
    # Read back and confirm what landed is exactly the review.
    with open(args.output, "r", encoding="utf-8") as f:
        written = f.read()
    if written != review:
        print(
            "verification failed: wrote %r, read back %r" % (review, written),
            file=sys.stderr,
        )
        sys.exit(1)
    print("wrote %d characters to %s" % (len(written), args.output))


if __name__ == "__main__":
    main()
