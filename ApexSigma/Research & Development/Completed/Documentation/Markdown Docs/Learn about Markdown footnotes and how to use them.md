<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Learn about Markdown footnotes and how to use them effectively

**Footnotes in Markdown** are a powerful tool for adding citations, references, and supplementary information without disrupting the flow of your main text. They create clickable superscript numbers that link to detailed information at the bottom of your document.[^1][^7]

### Basic Footnote Syntax

The foundation of Markdown footnotes consists of **two essential parts**: the reference marker in your text and the footnote definition.[^3]

**Reference Marker**
Place `[^label]` directly after the text you want to footnote, without any spaces :[^1]

```markdown
This is an example sentence.[^1]
```

**Footnote Definition**
Define your footnote content anywhere in the document (typically at the bottom) :[^5]

```markdown
[^1]: This is the footnote text that appears at the bottom of the page.
```


### Advanced Footnote Techniques

**Named Labels**
Use descriptive labels instead of numbers for better organization :[^5]

```markdown
The project deadline is Friday[^deadline].

[^deadline]: Subject to management approval.
```

**Reusable Footnotes**
Reference the same footnote multiple times throughout your document :[^1]

```markdown
This fact is important[^1]. This confirms the earlier point[^1].

[^1]: Supporting evidence from research study.
```

**Rich Content Footnotes**
Include formatting, links, and emphasis within footnotes :[^1]

```markdown
This requires additional explanation[^complex].

[^complex]: This footnote contains *italic*, **bold**, and `code` text, plus a [link](https://example.com).
```


### Multi-Paragraph Footnotes

For longer explanations, create multi-paragraph footnotes by indenting subsequent paragraphs with four spaces or a tab :[^5]

```markdown
This statement needs elaboration[^detailed].

[^detailed]: This is the first paragraph of the footnote.

    This is the second paragraph, indented with four spaces.
    
    This is the third paragraph of the same footnote.
```


### Footnotes with Lists

Include bulleted or numbered lists within footnote definitions :[^1]

```markdown
This topic covers several aspects[^points].

[^points]: Key considerations:
    - First important point
    - Second critical aspect  
    - Third essential element
```


### Effective Usage Best Practices

**Strategic Placement**
Position footnotes where they add value without interrupting the reading flow. Use them for citations, clarifications, or supplementary details that would otherwise clutter the main text.[^6][^5]

**Concise Content**
Keep footnotes brief and focused. If you find yourself writing lengthy footnotes, consider whether that information belongs in the main text or an appendix section instead.[^5]

**Consistent Labeling**
Use descriptive labels like `[^source]` or `[^explanation]` rather than sequential numbers, as this makes your Markdown more maintainable when adding or removing footnotes later.[^5]

**Citation Standards**
Maintain consistent citation formatting (APA, MLA, Chicago, etc.) throughout your document when using footnotes for academic references :[^5]

```markdown
According to recent research[^study1].

[^study1]: Smith, J. (2023). The Rise of Markdown. *Journal of Documentation*, 45(2), 18-27.
```


### Platform Compatibility

**GitHub Support**
GitHub now fully supports footnote syntax across all Markdown fields, displaying them as clickable superscript links. The footnotes appear in a dedicated section at the bottom of rendered documents.[^7]

**Processor Variations**
While footnotes are part of extended Markdown syntax, not all processors support them. Test your footnotes in your target environment to ensure proper rendering and functionality.[^5]

Footnotes transform simple Markdown documents into professional, well-referenced materials by providing a clean way to include citations and explanatory content without disrupting the main narrative flow.[^3][^1][^5]
<span style="display:none">[^2][^4][^8][^9]</span>

<div style="text-align: center">⁂</div>

[^1]: https://tiiny.host/blog/markdown-footnotes/

[^2]: https://www.codecademy.com/resources/docs/markdown/footnotes

[^3]: https://blog.markdowntools.com/posts/footnotes-in-markdown

[^4]: https://www.markdownguide.org/extended-syntax/

[^5]: https://www.321markdown.com/markdown-guide/footnotes

[^6]: https://justdone.com/blog/writing/how-to-do-footnotes

[^7]: https://github.blog/changelog/2021-09-30-footnotes-now-supported-in-markdown-fields/

[^8]: https://www.markdownguide.org/cheat-sheet/

[^9]: https://www.wisp.blog/blog/the-essential-markdown-syntax-guide-everything-you-need-to-know

