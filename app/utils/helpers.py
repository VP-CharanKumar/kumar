import json
from typing import Any, Dict, Optional

def sanitize_json(data: Any) -> str:
    """Safely serialize data to indented JSON string."""
    return json.dumps(data, indent=2, default=str)

def format_percentage(val: Optional[float]) -> str:
    if val is None:
        return "N/A"
    return f"{val:.1f}%"

def truncate_text(text: str, max_chars: int = 200) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."
