from src.ingestion.cleaning.cleaner import (
    remove_noise,
    remove_duplicate_lines,
    remove_empty_lines,
    remove_noise_keywords,
    remove_repeated_footer,
)


def test_remove_noise():
    text = "Hello\npage 10\n world"
    res = remove_noise(text, [r"page \d+"])
    assert "page 10" not in res
    assert "Hello" in res


def test_remove_empty_lines():
    text = "Hello\n\n\nWorld"
    res = remove_empty_lines(text)
    assert res == "Hello\nWorld"
