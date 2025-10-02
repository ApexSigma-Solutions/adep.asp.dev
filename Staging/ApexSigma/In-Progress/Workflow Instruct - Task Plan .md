---
aliases:
  - Untitled 15
title: "Workflow Instruct - Task Plan "
---
I'll lay out the battle plan. When you get to your machine, this will be your step-by-step guide.

We will use three essential community plugins to achieve this. Think of them as the core components of our factory floor:

1. **Templater:** This makes our templates "smart." It can automatically fill in dates, times, and other dynamic information.
    
2. **QuickAdd:** This is the magic button. It will give us a single command or a clickable icon to run our "New Task" workflow.
    
3. **Dataview:** This is our dashboard. It will automatically scan all our task notes and create dynamic lists, like a "To-Do" list that is always up-to-date.
    

---

### **Phase 1: Forge the Smart Template (with Templater)**

First, we'll upgrade the `TASK_TEMPLATE.md` we designed. We'll tell Templater to auto-fill the boring stuff.

Your current template looks like this:

Markdown

```
---
id: YYYYMMDD-000
title: "A Clear and Concise Title"
status: backlog
...
created: 2025-09-22
updated: 2025-09-22
---
...
```

We'll change it to use Templater's syntax. Create this file in a folder, let's say `00_Templates/TASK_TEMPLATE.md`:

Markdown

```
---
id: <% tp.date.now("YYYYMMDD") %>-
title: "<% tp.file.title %>"
status: backlog
implementer: SigmaDev11
reviewer: Gemini
roadmap:
domain:
tags: []
dependencies: []
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
---

### Objective
*A one-sentence summary of the desired outcome.*

### Description
*A detailed breakdown of the task. What is the problem? What is the proposed solution?*

### "Done means Done" Criteria
- [ ] Criterion 1 is met.
- [ ] Criterion 2 is met and tested.
- [ ] All relevant documentation is updated.
- [ ] The plan has passed Mandatory Agent Review (MAR).

### Notes
*Any additional thoughts, links, or context.*
```

**What this does:** When you create a new note from this template, Templater will automatically fill in the `id` with the current date, set the `title` to whatever you name the file, and fill in the `created` and `updated` dates.

---

### **Phase 2: Build the "New Task" Shortcut (with QuickAdd)**

Now we'll create the trigger. This will give you a single command to create a new task.

1. Install the **QuickAdd** plugin and open its settings.
    
2. Choose **"Template"** as your choice type and click "Add Choice".
    
3. Name it something clear, like **`⚡ New Task`**.
    
4. Point it to the `TASK_TEMPLATE.md` file we just created.
    
5. **Crucially**, turn on the setting that says **"Create file in folder"** and choose a folder like `01_Tasks/`. This keeps everything organized.
    
6. You can also set the file name format. A good one is `<% tp.date.now("YYYY-MM-DD") %> - {{VALUE}}`, where `{{VALUE}}` will be the task title you type in.
    
7. Save it, then click the lightning bolt icon next to your new command. This adds it to the command palette and the sidebar, giving you a one-click icon to create a new task.
    

Now, you click that icon, a box pops up asking for the task title, you type it in, hit enter, and **BAM**. A new, perfectly formatted task note is created in the right folder with all the metadata pre-filled.

---

### **Phase 3: The Command Center (with Dataview)**

This is the payoff. Create a new note called `_KANBAN_BOARD.md` or `_DASHBOARD.md`. In this file, you can now create live, automated views of all your tasks.

Paste this into the file:

Markdown

````
### To-Do
```dataview
TABLE implementer, reviewer, roadmap
FROM "01_Tasks"
WHERE status = "todo"
SORT created ASC
```

### In Progress
```dataview
TABLE implementer, reviewer, roadmap
FROM "01_Tasks"
WHERE status = "in-progress"
SORT updated DESC
```

### In Review (MAR)
```dataview
TABLE implementer, reviewer, roadmap
FROM "01_Tasks"
WHERE status = "mar"
SORT updated DESC
```
````

This will give you three lists that automatically update whenever you change the `status` field in any of your task files.

This setup gives you a frictionless workflow: one click to create a task, and one central dashboard to see the entire state of the project. It's a system built for speed and clarity.