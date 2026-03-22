# Gloss

✨ Convert Markdown files into beautiful, editorial-style HTML pages.



![](https://raw.githubusercontent.com/devanshbatham/gloss/refs/heads/main/static/demo-c.png)


![](https://raw.githubusercontent.com/devanshbatham/gloss/refs/heads/main/static/demo-a.png)


![](https://raw.githubusercontent.com/devanshbatham/gloss/refs/heads/main/static/demo-b.png)


## Features

- **Editorial aesthetic**: with serif typography, drop caps, and crosshair section accents
- **8 themes**: Light, Dark, Sepia, Nord, Dracula, Green, Rose, Ocean
- **Zen mode**: for distraction-free reading
- **Table of contents**: sidebar with hover previews
- **Text highlighting**: select text, click the marker to highlight. Persists across refreshes.
- **Syntax highlighting**: via highlight.js
- **KaTeX**: math rendering
- **Mermaid**: diagram support
- **Image lightbox** — click images to zoom
- Hover effects on code blocks, tables, and diagrams
- Smooth theme transitions
- Fully self-contained single HTML file output

## Install

### Global install (recommended)

Install `gloss` as a global CLI tool using [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/devansh/gloss
```

Or from a local clone:

```bash
git clone https://github.com/devansh/gloss.git
cd gloss
uv tool install .
```

This puts `gloss` on your PATH (`~/.local/bin/gloss`) so you can use it from anywhere.

### Project-local install

```bash
uv pip install .
```

## Usage

```bash
gloss input.md                  # outputs input.html
gloss input.md output.html      # custom output path
```

### Standalone (no install)

Run the single file directly:

```bash
python3 gloss.py input.md [output.html]
```

## Using as a Library

Install gloss into your project:

```bash
uv pip install git+https://github.com/devansh/gloss
```

Convert a markdown string to a self-contained HTML string:

```python
import gloss

html = gloss.render("# Hello World\n\nThis is **gloss**.")
# html is a complete, self-contained HTML page string

# Write it yourself, serve it, embed it — whatever you need
with open("output.html", "w") as f:
    f.write(html)
```


Convert a markdown file to an HTML file and return the HTML:

```python
import gloss

# Writes to report.html, returns the HTML string
html = gloss.convert("report.md", "report.html")

# output_path is optional — defaults to replacing .md with .html
html = gloss.convert("report.md")  # writes report.html
```

## Try It

The repo includes `test_all_features.md`, a comprehensive markdown file that exercises all supported features (headings, code blocks, math, mermaid diagrams, tables, images, blockquotes, etc.). Use it to see what gloss produces:

```bash
gloss test_all_features.md
open test_all_features.html
```

Or via the library:

```python
import gloss

html = gloss.convert("test_all_features.md")
```

Or via the standalone single file (no install needed):

```bash
python3 gloss.py test_all_features.md
open test_all_features.html
```
