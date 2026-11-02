import re


def remove_noise(text: str, noise_patterns: list[str]) -> str:
    """Remove lines matching configured noise patterns."""
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            cleaned_lines.append("")
            continue

        is_noise = False
        for pattern in noise_patterns:
            if re.match(pattern, stripped_line):
                is_noise = True
                break

        if not is_noise:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_noise_keywords(text: str, keywords: list[str]) -> str:
    """Remove lines containing configured noise keywords."""
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in keywords):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_consecutive_duplicates(text: str) -> str:
    """Remove consecutive identical lines."""
    lines = text.splitlines()
    cleaned_lines = []
    previous_line = None

    for line in lines:
        normalized = line.strip()

        if not normalized:
            cleaned_lines.append("")
            continue

        if normalized == previous_line:
            continue

        cleaned_lines.append(line)
        previous_line = normalized

    return "\n".join(cleaned_lines)


def remove_duplicate_lines(text: str) -> str:
    """Remove duplicate lines appearing anywhere in the document."""
    lines = text.splitlines()
    seen = set()
    cleaned_lines = []

    for line in lines:
        normalized = line.strip()

        if not normalized:
            cleaned_lines.append(line)
            continue

        if normalized in seen:
            continue

        seen.add(normalized)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_empty_lines(text: str) -> str:
    """Remove completely empty lines."""
    lines = text.splitlines()
    cleaned_lines = [line for line in lines if line.strip()]
    return "\n".join(cleaned_lines)


def remove_repeated_footer(text: str, footer_patterns: list[str]) -> str:
    """Remove lines matching footer patterns."""
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        if any(re.match(pattern, stripped) for pattern in footer_patterns):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)
