#!/usr/bin/env python3
"""
gloss - Convert Markdown to beautiful, editorial-style HTML pages.

Usage:
    gloss input.md [output.html]
"""

import sys
import base64
import os


TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Editorial Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/iosevka@5/400.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/iosevka@5/500.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/iosevka@5/600.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/iosevka@5/700.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/mocha.min.css" id="hljs-theme">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.1/marked.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  :root {
    --bg: #faf8f4;
    --text: #2c2c2c;
    --text-light: #555;
    --accent: #b08d57;
    --link: #4a6fa5;
    --border: #d4c5a9;
    --code-bg: #f0ebe0;
    --code-block-bg: #2c2c2c;
    --code-block-text: #e8e0d0;
    --blockquote-border: #b08d57;
    --blockquote-bg: #f5f0e8;
    --table-header-bg: #f0ebe0;
    --table-border: #d4c5a9;
    --toast-bg: #2c2c2c;
    --toast-fg: #faf8f4;
    --toc-width: 260px;
    --toc-bg: #f5f1ea;
    --toc-preview-bg: #fff;
    --toc-preview-fade: #fff;
    --toolbar-bg: rgba(250,248,244,0.95);
    --sel-bg: rgba(220, 50, 50, 0.35);
    --hl-bg: rgba(220, 50, 50, 0.45);
    --hl-bg-hover: rgba(220, 50, 50, 0.65);
    --hl-tick: rgba(220, 50, 50, 0.6);
    --hl-tick-hover: rgba(220, 50, 50, 1);
  }

  [data-theme="dark"] {
    --bg: #002b36;
    --text: #839496;
    --text-light: #657b83;
    --accent: #b58900;
    --link: #268bd2;
    --border: #073642;
    --code-bg: #073642;
    --code-block-bg: #00212b;
    --code-block-text: #93a1a1;
    --blockquote-border: #b58900;
    --blockquote-bg: #073642;
    --table-header-bg: #073642;
    --table-border: #073642;
    --toast-bg: #eee8d5;
    --toast-fg: #002b36;
    --toc-bg: #00212b;
    --toc-preview-bg: #073642;
    --toc-preview-fade: #073642;
    --toolbar-bg: rgba(0,43,54,0.95);
    --sel-bg: rgba(38, 139, 210, 0.4);
    --hl-bg: rgba(38, 139, 210, 0.5);
    --hl-bg-hover: rgba(38, 139, 210, 0.7);
    --hl-tick: rgba(38, 139, 210, 0.6);
    --hl-tick-hover: rgba(38, 139, 210, 1);
  }

  [data-theme="sepia"] {
    --bg: #f4ecd8;
    --text: #3b2e1a;
    --text-light: #6b5a42;
    --accent: #8b6914;
    --link: #5a7a3a;
    --border: #c8b896;
    --code-bg: #e8dcc4;
    --code-block-bg: #2e2418;
    --code-block-text: #e8dcc4;
    --blockquote-border: #8b6914;
    --blockquote-bg: #ede3c8;
    --table-header-bg: #e8dcc4;
    --table-border: #c8b896;
    --toast-bg: #3b2e1a;
    --toast-fg: #f4ecd8;
    --toc-bg: #ebe0c8;
    --toc-preview-bg: #f4ecd8;
    --toc-preview-fade: #f4ecd8;
    --toolbar-bg: rgba(244,236,216,0.95);
    --sel-bg: rgba(139, 105, 20, 0.35);
    --hl-bg: rgba(139, 105, 20, 0.45);
    --hl-bg-hover: rgba(139, 105, 20, 0.65);
    --hl-tick: rgba(139, 105, 20, 0.6);
    --hl-tick-hover: rgba(139, 105, 20, 1);
  }

  [data-theme="nord"] {
    --bg: #2e3440;
    --text: #d8dee9;
    --text-light: #9aa5b4;
    --accent: #88c0d0;
    --link: #81a1c1;
    --border: #3b4252;
    --code-bg: #3b4252;
    --code-block-bg: #242933;
    --code-block-text: #d8dee9;
    --blockquote-border: #88c0d0;
    --blockquote-bg: #3b4252;
    --table-header-bg: #3b4252;
    --table-border: #434c5e;
    --toast-bg: #eceff4;
    --toast-fg: #2e3440;
    --toc-bg: #292e39;
    --toc-preview-bg: #3b4252;
    --toc-preview-fade: #3b4252;
    --toolbar-bg: rgba(46,52,64,0.95);
    --sel-bg: rgba(136, 192, 208, 0.35);
    --hl-bg: rgba(136, 192, 208, 0.45);
    --hl-bg-hover: rgba(136, 192, 208, 0.65);
    --hl-tick: rgba(136, 192, 208, 0.6);
    --hl-tick-hover: rgba(136, 192, 208, 1);
  }

  [data-theme="dracula"] {
    --bg: #282a36;
    --text: #f8f8f2;
    --text-light: #9a9caa;
    --accent: #bd93f9;
    --link: #8be9fd;
    --border: #44475a;
    --code-bg: #44475a;
    --code-block-bg: #1e1f29;
    --code-block-text: #f8f8f2;
    --blockquote-border: #bd93f9;
    --blockquote-bg: #343746;
    --table-header-bg: #44475a;
    --table-border: #44475a;
    --toast-bg: #f8f8f2;
    --toast-fg: #282a36;
    --toc-bg: #21222c;
    --toc-preview-bg: #343746;
    --toc-preview-fade: #343746;
    --toolbar-bg: rgba(40,42,54,0.95);
    --sel-bg: rgba(189, 147, 249, 0.35);
    --hl-bg: rgba(189, 147, 249, 0.45);
    --hl-bg-hover: rgba(189, 147, 249, 0.65);
    --hl-tick: rgba(189, 147, 249, 0.6);
    --hl-tick-hover: rgba(189, 147, 249, 1);
  }

  [data-theme="green"] {
    --bg: #f0f5f0;
    --text: #1a2e1a;
    --text-light: #4a6a4a;
    --accent: #2d8a4e;
    --link: #1a6b3a;
    --border: #b8d4b8;
    --code-bg: #dceadc;
    --code-block-bg: #1a2e1a;
    --code-block-text: #d0e8d0;
    --blockquote-border: #2d8a4e;
    --blockquote-bg: #e4f0e4;
    --table-header-bg: #dceadc;
    --table-border: #b8d4b8;
    --toast-bg: #1a2e1a;
    --toast-fg: #f0f5f0;
    --toc-bg: #e6f0e6;
    --toc-preview-bg: #f0f5f0;
    --toc-preview-fade: #f0f5f0;
    --toolbar-bg: rgba(240,245,240,0.95);
    --sel-bg: rgba(45, 138, 78, 0.3);
    --hl-bg: rgba(45, 138, 78, 0.4);
    --hl-bg-hover: rgba(45, 138, 78, 0.6);
    --hl-tick: rgba(45, 138, 78, 0.6);
    --hl-tick-hover: rgba(45, 138, 78, 1);
  }

  [data-theme="rose"] {
    --bg: #1e1218;
    --text: #e8d0d8;
    --text-light: #a08890;
    --accent: #d4748a;
    --link: #e8a0b0;
    --border: #3a2430;
    --code-bg: #2a1a22;
    --code-block-bg: #160e14;
    --code-block-text: #e0c8d0;
    --blockquote-border: #d4748a;
    --blockquote-bg: #2a1a22;
    --table-header-bg: #2a1a22;
    --table-border: #3a2430;
    --toast-bg: #e8d0d8;
    --toast-fg: #1e1218;
    --toc-bg: #1a1016;
    --toc-preview-bg: #2a1a22;
    --toc-preview-fade: #2a1a22;
    --toolbar-bg: rgba(30,18,24,0.95);
    --sel-bg: rgba(212, 116, 138, 0.35);
    --hl-bg: rgba(212, 116, 138, 0.45);
    --hl-bg-hover: rgba(212, 116, 138, 0.65);
    --hl-tick: rgba(212, 116, 138, 0.6);
    --hl-tick-hover: rgba(212, 116, 138, 1);
  }

  [data-theme="ocean"] {
    --bg: #0f1b2d;
    --text: #c8dce8;
    --text-light: #7a9ab8;
    --accent: #4a9fd4;
    --link: #68b8e8;
    --border: #1a2e48;
    --code-bg: #162440;
    --code-block-bg: #0a1420;
    --code-block-text: #b8d0e0;
    --blockquote-border: #4a9fd4;
    --blockquote-bg: #132238;
    --table-header-bg: #162440;
    --table-border: #1a2e48;
    --toast-bg: #c8dce8;
    --toast-fg: #0f1b2d;
    --toc-bg: #0c1826;
    --toc-preview-bg: #162440;
    --toc-preview-fade: #162440;
    --toolbar-bg: rgba(15,27,45,0.95);
    --sel-bg: rgba(74, 159, 212, 0.35);
    --hl-bg: rgba(74, 159, 212, 0.45);
    --hl-bg-hover: rgba(74, 159, 212, 0.65);
    --hl-tick: rgba(74, 159, 212, 0.6);
    --hl-tick-hover: rgba(74, 159, 212, 1);
  }

  ::selection {
    background-color: var(--sel-bg);
    color: inherit;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Source Serif 4', 'Spectral', 'Georgia', serif;
    font-size: 18px;
    line-height: 1.85;
    color: var(--text);
    background-color: var(--bg);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    transition: background-color 0.6s ease, color 0.6s ease;
  }


  /* Smooth transitions on themed elements */
  .toc-sidebar,
  .editorial-body pre,
  .editorial-body blockquote,
  .editorial-body table,
  .editorial-body th,
  .editorial-body td,
  .editorial-body code,
  .mermaid-wrapper,
  .toolbar-btn,
  .toc-list span,
  .toast,
  .editorial-title,
  .editorial-body h2,
  .editorial-body h3,
  .editorial-body h4,
  .editorial-body a,
  .editorial-body hr,
  .header-divider {
    transition: background-color 0.6s ease, color 0.6s ease, border-color 0.6s ease;
  }

  /* ---- Layout: TOC sidebar + main content ---- */
  .page-layout {
    display: flex;
    min-height: 100vh;
  }

  /* TOC Sidebar */
  .toc-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--toc-width);
    height: 100vh;
    overflow-y: auto;
    background: var(--toc-bg);
    border-right: 1px solid var(--border);
    padding: 32px 20px 40px;
    z-index: 50;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
    transition: left 0.3s ease, background-color 0.3s ease;
  }
  .toc-sidebar.collapsed {
    left: calc(-1 * var(--toc-width));
  }
  .toc-sidebar::-webkit-scrollbar { width: 5px; }
  .toc-sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  .toc-heading {
    font-family: 'Cormorant Garamond', 'Georgia', serif;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--accent);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }

  .toc-list { list-style: none; }
  .toc-list li { margin-bottom: 2px; }

  .toc-list span {
    display: block;
    padding: 5px 10px;
    font-family: 'Source Serif 4', 'Georgia', serif;
    font-size: 0.82rem;
    line-height: 1.4;
    color: var(--text-light);
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.2s ease;
    border-left: 2px solid transparent;
    cursor: pointer;
  }
  .toc-list span:hover {
    background: rgba(176,141,87,0.1);
    color: var(--text);
    border-left-color: var(--accent);
  }
  .toc-list span.active {
    background: rgba(176,141,87,0.15);
    color: var(--text);
    font-weight: 600;
    border-left-color: var(--accent);
  }

  .toc-list .toc-h3 { padding-left: 24px; font-size: 0.78rem; }
  .toc-list .toc-h4 { padding-left: 38px; font-size: 0.74rem; }

  /* Hover preview tooltip */
  .toc-preview {
    position: fixed;
    left: calc(var(--toc-width) + 8px);
    width: 400px;
    max-height: 70vh;
    overflow-y: auto;
    background: var(--toc-preview-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    padding: 16px 20px;
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text);
    pointer-events: none;
    opacity: 0;
    transform: translateY(4px);
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 100;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .toc-preview::-webkit-scrollbar { width: 4px; }
  .toc-preview::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  .toc-preview.visible {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }
  .toc-preview h2, .toc-preview h3, .toc-preview h4 {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text);
  }
  .toc-preview p { margin-bottom: 0.6em; text-align: left; }
  .toc-preview img {
    max-width: 100%;
    max-height: 120px;
    width: auto;
    height: auto;
    border-radius: 3px;
    margin: 0.5em auto;
    box-shadow: none;
    transform: none !important;
    display: block;
    object-fit: contain;
  }
  .toc-preview blockquote {
    margin: 0.5em 0;
    padding: 0.5em 0.8em;
    border-left: 3px solid var(--blockquote-border);
    background: var(--blockquote-bg);
    border-radius: 0 3px 3px 0;
    font-style: italic;
    font-size: 0.82rem;
    color: var(--text);
  }
  .toc-preview blockquote p { margin-bottom: 0.3em; }
  .toc-preview blockquote p:last-child { margin-bottom: 0; }
  .toc-preview ul, .toc-preview ol {
    margin: 0.4em 0;
    padding-left: 1.4em;
    font-size: 0.82rem;
  }
  .toc-preview li { margin-bottom: 0.2em; }
  .toc-preview table {
    width: 100%;
    font-size: 0.75rem;
    border-collapse: collapse;
    margin: 0.5em 0;
  }
  .toc-preview th, .toc-preview td {
    padding: 3px 6px;
    border: 1px solid var(--border);
    text-align: left;
  }
  .toc-preview hr {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 0.8em auto;
    max-width: 80px;
  }
  .toc-preview .mermaid-wrapper {
    max-height: none;
    overflow: visible;
    padding: 8px;
    margin: 0.5em 0;
    border: 1px solid var(--border);
    border-radius: 4px;
    cursor: default;
    transform: none !important;
    box-shadow: none !important;
  }
  .toc-preview .mermaid-wrapper svg {
    max-width: 100%;
    height: auto;
  }
  .toc-preview .corner-section {
    padding: 0;
    margin: 0;
  }
  .toc-preview .crosshair { display: none; }
  .toc-preview pre {
    font-size: 12px;
    background: var(--code-block-bg);
    color: var(--code-block-text);
    padding: 8px 10px;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
  }
  .toc-preview pre .copy-code-btn { display: none; }
  .toc-preview pre .code-lang { display: none; }
  .toc-preview code {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 0.85em;
  }

  /* Main content area */
  .main-content {
    margin-left: var(--toc-width);
    flex: 1;
    padding: 60px 24px 80px;
    transition: margin-left 0.3s ease;
  }
  .main-content.expanded {
    margin-left: 0;
  }

  /* Container */
  .editorial-body { max-width: 700px; margin: 0 auto; }

  /* Title */
  .editorial-title {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 2.4rem;
    font-weight: 600;
    text-align: center;
    color: var(--text);
    margin-bottom: 8px;
    line-height: 1.3;
  }

  .editorial-meta {
    text-align: center;
    font-style: italic;
    color: var(--text-light);
    font-size: 0.95rem;
    margin-bottom: 0;
  }

  .header-divider {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 32px auto;
    max-width: 200px;
  }

  /* Section headings */
  .editorial-body h2 {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--text);
    margin-top: 2.5em;
    margin-bottom: 0.8em;
    letter-spacing: -0.01em;
    scroll-margin-top: 24px;
  }
  .editorial-body h3 {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
    margin-top: 2em;
    margin-bottom: 0.6em;
    scroll-margin-top: 24px;
  }
  .editorial-body h4 {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 1.8em;
    margin-bottom: 0.5em;
    scroll-margin-top: 24px;
  }

  /* Paragraphs */
  .editorial-body p {
    margin-bottom: 1.2em;
    text-align: justify;
    hyphens: none;
    -webkit-hyphens: none;
    overflow-wrap: normal;
    word-break: normal;
  }

  /* Drop cap */
  .editorial-body .drop-cap::first-letter {
    float: left;
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 3.8em;
    line-height: 0.8;
    padding-right: 8px;
    padding-top: 6px;
    color: var(--accent);
    font-weight: 700;
  }

  /* Lists */
  .editorial-body ul, .editorial-body ol {
    margin-bottom: 1.2em;
    padding-left: 1.6em;
  }
  .editorial-body li {
    margin-bottom: 0.4em;
    text-align: justify;
    hyphens: none;
    -webkit-hyphens: none;
    overflow-wrap: normal;
    word-break: normal;
  }
  .editorial-body li > p { margin-bottom: 0.5em; }

  /* Blockquote */
  .editorial-body blockquote {
    margin: 1.5em 0;
    padding: 1em 1.4em;
    border-left: 4px solid var(--blockquote-border);
    background: var(--blockquote-bg);
    border-radius: 0 4px 4px 0;
    font-style: italic;
    color: var(--text);
  }
  .editorial-body blockquote p:last-child { margin-bottom: 0; }

  /* Inline code */
  .editorial-body code {
    padding: 0.15em 0.4em;
    font-size: 0.85em;
    background-color: var(--code-bg);
    border-radius: 3px;
    font-family: 'Iosevka', 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    color: var(--text);
  }

  /* Code blocks */
  .editorial-body pre {
    padding: 20px 24px;
    overflow-x: auto;
    font-size: 14px;
    line-height: 1.55;
    background-color: var(--code-block-bg);
    border-radius: 6px;
    margin: 1.5em 0;
    position: relative;
    transition: box-shadow 0.3s ease;
  }
  .editorial-body pre:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.12), 0 20px 40px -10px var(--hl-bg);
    outline: 1px solid var(--accent);
    outline-offset: 2px;
  }
  .editorial-body pre code {
    padding: 0;
    background-color: transparent;
    border: none;
    color: var(--code-block-text);
    font-size: 100%;
    white-space: pre;
  }

  /* Code block language label */
  .editorial-body pre .code-lang {
    position: absolute;
    top: 8px;
    right: 12px;
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    user-select: none;
  }

  /* Code block copy button */
  .editorial-body pre .copy-code-btn {
    position: absolute;
    bottom: 8px;
    right: 10px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #888;
    padding: 3px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 11px;
    opacity: 0;
    transition: opacity 0.2s ease, background 0.2s ease;
    z-index: 5;
    user-select: none;
  }
  .editorial-body pre:hover .copy-code-btn { opacity: 1; }
  .editorial-body pre .copy-code-btn:hover {
    background: rgba(255,255,255,0.16);
    color: #ccc;
  }
  .editorial-body pre .copy-code-btn.copied {
    color: #5a8;
    border-color: #5a8;
  }

  /* Mermaid diagrams */
  .mermaid-wrapper {
    margin: 1.5em 0;
    text-align: center;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 20px;
    overflow-x: auto;
    cursor: default;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
  }
  .mermaid-wrapper:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.12), 0 20px 40px -10px var(--hl-bg);
    border-color: var(--accent);
  }
  .mermaid-wrapper * {
    pointer-events: none !important;
    cursor: default !important;
  }

  /* Horizontal rule */
  .editorial-body hr {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 2.5em auto;
    max-width: 200px;
  }

  /* Tables */
  .editorial-body table {
    border-collapse: collapse;
    margin: 1.5em 0;
    width: 100%;
    font-size: 0.92em;
    transition: box-shadow 0.3s ease;
  }
  .editorial-body table:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.12), 0 20px 40px -10px var(--hl-bg);
    outline: 1px solid var(--accent);
    outline-offset: 2px;
  }
  .editorial-body th, .editorial-body td {
    padding: 10px 14px;
    border: 1px solid var(--table-border);
    text-align: left;
  }
  .editorial-body th {
    font-weight: 700;
    background-color: var(--table-header-bg);
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
  }
  .editorial-body tr:nth-child(2n) {
    background-color: rgba(212,197,169,0.1);
  }

  .editorial-body strong { font-weight: 700; }

  .editorial-body a {
    color: var(--link);
    text-decoration: underline;
    text-decoration-color: rgba(74,111,165,0.3);
    text-underline-offset: 2px;
    transition: text-decoration-color 0.2s;
  }
  .editorial-body a:hover { text-decoration-color: var(--link); }

  .editorial-body img {
    max-width: 100%;
    border-radius: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    display: block;
    margin: 1.5em auto;
    cursor: zoom-in;
    transition: box-shadow 0.3s ease;
  }
  .editorial-body img:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.15), 0 20px 40px -10px var(--hl-bg);
    outline: 1px solid var(--accent);
    outline-offset: 2px;
  }

  /* Image lightbox overlay */
  .img-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.85);
    z-index: 200;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: zoom-out;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }
  .img-overlay.visible {
    opacity: 1;
    pointer-events: auto;
  }
  .img-overlay img {
    max-width: 90vw;
    max-height: 90vh;
    border-radius: 6px;
    box-shadow: 0 12px 60px rgba(0,0,0,0.5);
    transform: scale(0.92);
    transition: transform 0.3s ease;
  }
  .img-overlay.visible img {
    transform: scale(1);
  }

  /* Crosshair-accented section frames */
  .corner-section {
    position: relative;
    padding: 48px 36px;
    margin: 3.5em 0;
  }
  .corner-section > h2:first-child {
    margin-top: 0;
  }

  /* Crosshair: two thin perpendicular lines extending beyond intersection */
  .crosshair {
    position: absolute;
    pointer-events: none;
  }
  /* Horizontal stroke (longer side) */
  .crosshair::before {
    content: '';
    position: absolute;
    width: 120px;
    height: 0;
    border-top: 1px solid var(--text);
    opacity: 0.18;
    transition: opacity 0.4s ease, width 0.4s ease;
  }
  /* Vertical stroke (shorter side) */
  .crosshair::after {
    content: '';
    position: absolute;
    height: 100px;
    width: 0;
    border-left: 1px solid var(--text);
    opacity: 0.18;
    transition: opacity 0.4s ease, height 0.4s ease;
  }

  /* Top-left crosshair */
  .crosshair-tl {
    top: 12px;
    left: 4px;
  }
  .crosshair-tl::before {
    top: 0;
    left: -14px;
  }
  .crosshair-tl::after {
    left: 0;
    top: -14px;
  }

  /* Bottom-right crosshair */
  .crosshair-br {
    bottom: 12px;
    right: 4px;
  }
  .crosshair-br::before {
    top: 0;
    right: -14px;
  }
  .crosshair-br::after {
    right: 0;
    bottom: -14px;
  }

  .corner-section:hover .crosshair::before {
    opacity: 0.4;
    width: 150px;
  }
  .corner-section:hover .crosshair::after {
    opacity: 0.4;
    height: 120px;
  }

  .editorial-end {
    text-align: center;
    color: var(--accent);
    font-size: 1.4rem;
    margin-top: 3em;
    letter-spacing: 0.3em;
  }

  .toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--toast-bg);
    color: var(--toast-fg);
    padding: 10px 20px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14px;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
    pointer-events: none;
    z-index: 100;
  }
  .toast.show { opacity: 1; transform: translateY(0); }

  /* ---- Toolbar (top-right floating) ---- */
  .toolbar {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 60;
    display: flex;
    gap: 8px;
  }
  .toolbar-btn {
    width: 40px;
    height: 40px;
    background: var(--toolbar-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--accent);
    font-size: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    line-height: 1;
  }
  .toolbar-btn:hover {
    background: var(--border);
    color: var(--text);
  }
  .toolbar-btn svg {
    width: 20px;
    height: 20px;
    fill: currentColor;
  }

  /* ---- Zen Mode ---- */
  body.zen-mode .toc-sidebar { left: calc(-1 * var(--toc-width)); }
  body.zen-mode .main-content { margin-left: 0; }

  body.zen-mode .toolbar {
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  body.zen-mode:hover .toolbar {
    opacity: 1;
  }
  body.zen-mode .editorial-body {
    max-width: 750px;
  }

  /* ---- Text Highlight Feature ---- */
  .highlight-marker {
    position: fixed;
    z-index: 150;
    width: 36px;
    height: 36px;
    background: var(--toolbar-bg);
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 3px 12px rgba(0,0,0,0.15);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    pointer-events: auto;
  }
  .highlight-marker:hover {
    transform: scale(1.15);
    box-shadow: 0 4px 16px rgba(0,0,0,0.22);
  }
  .highlight-marker svg {
    width: 20px;
    height: 20px;
    fill: var(--accent);
  }

  mark.user-highlight {
    background-color: var(--hl-bg);
    color: inherit;
    padding: 0;
    border-radius: 2px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  mark.user-highlight:hover {
    background-color: var(--hl-bg-hover);
  }

  /* Highlight position markers on right edge */
  .hl-markers {
    position: fixed;
    top: 180px;
    bottom: 32px;
    right: 70px;
    width: 18px;
    z-index: 55;
    pointer-events: none;
  }
  .hl-markers .hl-tick {
    position: absolute;
    right: 0;
    width: 22px;
    height: 5px;
    background: var(--hl-tick);
    border-radius: 2px;
    cursor: pointer;
    pointer-events: auto;
    transition: background 0.2s ease, transform 0.2s ease;
  }
  .hl-tick:hover {
    background: var(--hl-tick-hover);
    transform: scaleX(1.5);
  }

  /* Highlight hover preview */
  .hl-preview {
    position: fixed;
    right: 100px;
    width: 360px;
    max-height: 50vh;
    overflow-y: auto;
    background: var(--toc-preview-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    padding: 14px 18px;
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text);
    pointer-events: none;
    opacity: 0;
    transform: translateX(4px);
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 100;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .hl-preview.visible {
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }
  .hl-preview .hl-preview-text {
    background: var(--hl-bg);
    border-radius: 2px;
    padding: 0 2px;
  }
  .hl-preview p { margin-bottom: 0.5em; text-align: left; }
  .hl-preview blockquote {
    margin: 0.5em 0;
    padding: 0.4em 0.8em;
    border-left: 3px solid var(--blockquote-border);
    background: var(--blockquote-bg);
    border-radius: 0 3px 3px 0;
    font-style: italic;
    font-size: 0.82rem;
  }
  .hl-preview ul, .hl-preview ol {
    margin: 0.4em 0;
    padding-left: 1.4em;
    font-size: 0.82rem;
  }
  .hl-preview pre {
    font-size: 12px;
    background: var(--code-block-bg);
    color: var(--code-block-text);
    padding: 8px 10px;
    border-radius: 4px;
    overflow: hidden;
  }
  .hl-preview code {
    font-family: 'Iosevka', 'JetBrains Mono', monospace;
    font-size: 0.85em;
  }
  .hl-preview img {
    max-width: 100%;
    max-height: 120px;
    width: auto;
    height: auto;
    border-radius: 3px;
    margin: 0.5em auto;
    box-shadow: none;
    transform: none !important;
    display: block;
    object-fit: contain;
  }

  /* Responsive: collapse TOC on small screens */
  @media (max-width: 900px) {
    .toc-sidebar {
      left: calc(-1 * var(--toc-width));
      box-shadow: 4px 0 24px rgba(0,0,0,0.15);
    }
    .toc-sidebar.mobile-open { left: 0; }
    .main-content { margin-left: 0; }
    .main-content.expanded { margin-left: 0; }
  }
</style>
</head>
<body>

<!-- Toolbar (top-right) -->
<div class="toolbar">
  <button class="toolbar-btn" id="themeToggle" aria-label="Toggle theme" title="Switch theme">
    <svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>
  </button>
  <button class="toolbar-btn" id="zenToggle" aria-label="Toggle zen mode" title="Zen mode">
    <svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
  </button>
  <button class="toolbar-btn" id="clearHighlights" aria-label="Clear all highlights" title="Clear all highlights">
    <svg viewBox="0 0 24 24" style="fill:currentColor"><path d="M7 14l5-5 5 5z"/><rect x="9" y="14" width="6" height="4" rx="1"/><line x1="4" y1="4" x2="20" y2="20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  </button>
</div>

<!-- TOC Sidebar -->
<nav class="toc-sidebar" id="tocSidebar">
  <div class="toc-heading">Contents</div>
  <ul class="toc-list" id="tocList"></ul>
</nav>

<!-- Hover preview tooltip -->
<div class="toc-preview" id="tocPreview"></div>

<div class="page-layout">
  <div class="main-content" id="mainContent">
    <div class="editorial-body" id="content"></div>
  </div>
</div>

<div id="toast" class="toast"></div>
<div class="hl-markers" id="hlMarkers"></div>
<div class="hl-preview" id="hlPreview"></div>
<div class="img-overlay" id="imgOverlay"><img id="imgOverlayImg" src="" alt=""></div>

<script>
const MD_B64 = "__MD_B64__";
const RAW_MD = new TextDecoder().decode(Uint8Array.from(atob(MD_B64), c => c.charCodeAt(0)));

marked.setOptions({
  gfm: true,
  breaks: true
});

// Protect math expressions from marked's escaping/processing.
// Extract $$ blocks, inline $, \[...\], \(...\) before parsing, restore after.
var mathStore = [];
function stashMath(text) {
  // Display math: $$ ... $$ (multiline)
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, function(m) {
    mathStore.push(m);
    return '\x00MATH' + (mathStore.length - 1) + 'MATH\x00';
  });
  // Display math: \[ ... \]
  text = text.replace(/\\\[([\s\S]*?)\\\]/g, function(m) {
    mathStore.push(m);
    return '\x00MATH' + (mathStore.length - 1) + 'MATH\x00';
  });
  // Inline math: \( ... \)
  text = text.replace(/\\\((.*?)\\\)/g, function(m) {
    mathStore.push(m);
    return '\x00MATH' + (mathStore.length - 1) + 'MATH\x00';
  });
  // Inline math: $ ... $ (single line, not $$)
  text = text.replace(/(?<!\$)\$(?!\$)([^\n$]+?)\$(?!\$)/g, function(m) {
    mathStore.push(m);
    return '\x00MATH' + (mathStore.length - 1) + 'MATH\x00';
  });
  return text;
}
function unstashMath(text) {
  return text.replace(/\x00MATH(\d+)MATH\x00/g, function(m, idx) {
    return mathStore[parseInt(idx)];
  });
}

var processedMd = stashMath(RAW_MD);
let html = unstashMath(marked.parse(processedMd));
const container = document.getElementById('content');

// Extract first h1 as title
const titleMatch = html.match(/<h1[^>]*>(.*?)<\/h1>/);
let titleText = 'Untitled';
if (titleMatch) {
  titleText = titleMatch[1];
  html = html.replace(titleMatch[0], '');
}

// Inject IDs into h2/h3/h4 tags in the HTML string BEFORE DOM insertion.
// This guarantees every section heading has a proper id attribute baked in.
var tocEntries = [];
var sectionCounter = 0;
html = html.replace(/<(h[2-4])([^>]*)>([\s\S]*?)<\/h[2-4]>/gi, function(match, tag, attrs, inner) {
  var id = 'section-' + sectionCounter;
  var level = parseInt(tag.charAt(1));
  // Strip any HTML tags from inner to get plain text for TOC
  var plainText = inner.replace(/<[^>]*>/g, '').trim();
  tocEntries.push({ id: id, level: level, text: plainText });
  sectionCounter++;
  return '<' + tag + ' id="' + id + '"' + attrs + '>' + inner + '</' + tag + '>';
});

const titleEl = document.createElement('h1');
titleEl.className = 'editorial-title';
titleEl.innerHTML = titleText;

const divider = document.createElement('hr');
divider.className = 'header-divider';

// Insert content into DOM with IDs already in place
container.appendChild(titleEl);
container.appendChild(divider);
const bodyEl = document.createElement('div');
bodyEl.innerHTML = html;
while (bodyEl.firstChild) {
  container.appendChild(bodyEl.firstChild);
}

// Drop cap on first paragraph
const allP = container.querySelectorAll('p');
for (const p of allP) {
  if (!p.closest('blockquote') && p.textContent.trim().length > 0) {
    p.classList.add('drop-cap');
    break;
  }
}

document.title = titleText.replace(/<[^>]*>/g, '');

// External links open in new tab
container.querySelectorAll('a[href]').forEach(a => {
  if (a.hostname !== location.hostname || a.href.startsWith('http')) {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  }
});

// Lightbox helper — shows image only
function openLightbox(mode, content) {
  var overlay = document.getElementById('imgOverlay');
  var overlayImg = document.getElementById('imgOverlayImg');
  overlayImg.src = content;
  overlayImg.style.display = 'block';
  overlay.classList.add('visible');
}

// Block all clicks inside mermaid wrappers
document.addEventListener('click', function(e) {
  if (e.target.closest && e.target.closest('.mermaid-wrapper')) {
    e.stopPropagation();
    e.preventDefault();
  }
}, true);

// Click on image to open lightbox overlay (skip images inside mermaid diagrams)
container.querySelectorAll('img').forEach(function(img) {
  if (img.closest('.mermaid-wrapper')) return;
  img.style.cursor = 'zoom-in';
  img.addEventListener('click', function() {
    openLightbox('img', img.src);
  });
});

// Wrap each h2-level section with crosshair accents
(function() {
  var h2s = Array.from(container.querySelectorAll('h2'));
  h2s.forEach(function(h2) {
    var wrapper = document.createElement('div');
    wrapper.className = 'corner-section';

    var tl = document.createElement('div');
    tl.className = 'crosshair crosshair-tl';
    var br = document.createElement('div');
    br.className = 'crosshair crosshair-br';

    var els = [h2];
    var sib = h2.nextElementSibling;
    while (sib && sib.tagName !== 'H2' && !sib.classList.contains('editorial-end')) {
      els.push(sib);
      sib = sib.nextElementSibling;
    }
    h2.parentNode.insertBefore(wrapper, h2);
    els.forEach(function(el) { wrapper.appendChild(el); });
    wrapper.appendChild(tl);
    wrapper.appendChild(br);
  });
})();

// Closing symbol
const endEl = document.createElement('div');
endEl.className = 'editorial-end';
endEl.innerHTML = '&#10022;';
container.appendChild(endEl);

// ---- Build TOC ----
// Uses <span> (not <a>) to avoid all anchor navigation side-effects.
// Stores direct DOM references in closures — no getElementById at click time.
var tocList = document.getElementById('tocList');
var tocPreview = document.getElementById('tocPreview');
var headingEls = [];
var tocSpans = [];
var previewHideTimer = null;

// Keep preview open when mouse moves into it
tocPreview.addEventListener('mouseenter', function() {
  clearTimeout(previewHideTimer);
});
tocPreview.addEventListener('mouseleave', function() {
  tocPreview.classList.remove('visible');
});

tocEntries.forEach(function(entry) {
  // Grab a direct reference to the heading element NOW
  var headingEl = document.getElementById(entry.id);
  if (!headingEl) return;
  headingEls.push(headingEl);

  var li = document.createElement('li');
  var span = document.createElement('span');
  span.textContent = entry.text;
  span.dataset.idx = String(headingEls.length - 1);

  if (entry.level === 3) span.classList.add('toc-h3');
  if (entry.level === 4) span.classList.add('toc-h4');

  // Hover preview — uses cloneNode, collects full section content
  span.addEventListener('mouseenter', function() {
    clearTimeout(previewHideTimer);
    var idx = parseInt(this.dataset.idx);
    var el = headingEls[idx];
    if (!el) return;
    var level = el.tagName; // e.g. 'H2', 'H3', 'H4'
    var levelNum = parseInt(level.charAt(1));

    var clone = el.cloneNode(true);
    clone.removeAttribute('id');
    var previewHtml = clone.outerHTML;
    var sib = el.nextElementSibling;
    // Collect everything until the next heading of same or higher level
    while (sib) {
      var sibTag = sib.tagName;
      if (/^H[2-4]$/.test(sibTag) && parseInt(sibTag.charAt(1)) <= levelNum) break;
      var sc = sib.cloneNode(true);
      sc.removeAttribute('id');
      previewHtml += sc.outerHTML;
      sib = sib.nextElementSibling;
    }

    tocPreview.innerHTML = previewHtml;
    tocPreview.scrollTop = 0;
    var rect = this.getBoundingClientRect();
    var top = Math.min(rect.top, window.innerHeight - 280);
    tocPreview.style.top = Math.max(8, top) + 'px';
    tocPreview.classList.add('visible');
  });

  span.addEventListener('mouseleave', function() {
    previewHideTimer = setTimeout(function() {
      tocPreview.classList.remove('visible');
    }, 150);
  });

  // Click to navigate — direct reference, scrollIntoView
  (function(targetEl) {
    span.addEventListener('click', function() {
      tocPreview.classList.remove('visible');
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Highlight briefly
      targetEl.style.transition = 'background-color 0.3s ease';
      targetEl.style.backgroundColor = 'rgba(176,141,87,0.15)';
      setTimeout(function() { targetEl.style.backgroundColor = ''; }, 1500);
      document.getElementById('tocSidebar').classList.remove('mobile-open');
    });
  })(headingEl);

  tocSpans.push(span);
  li.appendChild(span);
  tocList.appendChild(li);
});

// Active heading tracking on scroll
function updateActiveToc() {
  var current = -1;
  for (var i = 0; i < headingEls.length; i++) {
    if (headingEls[i].getBoundingClientRect().top <= 60) current = i;
  }
  for (var j = 0; j < tocSpans.length; j++) {
    tocSpans[j].classList.toggle('active', j === current);
  }
  var tocSb = document.getElementById('tocSidebar');
  if (current >= 0 && tocSpans[current]) {
    var span = tocSpans[current];
    var spanRect = span.getBoundingClientRect();
    var sbRect = tocSb.getBoundingClientRect();
    if (spanRect.top < sbRect.top || spanRect.bottom > sbRect.bottom) {
      span.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  } else if (current === -1) {
    tocSb.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
window.addEventListener('scroll', updateActiveToc, { passive: true });
updateActiveToc();

// ---- Sidebar references ----
const tocSidebar = document.getElementById('tocSidebar');
const mainContent = document.getElementById('mainContent');

// ---- Theme toggle ----
const THEMES = ['light', 'dark', 'sepia', 'nord', 'dracula', 'green', 'rose', 'ocean'];
const THEME_ICONS = {
  light: '<svg viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>',
  dark: '<svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>',
  sepia: '<svg viewBox="0 0 24 24"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg>',
  nord: '<svg viewBox="0 0 24 24"><path d="M14 6l-3.75 5 2.85 3.8-1.6 1.2C9.81 13.75 7 10 7 10l-6 8h22L14 6z"/></svg>',
  dracula: '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
  green: '<svg viewBox="0 0 24 24"><path d="M17.8 4.8C16.45 3.15 14.35 2 12 2 6.48 2 2 6.48 2 12s4.48 10 10 10c4.25 0 7.9-2.65 9.35-6.4-1.2.5-2.5.4-3.6-.2-1.45-.85-2.3-2.4-2.3-4.1 0-.9.25-1.7.65-2.4.85-1.5 2.2-2.6 3.7-3.1zM8.5 15c-.83 0-1.5-.67-1.5-1.5S7.67 12 8.5 12s1.5.67 1.5 1.5S9.33 15 8.5 15z"/></svg>',
  rose: '<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>',
  ocean: '<svg viewBox="0 0 24 24"><path d="M21 14c0 1.1-.9 2-2 2h-1l-2 2-2-2H3c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h16c1.1 0 2 .9 2 2v10zm-5.55-4.63c-.09-.23-.32-.37-.56-.37s-.47.14-.56.37L12 15h1.5l.42-1.26h2.16L16.5 15H18l-2.55-5.63zM14.28 12.5L15 10.46l.72 2.04h-1.44zM2 20l4-4H2v4z"/></svg>'
};
const HLJS_THEMES = {
  light: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/mocha.min.css',
  dark: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/solarized-dark.min.css',
  sepia: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/mocha.min.css',
  nord: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/nord.min.css',
  dracula: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/dracula.min.css',
  green: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/atelier-forest.min.css',
  rose: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/ros-pine.min.css',
  ocean: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/ocean.min.css'
};

let currentThemeIndex = 0;
const themeBtn = document.getElementById('themeToggle');

function applyTheme(theme) {
  if (theme === 'light') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', theme);
  }
  document.getElementById('hljs-theme').href = HLJS_THEMES[theme];
  if (typeof mermaid !== 'undefined' && window._mermaidSources && window._mermaidSources.length) {
    var mermaidTheme = ['dark','nord','dracula','rose','ocean'].indexOf(theme) !== -1 ? 'dark' : 'default';
    mermaid.initialize({ startOnLoad: false, theme: mermaidTheme });
    document.querySelectorAll('.mermaid-wrapper').forEach(function(wrapper) {
      var idx = parseInt(wrapper.dataset.mermaidIdx);
      var code = window._mermaidSources[idx];
      if (!code) return;
      var newId = 'mermaid-re-' + idx + '-' + Date.now();
      mermaid.render(newId, code).then(function(result) {
        wrapper.innerHTML = result.svg;
      }).catch(function() {});
    });
  }
  const nextIdx = (THEMES.indexOf(theme) + 1) % THEMES.length;
  themeBtn.innerHTML = THEME_ICONS[THEMES[nextIdx]];
  themeBtn.title = 'Switch to ' + THEMES[nextIdx];
  localStorage.setItem('md2html-theme', theme);
}

themeBtn.addEventListener('click', function() {
  currentThemeIndex = (currentThemeIndex + 1) % THEMES.length;
  applyTheme(THEMES[currentThemeIndex]);
});

// Restore saved theme
const savedTheme = localStorage.getItem('md2html-theme');
if (savedTheme && THEMES.includes(savedTheme)) {
  currentThemeIndex = THEMES.indexOf(savedTheme);
  applyTheme(savedTheme);
} else {
  applyTheme('light');
}

// ---- Zen mode toggle ----
const zenBtn = document.getElementById('zenToggle');
let zenActive = false;

zenBtn.addEventListener('click', function() {
  zenActive = !zenActive;
  document.body.classList.toggle('zen-mode', zenActive);
  zenBtn.title = zenActive ? 'Exit zen mode' : 'Zen mode';
});

// Image lightbox close
var imgOverlay = document.getElementById('imgOverlay');
imgOverlay.addEventListener('click', function() {
  imgOverlay.classList.remove('visible');
});

// Escape key exits zen mode or lightbox
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    if (imgOverlay.classList.contains('visible')) {
      imgOverlay.classList.remove('visible');
    } else if (zenActive) {
      zenActive = false;
      document.body.classList.remove('zen-mode');
      zenBtn.title = 'Zen mode';
    }
  }
});

// ---- Toast helper ----
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

// ---- CDN-dependent rendering (runs after TOC is set up) ----
// Wrapped in DOMContentLoaded + try-catch so failures never break TOC navigation
document.addEventListener('DOMContentLoaded', function() {
  // Syntax highlighting
  try {
    if (typeof hljs !== 'undefined') {
      container.querySelectorAll('pre code').forEach(function(block) {
        if (block.classList.contains('language-mermaid')) return;
        hljs.highlightElement(block);
      });
      // Add language labels
      container.querySelectorAll('pre code').forEach(function(block) {
        if (block.classList.contains('language-mermaid')) return;
        var cls = Array.from(block.classList).find(function(c) { return c.startsWith('language-'); });
        if (cls) {
          var lang = cls.replace('language-', '');
          var label = document.createElement('span');
          label.className = 'code-lang';
          label.textContent = lang;
          block.closest('pre').appendChild(label);
        }
      });
    }
  } catch(e) { console.warn('hljs error:', e); }

  // Copy buttons for code blocks
  container.querySelectorAll('pre code').forEach(function(block) {
    if (block.classList.contains('language-mermaid')) return;
    var pre = block.closest('pre');
    var btn = document.createElement('button');
    btn.className = 'copy-code-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function() {
      navigator.clipboard.writeText(block.textContent).then(function() {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      });
    });
    pre.appendChild(btn);
  });

  // Mermaid — render sequentially (concurrent renders cause conflicts in v10)
  try {
    if (typeof mermaid !== 'undefined') {
      var dt = document.documentElement.getAttribute('data-theme') || '';
      var initialTheme = ['dark','nord','dracula','rose','ocean'].indexOf(dt) !== -1 ? 'dark' : 'default';
      mermaid.initialize({ startOnLoad: false, theme: initialTheme });
      window._mermaidSources = [];
      (async function() {
        var blocks = container.querySelectorAll('pre code.language-mermaid');
        for (var i = 0; i < blocks.length; i++) {
          var block = blocks[i];
          var pre = block.closest('pre');
          var code = block.textContent;
          window._mermaidSources.push(code);
          var wrapper = document.createElement('div');
          wrapper.className = 'mermaid-wrapper';
          wrapper.dataset.mermaidIdx = String(i);
          var mermaidId = 'mermaid-' + i;
          try {
            var result = await mermaid.render(mermaidId, code);
            wrapper.innerHTML = result.svg;
          } catch(err) {
            wrapper.textContent = 'Mermaid error: ' + err.message;
          }
          pre.replaceWith(wrapper);
        }
      })();
    }
  } catch(e) { console.warn('mermaid error:', e); }

  // KaTeX
  try {
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(container, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false},
          {left: '\\(', right: '\\)', display: false},
          {left: '\\[', right: '\\]', display: true}
        ],
        throwOnError: false
      });
    }
  } catch(e) { console.warn('katex error:', e); }
});

