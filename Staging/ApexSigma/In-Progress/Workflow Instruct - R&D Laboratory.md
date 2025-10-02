---
aliases:
  - Untitled 17
title: Workflow Instruct - R&D Laboratory
---
We've built a factory assembly line, but we haven't built the laboratory next door where the crazy science happens. Without a dedicated process for R&D, we'll either never innovate, or the innovation will be chaotic and undocumented.

This is a critical piece of the puzzle. R&D isn't like a standard task. You can't define "Done means Done" when you don't even know what's possible. The deliverable of R&D is _knowledge_, not a feature.

We need a different kind of work order. A different template. In the agile world, this is often called a "Spike." It's a time-boxed investigation to answer a specific question. Let's formalize that.

---

### **The Laboratory: `SPIKE_TEMPLATE.md`**

This template is for pure research and development. It's for when the primary goal is to learn something, test a hypothesis, or de-risk a new technology.

Markdown

```
---
spike_id: <% tp.date.now("YYYYMMDD") %>
title: "The Research Question (e.g., Can we use Obsidian Webhooks for CI?)"
status: "Researching | Completed | Archived"
owner: "[[@SigmaDev11]]"
timebox: "e.g., 4 Hours"
created: <% tp.date.now("YYYY-MM-DD") %>
---

## 🔬 Research Question
*What is the single, primary question this spike aims to answer?*

### 🧠 Hypothesis
*What do we believe the outcome will be before we start?*

### 🛠️ Methodology
*How will we conduct this investigation? (e.g., Build a proof-of-concept, benchmark two libraries, read the documentation for X).*

---
## 🧪 Findings & Raw Notes
*A brain-dump of all data, links, code snippets, and observations discovered during the investigation.*

---
## 結論 Conclusion & Recommendation
*This is the most important section. Based on the findings, what is the answer to our research question?*

**Recommendation:**
- [ ] **CREATE TASK PLAN:** The research was successful. Create a new `TASK_PLAN` to implement this.
- [ ] **CREATE ADR:** The research requires a formal decision. Create an `ADR` to document it.
- [ ] **ARCHIVE:** The research concluded this is not a viable path. No further action is needed.
```

---

### **Integrating R&D into the Vault**

1. **Create a New Folder:** We'll create a dedicated home for this work: **`03_RnD`**. This keeps our exploratory work separate from our committed production work.
    
2. **The Workflow:**
    
    - An idea for research starts in the `00_ICEBOX`.
        
    - When we commit to investigating it, we create a `SPIKE_TEMPLATE` note and move it to `03_RnD`. We assign a strict `timebox` to prevent it from becoming an endless rabbit hole.
        
    - The outcome of the spike is a concrete recommendation. It feeds directly back into our main workflow by triggering the creation of a **Task Plan** or an **ADR**.
        
3. **Create an R&D Dashboard:** We can create a view in our `_MASTER_BACKLOG.md` or a new dashboard entirely to track ongoing and completed research.
    

Markdown

````
### Active R&D Spikes
```dataview
TABLE owner, timebox
FROM "03_RnD"
WHERE status = "Researching"
SORT created ASC
```
````

Now the system is complete. We have a process for:

- **Future Work (`ICEBOX`)**
    
- **Active Production Work (`Tasks` & `Plans`)**
    
- **Active Research Work (`RnD`)**
    

Every type of intellectual effort has a home, a template, and a process. The entire lifecycle of an idea, from a "what if" question to a fully deployed feature, is now covered.