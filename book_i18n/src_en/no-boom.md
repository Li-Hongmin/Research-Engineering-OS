# Three Proactive Actions to Prevent a Last-Stage Blow-Up

## Story Setup: The Nightmare of One Week Before the Deadline

On Monday morning, you check your calendar and your heart sinks—the paper submission countdown: **7 days**.

You originally planned to do only “final polishing” this week: organize experimental results into figures and tables, write the related work, and check formatting once. It should be easy, right?

But when you start preparing the paper, problems come rushing in like an avalanche:

### Monday: The Main Experiment Cannot Be Reproduced

You want to rerun the main experiment to confirm you did not misrecord the numbers. But after running the script, the results differ from three weeks ago—the accuracy drops from 94.3% to 92.1%.

You panic and begin troubleshooting:

- Did the code change? The Git history is a mess, and you are not sure which version you used back then.

- Did the data change? The data directory contains v1, v2, v3—you cannot remember.

- Did the environment change? Did some dependency library auto-upgrade?

You spend an entire day and still cannot find the cause.

#### Tuesday: The Baseline Turns Out to Be Unfair

Reviewers will certainly focus on your comparison with the baseline. You check carefully and discover a fatal issue: your method uses the latest data preprocessing, but the baseline uses an older version. The evaluation protocol is not consistent at all.

You need to rerun the baseline—but that requires 6 hours of training time.

#### Wednesday: A Key Ablation Study Is Missing

Your advisor reads your first draft and points out: “Your method includes three improvements (A, B, C), but you did not explain how much each contributes. Reviewers will definitely ask.”

You realize you are missing an ablation study. You need to run:

- baseline

- baseline + A

- baseline + B

- baseline + C

- baseline + A + B

- baseline + A + C

- baseline + B + C

- baseline + A + B + C (full method)

Each experiment takes 2 hours; 8 experiments = 16 hours. But you have only 4 days left.

#### Thursday: The Data for Figures Cannot Be Found

You want to generate the paper’s figures, but you discover that the output files for a key experiment are gone—perhaps you accidentally deleted them, or they were lost during some cleanup. You only remember that “the results were good,” but the raw data is gone.

You have no choice but to rerun those experiments.

#### Friday: You Start Questioning Your Life Choices

You have not slept well for three days. Experiments are still running, the paper has not even started, and the figures are not finished. You begin to wonder: **“Why do I always blow up at the last stage?”**

**The answer is simple: because you did not do three things in advance.**

## Why a “Last-Stage Blow-Up” Is Almost Inevitable

Looking back at Chapter 1, we said there are three kinds of debt in research:

- **Exploration debt:** messy code, scattered outputs, unclear paths

- **Validation debt:** weak baseline, missing ablations, unfair comparisons

- **Reproducibility debt:** unfixed environments, incomplete configurations, unclear versions

If these debts accumulate in daily work, the final stage becomes a **concentrated repayment period**. And deadline pressure amplifies every problem:

- Issues you could debug slowly now must be solved immediately

- Experiments you could rerun now cannot be rerun due to lack of time

- Questions you could ask others now go unanswered because everyone is busy

**The harshest truth: if you discover problems only in the last week, in most cases it is already too late to fix them.**

So what should you do? The answer is: **expose problems early, solve them early, or at least know early that they exist.**

## Proactive Action 1: A Weekly “Reproducibility Self-Check” (15 Minutes)

### Why It Matters

**Core idea:** you cannot wait until right before submission to discover that results are not reproducible. You must continuously verify reproducibility in day-to-day work.

If you do a self-check every week, problems will be discovered in the week they appear, rather than accumulating until the end.

### Self-Check Checklist (Finish in 15 Minutes)

#### Item 1: Check Whether This Week’s Most Important Experiment Is Reproducible (5 Minutes)

    # Find this week’s best/most important experiment
    RUN_ID="this week’s best run_id"

    # Check record completeness
    [ ] outputs/$RUN_ID/run.json exists
    [ ] run.json contains git commit
    [ ] run.json contains the config path
    [ ] run.json contains seed
    [ ] run.json contains the data version
    [ ] run.json contains environment information

    # If any item is missing, remediate immediately

#### Item 2: Attempt a Quick Reproduction (5 Minutes)

You do not need to rerun everything (too slow), but you must verify that **the pipeline runs end-to-end**:

    # Quick test with a small dataset
    python train.py \
        --config outputs/$RUN_ID/config.yaml \
        --data_subset 100 \
        --epochs 2 \
        --seed 42

    # Check:
    [ ] starts normally
    [ ] data loads correctly
    [ ] model forward pass is correct
    [ ] loss computation is normal
    [ ] evaluation pipeline is correct

If even this 2-minute test cannot run through, full reproduction will definitely have issues. **Fixing it now is still in time.**