// ---- Text Highlight Feature ----
var _hlMarker = null;
var _hlKey = 'md2html-hl-' + location.pathname;

function _hlRemoveMarker() {
  if (_hlMarker) { _hlMarker.remove(); _hlMarker = null; }
}

var _hlPreviewHideTimer = null;
var _hlPreviewEl = null;

function _hlUpdateTicks() {
  var container = document.getElementById('hlMarkers');
  _hlPreviewEl = document.getElementById('hlPreview');
  container.innerHTML = '';
  var docHeight = document.documentElement.scrollHeight;
  document.querySelectorAll('mark.user-highlight').forEach(function(mark) {
    var contentEl = document.getElementById('content');
    var firstSection = contentEl.querySelector('.corner-section') || contentEl.querySelector('p');
    var contentTop = firstSection ? firstSection.getBoundingClientRect().top + window.scrollY : contentEl.getBoundingClientRect().top + window.scrollY;
    var contentBottom = contentEl.getBoundingClientRect().bottom + window.scrollY;
    var contentHeight = contentBottom - contentTop;
    var rect = mark.getBoundingClientRect();
    var absTop = rect.top + window.scrollY;
    var pct = Math.max(0, Math.min(100, ((absTop - contentTop) / contentHeight) * 100));
    var tick = document.createElement('div');
    tick.className = 'hl-tick';
    tick.style.top = pct + '%';

    // Hover preview: show surrounding content like TOC preview
    tick.addEventListener('mouseenter', function() {
      clearTimeout(_hlPreviewHideTimer);
      // Find the parent block element of the highlight
      var block = mark.closest('p, li, blockquote, pre, td, h2, h3, h4');
      if (!block) block = mark.parentNode;
      // Collect the block and a few siblings for context
      var previewHtml = '';
      var prev = block.previousElementSibling;
      if (prev && prev.tagName === 'P') previewHtml += prev.outerHTML;
      // Clone the block and highlight the marked text within it
      var clone = block.cloneNode(true);
      var marksInClone = clone.querySelectorAll('mark.user-highlight');
      marksInClone.forEach(function(m) {
        var span = document.createElement('span');
        span.className = 'hl-preview-text';
        span.innerHTML = m.innerHTML;
        m.replaceWith(span);
      });
      previewHtml += clone.outerHTML;
      var next = block.nextElementSibling;
      if (next && next.tagName === 'P') previewHtml += next.outerHTML;

      _hlPreviewEl.innerHTML = previewHtml;
      _hlPreviewEl.scrollTop = 0;
      var tickRect = tick.getBoundingClientRect();
      var top = Math.min(tickRect.top, window.innerHeight - 200);
      _hlPreviewEl.style.top = Math.max(8, top) + 'px';
      _hlPreviewEl.classList.add('visible');
    });

    tick.addEventListener('mouseleave', function() {
      _hlPreviewHideTimer = setTimeout(function() {
        _hlPreviewEl.classList.remove('visible');
      }, 150);
    });

    tick.addEventListener('click', function() {
      _hlPreviewEl.classList.remove('visible');
      mark.scrollIntoView({ behavior: 'smooth', block: 'center' });
      mark.style.transition = 'background-color 0.3s ease';
      mark.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--hl-bg-hover');
      setTimeout(function() { mark.style.backgroundColor = ''; }, 1200);
    });
    container.appendChild(tick);
  });
}

