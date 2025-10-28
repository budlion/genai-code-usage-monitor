# Theme System Quick Start Guide

## 5-Minute Setup

### 1. Basic Usage (Default Auto-Detection)

The theme system automatically detects the best theme for your environment:

```python
from genai_code_usage_monitor.ui import TokenProgressBar

# Just create and use - theme is auto-detected
bar = TokenProgressBar()
print(bar.render(75.5))
```

### 2. Manual Theme Selection

Set your preferred theme explicitly:

```python
from genai_code_usage_monitor.ui import set_theme, ThemeType, TokenProgressBar

# Set light theme for daytime use
set_theme(ThemeType.LIGHT)

# Now all progress bars use light theme
bar = TokenProgressBar()
print(bar.render(75.5))
```

### 3. Interactive Theme Switcher

Use the CLI to explore themes:

```bash
# List available themes
python -m genai_code_usage_monitor.ui.theme_switcher --list

# Preview dark theme with samples
python -m genai_code_usage_monitor.ui.theme_switcher --preview dark

# Switch to light theme
python -m genai_code_usage_monitor.ui.theme_switcher --switch light
```

### 4. Run the Demo

See all themes in action:

```bash
python examples/theme_demo.py
```

## Common Use Cases

### For CLI Applications

```python
import argparse
from genai_code_usage_monitor.ui import set_theme, ThemeType

parser = argparse.ArgumentParser()
parser.add_argument('--theme', choices=['light', 'dark', 'classic', 'auto'],
                    default='auto', help='UI theme')
args = parser.parse_args()

# Apply user's theme choice
theme_map = {
    'light': ThemeType.LIGHT,
    'dark': ThemeType.DARK,
    'classic': ThemeType.CLASSIC,
    'auto': ThemeType.AUTO,
}
set_theme(theme_map[args.theme])

# Rest of your application...
```

### For Web/Desktop Apps

```python
from genai_code_usage_monitor.ui import WCAGTheme, ThemeType

class UserSettings:
    def __init__(self):
        self.theme = WCAGTheme(ThemeType.AUTO)

    def set_user_theme(self, preference: str):
        """Apply user's saved preference."""
        theme_types = {
            'light': ThemeType.LIGHT,
            'dark': ThemeType.DARK,
        }
        self.theme.switch_theme(theme_types.get(preference, ThemeType.AUTO))
```

### For Testing Different Themes

```python
from genai_code_usage_monitor.ui import WCAGTheme, ThemeType, TokenProgressBar

# Test in both light and dark
for theme_type in [ThemeType.LIGHT, ThemeType.DARK]:
    theme = WCAGTheme(theme_type)
    bar = TokenProgressBar(theme=theme)

    print(f"\n{theme.current.name} Theme:")
    print(bar.render(50.0))
    print(bar.render(85.0))
```

## Theme Comparison

| Theme | Best For | Contrast | WCAG |
|-------|----------|----------|------|
| **Light** | Bright rooms, daytime | 4.5:1+ | ✓ AA |
| **Dark** | Low light, night | 7.0:1+ | ✓ AA+ |
| **Classic** | Compatibility | ~3.0:1 | ⚠ |
| **Auto** | Automatic detection | Varies | ✓ |

## Quick Troubleshooting

### Colors don't look right?

```python
# Try switching manually instead of auto
from genai_code_usage_monitor.ui import set_theme, ThemeType
set_theme(ThemeType.DARK)  # or LIGHT
```

### Icons not showing?

```python
# Disable icons
bar = TokenProgressBar()
print(bar.render(75.5, use_icons=False))
```

### Terminal doesn't support colors?

```python
# Use classic theme for basic compatibility
set_theme(ThemeType.CLASSIC)
```

## Next Steps

- Read full documentation: [THEME_SYSTEM.md](../THEME_SYSTEM.md)
- Run tests: `pytest tests/test_themes.py -v`
- Explore API: See docstrings in `ui/themes.py`

## Need Help?

- Check theme info: `python -m genai_code_usage_monitor.ui.theme_switcher --show`
- View accessibility details: `python -m genai_code_usage_monitor.ui.theme_switcher --accessibility`
- Run demo: `python examples/theme_demo.py`

---

**That's it!** The theme system works automatically in most cases. Just import and use. 🎨
