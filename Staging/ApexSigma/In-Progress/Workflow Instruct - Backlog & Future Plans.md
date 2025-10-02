---
aliases:
  - Untitled 16
title: Workflow Instruct - Backlog & Future Plans
---
We've designed the factory floor for active production, but we haven't designated the warehouse for raw materials and future orders. If we don't have a system for the backlog, it'll just become a chaotic pile in the corner.

You're thinking about the full lifecycle, which is exactly right.

We don't need new templates. The ones we have are perfect. The `status` field is the key. We just need to define the **process** and the **view** for handling things that aren't active yet.

The solution is simple and clean.

---

### **1. The "Icebox" - A Designated Place for Future Work**

We create a dedicated folder at the top of our vault, let's call it **`00_ICEBOX`**.

This folder is the official "dumping ground" for any new idea.

- Got a random idea for a single task? Create a new `TASK_TEMPLATE` note, leave the status as `backlog`, and save it in the `00_ICEBOX`.
    
- Thinking about a potential future project? Create a new `TASK_PLAN_TEMPLATE` note, set the status to `Planning` or even a new status like `Future`, and save it in the `00_ICEBOX`.
    

This keeps our active folders (`01_Tasks`, `02_Plans`) clean and focused only on what we're actually committed to right now.

---

### **2. The "War Room" - A Master Backlog Dashboard**

This is the most important part. We create a new dashboard note, `_MASTER_BACKLOG.md`, that _only_ looks inside the `00_ICEBOX` folder. It becomes our single view of all potential future work, neatly separated.

Paste this into `_MASTER_BACKLOG.md`:

Markdown

````
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
````

### The Workflow is Now Complete:

1. **Capture:** Any new idea, big or small, gets created from a template and dropped into the `00_ICEBOX`. You don't have to think about it; just get it out of your head.
    
2. **Review:** Periodically (e.g., once a week), we look at the `_MASTER_BACKLOG.md` dashboard. This is our strategic review meeting.
    
3. **Promote:** When we decide to commit to a plan or a set of tasks, we simply:
    
    - Update the `status` from `Planning` to `Active` or from `backlog` to `todo`.
        
    - Move the file(s) from the `00_ICEBOX` to the `01_Tasks` or `02_Plans` folder.
        

They will instantly disappear from the Master Backlog dashboard and appear on our active Kanban/Dashboard views.

This system separates the signal from the noise. It gives us a safe place to put all our future ideas without them cluttering the work we need to focus on _right now_.