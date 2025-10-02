---
title: '"<% tp.file.title %>"'
noteTYPE: taskPLAN
roadmap:
taskplanID: <% tp.date.now("YYYYMMDD") %>
status: Planning | Active | Completed | On-Hold
priority: Critical | High | Medium | Low
owner: "[[@SigmaDev11]]"
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - TaskPlan
aliases:
  - Untitled 6
---


## 🎯 Objective
*A single, clear sentence describing the desired outcome of this plan. What will be true when this is done?*

###  Kontext
*Why are we doing this? What is the problem or opportunity this plan addresses?*

###  scope
#### In Scope
-
-

#### Out of Scope
-
-

### ✅ "Done Means Done" Criteria
*What are the high-level conditions that prove this entire plan is complete?*
- [ ] All linked tasks are `done`.
- [ ] The objective has been met and verified.
- [ ] A final review/demo has been completed.

---
## 📝 Linked Tasks

### Todo
```dataview
TABLE implementer, reviewer
FROM "01_Tasks"
WHERE plan = this.file.link AND status = "todo"
SORT created ASC
```
### In-Progress
```dataview
TABLE implementer, reviewer
FROM "01_Tasks"
WHERE plan = this.file.link AND status = "done"
SORT updated DESC
```
### Done
```dataview
TABLE implementer, reviewer 
FROM "01_Tasks" 
WHERE plan = this.file.link AND status = "done" SORT updated DESC
```
--- 
### **Crucial Update to `TASK_TEMPLATE.md`** 

To make that automatic dashboard work, we need to add **one line** to our existing `TASK_TEMPLATE.md` frontmatter. This links a child task back to its parent plan. 

The new line is `plan:`.

 ```markdown
 id: <% tp.date.now("YYYYMMDD") %>-
 title: "<% tp.file.title %>" 
 status: backlog 
 implementer: SigmaDev11 
 reviewer: Gemini 
 plan: "[[YYYYMMDD_TASK_PLAN_TITLE]]"
 roadmap:
 ```
 ---
 