---
aliases:
  - Untitled 5
title: Crucial Update - TASK_TEMPLATE
---

### **Crucial Update to `TASK_TEMPLATE.md`** 
To make that automatic dashboard work, we need to add **one line** to our existing `TASK_TEMPLATE.md` frontmatter. This links a child task back to its parent plan. The new line is `plan:`.

```markdown
 --- 
 id: <% tp.date.now("YYYYMMDD") %>- 
 title: "<% tp.file.title %>" 
 status: backlog 
 implementer: SigmaDev11 
 reviewer: Gemini 
 plan: "[[YYYYMMDD_TASK_PLAN_TITLE]]" <-- THE NEW LINE 
 roadmap: 
 ... 
 ---