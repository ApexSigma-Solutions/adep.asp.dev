---
aliases:
  - Untitled 19
title: ObsidianToApexSigma - Webhook Automation
---
That's the other half of the fucking feedback loop. You've nailed it.

- **Phase 3 (The Mind of Odin)** was about getting data _into_ the vault automatically.
    
- **Phase 4 (The Einherjar Protocol)** is about triggering actions _from_ the vault.
    

You're thinking about how to connect the state of a task note in your local vault to the state of the real world—the CI/CD pipeline, the GitHub repo, the Linear ticket.

Just like receiving webhooks, Obsidian doesn't _send_ them natively. But, again, we can forge the tools to make it happen. The key is a different plugin: **Obsidian Shell Commands**.

---

### **The Outbound Trigger: Forging the "Big Red Button"**

This plugin lets us create custom commands inside Obsidian that can run any script on our local machine. This is fucking brilliant because it means we can write a simple script that does two things:

1. Reads the metadata from the current task note.
    
2. Uses `curl` to fire a webhook to any service we want.
    

**Here's the workflow for submitting a task for review. This is how we automate the handoff:**

1. **The Human Trigger:** You've finished your work on `TASK-123`. The `status` is `in-progress`. You open the command palette in Obsidian and run a custom command we'll create called: `🚀 Submit for MAR`.
    
2. **The Plugin Action:** The **Shell Commands** plugin executes a script we'll write, `submit_for_review.sh`. It passes the path of the current note to the script.
    
3. **The Script's Job:** The `submit_for_review.sh` script wakes up and:
    
    - **Reads the note:** It parses the YAML frontmatter of `TASK-123.md` to get the `task_id`, `implementer`, `reviewer`, and maybe a `github_pr_link`.
        
    - **Fires the Webhook:** It uses `curl` to send a POST request to our webhook service (the one we planned in Phase 4). The JSON payload looks something like this:
        
        JSON
        
        ```
        {
          "event": "MAR_SUBMISSION",
          "task_id": "TASK-123",
          "pr_link": "http://github.com/...",
          "implementer": "SigmaDev11",
          "reviewer": "Gemini"
        }
        ```
        
    - **Updates the Note:** As its final act, the script can even modify the local file, changing the `status` from `in-progress` to `mar`.
        
4. **The Automation Cascade:** Our external webhook service catches this and kicks off the real-world automation:
    
    - It posts a comment on the GitHub PR: "@Gemini, this PR is now ready for your review."
        
    - It updates the Linear ticket's status to "In Review."
        
    - It pings the Reviewer Agent (Qwen/Gemini) to begin its analysis.
        

This is the very definition of the **Einherjar Protocol**. It's a human-initiated, machine-executed workflow. You're not just changing a line of text in a markdown file; you're launching a missile. You're giving the order, and the automated systems are carrying it out.