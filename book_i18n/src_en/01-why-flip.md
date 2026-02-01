# Why Do You Always Overturn Everything at the End (Exploration Debt / Validation Debt / Reproducibility Debt)
## Story Setup: With Only a Few Days Left Before the Deadline, You Suddenly Stop Trusting Your Results

![截止日期恐慌](images/comics/01_deadline_panic.png)
Imagine this scenario: only a few days remain before the paper deadline. After finally finishing all experiments, you are about to write the conclusions. But then doubt creeps in: perhaps a key experiment has not been validated under another data split? Perhaps a baseline was run unfairly? You decide to be cautious and rerun it.

Then the nightmare happens: after rerunning, the metrics differ from before. A method that was previously “significantly better” is suddenly no longer clearly ahead; or you find that changing the random seed makes the result drop. Cold sweat breaks out—months of work feel as if they were built on sand. With an imminent DDL (deadline) on one side and conclusions that no longer hold on the other, you are forced to overturn everything and start over.

Does this kind of “late-stage explosion” feel familiar?

## Why This Happens: Three Types of Debt Explode in the Late Stage

![三类债务](images/comics/01_three_debts.png)
Why is it that at the very last moment—“about to write the paper / about to defend / about to submit”—we suddenly discover that our results do not hold, and we have to overturn and redo everything?

This is not an isolated case. My observation is that it is usually not caused by a single-point bug, but by **three types of debt** that are tacitly accumulated early and then explode collectively later—exploration debt, validation debt, and reproducibility debt.

In other words, in order to save effort during the research process, we accumulate a great deal of “debt,” and only at the end are we forced to repay it all at once. The purpose of this book is to decompose this last-minute, fire-under-the-feet rework into small, manageable daily steps, so that the tragedy does not repeat.

## Symptom Checklist: You May Be Heading Toward a Final Overturn

![症状自查](images/comics/01_04_symptoms.png)
If the following symptoms feel familiar, you are likely accumulating research debt without realizing it, laying the groundwork for a final-stage “explosion”:

- **Your conclusions require “storytelling” to be self-consistent:** You can explain why it works, but cannot clearly state under what conditions it fails; you rarely proactively discuss negative results and boundary conditions.

- **Results are extremely sensitive to environment/random seeds:** Switching machines, changing a driver version, or using a different random seed causes the metrics to drift unpredictably.

- **No single “clean mainline” runs end-to-end:** There are many branches, scripts, and outputs, but you cannot go from preprocessing to the paper’s main metrics with a single command.

- **Incomplete controls:** Baselines are not strong enough, evaluation protocols are inconsistent, key ablations are missing, and failure cases are not explained.

- **Figures depend on manual operations:** Tables and curves rely on copy-paste/manual run selection; once source data updates, everything must be redone by hand, so the closer you get to the deadline, the less you dare to touch anything.

- **You start to fear rerunning:** You vaguely know that if you rerun, the results may not match your memory—or may not be recoverable at all.

The more boxes you tick, the more you are borrowing from the future: trading convenience now for high-pressure rework at the end.

## A Common Plot: Why “Late-Stage Explosion” Is Almost Inevitable

![最后阶段混乱](images/comics/01_last_minute_chaos.png)
Looking back at the trajectory of many projects, one finds that a “late-stage explosion” is almost inevitable. The plot often goes like this:

1. **Early sprint:** To see a signal as quickly as possible, you cobble together code in the fastest—but not necessarily disciplined—way: if you can edit a script directly, you do not create a new module; parameters are hard-coded; experimental outputs are scattered everywhere... In short, you just make it run first.

2. **Signal appears:** You see a curve that “looks good,” so you keep stacking tricks, adjusting data splits, and modifying training details to push the metric a bit higher; meanwhile, you postpone control experiments and organization work.

3. **Paper pressure hits:** You suddenly need reproducible main results, complete baselines, and interpretable ablation analyses; you start filling in these validations.

4. **System collapse:** As soon as you try to fill them in, things break: results are unstable, baselines catch up, hidden bugs or data leakage are exposed; you realize you cannot answer questions like “Is it accidental? Is there leakage? Does it only work for a particular seed?”

The key issue is not that “exploration should not be fast”—exploration can certainly be fast. But speed presupposes that what follows is **cleanable and traceable**. Otherwise, the faster you run, the more leverage you apply to accumulate debt, and the higher the risk of crashing at the end.

## Explanatory Model: Three Types of Debt
To explain the above issues more systematically, we introduce the concept of “debt.” Similar to technical debt in software engineering, research work can also incur different forms of debt—exploration debt, validation debt, and reproducibility debt.