// Keep preview open when hovering over it
document.getElementById('hlPreview').addEventListener('mouseenter', function() {
  clearTimeout(_hlPreviewHideTimer);
});
document.getElementById('hlPreview').addEventListener('mouseleave', function() {
  document.getElementById('hlPreview').classList.remove('visible');
});

function _hlSaveAll() {
  try {
    var items = [];
    document.querySelectorAll('mark.user-highlight').forEach(function(m) {
      items.push(m.textContent);
    });
    localStorage.setItem(_hlKey, JSON.stringify(items));
  } catch(e) {}
  _hlUpdateTicks();
}

function _hlAddRemoveListener(mark) {
  mark.addEventListener('click', function(e) {
    e.stopPropagation();
    var p = mark.parentNode;
    while (mark.firstChild) p.insertBefore(mark.firstChild, mark);
    p.removeChild(mark);
    p.normalize();
    _hlSaveAll();
    showToast('Highlight removed');
  });
}

function _hlWrapRange(range) {
  try {
    // Simple case: range within a single text node
    if (range.startContainer === range.endContainer && range.startContainer.nodeType === 3) {
      var mark = document.createElement('mark');
      mark.className = 'user-highlight';
      range.surroundContents(mark);
      _hlAddRemoveListener(mark);
      return true;
    }
    // Complex case: range spans multiple nodes — wrap each text node individually
    var textNodes = [];
    var walker = document.createTreeWalker(
      range.commonAncestorContainer.nodeType === 1 ? range.commonAncestorContainer : range.commonAncestorContainer.parentNode,
      NodeFilter.SHOW_TEXT
    );
    while (walker.nextNode()) {
      if (range.intersectsNode(walker.currentNode)) {
        textNodes.push(walker.currentNode);
      }
    }
    if (!textNodes.length) return false;
    var wrapped = false;
    textNodes.forEach(function(textNode) {
      var start = 0, end = textNode.textContent.length;
      if (textNode === range.startContainer) start = range.startOffset;
      if (textNode === range.endContainer) end = range.endOffset;
      if (start >= end) return;
      var nodeRange = document.createRange();
      nodeRange.setStart(textNode, start);
      nodeRange.setEnd(textNode, end);
      try {
        var mark = document.createElement('mark');
        mark.className = 'user-highlight';
        nodeRange.surroundContents(mark);
        _hlAddRemoveListener(mark);
        wrapped = true;
      } catch(ex) {}
    });
    return wrapped;
  } catch(e) { return false; }
}

