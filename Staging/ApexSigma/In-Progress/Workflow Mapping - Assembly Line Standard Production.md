---
aliases:
  - Untitled 18
  - Workflow - Assembly Line Standard Production
title: Workflow Mapping - Assembly Line Standard Production
---
Let's get this mapped out. A set of templates is useless without a clear, universally understood process for how they move through the system. This is the playbook for the entire operation.

I'll break it down into the three core processes we've defined. Think of them as the different factory lines in our facility.

---

### **1. The Assembly Line: Standard Production Workflow**

_This is the primary workflow for turning a plan into a tangible, finished product._

**Metaphor:** A car assembly line. From chassis to final inspection.

**Flowchart:**

1. **`[PLANNING]`** -> A new **Task Plan** is created in `02_Plans` (or promoted from the `ICEBOX`).
    
    - **Status:** `Active`
        
    - **Artifact:** `TASK_PLAN_TEMPLATE.md`
        
2. **`[DEFINITION]`** -> Individual **Tasks** are created in `01_Tasks` and linked to the plan.
    
    - **Status:** `todo`
        
    - **Artifact:** `TASK_TEMPLATE.md`
        
3. **`[IMPLEMENTATION]`** -> Implementer pulls a task and begins work.
    
    - **Status Change:** `todo` -> `in-progress`
        
4. **`[HANDOFF]`** -> Implementer finishes, creates a report, and submits for review.
    
    - **Status Change:** `in-progress` -> `mar`
        
    - **Artifact:** `IMPLEMENTATION_REPORT.md` is created and linked.
        
5. **`[REVIEW]`** -> Reviewer conducts the Mandatory Agent Review.
    
    - **Artifact:** `MAR_REVIEW.md` is created and linked.
        
6. **`[VERDICT]`** -> The decision is made.
    
    - **IF APPROVED:**
        
        - `MAR_REVIEW` Status -> `APPROVED`
            
        - `TASK` Status -> `done`
            
        - **-> END OF TASK**
            
    - **IF REJECTED:**
        
        - `MAR_REVIEW` Status -> `REJECTED` (with feedback)
            
        - `TASK` Status -> `in-progress`
            
        - **-> GOTO STEP 3 `[IMPLEMENTATION]`**
            
7. **`[COMPLETION]`** -> Once all linked tasks are `done`, the parent **Task Plan** is marked as complete.
    
    - **Status Change:** `Active` -> `Completed`
        

---

### **2. The Laboratory: R&D / Spike Workflow**

_This workflow is for investigation, not production. The output is knowledge, not a feature._

**Metaphor:** The scientific method. From hypothesis to conclusion.

**Flowchart:**

1. **`[QUESTION]`** -> A research question is identified. A new **Spike** is created in `03_RnD`.
    
    - **Status:** `Researching`
        
    - **Artifact:** `SPIKE_TEMPLATE.md`
        
    - **Constraint:** A strict `timebox` is defined.
        
2. **`[INVESTIGATION]`** -> The owner conducts the research within the timebox, documenting all findings.
    
3. **`[CONCLUSION]`** -> The owner answers the research question and makes a formal recommendation in the note.
    
4. **`[OUTCOME]`** -> The recommendation determines the next step.
    
    - **IF "CREATE TASK PLAN":**
        
        - The spike has proven a path forward.
            
        - **-> TRIGGER: Standard Production Workflow (Step 1)**
            
    - **IF "CREATE ADR":**
        
        - The findings require a formal, architectural decision.
            
        - **-> TRIGGER: Architectural Decision Workflow (Step 1)**
            
    - **IF "ARCHIVE":**
        
        - The path is not viable. The spike is a dead end.
            
        - `SPIKE` Status -> `Archived`
            
        - **-> END OF SPIKE** (The documented failure is itself a valuable asset)
            

---

### **3. Passing a Law: Architectural Decision Workflow**

_This workflow is for codifying significant, system-wide decisions._

**Metaphor:** Passing a bill into law. From proposal to ratification.

**Flowchart:**

1. **`[PROPOSAL]`** -> The need for a binding decision is identified.
    
    - **Status:** `Proposed`
        
    - **Artifact:** `ADR_TEMPLATE.md` created in `04_ADR`.
        
2. **`[DEBATE]`** -> The team discusses the context, trade-offs, and consequences outlined in the ADR.
    
3. **`[RATIFICATION]`** -> A final decision is reached.
    
    - `ADR` Status -> `Accepted`
        
4. **`[ENFORCEMENT]`** -> The ADR is now considered "law." All future `Task Plans` and `Tasks` that fall within its domain must adhere to it and should link to it for context.
    

---

These three workflows cover every type of intellectual work in our system. They provide a clear, unambiguous path for any idea, ensuring nothing gets lost and everything is documented. This is the machine. Now we just need to run it.