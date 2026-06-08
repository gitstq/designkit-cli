"""
Terminal UI — Rich-based interactive design token preview and exploration.

This module provides a beautiful terminal interface for visualizing
and exploring design tokens in real-time.
"""

import sys

from .themes import PRESET_THEMES, list_themes
from .tokens import generate_design_tokens
from .export import to_css, to_json, to_tailwind_config, to_scss


try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def _get_console():
    """Get a Rich Console instance if available."""
    if RICH_AVAILABLE:
        return Console()
    return None


def show_theme_preview(theme_name: str = None):
    """Display an interactive preview of a design theme in the terminal."""
    if not RICH_AVAILABLE:
        print("⚠️  Rich library not installed. Install with: pip install rich")
        print("   Falling back to basic text output.\n")

    console = _get_console()

    if theme_name:
        if theme_name not in PRESET_THEMES:
            print(f"❌ Unknown theme: '{theme_name}'")
            return
        themes = {theme_name: PRESET_THEMES[theme_name]}
    else:
        themes = PRESET_THEMES

    for tid, theme in themes.items():
        tokens = generate_design_tokens({**theme, "id": tid})

        if console:
            # Show theme header
            console.print()
            header = Panel(
                f"[bold]{theme['name']}[/bold]\n{theme['description']}",
                border_style="bright_blue",
                padding=(1, 2),
            )
            console.print(header)

            # Color palette preview
            _show_color_preview(console, tokens, tid)

            # Typography preview
            _show_typography_preview(console, tokens)

            # Spacing & border preview
            _show_spacing_preview(console, tokens)

            # Component preview (simulated)
            _show_component_preview(console, tokens)

            # Export options
            console.print(f"\n[bold cyan]📦 Export Options:[/bold cyan]")
            console.print(
                "   designkit export --theme [i]theme_id[/i] --format css\n"
                "   designkit export --theme [i]theme_id[/i] --format json\n"
                "   designkit export --theme [i]theme_id[/i] --format tailwind\n"
                "   designkit export --theme [i]theme_id[/i] --format scss"
            )
            console.print()
        else:
            _text_preview(theme, tokens)


def _show_color_preview(console, tokens: dict, tid: str):
    """Display color palette as a terminal table."""
    console.print("\n[bold]🎨 Color Palette:[/bold]")

    primary = tokens.get("color", {}).get("primary", {})
    neutral = tokens.get("color", {}).get("neutral", {})
    semantic = tokens.get("color", {}).get("semantic", {})

    table = Table(box=box.SIMPLE, show_header=False)
    table.add_column("Token", style="dim")
    table.add_column("Shade")
    table.add_column("Preview")

    for label in ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"):
        p_color = primary.get(label, "#fff")
        n_color = neutral.get(label, "#fff")
        table.add_row(
            f"primary-{label}",
            p_color,
            f"[on {p_color}]      [/on {p_color}]",
        )

    table.add_row("", "", "")
    table.add_row(
        f"accent",
        tokens.get("color", {}).get("accent", ""),
        f"[on {tokens.get('color', {}).get('accent', '#fff')}]      [/on {tokens.get('color', {}).get('accent', '#fff')}]",
    )

    # Semantic colors
    for sk in ("success", "warning", "error", "info"):
        sc = semantic.get(sk, "#000")
        table.add_row(
            sk,
            sc,
            f"[on {sc}]      [/on {sc}]",
        )

    console.print(table)


