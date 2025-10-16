# DevContainer Quick Reference

## 🚀 Quick Start

```bash
# Rebuild DevContainer (VS Code Command Palette)
Ctrl+Shift+P → Dev Containers: Rebuild Container

# Manual integrity check (inside DevContainer)
./.devcontainer/integrity-check.sh
```

## 🔍 What Was Fixed

**Problem**: Build failed with "docker group does not exist"
**Root Cause**: Distributed state synchronization failure across git/poetry/docker
**Solution**: Atomic validation checkpoint + docker-in-docker feature

## ✅ Validation Layers

1. **Git Submodules** - Verifies commit hash integrity
2. **Poetry Lockfiles** - Auto-fixes dependency drift
3. **Docker Contexts** - Validates compose configuration
4. **BuildKit Cache** - Purges stale layers

## 🛠️ Commands

### Inside DevContainer

```bash
# Check Docker CLI
docker --version
docker compose --version

# Verify services
docker ps
docker compose -f docker-compose.unified.yml ps

# Manual lockfile fix
cd services/memos.as && poetry lock --no-update
cd libs/apexsigma-core && poetry lock --no-update
```

### Outside DevContainer (Host)

```bash
# Run integrity check (limited validation)
wsl bash -c "cd /mnt/c/Users/steyn/ApexSigmaProjects.Dev && ./.devcontainer/integrity-check.sh"

# Purge Docker cache
docker builder prune -af
docker system prune -af --volumes

# Rebuild workspace
docker compose -f docker-compose.unified.yml build --no-cache workspace
```

## 🚨 Troubleshooting

### Build Still Fails

1. Purge all Docker state
2. Fix Poetry locks manually
3. Rebuild from scratch
4. Check `.devcontainer/README.md` troubleshooting section

### Integrity Check Fails

- **Git submodule error**: `git submodule update --init --recursive`
- **Poetry error**: Manually run `poetry lock --no-update` in service dir
- **Docker error**: Check `docker-compose.unified.yml` syntax

### Docker Group Error (Should Not Happen)

- Verify `devcontainer.json` has `docker-in-docker:2` feature
- Ensure Dockerfile does NOT manually install Docker CLI
- Rebuild container completely

## 📚 Documentation

- **Summary**: `.devcontainer/BUILD_FIX_SUMMARY.md`
- **Deep Dive**: `.devcontainer/ARCHITECTURE.md`
- **User Guide**: `.devcontainer/README.md`

## 🎯 Key Files

```
.devcontainer/
├── integrity-check.sh       # Validation script
├── devcontainer.json        # Docker-in-docker feature
├── Dockerfile               # Clean build (no manual Docker CLI)
├── BUILD_FIX_SUMMARY.md     # This fix explained
├── ARCHITECTURE.md          # Technical deep dive
└── README.md                # Full documentation
```

## ✨ Success Indicators

- ✅ Build completes without errors
- ✅ `docker --version` works inside container
- ✅ Integrity check shows all green checkmarks
- ✅ No "docker group does not exist" error

## 🔄 Workflow

```
Trigger rebuild
    ↓
integrity-check.sh runs
    ↓
Validates git/poetry/docker
    ↓
Auto-fixes Poetry drift
    ↓
Purges stale cache
    ↓
Build proceeds
    ↓
Docker-in-docker feature installs CLI
    ↓
Container ready ✅
```

---

**Need Help?** See `.devcontainer/README.md` or `.devcontainer/ARCHITECTURE.md`
