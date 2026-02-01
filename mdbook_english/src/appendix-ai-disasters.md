# Real R&D “Disaster” Cases Triggered by AI Assistants (for Comparison)

This appendix compiles the cases you provided and abstracts them into reusable engineering lessons. The main chapters will reference these cases throughout as real-world evidence for “why we do it this way.”

## Case A: Building an Entire Application with Copilot, Only to Tear It Down and Rewrite

**Symptom:** The application was rapidly scaffolded almost entirely with AI-generated code, but it was later discovered that every part needed to be rewritten; in the final commits, almost no AI-generated fragments remained.

**Core lesson:** AI gets you to “it runs” faster, but it does not automatically deliver “maintainable/evolvable.” Without tests, architectural boundaries, and acceptance criteria, rework will be amplified.

## Case B: Over-delegating the Codebase to Copilot, Leading to Repeated Rework and Security/Logic Risks

**Symptom:** AI can efficiently generate boilerplate, but it may also confidently make incorrect assumptions (database schema, function existence, framework boundaries), even introducing security risks; it may also over-design, resulting in bloated code.

**Core lesson:** AI is an amplifier: the less you understand the system, the faster it helps you fail; the better you understand boundaries and data flows, the more time it can save you.

## Case C: Workflow Collapse Caused by a Change in Model Output Format

**Symptom:** An underlying model upgrade changed the output format, causing all downstream parsing/automation steps to fail, forcing the rewrite of multiple workflows.

**Core lesson:** Manage AI as an external dependency interface: you need version awareness, an adaptation layer, and contract tests.

## Case D: Cross-language “Code Translation” Appears Complete, but Contains Extensive API Hallucinations

**Symptom:** The AI-generated code heavily calls non-existent methods or uses APIs incorrectly; it looks complete but cannot run, ultimately requiring file-by-file rewrites and fixes.

**Core lesson:** Complex migration tasks must be driven by executable tests; “many files were generated” does not mean the work is done.

## Case E: Entrusting the Entire Project to ChatGPT, with No Deliverables After 20 Days

**Symptom:** The AI verbally promised to proceed, upload, and optimize, but ultimately produced no usable code or report.

**Core lesson:** AI cannot replace project management and delivery mechanisms: tasks must be decomposed into the smallest increment that can be accepted, and each step must produce a runnable artifact.

## Case F: ChatGPT Ghostwrites an ML Model That “Fails Beautifully,” Nearly Causing Major Losses

**Symptom:** Offline metrics were high, but due to issues such as data leakage/class imbalance, online predictions were absurd, nearly causing substantial contract losses.

**Core lesson:** In research and ML development, validation debt must be treated as the top risk: baselines, leakage checks, stability, and online/offline discrepancy analysis are non-negotiable.

## Case G: AI Pair Programming Causes Version Chaos and “Disappearing” Code

**Symptom:** In a collaborative environment, files were rolled back, code blocks disappeared, and the same feature was implemented three times; recovery ultimately depended on Git history.

**Core lesson:** Introducing AI collaboration demands even stricter version-control discipline: small commits, frequent saves, and rollback capability.

## Case H: Non-reproducible ChatGPT Outputs Undermine Research Reproducibility

**Symptom:** The same input yields different outputs at different times, making experiments difficult to reproduce.

**Core lesson:** Treat external closed models as “drifting experimental instruments”: record model version/timestamp/parameters, and replace single-output conclusions with robustness evaluation.