// Show the marker icon above selection
function _hlShowMarker(rect) {
  _hlRemoveMarker();
  var el = document.createElement('div');
  el.className = 'highlight-marker';
  el.innerHTML = '<svg viewBox="0 0 24 24"><path d="M7 14l5-5 5 5z"/><rect x="9" y="14" width="6" height="4" rx="1"/></svg>';
  el.title = 'Highlight selection';
  var x = rect.left + rect.width / 2 - 18;
  var y = rect.top - 44;
  if (y < 4) y = rect.bottom + 8;
  el.style.left = x + 'px';
  el.style.top = y + 'px';
  document.body.appendChild(el);
  _hlMarker = el;

  el.addEventListener('mousedown', function(e) {
    e.preventDefault();
    e.stopPropagation();
    var sel = window.getSelection();
    if (!sel.rangeCount || sel.isCollapsed) { _hlRemoveMarker(); return; }
    // Check if selection is inside an existing highlight
    var range = sel.getRangeAt(0);
    var node = range.startContainer;
    while (node) {
      if (node.nodeType === 1 && node.tagName === 'MARK' && node.classList.contains('user-highlight')) {
        sel.removeAllRanges();
        _hlRemoveMarker();
        showToast('Already highlighted');
        return;
      }
      node = node.parentNode;
    }
    _hlWrapRange(range.cloneRange());
    sel.removeAllRanges();
    _hlRemoveMarker();
    _hlSaveAll();
    showToast('Text highlighted');
  });
}