def _show_typography_preview(console, tokens: dict):
    """Display typography scale in terminal."""
    console.print("\n[bold]🔤 Typography:[/bold]")

    type_scale = tokens.get("typography", {}).get("type_scale", {})
    families = tokens.get("typography", {}).get("font_family", {})

    table = Table(box=box.SIMPLE, show_header=True)
    table.add_column("Level", style="dim")
    table.add_column("Size (px)")
    table.add_column("Size (rem)")
    table.add_column("Line Height")
    table.add_column("Weight")

    for label in ("display", "h1", "h2", "h3", "h4", "body", "small", "caption"):
        if label in type_scale:
            info = type_scale[label]
            table.add_row(
                label,
                str(info["px"]),
                str(info["rem"]),
                str(info["line_height"]),
                str(info["font_weight"]),
            )

    console.print(table)
    console.print(
        f"[dim]Headings: {families.get('heading', 'system-ui')}[/dim]"
    )
    console.print(
        f"[dim]Body: {families.get('body', 'system-ui')}[/dim]"
    )


def _show_spacing_preview(console, tokens: dict):
    """Display spacing scale in terminal."""
    console.print("\n[bold]📐 Spacing & Borders:[/bold]")

    border_radius = tokens.get("border", {}).get("radius", {})
    unit = tokens.get("spacing", {}).get("unit", 4)

    console.print(
        f"   [dim]Base Unit:[/dim] {unit}px  "
        f"[dim]Border Radius:[/dim] md={border_radius.get('md', '6px')}"
    )

    # Show spacing bar chart
    spacing = tokens.get("spacing", {}).get("scale", {})
    console.print("   [dim]Spacing Scale:[/dim]")
    for label in ("0", "1", "2", "4", "8", "16", "24", "32", "48", "64", "96"):
        if label in spacing:
            bar_len = min(int(spacing[label].replace("px", "")) // unit, 40)
            bar = "█" * max(bar_len, 1)
            console.print(f"   {label:>4s}  {spacing[label]:<8s} {bar}")


def _show_component_preview(console, tokens: dict):
    """Show a simulated button component preview."""
    console.print("\n[bold]🧩 Component Preview:[/bold]")

    primary = tokens.get("color", {}).get("primary", {})
    p500 = primary.get("500", primary.get("DEFAULT", "#2563eb"))
    p600 = primary.get("600", "#1d4ed8")
    radius = tokens.get("border", {}).get("radius", {}).get("md", "6px")
    accent = tokens.get("color", {}).get("accent", "#06b6d4")

    console.print(Panel(
        f"[on {p500} white bold]  Primary Button  [/on {p500}]  "
        f"[on {accent} white bold]  Accent Button  [/on {accent}]  "
        f"[dim]  [Link]Text Link[/Link]  [/dim]",
        title="Buttons",
        border_style="dim",
        padding=(1, 1),
    ))

    # Show a card preview
    bg_color = tokens.get("color", {}).get("background", {}).get("light", "#fff")
    card_bg = "#f8fafc"

    console.print(Panel(
        f"[bold]Card Title[/bold]\n\n"
        f"[dim]This is a sample card component showing how the design system\n"
        f"would look in practice. Colors, spacing, and typography all\n"
        f"follow the specified theme.[/dim]\n\n"
        f"[on {p500} white]  Action  [/on {p500}]   [dim]Cancel[/dim]",
        title="Card Component",
        border_style="bright_white",
        padding=(1, 2),
    ))


def _text_preview(theme: dict, tokens: dict):
    """Fallback text preview when Rich is not available."""
    print(f"\n{'='*60}")
    print(f"  Theme: {theme['name']}")
    print(f"  {theme['description']}")
    print(f"{'='*60}")

    primary = tokens.get("color", {}).get("primary", {})
    print(f"\n  Primary: {primary.get('DEFAULT', '#000')}")
    print(f"  Accent: {tokens.get('color', {}).get('accent', '#000')}")

    type_scale = tokens.get("typography", {}).get("type_scale", {})
    print(f"\n  Type Scale: base={type_scale.get('body', {}).get('px', 16)}px")
    print(f"  Ratio: {theme.get('type_ratio', 1.25)}")
    print(f"  Spacing Unit: {theme.get('spacing_unit', 4)}px")

    print(f"\n  Export: designkit export --theme {theme.get('id', 'custom')} --format css\n")