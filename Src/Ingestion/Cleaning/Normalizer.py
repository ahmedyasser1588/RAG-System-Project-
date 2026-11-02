import re


def normalize_whitespace(text: str) -> str:
    """Normalize spaces, tabs and excessive blank lines."""
    # Convert tabs to spaces
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Collapse multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace
    return text.strip()


def normalize_lines(text: str) -> str:
    """Normalize individual lines.
    Removes unnecessary spaces at the beginning/end of each line.
    """
    lines = text.splitlines()
    normalized_lines = []

    for line in lines:
        line = line.strip()
        normalized_lines.append(line)

    return "\n".join(normalized_lines)


def fix_ocr_errors(text: str, replacements: dict[str, str]) -> str:
    """Apply targeted OCR corrections.

    Important:
    We intentionally use exact replacements instead of globally replacing
    characters such as 0->o.
    """
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


def normalize_punctuations(text: str) -> str:
    """Normalize common punctuation errors."""
    # Normalize different dash characters
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")

    # Normalize curly quotes
    text = text.replace("\u2019", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')

    return text