#### Item 3: Check Whether Dependencies Have Drifted (3 Minutes)

    # Save current dependencies
    pip freeze > requirements_$(date +%Y%m%d).txt

    # Compare with last week’s dependencies
    diff requirements_last_week_date.txt requirements_$(date +%Y%m%d).txt

    # If there are changes, record them in CHANGELOG.md

Dependency changes are a common cause of reproducibility problems. Recording them weekly enables rapid localization when issues arise.

#### Item 4: Check Whether Outputs Are Properly Labeled (2 Minutes)

    # Check whether this week’s outputs all have run_id
    ls outputs/

    # Check for temporary directories such as "unnamed", "temp", "test"
    # If any exist, either delete them or give them formal names

Unlabeled outputs are “future traps”—you know what they are now, but you will forget a month later.

### Frequency and Timing of the Self-Check

**Recommended time:** the last 15 minutes on Friday afternoon

**Why Friday?**

- The week’s work is ending, making it easy to review comprehensively

- If you do not work on weekends, you can rest with peace of mind (knowing the project is under control)

- If you find problems, you can address them immediately on Monday

**Special cases:**

- When you obtain results that “look good”: do the self-check immediately; do not wait until Friday

- After modifying core code: do the self-check the same day

- After switching data versions: do the self-check immediately

### Common Pitfalls

#### Pitfall 1: “I remember it anyway; no need to check.”

**Reality:** two weeks later you will forget the details. Memory is unreliable; records are reliable.

#### Pitfall 2: “This is just a test; no need to record it.”

**Reality:** many “just a test” experiments later become the main results in the paper. If you did not record them at the time, you will regret it in the end.

#### Pitfall 3: “It runs, so it should be reproducible.”

**Reality:** “it runs” and “it can be reproduced on another machine/in another environment/two months later” are completely different things.

## Proactive Action 2: A Monthly “Debt Inventory” (30 Minutes)

### Why It Matters

The weekly self-check addresses whether “recent experiments can be reproduced,” but there are deeper issues:

- How much exploration debt does the entire project have?
- How much validation debt?
- How much reproducibility debt?

A monthly review **forces you to look up and see the whole picture**, rather than continuously burying yourself in experiments.

### Review Checklist (Complete in 30 Minutes)

#### Exploration Debt Review (10 Minutes)

```bash
# 1. Quantify code disorder
git ls-files | wc -l                    # total number of files
git ls-files | grep "test\|tmp" | wc -l  # number of temporary files
git log --oneline | head -20            # most recent 20 commits

# 2. Quantify output disorder
du -sh outputs/                         # total size
ls outputs/ | wc -l                     # number of directories
find outputs/ -name "run.json" | wc -l  # number of experiments with records

# 3. Compute the exploration-debt metric
recorded experiments / total number of directories = record coverage
```

**Health criteria:**

- Record coverage \>80%: Good
- Record coverage 60–80%: Warning
- Record coverage \<60%: Dangerous (requires immediate cleanup)

## Validation Debt Review (10 Minutes)

```text
# Check validation completeness

Candidate paper results checklist:
[ ] Main experiment (Table 2) → run_id: __________
[ ] Baseline comparison (Table 3) → run_id: __________
[ ] Ablation study (Table 4) → run_id: __________
[ ] Failure case analysis (Figure 5) → run_id: __________

For each result:
[ ] Has a complete run.json
[ ] Has a baseline comparison (fair evaluation)
[ ] Has multiple runs (not a fluke)
[ ] Has test coverage (smoke test passes)
```

**Health criteria:**

- All candidate paper results have run_id: Good
- Missing 1–2: Warning (fill in next month)
- Missing 3 or more: Dangerous (the paper cannot be written)

## Reproducibility Debt Review (10 Minutes)

```bash
# Identify the 3 most important experiments
TOP_3_RUNS="..."

# Run a reproducibility test for each experiment
for run_id in $TOP_3_RUNS; do
    echo "Testing $run_id..."

    # Check records
    [ -f outputs/$run_id/run.json ] || echo "❌ Missing run.json"

    # Quick reproduction test (small data)
    python train.py \
        --config outputs/$run_id/config.yaml \
        --data_subset 100 --epochs 2 \
        || echo "❌ Quick reproduction failed"

    # Dependency check
    pip install -r outputs/$run_id/requirements.txt \
        || echo "⚠️  Dependencies may have changed"
done
```

**Health criteria:**

- All 3 can be quickly reproduced: Good
- 2 can be reproduced: Warning
- 1 or 0 can be reproduced: Dangerous (requires urgent fixes)

## Debt Visualization

It is recommended to maintain a “debt trend chart”:

```text
# debt_tracking.csv
Month,Exploration debt (record coverage),Validation debt (candidate result completeness),Reproducibility debt (reproducible ratio)
2026-01,50%,60%,33%
2026-02,70%,80%,67%
2026-03,85%,100%,100%
```

