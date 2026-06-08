"""AI prompt templates — generate AI coding prompts optimized for consistent UI design."""

TEMPLATES = {
    "glm": {
        "name": "GLM-5.1 优化版",
        "description": "Optimized for GLM-5.1 and similar Chinese LLMs",
        "system_prompt_template": """你是一个专业的前端设计师和开发者。请严格遵循以下设计规范来生成代码。

## 设计系统: {theme_name}
{theme_description}

### 设计参数
- 设计差异度 (1-10): {design_variance} — 值越高设计越大胆创新
- 动效强度 (1-10): {motion_intensity} — 值越高动效越丰富
- 视觉密度 (1-10): {visual_density} — 值越高内容越紧凑

### 颜色体系
主色: {primary_color}
强调色: {accent_color}
背景（浅色）: {bg_light}
背景（深色）: {bg_dark}

### 排版
标题字体: {heading_font}
正文字体: {body_font}
字号比例: {type_ratio}

### 间距与圆角
基础间距: {spacing_unit}px
默认圆角: {border_radius}px
阴影透明度: {shadow_opacity}

## 代码生成要求
1. 所有颜色、间距、圆角必须使用上面定义的值
2. 保持视觉风格一致性
3. 关注的用户界面体验和可访问性
4. 生成的代码应该是可直接运行的完整片段
""",
        "component_prompt_template": """请用以上设计系统创建一个{component_name}组件。

具体要求：
- 使用 {framework} 实现
- 遵循 {theme_name} 设计规范
- 确保高对比度和可访问性
- 添加适当的过渡动效（动效强度: {motion_intensity}/10）
- 输出完整的可运行代码
""",
    },
    "openai": {
        "name": "OpenAI/GPT 优化版",
        "description": "Optimized for GPT-4o, GPT-4 and similar models",
        "system_prompt_template": """You are a professional front-end designer and developer. Follow this design system strictly:

## Design System: {theme_name}
{theme_description}

### Design Parameters
- Design Variance (1-10): {design_variance}
- Motion Intensity (1-10): {motion_intensity}
- Visual Density (1-10): {visual_density}

### Colors
Primary: {primary_color}
Accent: {accent_color}
Background (Light): {bg_light}
Background (Dark): {bg_dark}

### Typography
Heading Font: {heading_font}
Body Font: {body_font}
Type Ratio: {type_ratio}

### Spacing & Borders
Base Spacing: {spacing_unit}px
Border Radius: {border_radius}px
Shadow Opacity: {shadow_opacity}

## Requirements
1. Use the exact colors, spacing, and border radius values above
2. Maintain visual consistency throughout
3. Focus on UX and accessibility
4. Output complete, runnable code
""",
        "component_prompt_template": """Create a {component_name} component using the design system above.

Requirements:
- Framework: {framework}
- Follow {theme_name} design system
- Ensure high contrast and accessibility
- Add smooth transitions (intensity: {motion_intensity}/10)
- Output complete runnable code
""",
    },
    "claude": {
        "name": "Claude 优化版",
        "description": "Optimized for Claude 3.5/4 models",
        "system_prompt_template": """You are a front-end design expert. I will provide a design system — create interfaces that match it precisely.

DESIGN SYSTEM: {theme_name}
{theme_description}

Parameters:
- Design Variance: {design_variance}/10
- Motion Intensity: {motion_intensity}/10
- Visual Density: {visual_density}/10

COLORS:
Primary → {primary_color}
Accent → {accent_color}
BG Light → {bg_light}
BG Dark → {bg_dark}

TYPOGRAPHY:
Headings: {heading_font}
Body: {body_font}
Scale Ratio: {type_ratio}

SPACING:
Unit: {spacing_unit}px
Radius: {border_radius}px

RULES:
- Use exact values provided
- Consistency is critical
- Prioritize accessibility
- Produce production-quality code
""",
        "component_prompt_template": """Build a {component_name} component using the design system above.

Framework: {framework}
Style: {theme_name}
Animation intensity: {motion_intensity}/10

Output: complete, functional, accessible code.
""",
    },
}


def generate_system_prompt(
    tokens: dict, model_type: str = "glm"
) -> str:
    """Generate a system prompt for AI coding with design system context."""
    template_key = model_type if model_type in TEMPLATES else "glm"
    template = TEMPLATES[template_key]["system_prompt_template"]

    meta = tokens.get("meta", {})
    color = tokens.get("color", {})
    typo = tokens.get("typography", {})
    spacing = tokens.get("spacing", {})

    # Font names (use first font from the family string)
    heading_font = typo.get("font_family", {}).get("heading", "system-ui").split(",")[0].strip().strip("'\"")
    body_font = typo.get("font_family", {}).get("body", "system-ui").split(",")[0].strip().strip("'\"")

    return template.format(
        theme_name=meta.get("theme_name", "Custom"),
        theme_description="",
        design_variance=meta.get("design_variance", 5),
        motion_intensity=meta.get("motion_intensity", 3),
        visual_density=meta.get("visual_density", 5),
        primary_color=color.get("primary", {}).get("DEFAULT", "#2563eb"),
        accent_color=color.get("accent", "#06b6d4"),
        bg_light=color.get("background", {}).get("light", "#ffffff"),
        bg_dark=color.get("background", {}).get("dark", "#0f172a"),
        heading_font=heading_font,
        body_font=body_font,
        type_ratio="1.25",
        spacing_unit=spacing.get("unit", 4),
        border_radius="6",
        shadow_opacity="0.1",
    )


def generate_component_prompt(
    tokens: dict,
    component_name: str,
    framework: str = "HTML+CSS",
    model_type: str = "glm",
) -> str:
    """Generate a component-specific prompt incorporating the design system."""
    template_key = model_type if model_type in TEMPLATES else "glm"
    template = TEMPLATES[template_key]["component_prompt_template"]

    meta = tokens.get("meta", {})

    return template.format(
        component_name=component_name,
        framework=framework,
        theme_name=meta.get("theme_name", "Custom"),
        motion_intensity=meta.get("motion_intensity", 3),
    )


def list_model_types() -> dict:
    """List available AI model prompt templates."""
    return {
        key: {"name": val["name"], "description": val["description"]}
        for key, val in TEMPLATES.items()
    }