"""Tests for DesignKit-CLI core modules."""

import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from designkit.palette import (
    generate_palette,
    generate_neutral_palette,
    generate_complementary,
    generate_analogous,
    generate_triadic,
    is_valid_hex,
    contrast_ratio,
)
from designkit.themes import PRESET_THEMES, list_themes, get_theme, resolve_theme_colors
from designkit.tokens import generate_design_tokens
from designkit.typography import generate_type_scale, FONT_PAIRS
from designkit.export import to_css, to_json, to_tailwind_config, to_scss


class TestPalette(unittest.TestCase):
    """Test color palette generation."""

    def test_generate_palette(self):
        """Test that a palette has all required keys."""
        palette = generate_palette("#2563eb")
        for label in ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950", "DEFAULT", "FOREGROUND"):
            self.assertIn(label, palette)
        self.assertTrue(palette["DEFAULT"].startswith("#"))

    def test_generate_neutral_palette(self):
        """Test neutral palette generation."""
        neutral = generate_neutral_palette("#2563eb")
        self.assertIn("500", neutral)

    def test_complementary(self):
        """Test complementary color generation."""
        comp = generate_complementary("#2563eb")
        self.assertTrue(comp.startswith("#"))

    def test_analogous(self):
        """Test analogous color generation."""
        colors = generate_analogous("#2563eb", count=3)
        self.assertEqual(len(colors), 3)
        for c in colors:
            self.assertTrue(c.startswith("#"))

    def test_triadic(self):
        """Test triadic color generation."""
        colors = generate_triadic("#2563eb")
        self.assertEqual(len(colors), 3)

    def test_is_valid_hex(self):
        """Test hex validation."""
        self.assertTrue(is_valid_hex("#2563eb"))
        self.assertTrue(is_valid_hex("#fff"))
        self.assertTrue(is_valid_hex("2563eb"))
        self.assertFalse(is_valid_hex("#zzz"))
        self.assertFalse(is_valid_hex("not-a-color"))

    def test_contrast_ratio(self):
        """Test WCAG contrast ratio calculation."""
        ratio = contrast_ratio("#000000", "#ffffff")
        self.assertGreater(ratio, 20)  # Black on white should be high contrast


class TestThemes(unittest.TestCase):
    """Test theme presets."""

    def test_all_themes_have_required_keys(self):
        """Test that all theme presets have required configuration keys."""
        required = {"name", "primary", "font_pair", "type_ratio", "spacing_unit"}
        for tid, theme in PRESET_THEMES.items():
            with self.subTest(theme=tid):
                for key in required:
                    self.assertIn(key, theme, f"{tid} missing key: {key}")

    def test_list_themes(self):
        """Test listing themes."""
        themes = list_themes()
        self.assertEqual(len(themes), len(PRESET_THEMES))
        for t in themes:
            self.assertIn("id", t)
            self.assertIn("name", t)
            self.assertIn("description", t)

    def test_get_theme(self):
        """Test getting a specific theme."""
        theme = get_theme("minimal")
        self.assertEqual(theme["primary"], "#2563eb")

    def test_get_theme_invalid(self):
        """Test that invalid theme name raises error."""
        with self.assertRaises(ValueError):
            get_theme("nonexistent")

    def test_resolve_theme_colors(self):
        """Test resolving theme colors."""
        theme = get_theme("minimal")
        colors = resolve_theme_colors(theme)
        self.assertIn("primary_palette", colors)
        self.assertIn("neutral_palette", colors)
        self.assertIn("secondary", colors)


class TestTypography(unittest.TestCase):
    """Test typography scale generation."""

    def test_generate_type_scale(self):
        """Test type scale generation."""
        scale = generate_type_scale(16, 1.25)
        required_levels = {"body", "h1", "h2", "h3", "h4", "small", "display"}
        for level in required_levels:
            self.assertIn(level, scale)
        # body should be close to 16px
        self.assertAlmostEqual(scale["body"]["px"], 16, delta=1)

    def test_different_ratios(self):
        """Test different type scale ratios."""
        for ratio in [1.125, 1.250, 1.333, 1.618]:
            with self.subTest(ratio=ratio):
                scale = generate_type_scale(16, ratio)
                self.assertIn("body", scale)

    def test_font_pairs(self):
        """Test font pair definitions."""
        for pair_id in ("modern", "classic", "code", "elegant", "technical"):
            self.assertIn(pair_id, FONT_PAIRS)


class TestTokens(unittest.TestCase):
    """Test design token generation."""

    def setUp(self):
        self.theme = get_theme("minimal")
        self.tokens = generate_design_tokens({**self.theme, "id": "minimal"})

    def test_token_structure(self):
        """Test that tokens have expected top-level keys."""
        required = {"meta", "color", "typography", "spacing", "border", "shadow", "motion", "breakpoint"}
        for key in required:
            self.assertIn(key, self.tokens, f"Missing token key: {key}")

    def test_color_tokens(self):
        """Test color token structure."""
        self.assertIn("primary", self.tokens["color"])
        self.assertIn("neutral", self.tokens["color"])
        self.assertIn("accent", self.tokens["color"])
        self.assertIn("semantic", self.tokens["color"])

    def test_typography_tokens(self):
        """Test typography token structure."""
        self.assertIn("type_scale", self.tokens["typography"])
        self.assertIn("font_family", self.tokens["typography"])


class TestExport(unittest.TestCase):
    """Test export formats."""

    def setUp(self):
        self.theme = get_theme("minimal")
        self.tokens = generate_design_tokens({**self.theme, "id": "minimal"})

    def test_css_export(self):
        """Test CSS export."""
        css = to_css(self.tokens)
        self.assertIn(":root", css)
        self.assertIn("--dk", css)
        self.assertIn("color", css.lower())

    def test_json_export(self):
        """Test JSON export."""
        data = to_json(self.tokens)
        parsed = json.loads(data)
        self.assertIn("color", parsed)
        self.assertIn("meta", parsed)

    def test_tailwind_config(self):
        """Test Tailwind config export."""
        config = to_tailwind_config(self.tokens)
        self.assertIn("tailwindcss", config.lower())
        self.assertIn("module.exports", config)
        self.assertIn("colors", config.lower())

    def test_scss_export(self):
        """Test SCSS export."""
        scss = to_scss(self.tokens)
        self.assertIn("$dk-", scss)


if __name__ == "__main__":
    unittest.main()