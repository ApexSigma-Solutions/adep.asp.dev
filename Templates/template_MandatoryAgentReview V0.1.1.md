---
review_id: <% tp.date.now("YYYYMMDD-HHmmss") %>
report_id: <% tp.date.now("YYYYMMDD-HHmmss") %>_IMPLEMENTATION_REPORT
reviewer: "[[@Gemini]]"
status: Active | Rejected | Approved
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
aliases:
  - Untitled 8
title: template_MandatoryAgentReview V0.1.1
noteTYPE: marNOTE
---

## Mandatory Agent Review for: <% tp.file.selection() %>

### Verdict: **<+ VERDICT +>**

### Rationale & Feedback
*(Required for REJECTED, optional for APPROVED)*
*Clear, actionable feedback on what needs to be fixed, or confirmation that the work meets the standard.*

### Final Checklist
- [ ] Verified all claims made in the implementation report.
- [ ] Code meets all Valhalla Shield Engineering Standards.
- [ ] The work is approved for merge/deployment.