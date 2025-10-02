---
tags:
  - ApexSigma
  - MKDocs
  - Docstrings
  - Automation
  - PolicyAsCode
---
# Integrating MkDocs for Public Documentation

This guide provides a step-by-step plan for integrating a professional, searchable documentation site into the ecosystem using MkDocs. This represents the **public-facing layer** of our three-part documentation strategy.

## Documentation Strategy Recap

1.  **Source of Truth (/Docs/ & Code Docstrings):** Internal, collaborative Markdown files and the docstrings within the Python source code. **This is where we write.**
2.  **Agent Ingestion (/.ingest/):** Compiled, token-efficient JSON files for agents, generated from both Markdown and docstrings. **This is what agents read.**
3.  **Public Docs (/docs/):** Curated, polished content for end-users, built by MkDocs from both Markdown and docstrings. **This is what the world sees.**

Of course. Here is Step 1 converted to the YAML format for a `pyproject.toml` file using Poetry, along with the recommended CLI commands.

I'll update the content for "Step 1" in your note.

---

### Step 1: Add Dependencies with Poetry

Add MkDocs and its plugins to your development dependencies using the Poetry CLI. It's best practice to add these to a dedicated group like `docs`.

1.  **Run the following commands in your terminal:**
    ```bash
    poetry add mkdocs --group docs
    poetry add mkdocs-material --group docs
    poetry add "mkdocstrings[python]" --group docs
    ```

2.  **Verify your `pyproject.toml`:** After running the commands, Poetry will automatically add a new section to your `pyproject.toml` file that looks like this:

    ```toml
    [tool.poetry.group.docs.dependencies]
    mkdocs = "^1.6.0"
    mkdocs-material = "^9.5.25"
    mkdocstrings = {extras = ["python"], version = "^0.25.1"}
    ```
    *(Note: The version numbers may vary slightly.)*
## Step 2: Configure mkdocs.yml

Update your `mkdocs.yml` file to enable and configure the mkdocstrings plugin for the ApexSigma ecosystem.

```yaml
# mkdocs.yml
site_name: ApexSigma Ecosystem Documentation
site_url: https://docs.apexsigma.as/
repo_url: https://github.com/ApexSigma-Solutions/apexsigma.as

theme:
  name: material
  palette:
    - scheme: default
      toggle:
        icon: material/weather-sunny
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/weather-night
        name: Switch to light mode
  features:
    - navigation.tabs
    - search.suggest
    - content.code.copy

# Add the mkdocstrings plugin
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true

# The 'nav' section defines the site's navigation.
nav:
  - 'Introduction': 'index.md'
  - 'Tutorials': 'tutorials/index.md'
  - 'How-To Guides': 'how-to/index.md'
  - 'API Reference':
    - 'reference/index.md'
    - 'memOS Service': 'reference/memos_service.md'
```

## Step 3: Automate API Doc Generation

Instead of manually creating API documentation, we will let `mkdocstrings` generate it automatically from the source code of our core services.

1.  **Create a Reference Markdown File:** In your `/docs` directory, create a file named `reference/memos_service.md`.

2.  **Add the Docstring Directive:** Inside this file, add a single line that tells `mkdocstrings` which Python module to scan. The `:::` syntax will automatically pull in all functions and classes from the `memOS.as` main application file and render their docstrings.

    ```markdown
    # /docs/reference/memos_service.md
    
    ::: memos.main
    ```

## Step 4: The Unified Build Process

Our `build_docs.py` script now has two primary responsibilities: copying our handwritten Markdown and letting `mkdocstrings` handle the code documentation.

**The script's responsibilities:**

1.  **Clean:** Delete the contents of the `/docs` directory (except for files with `mkdocstrings` directives) to ensure a fresh build.
2.  **Select & Copy:** Read the `/.md/` directory and copy the approved, public-facing documents into the `/docs` directory.
3.  **Trigger MkDocs:** The `mkdocs serve` or `mkdocs build` command will now automatically find the `::: memos.main` directive and generate the API documentation on the fly.

## Step 5: Run the Local Docs Server

1.  **Run the build script** to populate the `/docs` directory with your handwritten guides.
2.  **Serve the site** using MkDocs.
    ```bash
    mkdocs serve
    ```
3.  **View the site** at `http://127.0.0.1:8000`. Navigate to the "API Reference" -> "memOS Service" section to see your auto-generated documentation from your Python docstrings.