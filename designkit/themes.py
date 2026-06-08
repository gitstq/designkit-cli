"""
Design theme presets — pre-built design systems with adjustable parameters.

Each theme is a complete design specification including colors, typography,
spacing, border radius, shadows, and other design tokens.
"""

from .palette import generate_palette, generate_neutral_palette


PRESET_THEMES = {
    "minimal": {
        "name": "极简 Minimal",
        "description": "Clean, whitespace-driven design with subtle colors. Perfect for content-focused applications.",
        "primary": "#2563eb",
        "secondary": "#7c3aed",
        "accent": "#06b6d4",
        "background_light": "#ffffff",
        "background_dark": "#0f172a",
        "border_radius": 6,
        "shadow_opacity": 0.08,
        "font_pair": "modern",
        "type_ratio": 1.250,
        "spacing_unit": 4,
        "design_variance": 3,
        "motion_intensity": 2,
        "visual_density": 2,
    },
    "brutalist": {
        "name": "粗野主义 Brutalist",
        "description": "Bold, high-contrast, unapologetic design. Thick borders, raw typography, maximum impact.",
        "primary": "#dc2626",
        "secondary": "#171717",
        "accent": "#f59e0b",
        "background_light": "#fafafa",
        "background_dark": "#0a0a0a",
        "border_radius": 0,
        "shadow_opacity": 0.15,
        "font_pair": "technical",
        "type_ratio": 1.333,
        "spacing_unit": 8,
        "design_variance": 9,
        "motion_intensity": 5,
        "visual_density": 7,
    },
    "warm": {
        "name": "温暖 Warm",
        "description": "Soft, approachable, human-centered design. Earthy tones and gentle curves.",
        "primary": "#d97706",
        "secondary": "#b45309",
        "accent": "#059669",
        "background_light": "#fffbeb",
        "background_dark": "#1c1917",
        "border_radius": 12,
        "shadow_opacity": 0.06,
        "font_pair": "elegant",
        "type_ratio": 1.200,
        "spacing_unit": 6,
        "design_variance": 5,
        "motion_intensity": 4,
        "visual_density": 4,
    },
    "neon": {
        "name": "霓虹 Neon",
        "description": "Vibrant, dark-mode-first digital aesthetic. Glowing colors and dramatic contrast.",
        "primary": "#a855f7",
        "secondary": "#ec4899",
        "accent": "#22d3ee",
        "background_light": "#f5f3ff",
        "background_dark": "#09090b",
        "border_radius": 8,
        "shadow_opacity": 0.2,
        "font_pair": "technical",
        "type_ratio": 1.250,
        "spacing_unit": 4,
        "design_variance": 8,
        "motion_intensity": 8,
        "visual_density": 5,
    },
    "corporate": {
        "name": "商务 Corporate",
        "description": "Professional, trustworthy, data-dense design. Optimized for dashboards and enterprise apps.",
        "primary": "#1e40af",
        "secondary": "#475569",
        "accent": "#0891b2",
        "background_light": "#f8fafc",
        "background_dark": "#0f172a",
        "border_radius": 4,
        "shadow_opacity": 0.1,
        "font_pair": "modern",
        "type_ratio": 1.125,
        "spacing_unit": 4,
        "design_variance": 2,
        "motion_intensity": 1,
        "visual_density": 8,
    },
    "playful": {
        "name": "活泼 Playful",
        "description": "Fun, colorful, engaging design with rounded elements and lively colors.",
        "primary": "#f43f5e",
        "secondary": "#f97316",
        "accent": "#8b5cf6",
        "background_light": "#fff1f2",
        "background_dark": "#1f2937",
        "border_radius": 16,
        "shadow_opacity": 0.12,
        "font_pair": "elegant",
        "type_ratio": 1.333,
        "spacing_unit": 6,
        "design_variance": 7,
        "motion_intensity": 7,
        "visual_density": 3,
    },
    "nature": {
        "name": "自然 Nature",
        "description": "Organic, calming, earth-inspired design. Green-centric palette with soft textures.",
        "primary": "#16a34a",
        "secondary": "#65a30d",
        "accent": "#0d9488",
        "background_light": "#f0fdf4",
        "background_dark": "#052e16",
        "border_radius": 10,
        "shadow_opacity": 0.07,
        "font_pair": "classic",
        "type_ratio": 1.200,
        "spacing_unit": 5,
        "design_variance": 4,
        "motion_intensity": 3,
        "visual_density": 4,
    },
}


def get_theme(theme_name: str, customizations: dict = None) -> dict:
    """Get a theme preset with optional overrides."""
    if theme_name not in PRESET_THEMES:
        available = ", ".join(PRESET_THEMES.keys())
        raise ValueError(f"Unknown theme '{theme_name}'. Available: {available}")

    theme = dict(PRESET_THEMES[theme_name])
    if customizations:
        theme.update(customizations)
    return theme


def list_themes() -> list:
    """List all available theme presets with descriptions."""
    return [
        {"id": tid, "name": t["name"], "description": t["description"]}
        for tid, t in PRESET_THEMES.items()
    ]


def resolve_theme_colors(theme: dict) -> dict:
    """Resolve all theme colors including generated palettes."""
    primary = theme["primary"]
    return {
        "primary_palette": generate_palette(primary),
        "neutral_palette": generate_neutral_palette(primary),
        "secondary": theme.get("secondary", generate_palette(theme.get("secondary", "#7c3aed"))["DEFAULT"]),
        "accent": theme.get("accent", "#06b6d4"),
        "background_light": theme.get("background_light", "#ffffff"),
        "background_dark": theme.get("background_dark", "#0f172a"),
    }