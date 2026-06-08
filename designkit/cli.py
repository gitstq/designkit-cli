"""
CLI entry point — command-line interface for DesignKit-CLI.

Commands:
  list          List available theme presets
  preview       Preview a design theme in the terminal
  export        Export design tokens to a file
  palette       Generate a color palette from a hex color
  prompt        Generate an AI system prompt with design context
  info          Show DesignKit-CLI version and info
"""

import argparse
import json
import os
import sys

from . import __version__
from .themes import PRESET_THEMES, list_themes, get_theme, resolve_theme_colors
from .tokens import generate_design_tokens
from .export import to_css, to_json, to_tailwind_config, to_scss, to_design_tokens_json
from .palette import (
    generate_palette,
    generate_neutral_palette,
    generate_complementary,
    generate_analogous,
    generate_triadic,
    is_valid_hex,
)
from .ai_prompts import generate_system_prompt, generate_component_prompt, list_model_types


def cmd_list(args):
    """List all available theme presets."""
    themes = list_themes()
    print(f"\n🎨 DesignKit-CLI — Available Theme Presets ({len(themes)} themes)\n")
    print(f"{'─' * 60}")
    for t in themes:
        print(f"  [bold]{t['id']}[/bold] — {t['name']}")
        print(f"      {t['description']}")
        print()
    print(f"Use: designkit preview --theme <theme_id>")
    print(f"Use: designkit export --theme <theme_id> --format <format>\n")


def cmd_preview(args):
    """Preview a design theme in the terminal."""
    try:
        from .tui import show_theme_preview
        show_theme_preview(args.theme)
    except ImportError:
        print("⚠️  Rich library is required for terminal preview.")
        print(f"   Install: pip install rich")
        print(f"   Or export tokens directly: designkit export --theme {args.theme or '<theme>'} --format css")


def cmd_export(args):
    """Export design tokens to a file."""
    theme_name = args.theme

    if theme_name and theme_name not in PRESET_THEMES:
        print(f"❌ Unknown theme: '{theme_name}'")
        print(f"   Available: {', '.join(PRESET_THEMES.keys())}")
        return

    # Export all themes if none specified
    theme_names = [theme_name] if theme_name else list(PRESET_THEMES.keys())

    for tname in theme_names:
        theme = get_theme(tname)
        tokens = generate_design_tokens({**theme, "id": tname})

        format_map = {
            "css": (to_css(tokens), ".css"),
            "json": (to_json(tokens), ".json"),
            "tailwind": (to_tailwind_config(tokens), ".config.js"),
            "scss": (to_scss(tokens), ".scss"),
            "dtcg": (to_design_tokens_json(tokens), ".tokens.json"),
        }

        if args.format not in format_map:
            print(f"❌ Unknown format: '{args.format}'")
            print(f"   Available: {', '.join(format_map.keys())}")
            return

        content, ext = format_map[args.format]
        filename = f"designkit-{tname}{ext}" if tname else f"designkit-output{ext}"

        if args.output:
            filepath = args.output
            if tname or not theme_name:
                # Multiple files
                fname, fext = os.path.splitext(args.output)
                filepath = f"{fname}-{tname}{fext}"
        else:
            filepath = filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Tokens exported: {filepath}")

    if not args.output and len(theme_names) == 1:
        print(f"\n📁 File: {filename}")
        print("   Preview: designkit preview")


def cmd_palette(args):
    """Generate a color palette from a hex color."""
    color = args.color.strip()

    if not is_valid_hex(color):
        print(f"❌ Invalid color: '{color}'")
        print("   Use format: #RRGGBB or #RGB")
        return

    if not color.startswith("#"):
        color = f"#{color}"

    print(f"\n🎨 Color Palette from {color}\n")

    # Full palette
    palette = generate_palette(color)
    neutral = generate_neutral_palette(color)
    comp = generate_complementary(color)
    analogous = generate_analogous(color)
    triadic = generate_triadic(color)

    print(f"  {'─' * 40}")
    print(f"  {'Shade':<10s}  {'Primary':<10s}{'Neutral':<10s}")
    print(f"  {'─' * 40}")

    for label in ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"):
        p = palette.get(label, "")
        n = neutral.get(label, "")
        print(f"  {label:<10s}  {p:<10s}{n:<10s}")

    print(f"\n  🎯 Complementary: {comp}")
    print(f"  🔷 Analogous:     {', '.join(analogous)}")
    print(f"  🔶 Triadic:       {', '.join(triadic)}")
    print(f"  ⬛ Foreground:    {palette.get('FOREGROUND', '')}")
    print(f"\n  Export: designkit export --palette {color}\n")


