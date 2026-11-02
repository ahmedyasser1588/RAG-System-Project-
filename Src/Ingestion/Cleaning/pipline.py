from Src.Ingestion.Cleaning.Cleaner import (
    remove_consecutive_duplicates,
    remove_duplicate_lines,
    remove_empty_lines,
    remove_noise_keywords,
    remove_noise,
    remove_repeated_footer,
)

from Src.Ingestion.Cleaning.Normalizer import (
    normalize_whitespace,
    normalize_lines,
    fix_ocr_errors,
    normalize_punctuations,
)

from Src.Ingestion.Cleaning.Rules import (
    BOILERPLATE_PATTERNS,
    NOISE_KEYWORDS,
    OCR_REPLACEMENTS,
    NOISE_PATTERNS,
)


def clean_text(text: str) -> str:
    """Main document cleaning pipeline.

    Raw text
    ↓ Remove Noise
    ↓ Remove Boilerplate
    ↓ Fix OCR Errors
    ↓ Remove Duplicate lines
    ↓ Normalize Punctuations
    ↓ Normalize Lines
    ↓ Normalize Whitespace
    ↓ Final clean text
    """
    if not text:
        return ""

    # 1 - Remove exact noise patterns
    text = remove_noise(text, NOISE_PATTERNS)
    # 2 - Remove noise keywords
    text = remove_noise_keywords(text, NOISE_KEYWORDS)
    # 3 - Remove boilerplate patterns
    text = remove_repeated_footer(text, BOILERPLATE_PATTERNS)
    # 4 - Fix OCR errors
    text = fix_ocr_errors(text, OCR_REPLACEMENTS)
    # 5 - Remove consecutive duplicates
    text = remove_consecutive_duplicates(text)
    # 6 - Normalize punctuation
    text = normalize_punctuations(text)
    # 7 - Normalize individual lines
    text = normalize_lines(text)
    # 8 - Remove duplicate lines
    text = remove_duplicate_lines(text)
    # 9 - Normalize whitespace
    text = normalize_whitespace(text)
    # 10 - Final formatting
    text = remove_empty_lines(text)
    text = text.strip()

    return text