### Exploration Debt

![探索债](images/comics/01_05_exploration_debt.png)
**Definition:** To iterate faster, we temporarily take nonstandard shortcuts in code and experimental workflows; the accumulated burden of these expedients is exploration debt. Exploration debt is not inherently evil, provided that it is **cleanable, discardable, and recoverable**.

**Typical signals:**

- A proliferation of “temporary scripts”: `test.py`, `try1.ipynb`, `debug_old.py`... no one dares to delete them.

- Chaotic output directories: `outputs/` is filled with folders like `final_final2/`, `exp_new_try/`, with unclear relationships.

- The same logic is copy-pasted and modified in multiple places; the codebase feels stitched together, and any change triggers cascading effects.

**Real cost:** When you need to converge onto a mainline, you cannot extract a clean path: you cannot tell what the final method needs versus what is a dead end; you have also likely forgotten how certain results were obtained.

### Validation Debt

![验证债](images/comics/01_06_validation_debt.png)
**Definition:** To prove that something “works” as quickly as possible, we skip the control experiments and rigorous tests that should have been done; these skipped validations must be paid back sooner or later, and the closer you are to publication, the higher the cost.

**Typical signals:**

- Baselines are not strong enough, or they do not share the same evaluation protocol as the method (not directly comparable).

- Missing ablations: you do not know which change contributes the main gain.

- Inconsistent metric definitions: thresholds/post-processing/data filtering differ across runs.

**Real cost:** Your claims cannot withstand scrutiny: reviewers often ask not for a “larger model,” but for “more rigorous controls and analysis.”

### Reproducibility Debt

![复现债](images/comics/01_07_reproducibility_debt.png)
**Definition:** To obtain results quickly, we fail to promptly freeze the environment, data versions, hyperparameter configurations, and sources of randomness; as a result, **the same code may not reproduce the same conclusion**.

**Typical signals:**

- You remember a run that performed very well, but cannot find the corresponding commit/config/seed/data version.

- Dependency drift: it ran yesterday, but today installing some package breaks it or causes a major performance drop.

- Training scripts are full of implicit defaults and hard-coded values: others (including your future self) cannot identify the key hyperparameters.

**Real cost:** Reproducibility debt takes away your initiative at the most critical moment: you cannot confidently answer “Are the results stable/reproducible?”, nor can you calmly handle paper checks and reproduction experiments.

## Chapter Conclusion: Default Behaviors, Not Complex Tools

When people encounter these problems, they often place their hopes on more complex toolchains. This chapter emphasizes instead: what you need is not more complex tools, but a set of good **default behaviors**.

In the AI era, the barrier to code generation is decreasing, but the cost of validation and reproducibility has not decreased accordingly; it may even **increase in relative terms** because iteration is faster.

Rather than relying on heavy post hoc remediation, it is better to cultivate lightweight default habits in daily research and keep debt at a minimum:

- **Any “promising” result must be rerunnable (at least once):** first confirm it is not an accidental fluctuation.

- **Any change that affects conclusions must be explainable as a controlled experimental difference:** change one thing, test one thing; control variables.

- **Any exploration path must be discardable:** archive what is valuable, clean what is not, and keep the mainline clean.

## Principles of This Book (Ideas That Run Through Subsequent Chapters)

- **Small, verifiable steps:** each iteration introduces only one interpretable variable change; prioritize ensuring the system can run and be tested.

- **Mandatory traceability:** commit, config, seed, data version, and environment summary are all treated as part of the experimental artifact.

- **Stability/Exploration Isolation:** The stable mainline is used to ensure paper reproducibility; the exploration branch is used for rapid trial-and-error, with linkage established via checklist-based acceptance.

## 10-Minute Actions You Can Do Right Now

![10分钟行动](images/comics/01_08_ten_min_action.png)
If you do only one thing right now: create a **reproducible minimal entry point** for the current best result.

1. **Centralize Outputs:** Assign a `run_id` to the best experiment and consolidate key outputs into the corresponding directory.

2. **Archive the Configuration:** Create a minimal config file and write down the key hyperparameters.

3. **Record the Fingerprint:** Note the commit, seed, data version, and major dependency versions (even if handwritten for now).

4. **Re-run Independently:** Re-run once in a new terminal/new process using that config, and confirm the result returns to the same order of magnitude.

If it goes smoothly, you obtain a reusable template; if not, you surface problems early—there is still time to fix them now.

Subsequent chapters will expand these 10-minute actions into a sustainable Research Engineering OS.