def cmd_prompt(args):
    """Generate an AI system prompt with design system context."""
    theme_name = args.theme
    model_type = args.model or "glm"

    if theme_name not in PRESET_THEMES:
        print(f"❌ Unknown theme: '{theme_name}'")
        print(f"   Available: {', '.join(PRESET_THEMES.keys())}")
        return

    available_models = list_model_types()
    if model_type not in available_models:
        print(f"⚠️  Unknown model type: '{model_type}'")
        print(f"   Available: {', '.join(available_models.keys())}")
        print(f"   Using default: glm")
        model_type = "glm"

    theme = get_theme(theme_name)
    tokens = generate_design_tokens({**theme, "id": theme_name})

    prompt = generate_system_prompt(tokens, model_type)
    model_info = available_models[model_type]

    print(f"\n🤖 AI System Prompt — {model_info['name']}")
    print(f"   Theme: {theme['name']} | Model: {model_type}")
    print(f"{'─' * 60}\n")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"✅ Prompt saved to: {args.output}")
    else:
        print(prompt)

    if args.component:
        component_prompt = generate_component_prompt(
            tokens, args.component, args.framework or "HTML+CSS", model_type
        )
        print(f"\n{'─' * 60}")
        print(f"\n🧩 Component Prompt:\n")
        print(component_prompt)


def cmd_info(args):
    """Show DesignKit-CLI version and info."""
    print(f"""
╔══════════════════════════════════════╗
║     🎨 DesignKit-CLI v{__version__:<14s}║
║     Design Token Generator &         ║
║     AI UI Style Engine               ║
╚══════════════════════════════════════╝

Features:
  • {len(PRESET_THEMES)} design theme presets
  • Color palette generation (primary, neutral, complementary, triadic)
  • Typography scale calculator
  • Multi-format export (CSS, JSON, Tailwind, SCSS, DTCG)
  • AI system prompt generation (GLM-5.1, GPT, Claude)
  • Interactive TUI preview (with Rich)

Quick start:
  designkit list                    # List themes
  designkit preview --theme minimal # Preview a theme
  designkit export --theme minimal --format css  # Export tokens
  designkit palette #ff6b6b         # Generate palette
  designkit prompt --theme minimal --model glm   # Generate AI prompt
""")


def main():
    parser = argparse.ArgumentParser(
        prog="designkit",
        description="🎨 DesignKit-CLI — Design Token Generator & AI UI Style Engine",
        epilog="Try: designkit list | designkit preview --theme minimal",
    )
    parser.add_argument(
        "--version", action="version",
        version=f"DesignKit-CLI v{__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = subparsers.add_parser("list", help="List available theme presets")

    # preview
    p_preview = subparsers.add_parser("preview", help="Preview a design theme")
    p_preview.add_argument(
        "--theme", "-t", type=str, default=None,
        help="Theme ID to preview (default: all themes)"
    )

    # export
    p_export = subparsers.add_parser("export", help="Export design tokens")
    p_export.add_argument(
        "--theme", "-t", type=str, default=None,
        help="Theme ID to export (default: all themes)"
    )
    p_export.add_argument(
        "--format", "-f", type=str, default="css",
        choices=["css", "json", "tailwind", "scss", "dtcg"],
        help="Export format (default: css)"
    )
    p_export.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file path"
    )

    # palette
    p_palette = subparsers.add_parser("palette", help="Generate color palette")
    p_palette.add_argument(
        "color", type=str,
        help="Primary hex color (e.g., #ff6b6b or ff6b6b)"
    )

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Generate AI system prompt")
    p_prompt.add_argument(
        "--theme", "-t", type=str, default="minimal",
        help="Theme ID to use (default: minimal)"
    )
    p_prompt.add_argument(
        "--model", "-m", type=str, default="glm",
        choices=list(list_model_types().keys()),
        help="AI model type (default: glm)"
    )
    p_prompt.add_argument(
        "--component", "-c", type=str, default=None,
        help="Generate a component-specific prompt"
    )
    p_prompt.add_argument(
        "--framework", "-fw", type=str, default="HTML+CSS",
        help="Target framework for component (default: HTML+CSS)"
    )
    p_prompt.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file path"
    )

    # info
    p_info = subparsers.add_parser("info", help="Show version and info")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    command_map = {
        "list": cmd_list,
        "preview": cmd_preview,
        "export": cmd_export,
        "palette": cmd_palette,
        "prompt": cmd_prompt,
        "info": cmd_info,
    }

    command_map[args.command](args)


if __name__ == "__main__":
    main()