If debt is accumulating (numbers decreasing), it indicates that you are “borrowing against the future.” If debt is decreasing (numbers increasing), it indicates that you are “repaying debt.”

**Goal:** In the three months before the paper deadline, all debt metrics should be \>90%.

## Early Action 3: Establish a “Reproducibility Baseline” Three Months Before the Paper (1 Hour)

### Why It Matters

**The biggest misconception:** believing that reproducibility only needs to be considered during the “paper writing phase.”

**Reality:** if you wait until writing the paper to start preparing reproducibility materials, you will find that:

- Many experimental details have already been forgotten
- Code versions no longer match
- Data can no longer be found
- The environment has changed

**Correct approach:** establish a reproducibility baseline during the “experimentation phase,” so that during the paper phase you only need to validate and supplement.

### Contents of the Reproducibility Baseline

#### Minimal Reproduction Package (Build in 1 Hour)

```text
reproduce/
  README.md              # reproduction guide
  environment.yaml       # environment specification
  data_manifest.txt      # data inventory
  baseline_runs.txt      # list of key experiments
  reproduce.sh           # one-click reproduction script
  verify.py              # verification script
```

#### README.md Template

```markdown
# Reproduction Guide

## Environment Setup (10 Minutes)

```bash
# Create the environment
conda env create -f environment.yaml
conda activate research-env

# Verify installation
python verify.py --check-env
```
## Data Preparation (30 Minutes)
```bash
    # Download data (requires ~5GB of space)
    bash scripts/download_data.sh

    # Verify data
    python verify.py --check-data
    ```
## Reproduce Key Experiments (6 Hours)
```bash
    # Reproduce the main experiment (Table 2, ~2 hours)
    make reproduce RUN=main_experiment
    # Expected result: accuracy 94.3% ± 0.5%

    # Reproduce the baseline (Table 3, ~2 hours)
    make reproduce RUN=baseline
    # Expected result: accuracy 92.0% ± 0.3%
```

# Reproducing the Ablation Study (Table 4, ~2 hours)
```bash
bash scripts/reproduce_ablation.sh
```

## Verifying the Results
```bash
# Automatically verify all results
python verify.py --check-results

# The output should show:
# ✅ Main experiment: within expected range
# ✅ Baseline: within expected range
# ✅ Ablation: all components verified
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md`

### verify.py Example

```python
import json
from pathlib import Path

def verify_environment():
    """Verify that the environment is correctly configured"""
    import torch
    print(f"✅ PyTorch version: {torch.__version__**")
    print(f"✅ CUDA available: {torch.cuda.is_available()**")
    # Additional checks...

def verify_data():
    """Verify that the data are complete"""
    data_manifest = Path("data_manifest.txt").read_text()
    # Check whether files exist and whether hashes match...
    print("✅ Data verification passed")

