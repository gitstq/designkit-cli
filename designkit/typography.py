"""Typography scale generator — create harmonious type scales for design systems."""

import math


# Font pairings: (heading font, body font) — system-safe fallbacks
FONT_PAIRS = {
    "modern": (
        ("Inter", "system-ui", "-apple-system", "sans-serif"),
        ("Inter", "system-ui", "-apple-system", "sans-serif"),
    ),
    "classic": (
        ("Georgia", "Palatino", "serif"),
        ("Georgia", "Palatino", "serif"),
    ),
    "code": (
        ("SF Mono", "Fira Code", "monospace"),
        ("SF Mono", "Fira Code", "monospace"),
    ),
    "elegant": (
        ("Playfair Display", "Georgia", "serif"),
        ("Source Sans Pro", "system-ui", "sans-serif"),
    ),
    "technical": (
        ("SF Pro Display", "system-ui", "sans-serif"),
        ("SF Pro Text", "system-ui", "sans-serif"),
    ),
}


def generate_type_scale(base_size: int = 16, ratio: float = 1.25, steps: int = 7) -> dict:
    """
    Generate a modular type scale.

    Args:
        base_size: Base font size in px (default: 16)
        ratio: Modular scale ratio (default: 1.25 = Major Third)
        steps: Number of steps above base (default: 7)

    Returns:
        Dict with scale levels and their px/rem values.

    Common ratios:
        1.067  — Minor Second (subtle)
        1.125  — Major Second
        1.200  — Minor Third
        1.250  — Major Third (default)
        1.333  — Perfect Fourth
        1.414  — Augmented Fourth
        1.500  — Perfect Fifth
        1.618  — Golden Ratio
    """
    scale = {}
    base_rem = base_size / 16.0

    # Step labels from small to large
    labels = [
        "caption",       # -2 steps
        "small",         # -1 step
        "body",          # base
        "h6",            # +1
        "h5",            # +2
        "h4",            # +3
        "h3",            # +4
        "h2",            # +5
        "h1",            # +6
        "display",       # +7
    ]

    offsets = list(range(-2, 8))

    for label, offset in zip(labels, offsets):
        size_px = round(base_size * (ratio ** offset), 1)
        size_rem = round(base_rem * (ratio ** offset), 3)

        scale[label] = {
            "px": size_px,
            "rem": size_rem,
            "line_height": _recommended_line_height(size_px),
            "font_weight": _recommended_weight(label),
        }

    return scale


def generate_spacing(
    base_unit: int = 4, max_steps: int = 12, ratio: float = 2.0
) -> dict:
    """
    Generate a spacing scale.

    Args:
        base_unit: Base spacing unit in px (default: 4)
        max_steps: Number of steps (default: 12)
        ratio: Exponential ratio (default: 2.0)
    """
    scale = {}
    for i in range(max_steps + 1):
        value = round(base_unit * (ratio ** (i / 4)))
        label = f"{i * 0.25}x" if i % 4 == 0 else f"step-{i}"
        scale[str(i)] = {
            "px": value,
            "label": label,
            "rem": round(value / 16, 3),
        }
    return scale


def _recommended_line_height(size_px: float) -> float:
    """Suggest a line-height based on font size."""
    if size_px <= 12:
        return 1.5
    elif size_px <= 16:
        return 1.6
    elif size_px <= 24:
        return 1.4
    elif size_px <= 36:
        return 1.3
    elif size_px <= 48:
        return 1.2
    else:
        return 1.1


def _recommended_weight(label: str) -> int:
    """Suggest a font weight based on type level."""
    heavy = {"display": 700, "h1": 700, "h2": 600}
    medium = {"h3": 600, "h4": 600, "h5": 500}
    if label in heavy:
        return heavy[label]
    if label in medium:
        return medium[label]
    return 400