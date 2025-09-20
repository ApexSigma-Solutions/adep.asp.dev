# EOD (End of Day) Command Protocol - Setup Guide

The EOD command is a mandatory standardized procedure for capturing development progress and ingesting it into the ApexSigma knowledge graph.

## Purpose

1. **Knowledge Persistence** - Create permanent, auditable log of project evolution
2. **Project Synchronization** - Provide daily summaries for collaboration and handoffs
3. **Cognitive Offloading** - Allow formal work session conclusion with secure archival

## Prerequisites

Before executing the EOD command, ensure:

1. **All Work is Committed** - Clean git working directory with descriptive commit messages
2. **Services are Running** - InGest-LLM.as service must be running on port 8000
3. **Project Root Location** - Execute from the root directory of your project repository

## Installation

### Quick Setup (Recommended)

Run this PowerShell command once to set up the EOD command:

```powershell
# From the ApexSigma root directory
.\setup-eod-command.ps1
. $PROFILE  # Reload PowerShell profile
```

After setup, you can use from any directory:
```powershell
eod                    # Basic EOD execution
eod -Project devenviro.as -SkipTests -DryRun
/eod                   # Using alias
```

### Manual Setup Options

#### Option 1: Direct Execution
```bash
# From ApexSigma root directory
cd C:\Users\steyn\ApexSigmaProjects.Dev
python eod.py --help
```

#### Option 2: Windows Batch File
```cmd
cd C:\Users\steyn\ApexSigmaProjects.Dev
eod.bat --project devenviro.as --skip-tests
```

#### Option 3: PowerShell Script
```powershell
cd C:\Users\steyn\ApexSigmaProjects.Dev
.\eod.ps1 -Project devenviro.as -SkipTests
```

## EOD Command Process

The EOD procedure executes in 7 sequential steps:

### Step 1: Automated Pre-Checks
- **Codebase Analysis** - Static analysis with complexity metrics
- **Image Scraping** - Caches relevant images for documentation
- **Git Status Verification** - Ensures clean working directory
- **Test Execution** - Runs local unit tests
- **Latest State Fetch** - Pulls latest changes from remote alpha branch

### Step 2: Interactive Summary Collection
You'll be prompted to provide:

```
TASKS_COMPLETED: P3-HIGH-01, P3-HIGH-02
KEY_DECISIONS_OR_INSIGHTS: Selected Linkerd over Istio for service mesh 
due to lower operational complexity.
BLOCKERS_ENCOUNTERED: None
NEXT_STEPS: Begin scaffolding React components for agent control UI.
```

### Step 3: Log Generation and Formatting
- Formats input into standardized JSON log entry
- Includes git metadata, session statistics, and project context

### Step 4: Knowledge Graph Ingestion
- Submits to InGest-LLM.as endpoint: `POST /ingest/eod-log`
- Creates entities and relationships in knowledge graph
- Generates embeddings for semantic search

### Step 5: Local Changelog Update
- Appends formatted entry to `changelog.md`
- Maintains local project history

### Step 6: Remote Push
- Pushes committed changes to remote feature branch
- Ensures work is backed up remotely

### Step 7: Confirmation
- Displays success confirmation with log ID
- Shows any errors that need attention

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--project PROJECT` | Specify project name | `--project devenviro.as` |
| `--skip-tests` | Skip running local tests | `--skip-tests` |
| `--dry-run` | Test run without actual submission | `--dry-run` |
| `--help` | Show help message | `--help` |

## Example Usage

### Basic EOD Session
```bash
C:\Users\steyn\ApexSigmaProjects.Dev\devenviro.as> /command eod

[INFO] Analyzing codebase... 15 files analyzed, complexity score: 2.8.
[INFO] Scraping images for keywords: 'dashboard', 'metrics'... 3 images cached.
[INFO] Git status is clean.
[INFO] Running local unit tests... All 128 tests passed.
[INFO] Fetching latest from origin/alpha... Done.

Please provide your EOD summary. Press CTRL+D when finished.

TASKS_COMPLETED: P3-HIGH-03
KEY_DECISIONS_OR_INSIGHTS: Decided to postpone Kubernetes migration. 
Re-confirmed the outstanding backlog items and prioritized clearing 
them before starting new infrastructure work.
BLOCKERS_ENCOUNTERED: None.
NEXT_STEPS: Begin formal design and task breakdown for user-facing control UI.

[INFO] Formatting EOD log...
[INFO] Submitting log to InGest-LLM.as...
[SUCCESS] Knowledge Graph ingestion successful. Log ID: 20250828-BacklogPrioritization.
[INFO] Pushing commits to origin/feature/sigma-ui-planning...
[SUCCESS] EOD procedure complete.
```

### EOD with Options
```powershell
# Skip tests during development
eod -SkipTests

# Test run without actually submitting
eod -DryRun

# Specify different project
eod -Project memos.as -Verbose
```

## Service Integration

### InGest-LLM.as Endpoints

The EOD command integrates with these endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Verify service availability |
| `POST /ingest/eod-log` | Submit EOD log for ingestion |
| `GET /ingest/eod-logs/{project}` | Retrieve project EOD history |
| `GET /ingest/eod-logs/{project}/metrics` | Get project development metrics |

### Knowledge Graph Storage

EOD logs are stored with these entity types:
- **Session Entity** - Development session metadata
- **Task Relationships** - Links to completed tasks
- **Project Relationships** - Session belongs to project
- **Branch Relationships** - Session occurred on branch

## Troubleshooting

### Common Issues

#### "Working directory is not clean"
```
[ERROR] Working directory is not clean. Uncommitted changes found:
M  src/main.py
?? temp_file.txt
```
**Solution**: Commit all changes before running EOD
```bash
git add .
git commit -m "Descriptive commit message"
```

#### "Could not connect to InGest-LLM service"
```
[ERROR] Could not connect to InGest-LLM service. Is it running on port 8000?
```
**Solution**: Start InGest-LLM service
```bash
cd InGest-LLM.as
poetry run uvicorn src.ingest_llm_as.main:app --reload
```

#### "Git push failed"
```
[ERROR] Git push failed: fatal: unable to access 'https://github.com/...': 
The requested URL returned error: 403
```
**Solution**: Verify git credentials and remote access
```bash
git remote -v
git push origin feature-branch-name
```

### Debug Mode

For troubleshooting, use dry-run mode:
```bash
python eod.py --dry-run --project devenviro.as
```

This will:
- Execute all pre-checks
- Collect EOD summary
- Format log entry  
- Show what would be submitted (without actually submitting)
- Show what would be pushed (without actually pushing)

## Integration with Development Workflow

### Daily Development Cycle
1. Start development session
2. Make changes and commit work
3. **Run EOD command before ending session**
4. Review generated report
5. Next session can reference previous EOD logs

### Team Coordination
- EOD logs provide handoff information between team members
- Key decisions are captured for future reference
- Blockers are documented for resolution tracking
- Project velocity can be measured over time

### Knowledge Graph Benefits
- Semantic search across all development sessions
- Pattern recognition in development blockers
- Automatic linking of related tasks and decisions
- Historical context for future development decisions

The EOD command ensures no development context is lost and enables powerful analysis of development patterns across the entire ApexSigma ecosystem.