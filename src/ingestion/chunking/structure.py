import re
from dataclasses import dataclass


@dataclass
class DocumentSection:
    title: str
    level: int
    content: str
    parent: str | None = None


def extract_heading(line: str) -> tuple[int, str] | None:
    """Extract heading level and title from a Markdown heading line."""
    match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
    if not match:
        return None
    hashes = match.group(1)
    level = len(hashes)
    title = match.group(2).strip()
    return level, title


def extract_sections(text: str) -> list[DocumentSection]:
    """Parse Markdown text into a list of DocumentSection objects."""
    lines = text.splitlines()
    sections: list[DocumentSection] = []

    current_title = ""
    current_level = 0
    current_content: list[str] = []
    heading_stack: dict[int, str] = {}

    def flush_section():
        if not current_content:
            return
        content = "\n".join(current_content).strip()
        if not content:
            return
        parent = None
        if current_level > 1:
            parent = heading_stack.get(current_level - 1)
        sections.append(DocumentSection(
            title=current_title,
            level=current_level,
            content=content,
            parent=parent,
        ))

    for line in lines:
        heading = extract_heading(line)
        if heading:
            flush_section()

            level, title = heading
            current_level = level
            current_title = title
            current_content = []

            for existing_level in list(heading_stack.keys()):
                if existing_level >= level:
                    del heading_stack[existing_level]

            heading_stack[level] = title
        else:
            current_content.append(line)

    flush_section()
    return sections
