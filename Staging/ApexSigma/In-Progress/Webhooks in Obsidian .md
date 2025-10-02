---
aliases:
  - Untitled 20
title: "Webhooks in Obsidian "
---
No. And this is a critical fucking distinction. It's a logical question to ask because the name is identical, but they do the exact opposite jobs. It's the difference between an ear and a mouth.

- The **Obsidian Webhooks** plugin gives your vault a phone number so it can **receive** calls.
    
- It does **not** give it a dial pad to **make** calls.
    

Let me break it down.

---

### **INBOUND vs. OUTBOUND**

**1. The `Obsidian Webhooks` Plugin (INBOUND 📥)**

- **Purpose:** To listen for incoming data from the outside world.
    
- **How it works:** It starts a local server and waits for a service like GitHub to send it information. It is passive. It's a catcher's mitt.
    
- **Use Case:** This is what we use for **Phase 3: The Mind of Odin**. It's how we will automatically create notes when a GitHub Action finishes. The data flows _from_ GitHub _to_ Obsidian.
    

`GitHub -> Webhook -> Obsidian`

**2. Our Requirement: The `Shell Commands` Plugin (OUTBOUND 📤)**

- **Purpose:** To trigger an action in the outside world from _inside_ Obsidian.
    
- **How it works:** You, the user, run a command. The plugin executes a script that actively sends data out. It is active. It's throwing the fucking ball.
    
- **Use Case:** This is what we need for **Phase 4: The Einherjar Protocol**. It's how you will click a button in Obsidian to tell our CI/CD pipeline that a task is ready for review. The data flows _from_ Obsidian _to_ GitHub.
    

`Obsidian -> Command -> Webhook -> GitHub`

---

### **The Verdict**

It's not simpler because it's the wrong tool for the job. It's like trying to use a screwdriver to hammer a nail.

To build the full, two-way automated system we've designed, we need **both**.

- **`Webhooks`** is the ear. It listens for automated reports.
    
- **`Shell Commands`** is the mouth. It gives the orders.
    

We're building a full command-and-control center. It needs to be able to both receive intelligence and issue commands. One plugin for each direction. That's the architecture.