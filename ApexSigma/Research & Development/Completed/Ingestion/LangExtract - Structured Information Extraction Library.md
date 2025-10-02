---
aliases: ["LangExtract: Structured Information Extraction Library"]
linter-yaml-title-alias: "LangExtract: Structured Information Extraction Library"
date created: 257,14O September9 2025 12:32 pm 
date modified: 266,23O September9 2025 11:33 pm 
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# LangExtract: Structured Information Extraction Library

**Main Takeaway**
LangExtract is a flexible Python library that leverages large language models (LLMs) to extract and structure information from unstructured text, with precise source grounding and interactive visualization capabilities.[^1]

## Overview

LangExtract enables users to define custom extraction tasks for any domain—literary analysis, medical reports, or technical documentation—by providing a clear prompt and example annotations. It supports both cloud-hosted models (Google Gemini, OpenAI) and local models (via Ollama), ensuring adaptable deployment.

## Key Features

- **Precise Source Grounding**: Maps each extracted entity directly to its location in the original text, allowing users to review and verify extractions easily.
- **Reliable Structured Outputs**: Enforces a consistent schema based on user-provided examples, reducing hallucinations and ensuring predictable formats.
- **Optimized for Long Documents**: Uses chunking, parallel processing, and multiple passes to maintain high recall in large texts.
- **Interactive Visualization**: Generates a standalone HTML visualization that highlights extractions in context, facilitating rapid review of thousands of entities.
- **Flexible Model Support**: Seamlessly integrates with cloud LLMs (Gemini, OpenAI) and local models (Ollama), with plugins for custom providers.
- **Domain Agnostic**: Works across any domain without model fine-tuning—just define extraction classes and examples.
- **Scalable Performance**: Configurable extraction passes, worker counts, and buffer sizes to balance speed and accuracy for large-scale tasks.

## Installation

Install from PyPI for quick setup:

```bash
pip install langextract
```

Or install from source for development:

```bash
git clone https://github.com/google/langextract.git
cd langextract
pip install -e .
```

Use Docker for containerized environments:

```bash
docker build -t langextract .
docker run --rm -e LANGEXTRACT_API_KEY="your-api-key" langextract python your_script.py
```

## Quick Start Example

1. **Define Prompt and Examples**

```python
import langextract as lx
prompt = """Extract characters, emotions, and relationships in order of appearance."""
examples = [
    lx.data.ExampleData(
        text="ROMEO. But soft! What light through yonder window breaks?",
        extractions=[
            lx.data.Extraction("character", "ROMEO", {"emotional_state":"wonder"}),
            lx.data.Extraction("emotion", "But soft!", {"feeling":"gentle awe"}),
            lx.data.Extraction("relationship", "Juliet is the sun", {"type":"metaphor"}),
        ]
    )
]
```

2. **Run Extraction**

```python
result = lx.extract(
    text_or_documents="Lady Juliet gazed longingly at the stars, her heart aching for Romeo",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash"
)
```

3. **Visualize Results**

```python
lx.io.save_annotated_documents([result], "extraction_results.jsonl", ".")
html = lx.visualize("extraction_results.jsonl")
with open("visualization.html","w") as f:
    f.write(html if isinstance(html,str) else html.data)
```

## Advanced Usage

- **Full-Text Extraction**: Process large documents (e.g., _Romeo and Juliet_ from Project Gutenberg) with multiple passes and parallel workers.
- **Medical Extraction**: Extract medication names, dosages, and routes from clinical notes; structure radiology reports with relationship mapping.
- **Custom Providers**: Extend with third-party or on-premise LLMs by registering plugins via the provider registry.

## Model Configuration

- **Cloud Models**: Set `LANGEXTRACT_API_KEY` in environment or `.env`, choose `gemini-2.5-flash` for balanced performance or `gemini-2.5-pro` for deeper reasoning.
- **Local Models**: Use Ollama (`gemma2:2b`) by installing and running a local server, then set `model_url="http://localhost:11434"` and `fence_output=False`.

***

<div style="text-align: center">⁂</div>

[^1]: <https://github.com/google/langextract>