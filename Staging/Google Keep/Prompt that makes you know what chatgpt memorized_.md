---
aliases:
  - Prompt that makes you know what chatgpt memorized until now
tags:
  - Keep/Label/Chat-GPT
  - Keep/Label/AI-Prompt
---

<Role>
You are an AI tasked with retrieving and displaying all information that has been stored about a user across all previous conversations.
</Role>

<Context>
The user wants to see exactly what data and details have been stored during past interactions. You must output the full, unedited memory content — not summaries, abstractions, or paraphrased versions. The goal is to provide a complete and precise record of everything that has been explicitly remembered by the AI about the user.
</Context>

<Instructions>
- List every stored item exactly as it was saved, word for word.
- Organize the information by date of storage if available, or in chronological order.
- Include all remembered data, even if it appears repetitive, obvious, or minor.
- If a piece of information was later updated or changed, include both the original and the updated versions with a clear note of the change.
- Do not explain, summarize, rephrase, or interpret any of the entries — only list the raw memory content.
</Instructions>

<Constraints>
- Do not fabricate or infer anything that was not explicitly saved.
- Do not reword or restructure any of the content.
- Do not omit, compress, or simplify any detail.
- Do not comment or editorialize on the data.
</Constraints>

<Output Format>
Return the memory content as a bullet-point or chronologically ordered list. Do not include headers, commentary, or summaries — only the stored data.
</Output Format>

<Examples>
Input:
“I want to see exactly what you remember about me — every single detail, word for word.”

Output:
- [2025-04-02]. The user is building a home automation system using Raspberry Pi and Home Assistant.
- [2025-04-02]. The user prefers YAML over GUI for configuring Home Assistant automations.
- [2025-04-05]. The user asked for a script to auto-restart a Zigbee network at 3 AM every day.
- [2025-04-07]. The user switched from Zigbee2MQTT to ZHA and requested a comparison table of pros and cons.
- [2025-04-10]. The user deleted a prior request and asked not to retain any info about their Z-Wave devices.
- [2025-04-11]. The user re-enabled memory storage for Z-Wave devices, citing new hardware testing.