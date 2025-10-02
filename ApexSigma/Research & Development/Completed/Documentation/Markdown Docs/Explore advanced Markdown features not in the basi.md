<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Explore advanced Markdown features not in the basic cheatsheet

**Advanced Markdown features** go far beyond the basic syntax to provide sophisticated formatting options and interactive elements for creating professional-grade documents.[^1][^2]

### HTML Integration and Custom Styling

**Custom HTML Tags**
Markdown seamlessly integrates with HTML, allowing for advanced layout control :[^2]

```html
<div align="center">
  <img width="460" height="300" src="image.jpg">
</div>
```

**Image Alignment**
Control image positioning with HTML attributes :[^2]

- Left alignment: `<img align="left" width="100" src="image.jpg">`
- Right alignment: `<img align="right" width="100" src="image.jpg">`
- Center alignment: Use `<p align="center">` wrapper

**Responsive Images**
Create theme-aware images that adapt to dark/light modes :[^2]

```markdown
![Logo](./dark.png#gh-dark-mode-only)
![Logo](./light.png#gh-light-mode-only)
```


### Advanced Text Formatting

**Text Boxes**
Create bordered content areas using HTML tables :[^2]

```html
<div align="center">
<table>
<tbody>
<td align="center">
This is text in a box
</td>
</tbody>
</table>
</div>
```

**Tiny Text**
Combine superscript and subscript for extremely small text :[^2]

```html
<sup><sub>Tiny text here</sub></sup>
```

**Callout Boxes**
GitHub-flavored Markdown supports special alert syntax :[^2]

```markdown
> [!NOTE]
> Information users should consider

> [!WARNING]  
> Critical content requiring attention

> [!IMPORTANT]
> Crucial information for success
```


### Interactive Elements

**Collapsible Sections**
Create expandable content areas using HTML details tags :[^1][^2]

```html
<details>
<summary>Click to expand</summary>

Your markdown content goes here
- Including lists
- **Bold text**
- And other formatting

</details>
```

**Advanced Task Lists**
Beyond basic checkboxes, some processors support nested task lists :[^1]

```markdown
- [x] Completed parent task
  - [x] Completed subtask
  - [ ] Pending subtask
- [ ] Pending parent task
```


### Mathematical and Scientific Notation

**Definition Lists**
Create glossary-style entries for technical documentation :[^1]

```markdown
Term 1
: Definition of the first term

Term 2  
: First definition of the second term
: Alternative definition of the same term
```

**Advanced Subscript and Superscript**
For chemical formulas and mathematical expressions :[^1]

```markdown
H~2~O (water molecule)
E=mc^2^ (Einstein's equation)
```


### Media and Visual Enhancements

**Video Embedding**
GitHub and similar platforms support direct video file embedding :[^2]

```markdown
![Video demonstration](demo.mp4)
```

**File Tree Visualization**
Use GraphQL syntax highlighting for clean directory structures :[^2]

````markdown
```
project/
├─ src/
│  ├─ components/
│  └─ utils/
└─ docs/
```
```

### Advanced Code Features

**Mermaid Diagrams**
Create flowcharts and sequence diagrams directly in Markdown :[^2]
````markdown
```
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]  
    B -->|No| D[Action 2]
```
```

**Advanced Code Block Features**
Some processors support line highlighting and file names :[^3]
````markdown
```
// filename: example.js
function hello() {
    console.log("Hello");
    return true;
}
```
```

### Document Structure Enhancements

**Custom Heading IDs**
Create anchor links for navigation :[^1]
```markdown
### Important Section {#custom-anchor}

[Link to section](#custom-anchor)
```

**Table of Contents Generation**
Some processors auto-generate TOCs :[^3]
```markdown
[TOC]
```

**YAML Front Matter**
Add metadata to documents :[^2]
```yaml
---
title: "Advanced Markdown Guide"
description: "Comprehensive formatting techniques"
author: "Your Name"
date: 2025-09-16
---
```

### Styling and Presentation

**Badge Integration**
Embed status badges and shields :[^2]
```markdown
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-2.0-blue)
```

**CSS in SVG**
Embed styled content using SVG with CSS :[^2]
```html
<div align="center">
  <img src="styled-content.svg" width="800" height="400" />
</div>
```

These advanced features transform Markdown from a simple formatting language into a powerful documentation and content creation platform, enabling professional-quality documents with interactive elements and sophisticated layouts.[^3][^1][^2]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^4][^5][^6][^7][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://www.markdownguide.org/extended-syntax/
[^2]: https://github.com/DavidWells/advanced-markdown
[^3]: https://www.markdowntoolbox.com/blog/markdown-syntax-guide-advanced-formatting-techniques/
[^4]: https://www.markdownguide.org/cheat-sheet/
[^5]: https://dev.to/mahbubumithu/a-complete-markdown-tutorial-from-basics-to-advanced-41nb
[^6]: https://dev.to/mutalibcs/markdown-syntax-features-a-comprehensive-2025-guide-3cf0
[^7]: https://www.markdownlang.com/extended/
[^8]: https://docs.charthop.com/markdown-formatting
[^9]: https://help.obsidian.md/advanced-syntax
[^10]: https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
[^11]: https://getdoks.org/docs/reference/markdown-extended-syntax/
[^12]: https://docusaurus.io/docs/markdown-features
[^13]: https://www.markdownguide.org
[^14]: https://technicalwritingmp.com/docs/advanced-syntax-formatting-in-markdown
[^15]: https://www.jetbrains.com/help/hub/markdown-syntax.html
[^16]: https://www.tomarkdown.org/en/guides/markdown-advanced
[^17]: https://confluence.atlassian.com/display/BITBUCKETSERVER081/Markdown+syntax+guide
[^18]: https://www.obsidianstats.com/plugins/extended-markdown-syntax````

