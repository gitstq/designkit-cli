"""Color palette generation — create harmonious color schemes from a primary color."""

import colorsys
import math
import re


def _parse_hex(color: str) -> tuple:
    """Parse a hex color string to (R, G, B) in 0-255 range."""
    color = color.strip("#")
    if len(color) == 3:
        color = "".join(c * 2 for c in color)
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def _to_hex(r: int, g: int, b: int) -> str:
    """Convert (R, G, B) to hex string with leading #."""
    return f"#{r:02x}{g:02x}{b:02x}"


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Convert RGB (0-255) to HSL (0-360, 0-100, 0-100)."""
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(rn, gn, bn)
    return (round(h * 360), round(s * 100), round(l * 100))


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple:
    """Convert HSL (0-360, 0-100, 0-100) to RGB (0-255)."""
    rn, gn, bn = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return (round(rn * 255), round(gn * 255), round(bn * 255))


def generate_palette(primary_hex: str, steps: int = 10) -> dict:
    """
    Generate a full color palette from a primary hex color.

    Returns a dict with: 50, 100, 200, ... 900, 950 scale + foreground color.
    """
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)

    # Find where the primary sits on the scale
    primary_step = round(l_val / 10) * 10  # nearest 10
    primary_step = max(50, min(950, primary_step * 10))

    lightness_levels = [95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5]
    step_labels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

    palette = {}
    for label, lv in zip(step_labels, lightness_levels):
        # Adjust saturation: more saturated in mid tones, less at extremes
        saturation_adj = s * (1.0 - 0.4 * abs(lv - 50) / 50)
        saturation_adj = max(0, min(100, round(saturation_adj)))

        cr, cg, cb = _hsl_to_rgb(h, saturation_adj, lv)
        palette[str(label)] = _to_hex(cr, cg, cb)

    palette["DEFAULT"] = primary_hex
    palette["FOREGROUND"] = "#ffffff" if l_val < 50 else "#111827"
    return palette


def generate_neutral_palette(primary_hex: str, steps: int = 10) -> dict:
    """Generate a neutral/gray palette that harmonizes with the primary color."""
    r, g, b = _parse_hex(primary_hex)
    h, _, _ = _rgb_to_hsl(r, g, b)

    # Use a very low saturation for neutrals
    neutral_sat = 8
    lightness_levels = [95, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5]
    step_labels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

    palette = {}
    for label, lv in zip(step_labels, lightness_levels):
        sat = max(0, round(neutral_sat * (1.0 - abs(lv - 50) / 60)))
        cr, cg, cb = _hsl_to_rgb(h, sat, lv)
        palette[str(label)] = _to_hex(cr, cg, cb)

    return palette


def generate_complementary(primary_hex: str) -> str:
    """Generate complementary color (opposite on color wheel)."""
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)
    comp_h = (h + 180) % 360
    cr, cg, cb = _hsl_to_rgb(comp_h, s, l_val)
    return _to_hex(cr, cg, cb)


def generate_analogous(primary_hex: str, count: int = 3) -> list:
    """Generate analogous colors (adjacent on color wheel)."""
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)
    step = 30
    colors = []
    for i in range(-(count // 2), count // 2 + 1):
        ah = (h + i * step) % 360
        cr, cg, cb = _hsl_to_rgb(ah, s, l_val)
        colors.append(_to_hex(cr, cg, cb))
    return colors


def generate_triadic(primary_hex: str) -> list:
    """Generate triadic color scheme (120 degrees apart)."""
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)
    colors = [primary_hex]
    for offset in (120, 240):
        th = (h + offset) % 360
        cr, cg, cb = _hsl_to_rgb(th, s, l_val)
        colors.append(_to_hex(cr, cg, cb))
    return colors


def generate_shades(primary_hex: str, count: int = 5) -> list:
    """Generate progressively darker shades of the primary color."""
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)
    shades = []
    for i in range(count):
        factor = 1.0 - (i / (count - 1)) * 0.7
        cr, cg, cb = _hsl_to_rgb(h, s, round(l_val * factor))
        shades.append(_to_hex(cr, cg, cb))
    return shades


def generate_tints(primary_hex: str, count: int = 5) -> list:
    """Generate progressively lighter tints of the primary color."""
    r, g, b = _parse_hex(primary_hex)
    h, s, l_val = _rgb_to_hsl(r, g, b)
    tints = []
    for i in range(count):
        factor = 1.0 + (i / (count - 1)) * 1.0
        new_l = min(100, round(l_val * factor))
        # Reduce saturation as we go lighter
        new_s = round(s * (1.0 - (i / (count - 1)) * 0.5))
        cr, cg, cb = _hsl_to_rgb(h, max(0, new_s), new_l)
        tints.append(_to_hex(cr, cg, cb))
    return tints


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    r1, g1, b1 = _parse_hex(hex1)
    r2, g2, b2 = _parse_hex(hex2)

    def relative_luminance(r: int, g: int, b: int) -> float:
        def linearize(c: int) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def is_valid_hex(color: str) -> bool:
    """Check if a string is a valid hex color."""
    return bool(re.match(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color))