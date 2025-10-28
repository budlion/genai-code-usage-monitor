# 📸 Screenshot Guide

## How to Generate Project Screenshots

This guide helps you create high-quality screenshots for the GenAI Code Usage Monitor project.

### 🎯 Prerequisites

1. **Install the tool**:
   ```bash
   pip install -e .
   ```

2. **Set up API keys**:
   ```bash
   export OPENAI_API_KEY="your-key"
   # or
   export ANTHROPIC_API_KEY="your-key"
   ```

### 📷 Taking Screenshots

#### Method 1: Using macOS Screenshot Tool

```bash
# Take a timed screenshot (5 seconds delay)
screencapture -T 5 docs/screenshots/screenshot.png

# Take interactive window screenshot
screencapture -w docs/screenshots/window.png
```

#### Method 2: Using Terminal Recording Tools

For animated demos, use tools like:
- **asciinema**: Record terminal sessions
- **terminalizer**: Create animated GIF
- **vhs**: Generate terminal GIFs from scripts

### 🎨 Screenshot Scenarios

#### 1. Dark Theme - Real-time Monitoring

```bash
# Start monitor with dark theme
code-monitor --theme dark --platform codex

# Wait for data to display, then capture screenshot
screencapture -w docs/screenshots/dark-theme-realtime.png
```

**Key features to show**:
- Real-time token usage
- Cost tracking
- Progress bars
- Alert levels

#### 2. Light Theme - Daily View

```bash
# Start monitor with light theme
code-monitor --theme light --view daily

# Capture screenshot
screencapture -w docs/screenshots/light-theme-daily.png
```

**Key features to show**:
- Daily aggregated statistics
- Table view
- Cost breakdown

#### 3. Classic Theme - Compact View

```bash
# Start monitor with classic theme
code-monitor --theme classic --view compact

# Capture screenshot
screencapture -w docs/screenshots/classic-theme-compact.png
```

**Key features to show**:
- Compact layout
- Essential metrics
- Classic terminal colors

#### 4. Dual Platform - Split Screen

```bash
# Start monitor with both platforms
code-monitor --platform both

# Capture screenshot
screencapture -w docs/screenshots/dual-platform.png
```

**Key features to show**:
- Side-by-side display
- Platform comparison
- Different metrics (cache for Claude)

### 📐 Screenshot Specifications

#### Image Requirements

| Property | Value |
|----------|-------|
| Format | PNG (preferred) or JPEG |
| Width | 800-1200px (recommended) |
| Aspect Ratio | 16:9 or 4:3 |
| Background | Clean terminal background |
| Content | Show meaningful data (not empty) |

#### Best Practices

1. **Terminal Size**: Set to standard size (e.g., 120x40 characters)
   ```bash
   # Resize terminal
   printf '\e[8;40;120t'
   ```

2. **Font**: Use a clear monospace font
   - JetBrains Mono
   - Fira Code
   - SF Mono

3. **Timing**: Let the monitor run for a few seconds to show real data

4. **Cleanup**: Remove sensitive information (API keys, real usage data if needed)

### 🎬 Creating Demo GIFs

#### Using terminalizer

```bash
# Install terminalizer
npm install -g terminalizer

# Record session
terminalizer record demo

# Edit config if needed
terminalizer config demo

# Render GIF
terminalizer render demo -o docs/screenshots/demo.gif
```

#### Using asciinema + agg

```bash
# Install asciinema
brew install asciinema

# Install agg for GIF conversion
cargo install --git https://github.com/asciinema/agg

# Record session
asciinema rec session.cast

# Convert to GIF
agg session.cast docs/screenshots/demo.gif
```

### 🖼️ Screenshot Naming Convention

Use descriptive names following this pattern:

```
<theme>-<view>-<feature>.png
```

Examples:
- `dark-theme-realtime.png`
- `light-theme-daily-table.png`
- `classic-theme-alerts.png`
- `dual-platform-split-screen.png`
- `demo-quick-start.gif`

### 📝 Screenshot Checklist

Before submitting screenshots:

- [ ] Terminal size is appropriate (120x40 or similar)
- [ ] Font is clear and readable
- [ ] Colors are accurate and WCAG compliant
- [ ] No sensitive information visible
- [ ] Image is properly compressed (< 500KB)
- [ ] Filename follows naming convention
- [ ] Image shows meaningful data/features
- [ ] Background is clean

### 🔄 Updating Screenshots

When updating screenshots:

1. Delete old screenshot
2. Generate new screenshot with same name
3. Update README references if needed
4. Commit changes

### 📤 Submitting Screenshots

```bash
# Add screenshots to git
git add docs/screenshots/*.png

# Commit
git commit -m "docs: Add/update screenshots"

# Push
git push origin main
```

### 🎨 Optional: Creating Mockups

For marketing materials, consider:

1. **Using design tools**:
   - Figma
   - Sketch
   - Canva

2. **Adding device frames**:
   - https://shots.so/ - Beautiful browser frames
   - https://www.screely.com/ - Clean screenshot editor

3. **Creating comparison views**:
   - Side-by-side screenshots
   - Before/after comparisons
   - Feature highlights

### 📚 Additional Resources

- [asciinema documentation](https://asciinema.org/)
- [terminalizer documentation](https://terminalizer.com/)
- [Screenshot best practices](https://github.com/sindresorhus/guides/blob/main/how-to-take-good-screenshots.md)

---

**Need help?** Open an issue at https://github.com/budlion/genai-code-usage-monitor/issues
