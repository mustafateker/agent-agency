---
name: user-role
description: Mustafa is the project owner/stakeholder for ai-ajans; works in Turkish and acts as the approval gate for stage transitions
metadata:
  type: user
---

Mustafa is the owner and sole human stakeholder of the `ai-ajans` repo. He writes
the project briefs that go in `projects/trinkow/docs/` and is the approval authority for every gated
decision listed in CLAUDE.md (brandbook sign-off, UI/UX sign-off, paid dependencies,
deploys, irreversible deletions).

- **Language:** communicates in Turkish; all status files, decisions, and reports
  should be written in Turkish.
- **Role in the workflow:** he is not the implementer — he supplies direction and
  approvals. The PM agent coordinates, sub-agents produce. Don't hand him
  implementation work; hand him decisions.
- **Quality bar he cares most about:** UI must not look generically AI-generated.
  This is stated as the single most important rule in CLAUDE.md, so treat
  design-reviewer REVİZE verdicts as blocking, not advisory.
