# MarkForge

A lightweight static site generator built from scratch in Python.

---

## Overview

MarkForge is a custom static site generator that converts Markdown files into structured HTML pages. It supports inline formatting, block parsing, templating, static asset management, and deployment via GitHub Pages.

---

## Features

* Markdown to HTML conversion
* Inline parsing:

  * Bold (`**text**`)
  * Italic (`_text_`)
  * Code (`` `code` ``)
  * Links `[text](url)`
  * Images `![alt](url)`
* Block parsing:

  * Headings (`#` to `######`)
  * Paragraphs
  * Code blocks
  * Blockquotes
  * Ordered and unordered lists
* Template-based HTML generation
* Recursive directory traversal
* Static asset copying (CSS, images)
* Multi-page generation
* GitHub Pages deployment support

---

## Project Structure

```
MarkForge/
├── content/          # Markdown source files
│   ├── index.md
│   ├── blog/
│   └── contact/
├── static/           # Static assets (CSS, images)
├── docs/             # Generated site (output for deployment)
├── src/
│   ├── htmlnode.py
│   ├── textnode.py
│   ├── inline_markdown.py
│   ├── block_markdown.py
│   └── main.py
├── template.html
├── build.sh
├── main.sh
└── README.md
```

---

## How It Works

### 1. Markdown Processing Pipeline

```
Markdown → Blocks → TextNodes → HTMLNodes → HTML
```

---

### 2. Inline Parsing

Text is converted into `TextNode` objects representing:

* Plain text
* Bold
* Italic
* Code
* Links
* Images

Handled through:

* `split_nodes_delimiter`
* `split_nodes_link`
* `split_nodes_image`

---

### 3. Block Parsing

Markdown is split into logical blocks:

```
markdown_to_blocks()
```

Each block is classified using:

```
block_to_block_type()
```

Supported block types:

* Paragraph
* Heading
* Code block
* Quote
* Unordered list
* Ordered list

---

### 4. HTML Node System

A custom DOM-like structure is implemented:

* `HTMLNode` (base class)
* `LeafNode` (no children)
* `ParentNode` (contains children)

Each node implements:

```
to_html()
```

---

### 5. Markdown to HTML Conversion

```
markdown_to_html_node(markdown)
```

* Converts blocks into HTML nodes
* Recursively builds structure
* Returns a root `<div>` node

---

### 6. Template Rendering

```
generate_page()
```

Steps:

1. Read Markdown file
2. Convert to HTML
3. Extract page title from `# Heading`
4. Inject into template:

```
<title>{{ Title }}</title>
<article>{{ Content }}</article>
```

---

### 7. Static Asset Handling

```
copy_static()
```

* Deletes existing output directory
* Recursively copies:

  * CSS files
  * Images
  * Other static assets

---

### 8. Multi-page Generation

```
generate_pages_recursive()
```

* Traverses `content/` directory
* Converts all `.md` files
* Maintains directory structure

---

### 9. Base Path Support

Supports deployment under subpaths such as:

```
/MarkForge/
```

Rewrites:

```
href="/..." → href="/MarkForge/..."
src="/..."  → src="/MarkForge/..."
```

---

## Usage

### Local Development

```
./main.sh
```

Open in browser:

```
http://localhost:8888
```

---

### Production Build

```
./build.sh
```

Generates the site in:

```
docs/
```

---

## Deployment (GitHub Pages)

1. Push repository to GitHub
2. Navigate to repository settings → Pages
3. Configure:

   * Branch: `main`
   * Folder: `/docs`

Your site will be available at:

```
https://shubh1855.github.io/MarkForge/
```

---

## Testing

Unit tests cover:

* HTML node rendering
* Text node parsing
* Inline markdown splitting
* Block classification
* Markdown to HTML conversion

Run tests:

```
./test.sh
```

---

## Key Learnings

* Markdown parsing fundamentals
* Recursive tree structures
* Text processing and pattern matching
* Static site generation pipelines
* File system automation in Python
* Deployment workflows using GitHub Pages

---

## Future Improvements

* Frontmatter support (metadata, dates)
* Blog index generation
* Tag and category systems
* CLI interface
* Live preview server
* Theme customization

---
