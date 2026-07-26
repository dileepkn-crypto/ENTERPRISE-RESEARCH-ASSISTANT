import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text while preserving
    useful academic content.
    """

    if not text:
        return ""

    # Remove null characters
    text = text.replace("\x00", " ")

    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Join words broken across lines by PDF hyphenation
    text = re.sub(
        r"(\w)-\n(\w)",
        r"\1\2",
        text
    )

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(
        r"[ ]{2,}",
        " ",
        text
    )

    # Remove spaces around newlines
    text = re.sub(
        r" *\n *",
        "\n",
        text
    )

    # Collapse excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def is_valid_text(text: str) -> bool:
    """
    Check whether extracted text contains enough
    meaningful content for indexing.
    """

    if not text:
        return False

    cleaned = clean_text(text)

    # Ignore nearly empty pages/chunks
    if len(cleaned) < 20:
        return False

    # Require at least some alphabetic content
    if not re.search(r"[A-Za-z]", cleaned):
        return False

    return True