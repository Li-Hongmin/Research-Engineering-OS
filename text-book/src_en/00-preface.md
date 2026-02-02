# Preface

![Illustration](images/00_preface_thinking.png)

The AI era has further blurred the boundary between research and development: from formulating hypotheses, building prototypes, and running experiments, to solidifying results into a reproducible chain of evidence—all of this is now completed within shorter cycles. Meanwhile, AI coding assistants have made it easier than ever to “write code that runs,” yet they have also made it harder to “write research code that is trustworthy, traceable, and reproducible.”

I wrote *Research Engineering OS* not to offer yet another abstract “methodology,” but to compress the pitfalls I have repeatedly encountered in academic machine learning / computational biology research into a set of executable default behaviors: use **standards** to reduce rework, use **templates** to lower collaboration costs, and use **checklists** to proactively absorb, within the daily rhythm, risks that would otherwise explode only at the final stage.

The central thesis of this short book is straightforward: **exploration can be wild, but outputs must be cleanable; conclusions may be temporarily fragile, but the chain of evidence must be solid.** You may iterate quickly, but you must leave enough information for every “apparently effective” result so that it can still be reproduced, questioned, and validated a week later, a month later, or on a different machine.

Accordingly, this book will repeatedly emphasize three things:

- **Experiments are the minimal unit:** what you record is not “which code was changed,” but “which versions and configurations constitute this experiment.”

- **Default automatic traceability:** make run_id, commit, config, data versions, and environment summaries part of the pipeline.

- **Front-load DoD and checklists:** decompose the rigor demanded at the paper-writing stage into small actions executable in everyday work.

If the work you are doing belongs to “research development” in the AI era—where you must maintain exploratory speed, remain accountable for results, and communicate efficiently with collaborators—I hope this book can serve as a minimal operating system beside your desk.

<div style="text-align: right; margin-top: 2em;">

**Li Hongmin (李鸿敏)**<br>
Department of Computational Biology and Medical Sciences<br>
Graduate School of Frontier Sciences, The University of Tokyo<br>
5-1-5 Kashiwanoha, Kashiwa-shi, Chiba 277-8561, Japan<br>
[li-hongmin.github.io](https://li-hongmin.github.io)<br>
[lihongmin@edu.k.u-tokyo.ac.jp](mailto:lihongmin@edu.k.u-tokyo.ac.jp)

</div>