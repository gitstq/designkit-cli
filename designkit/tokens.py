"""Design token generation — compose all design tokens from a theme configuration."""

from .themes import resolve_theme_colors
from .typography import generate_type_scale, FONT_PAIRS
from .palette import generate_palette, generate_neutral_palette


def generate_design_tokens(theme: dict) -> dict:
    """
    Generate a complete set of design tokens from a theme config.

    Returns a nested dict of all tokens organized by category.
    """
    colors = resolve_theme_colors(theme)
    font_pair = FONT_PAIRS.get(
        theme.get("font_pair", "modern"), FONT_PAIRS["modern"]
    )
    type_scale = generate_type_scale(
        base_size=16,
        ratio=theme.get("type_ratio", 1.25),
        steps=7,
    )

    tokens = {
        "meta": {
            "theme_name": theme.get("name", "Custom"),
            "theme_id": theme.get("id", "custom"),
            "version": "1.0.0",
            "design_variance": theme.get("design_variance", 5),
            "motion_intensity": theme.get("motion_intensity", 3),
            "visual_density": theme.get("visual_density", 5),
        },
        "color": {
            "primary": colors["primary_palette"],
            "neutral": colors["neutral_palette"],
            "secondary": colors["secondary"],
            "accent": colors["accent"],
            "background": {
                "light": colors["background_light"],
                "dark": colors["background_dark"],
            },
            "semantic": _generate_semantic_colors(
                colors["primary_palette"], colors["accent"]
            ),
        },
        "typography": {
            "font_family": {
                "heading": ", ".join(font_pair[0]),
                "body": ", ".join(font_pair[1]),
                "mono": "SF Mono, Fira Code, monospace",
            },
            "type_scale": type_scale,
            "font_weight": {
                "light": 300,
                "regular": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            },
        },
        "spacing": {
            "unit": theme.get("spacing_unit", 4),
            "scale": _generate_spacing_scale(theme.get("spacing_unit", 4)),
        },
        "border": {
            "radius": {
                "none": "0px",
                "sm": f"{max(2, theme.get('border_radius', 6) // 2)}px",
                "md": f"{theme.get('border_radius', 6)}px",
                "lg": f"{theme.get('border_radius', 6) * 2}px",
                "full": "9999px",
            },
            "width": {
                "none": "0px",
                "thin": "1px",
                "medium": "2px",
                "thick": "4px",
            },
        },
        "shadow": _generate_shadows(theme.get("shadow_opacity", 0.1)),
        "motion": {
            "duration": {
                "fast": "150ms",
                "normal": "300ms",
                "slow": "500ms",
                "slowest": "1000ms",
            },
            "easing": {
                "linear": "linear",
                "ease_in": "cubic-bezier(0.4, 0, 1, 1)",
                "ease_out": "cubic-bezier(0, 0, 0.2, 1)",
                "ease_in_out": "cubic-bezier(0.4, 0, 0.2, 1)",
                "spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
            },
        },
        "breakpoint": {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px",
        },
        "z_index": {
            "base": 0,
            "dropdown": 100,
            "sticky": 200,
            "modal_backdrop": 300,
            "modal": 400,
            "tooltip": 500,
            "toast": 600,
        },
    }

    return tokens


def _generate_semantic_colors(
    primary_palette: dict, accent: str
) -> dict:
    """Generate semantic/utility colors."""
    return {
        "success": primary_palette.get("500", "#22c55e"),
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": accent,
    }


def _generate_spacing_scale(unit: int) -> dict:
    """Generate a spacing scale from the base unit."""
    scale = {}
    multipliers = {
        "0": 0,
        "px": 1,
        "0.5": 0.5,
        "1": 1,
        "1.5": 1.5,
        "2": 2,
        "2.5": 2.5,
        "3": 3,
        "3.5": 3.5,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "14": 14,
        "16": 16,
        "20": 20,
        "24": 24,
        "28": 28,
        "32": 32,
        "36": 36,
        "40": 40,
        "44": 44,
        "48": 48,
        "52": 52,
        "56": 56,
        "60": 60,
        "64": 64,
        "72": 72,
        "80": 80,
        "96": 96,
    }
    for label, mult in multipliers.items():
        scale[f"{label}"] = f"{mult * unit}px"
    return scale


def _generate_shadows(opacity: float) -> dict:
    """Generate shadow tokens with configurable opacity."""
    return {
        "sm": f"0 1px 2px 0 rgba(0, 0, 0, {opacity})",
        "md": f"0 4px 6px -1px rgba(0, 0, 0, {opacity}), 0 2px 4px -2px rgba(0, 0, 0, {opacity * 0.5})",
        "lg": f"0 10px 15px -3px rgba(0, 0, 0, {opacity}), 0 4px 6px -4px rgba(0, 0, 0, {opacity * 0.5})",
        "xl": f"0 20px 25px -5px rgba(0, 0, 0, {opacity}), 0 8px 10px -6px rgba(0, 0, 0, {opacity * 0.5})",
        "2xl": f"0 25px 50px -12px rgba(0, 0, 0, {opacity * 1.2})",
        "inner": f"inset 0 2px 4px 0 rgba(0, 0, 0, {opacity * 0.5})",
    }