import re


def normalize_whitespace(text: str) -> str:
    """Normalize spaces, tabs and excessive blank lines."""
    text = text.replace("\t", " ")
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_lines(text: str) -> str:
    """Normalize individual lines."""
    lines = text.splitlines()
    normalized_lines = []
    for line in lines:
        normalized_lines.append(line.strip())
    return "\n".join(normalized_lines)


def fix_ocr_errors(text: str, replacements: dict[str, str]) -> str:
    """Apply targeted OCR corrections."""
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text


def normalize_punctuations(text: str) -> str:
    """Normalize common punctuation errors."""
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2019", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')
    return text