document.addEventListener('mouseup', function(e) {
  if (_hlMarker && _hlMarker.contains(e.target)) return;
  setTimeout(function() {
    try {
      var sel = window.getSelection();
      if (!sel || !sel.rangeCount || sel.isCollapsed) { _hlRemoveMarker(); return; }
      var text = sel.toString();
      if (!text || !text.trim()) { _hlRemoveMarker(); return; }
      var range = sel.getRangeAt(0);
      // Don't show marker if selection is inside TOC or an existing highlight
      var n = range.startContainer;
      while (n) {
        if (n.nodeType === 1) {
          if (n.tagName === 'MARK' && n.classList.contains('user-highlight')) { _hlRemoveMarker(); return; }
          if (n.classList && n.classList.contains('toc-sidebar')) { _hlRemoveMarker(); return; }
        }
        n = n.parentNode;
      }
      var rect = range.getBoundingClientRect();
      if (!rect || (rect.width === 0 && rect.height === 0)) { _hlRemoveMarker(); return; }
      _hlShowMarker(rect);
    } catch(e) { _hlRemoveMarker(); }
  }, 50);
});

document.addEventListener('mousedown', function(e) {
  if (_hlMarker && !_hlMarker.contains(e.target)) {
    _hlRemoveMarker();
  }
});

