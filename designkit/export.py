"""Export design tokens to various formats: CSS, JSON, Tailwind, SCSS, and more."""

import json


def to_css(tokens: dict, prefix: str = "dk") -> str:
    """Export design tokens as CSS custom properties."""
    lines = [f"/* DesignKit-CLI Generated Design Tokens */", ":root {"]

    def _flatten(obj, parent_key=""):
        items = []
        for key, value in obj.items():
            new_key = f"{parent_key}-{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(_flatten(value, new_key))
            else:
                css_var = f"--{prefix}-{new_key.replace('_', '-')}"
                items.append((css_var, str(value)))
        return items

    for var_name, value in _flatten(tokens):
        lines.append(f"  {var_name}: {value};")

    lines.append("}")
    return "\n".join(lines)


def to_json(tokens: dict, pretty: bool = True) -> str:
    """Export design tokens as JSON."""
    indent = 2 if pretty else None
    return json.dumps(tokens, indent=indent, ensure_ascii=False)


def to_tailwind_config(tokens: dict) -> str:
    """Export design tokens as a Tailwind CSS config extension."""
    lines = [
        "// DesignKit-CLI Generated Tailwind Config",
        "/** @type {import('tailwindcss').Config} */",
        "module.exports = {",
        "  theme: {",
        "    extend: {",
    ]

    # Colors
    lines.append("      colors: {")
    primary = tokens.get("color", {}).get("primary", {})
    neutral = tokens.get("color", {}).get("neutral", {})
    semantic = tokens.get("color", {}).get("semantic", {})

    lines.append("        primary: {")
    for k, v in primary.items():
        if k in ("DEFAULT", "FOREGROUND"):
            continue
        lines.append(f"          '{k}': '{v}',")
    if "DEFAULT" in primary:
        lines.append(f"          DEFAULT: '{primary['DEFAULT']}',")
    lines.append("        },")

    lines.append("        neutral: {")
    for k, v in neutral.items():
        if k in ("DEFAULT", "FOREGROUND"):
            continue
        lines.append(f"          '{k}': '{v}',")
    lines.append("        },")

    lines.append(f"        accent: '{tokens.get('color', {}).get('accent', '#000')}',")

    for sk in ("success", "warning", "error", "info"):
        lines.append(f"        '{sk}': '{semantic.get(sk, '#000')}',")

    lines.append("      },")

    # Spacing
    lines.append("      spacing: {")
    spacing = tokens.get("spacing", {}).get("scale", {})
    for k, v in list(spacing.items())[:30]:
        lines.append(f"        '{k}': '{v}',")
    lines.append("      },")

    # Border radius
    lines.append("      borderRadius: {")
    for k, v in tokens.get("border", {}).get("radius", {}).items():
        lines.append(f"        '{k}': '{v}',")
    lines.append("      },")

    # Font families
    lines.append("      fontFamily: {")
    for k, v in tokens.get("typography", {}).get("font_family", {}).items():
        families = [f"'{f.strip()}'" for f in v.split(",")]
        lines.append(f"        '{k}': [{', '.join(families)}],")
    lines.append("      },")

    # Font sizes
    lines.append("      fontSize: {")
    for k, v in tokens.get("typography", {}).get("type_scale", {}).items():
        lines.append(f"        '{k}': ['{v['px']}px', {{ lineHeight: '{v['line_height']}', fontWeight: '{v['font_weight']}' }}],")
    lines.append("      },")

    # Shadows
    lines.append("      boxShadow: {")
    for k, v in tokens.get("shadow", {}).items():
        lines.append(f"        '{k}': '{v}',")
    lines.append("      },")

    # Animations / transitions
    lines.append("      transitionDuration: {")
    for k, v in tokens.get("motion", {}).get("duration", {}).items():
        lines.append(f"        '{k}': '{v}',")
    lines.append("      },")

    lines.append("    },")
    lines.append("  },")
    lines.append("};")

    return "\n".join(lines)


def to_scss(tokens: dict, prefix: str = "dk") -> str:
    """Export design tokens as SCSS variables and maps."""
    lines = [
        "// DesignKit-CLI Generated SCSS Design Tokens",
        "// Prefix: $" + prefix,
        "",
    ]

    def _to_scss(obj, parent_key="", depth=0):
        result = []
        indent = "  " * depth
        is_map = isinstance(obj, dict) and any(
            isinstance(v, dict) for v in obj.values()
        )

        for key, value in obj.items():
            var_name = f"{parent_key}-{key}" if parent_key else key
            scss_name = var_name.replace("-", "_").replace(".", "-")

            if isinstance(value, dict):
                if is_map:
                    result.append(f"{indent}'{key}': (")
                    result.extend(_to_scss(value, var_name, depth + 1))
                    result.append(f"{indent}),")
                else:
                    result.append(f"${prefix}-{scss_name}: (")
                    result.extend(_to_scss(value, var_name, depth + 1))
                    result.append(f");")
            else:
                result.append(f"{indent}'{key}': '{value}'," if is_map else f"${prefix}-{scss_name}: '{value}';")

        return result

    lines.extend(_to_scss(tokens))
    return "\n".join(lines)


def to_design_tokens_json(tokens: dict, pretty: bool = True) -> str:
    """Export in Design Tokens Format (DTCG / W3C Design Tokens spec)."""
    dt = {
        "name": tokens.get("meta", {}).get("theme_name", "DesignKit"),
        "version": tokens.get("meta", {}).get("version", "1.0.0"),
        "tokens": {},
    }

    def _to_dt_value(value):
        """Convert a design value to DTCG format."""
        return {"$value": value, "$type": "dimension"}

    def _walk(obj, path=""):
        items = {}
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                result = _walk(value, new_path)
                items[key] = result if result else value
            elif isinstance(value, str):
                if "px" in value:
                    items[key] = {"$value": value, "$type": "dimension"}
                elif value.startswith("#"):
                    items[key] = {"$value": value, "$type": "color"}
                elif value.startswith("0 ") or value.startswith("inset"):
                    items[key] = {"$value": value, "$type": "shadow"}
                else:
                    items[key] = {"$value": value, "$type": "textStyle" if "font" in new_path else "other"}
            else:
                items[key] = {"$value": value, "$type": "number"}
        return items

    dt["tokens"] = _walk(tokens)
    return json.dumps(dt, indent=2 if pretty else None, ensure_ascii=False)