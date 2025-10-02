---
aliases:
  - Untitled 4
title: Master Backlog & Future Plans
---
# Master Backlog & Future Plans

## Future Plans (In Planning)
*High-level initiatives and sprints we are considering for the future.*
```dataview
TABLE owner, created
FROM "00_ICEBOX"
WHERE file.name != this.file.name AND contains(status, "Planning") OR contains(status, "Future")
SORT created ASC
```

## Task Backlog
*Granular tasks that have been captured but not yet prioritized into an active plan.*
```dataview
TABLE status, roadmap, domain
FROM "00_ICEBOX"
WHERE contains(status, "backlog")
SORT created ASC
```