// Clear all highlights button
document.getElementById('clearHighlights').addEventListener('click', function() {
  var marks = document.querySelectorAll('mark.user-highlight');
  if (!marks.length) { showToast('No highlights to clear'); return; }
  marks.forEach(function(m) {
    var p = m.parentNode;
    while (m.firstChild) p.insertBefore(m.firstChild, m);
    p.removeChild(m);
    p.normalize();
  });
  localStorage.removeItem(_hlKey);
  _hlUpdateTicks();
  showToast('All highlights cleared');
});

// Restore saved highlights by matching text content
try {
  var saved = JSON.parse(localStorage.getItem(_hlKey) || '[]');
  if (saved.length) {
    setTimeout(function() {
      var contentEl = document.getElementById('content');
      saved.forEach(function(text) {
        if (!text) return;
        var walker = document.createTreeWalker(contentEl, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
          var node = walker.currentNode;
          var idx = node.textContent.indexOf(text);
          if (idx !== -1) {
            try {
              var r = document.createRange();
              r.setStart(node, idx);
              r.setEnd(node, idx + text.length);
              _hlWrapRange(r);
            } catch(e) {}
            break;
          }
        }
      });
      _hlUpdateTicks();
    }, 600);
  }
} catch(e) {}
</script>
</body>
</html>'''


def render(markdown: str) -> str:
    """Convert a markdown string to a self-contained HTML string.

    Args:
        markdown: Raw markdown text.

    Returns:
        A complete, self-contained HTML page as a string.
    """
    md_b64 = base64.b64encode(markdown.encode('utf-8')).decode('ascii')
    return TEMPLATE.replace('__MD_B64__', md_b64)


def convert(input_path: str, output_path: str | None = None) -> str:
    """Convert a markdown file to an HTML file.

    Args:
        input_path: Path to the input markdown file.
        output_path: Path for the output HTML file. If None, replaces
            the .md extension with .html.

    Returns:
        The generated HTML string.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + '.html'

    html = render(md_content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return html


def main():
    if len(sys.argv) < 2:
        print("Usage: gloss <input.md> [output.html]")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    output_path = sys.argv[2] if len(sys.argv) >= 3 else None
    convert(input_path, output_path)
    out = output_path or os.path.splitext(input_path)[0] + '.html'
    print(f"Done! {out}")


if __name__ == '__main__':
    main()