def verify_results(run_id, expected_metric, tolerance=0.01):
    """Verify that results fall within the expected range"""
    run_json = Path(f"outputs/{run_id**/run.json")
    with open(run_json) as f:
        run_info = json.load(f)

    actual = run_info["metrics"]["test_acc"]
    diff = abs(actual - expected_metric)

    if diff <= tolerance:
        print(f"✅ {run_id**: {actual:.3f** "
              f"(expected {expected_metric:.3f** ± {tolerance:.3f**)")
        return True
    else:
        print(f"❌ {run_id**: {actual:.3f** "
              f"(expected {expected_metric:.3f**, diff {diff:.3f**)")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-env", action="store_true")
    parser.add_argument("--check-data", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()

    if args.check_env:
        verify_environment()
    if args.check_data:
        verify_data()
    if args.check_results:
        # Verify all key experiments
        verify_results("main_experiment", expected_metric=0.943)
        verify_results("baseline", expected_metric=0.920)
        # ...
```

### When to Establish It

**Best timing:** As soon as you obtain the first result that “looks publishable,” immediately establish a reproducibility baseline.

Do not wait until:

- ❌ all experiments are finished  
- ❌ you start writing the paper  
- ❌ you are preparing for submission  

Instead, do it when:

- ✅ you have the first promising result (even if it is not yet perfect)  
- ✅ you have confirmed the overall technical direction  
- ✅ you can answer “what this project ultimately aims to demonstrate”  

**Rule of thumb:** Establish the reproducibility baseline 3 months before the paper deadline. For a conference paper (a 6-month project), establish it in month 3.

## Emergency Remediation Plan: If You Are Already in the Final Stage

### If Only 2 Weeks Remain Until the Deadline

**Accept reality:** You do not have time to “do everything right.” You must focus on what matters most.

#### Priority 1: Ensure the Main Result Is Reproducible (3 days)

```text
# Day 1: Locate the code version for the main experiment
# - Reconstruct from Git history, chat logs, and notes
# - Find the closest commit
# - Fill in run.json (reconstruct parameters as much as possible)

# Day 2: Rerun in a clean environment
# - Create a new virtual environment
# - Record all dependencies
# - Rerun and record the results

# Day 3: If exact reproduction is not possible
# - If the discrepancy is within 1–2%: acceptable; report the error margin
# - If the discrepancy is larger: honestly explain the reasons in the paper
# - Worst case: switch to a reproducible, second-best result
```

## Priority 2: Patch the Most Critical Validations (2 days)

Only add validations that **reviewers will definitely ask for**:

- If you can only choose one: add a fair baseline comparison  
- If you can choose two: additionally add the main ablation study  
- For the rest: you can state “due to time constraints, left for future work”  

### Priority 3: Write Minimal Reproducibility Documentation (1 day)

```text
# Minimal reproducibility documentation includes:
```

1. Environment specification (Python version, key library versions)  
2. Data acquisition method (links or contact information)  
3. Execution commands (even if there is only one)  
4. Expected results (numerical ranges)  
5. Known issues (honestly describe reproducibility difficulties)

## If There Is Only 1 Week Left Until the Deadline

**The brutal truth:** you no longer have time to rerun experiments. You can only do your best to patch the records.

    # What you can do (2 hours each):
    [ ] Add run.json for all paper experiments (reconstruct from memory as much as possible)
    [ ] Tag the current code with a Git tag (preserve the current state)
    [ ] Write the simplest reproduction instructions (a section in the README)
    [ ] Package and back up all output files (to prevent loss)

    # What not to do (there is no time):
    [ ] Do not try to rerun all experiments
    [ ] Do not try to build a perfect reproduction environment
    [ ] Do not try to fix all inconsistencies

**Mindset adjustment:** accept imperfection, but ensure minimal traceability. Getting the paper submitted matters more than perfect reproducibility.

### Post-hoc Remediation

If the paper is accepted and you are asked to provide code:

    # You have 2–4 weeks to remediate

    Week 1: Trace back and document
- Locate all code versions relevant to the paper
- Reproduce key results as much as possible
- Document every point of "inconsistency"

    Week 2–3: Clean up and validate
- Clean up the code (remove irrelevant parts)
- Add documentation and comments
- Ensure at least 1–2 results are reproducible

    Week 4: Package and release
- Organize the code into a releasable form
- Write a clear README
- Honestly state the limitations of reproducibility in the paper

## 10-Minute Action: A Self-Check You Can Do Today

If you do only one thing right now: perform a minimal self-check on the current project.

1.  **Identify the most important experiment** (1 minute)

          Ask yourself: if you could keep only one experimental result, which would it be?
          Write down its run_id (if it does not exist, create one now)

2.  **Check record completeness** (3 minutes)

          [ ] Is there a run.json?
          [ ] Do you know which Git commit was used?
          [ ] Do you know which config was used?
          [ ] Do you know the random seed?
          [ ] Do you know the data version?

          If any item is missing, remediate immediately (writing it in your notes is fine)

3.  **Quick reproduction test** (5 minutes)

          # Use a small dataset to test whether the pipeline runs end-to-end
          python train.py \
              --config <your config> \
              --data_subset 100 \
              --epochs 2

          If an error occurs, record the error message and prioritize fixing it next time you work

4.  **Set the next self-check time** (1 minute)

          Add to your calendar:
          - Every Friday 17:00: reproducibility self-check (15 minutes)
          - The last day of each month: debt inventory (30 minutes)
          - [project start + 3 months]: establish a reproducibility baseline (1 hour)

After completing this 10-minute self-check, you will obtain two important outcomes:

1.  **Confidence:** you know the project’s core results are traceable

2.  **Early warning:** if you discover problems, you still have time to fix them

## Chapter Summary: Prevention Is Better Than Firefighting

The fundamental reason for last-stage blowups is: **postponing validation until the very end**.

The right mindset is:

- **Do not wait until you are "sure it works" to record**——any result that "looks good" should be recorded immediately

- **Do not wait until you "write the paper" to verify reproducibility**——verify continuously in day-to-day work

- **Do not wait until "reviewers ask" to add experiments**——identify validation debt early and proactively pay it down

**Three proactive actions are your insurance:**

1.  Weekly self-check: ensure recent work is traceable (15 minutes)

2.  Monthly inventory: ensure debt does not spiral out of control (30 minutes)

3.  Establish a reproducibility baseline early: ensure you are not scrambling in the final stage (1 hour)

Total monthly time investment: 15 minutes × 4 + 30 minutes + 1 hour (first time) = 2.5 hours

This 2.5-hour investment can avoid **3 days to 3 weeks of firefighting time** in the final stage.

**Remember: uncertainty in research is inevitable, but last-stage blowups are preventable.**