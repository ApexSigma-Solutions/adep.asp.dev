# Git Initialization Protocol


Execute these steps from the root of the ApexSigmaProjects.Dev directory in your terminal.

Step 1: Create a .gitignore File
This is the most critical first step. This file tells Git which files and directories to ignore, preventing secrets, virtual environments, and other junk from ever being committed to the repository.

Create the file:

PowerShell

```pwrshll
New-Item .gitignore
```

Paste the following content into the .gitignore file. This is a robust starting point for a Python/Docker project.

Code snippet

```python
# Byte-compiled / optimized / DLL files
__pycache__/
*.pyc
*.pyo
*.pyd

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE / Editor specific
.vscode/
.idea/
*.swp
*.swo

# Docker
docker-compose.override.yml
```
