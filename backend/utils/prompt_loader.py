"""Prompt template loader and variable mapper."""
import os
import re
from typing import Optional


def load_prompt_file() -> str:
    """
    Load the Name Tag prompt template from file.

    Returns:
        Content of the prompt file as string

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    # Try multiple possible paths for different environments
    possible_paths = [
        # Docker with volume: /Prompt (from docker-compose volume)
        "/Prompt/네임텍 로고 캐릭터 생성 프롬프트.md",
        # Docker without volume: /app/../Prompt
        os.path.join("/app", "..", "Prompt", "네임텍 로고 캐릭터 생성 프롬프트.md"),
        # Local development from backend/utils/
        os.path.join(os.path.dirname(__file__), "..", "..", "Prompt", "네임텍 로고 캐릭터 생성 프롬프트.md"),
    ]

    prompt_file = None
    for path in possible_paths:
        abs_path = os.path.abspath(path) if not path.startswith("/") else path
        if os.path.exists(abs_path):
            prompt_file = abs_path
            break

    if prompt_file is None:
        raise FileNotFoundError(
            f"Prompt file not found. Checked paths:\n"
            + "\n".join([f"  - {p}" for p in possible_paths])
            + "\nMake sure '네임텍 로고 캐릭터 생성 프롬프트.md' exists in the Prompt directory."
        )

    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()


def extract_section(content: str, section_title: str, end_marker: Optional[str] = None) -> Optional[str]:
    """
    Extract a specific section from prompt content.

    Args:
        content: Full prompt content
        section_title: Title of section to find
        end_marker: Optional marker that signals end of section

    Returns:
        Extracted section content or None if not found
    """
    # Find section start
    pattern = rf"#+\s+{re.escape(section_title)}.*?\n"
    match = re.search(pattern, content, re.IGNORECASE)

    if not match:
        return None

    start_pos = match.end()

    # Find section end
    if end_marker:
        end_match = re.search(re.escape(end_marker), content[start_pos:])
        end_pos = start_pos + end_match.end() if end_match else len(content)
    else:
        # Look for next heading
        next_heading = re.search(r"\n#+\s+", content[start_pos:])
        end_pos = start_pos + next_heading.start() if next_heading else len(content)

    return content[start_pos:end_pos].strip()


def get_logo_prompt_template() -> str:
    """
    Get the Korean logo generation prompt template.

    Returns:
        Logo prompt template with variables like [BRAND_NAME], etc.
    """
    content = load_prompt_file()

    # Find the Korean logo prompt section
    pattern = r"### 마스터 로고 프롬프트 \(한국어.*?\n```\n(.*?)\n```"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    raise ValueError("Logo prompt template not found in prompt file")


def get_character_prompt_template() -> str:
    """
    Get the Korean character generation prompt template.

    Returns:
        Character prompt template with variables like [BRAND_NAME], etc.
    """
    content = load_prompt_file()

    # Find the Korean character prompt section
    pattern = r"### 마스터 캐릭터 프롬프트 \(한국어\).*?\n```\n(.*?)\n```"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    raise ValueError("Character prompt template not found in prompt file")


def get_mood_mapping_table() -> dict[str, dict[str, str]]:
    """
    Extract mood mapping table from prompt file.

    Returns:
        Dictionary mapping mood codes to mood details
    """
    content = load_prompt_file()

    # Extract the table section
    pattern = r"\| 무드 코드 \|.*?\n\|.*?\n\|.*?\n((?:\|.*?\n)+)"
    match = re.search(pattern, content)

    if not match:
        raise ValueError("Mood mapping table not found")

    table_content = match.group(1)
    moods = {}

    for line in table_content.strip().split("\n"):
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) >= 5:
            mood_code = cells[0]
            mood_name = cells[1]
            color_palette = cells[2]
            font = cells[3]
            symbol_style = cells[4]

            moods[mood_code] = {
                "name": mood_name,
                "color": color_palette,
                "font": font,
                "symbol_style": symbol_style,
            }

    return moods


def replace_variables(
    template: str,
    brand_name: str,
    brand_topic: str,
    core_value: str,
    target_mood: str,
    brand_color: str = "",
    font_style: str = "",
    symbol_type: str = "기하학적",
    logo_type: str = "심볼+텍스트 조합",
    background: str = "흰색",
) -> str:
    """
    Replace template variables with actual values.

    Args:
        template: Template with [VARIABLE] placeholders
        brand_name: Brand name
        brand_topic: Business topic
        core_value: Core values
        target_mood: Brand mood
        brand_color: Brand color (auto-mapped if empty)
        font_style: Font style (auto-mapped if empty)
        symbol_type: Symbol style type
        logo_type: Logo composition type
        background: Background color

    Returns:
        Template with variables replaced
    """
    # Auto-map mood if colors/fonts not specified
    moods = get_mood_mapping_table()
    mood_data = moods.get(target_mood, {})

    if not brand_color and mood_data:
        brand_color = mood_data.get("color", "검정")

    if not font_style and mood_data:
        font_style = mood_data.get("font", "기본 산세리프")

    # Replace variables
    replacements = {
        "[BRAND_NAME]": brand_name,
        "[BRAND_TOPIC]": brand_topic,
        "[CORE_VALUE]": core_value,
        "[TARGET_MOOD]": target_mood,
        "[BRAND_COLOR]": brand_color,
        "[FONT_STYLE]": font_style,
        "[SYMBOL_TYPE]": symbol_type,
        "[LOGO_TYPE]": logo_type,
        "[BACKGROUND]": background,
    }

    result = template
    for var, value in replacements.items():
        result = result.replace(var, value)

    return result
