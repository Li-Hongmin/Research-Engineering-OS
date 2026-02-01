# Git Is Not for “Saving Code”; It Is for “Proving History”

## Story Setup: Reviewers Ask for Reproducibility, but You Can’t Find the Code from Back Then

![Git侦探](images/comics/04_git_detective.png)

![04 04 reviewer crisis](images/comics/04_04_reviewer_crisis.png)
Three months after submitting your paper, the reviews arrive. One comment is blunt: “Please provide the code and data; we would like to reproduce the results in Table 3.”

Your heart sinks—you quickly open the repository. But what you see makes your back go cold:

- The Git history contains only a handful of commits: “initial commit,” “update,” “fix bug,” “final version”;
- The results in the paper were produced three months ago, and you can no longer remember which version of the code was used;
- The code directory contains multiple versions of the training script: `train.py`, `train_v2.py`, `train_final.py`, and you are not sure which one was used;
- Worse still, you realize that you recently refactored the model code heavily for new experiments, and the current version can no longer reproduce the numbers reported in the paper.

You can only reply stiffly: “We are organizing the code and will provide it as soon as possible.” Then begins the painful “archaeology”—trying to reconstruct the code state from memory, chat logs, and experiment notes.

**Does this scenario feel familiar?**

## Why “Casual Commits” Won’t Save You

Many people think they are using Git, but in practice they treat it as a “cloud drive”:

- They change a lot of code and commit everything at once, with a message like “update”;
- They never use branches; all changes accumulate on `main`;
- They only remember to commit after an experiment finishes—by then the code has already changed again;
- The commit history provides no clue as to “which version corresponds to which experimental result.”

The problem with this workflow is that **you lose Git’s most essential value—the ability to serve as a “historical proof tool.”**

In engineering, Git is primarily used for collaboration and rollback. In research, Git’s core value is **proof**:

- Proving which version of the code produced a given result;
- Proving that every experiment in the paper corresponds to a specific code version;
- Proving that you can return to any historical version and reproduce the same results.

## Git Pitfalls in Research

### Pitfall 1: Commits Are Too Coarse-Grained, and Key Changes Become Untraceable

![04 05 commit too big](images/comics/04_05_commit_too_big.png)

**Symptom:** A single commit includes changes across a dozen files, spanning data processing, model architecture, training pipeline, and more. The commit message says only “improve model.”

**Consequences:**

- You cannot identify which change caused a metric to shift;
- When you want to roll back a faulty change, you find you cannot undo it in isolation;
- Months later, you cannot remember what the commit actually did.

**Correct practice:**

- Each commit should contain **one logical change** only;
- Commit messages should clearly state “what changed” and “why”;
- Follow the “atomicity principle”: every commit should keep the code in a runnable state.

### Pitfall 2: Misalignment Between Experiment Timing and Code Changes

![04 06 experiment time mismatch](images/comics/04_06_experiment_time_mismatch.png)

**Symptom:** You modify the code and run experiments first; the results look good; you commit two days later. Or you commit, then temporarily tweak a few parameters and rerun.

**Consequences:**

- The code version (commit) that produced the results does not actually match;
- Others (including your future self) attempt reproduction using the commit hash and obtain different results;
- When reviewers request reproduction, you cannot find the exact code version at all.

**Correct practice:**

- **Commit first, then run the experiment**;
- For each experiment, record the commit hash and dirty status in `run.json`;
- If you make temporary code changes, either recommit or document the dirty modifications in the run record.

### Pitfall 3: Improper Branch Usage Leads to a Chaotic Mainline

![04 07 branch chaos](images/comics/04_07_branch_chaos.png)
**Symptom:** All experiments are conducted on the `main` branch, mixing exploratory changes with stable code; or you create many branches but never clean them up, resulting in a tangled branch structure.

**Consequences:**

- The `main` branch becomes unstable and filled with experimental code;
- When you need the “paper reproduction version,” you do not know which branch to use;
- Too many branches leave team members unsure which branch to base new work on.

## A Git Branching Strategy Suitable for Research

![分支策略](images/comics/04_branch_strategy.png)
Unlike engineering projects, a research project’s branching strategy must balance two needs:

- **Stability:** the paper’s results must be supported by a clean, stable code version;
- **Exploration:** new ideas require rapid trial-and-error and should not be constrained by heavy process.

### Recommended Branch Structure
    main (or stable):
      - Accept only validated changes
      - Every merge must pass the DoD check (see Chapter 5)
      - Ensure the paper results are reproducible at any time

    exp/<hypothesis-name>:
      - One branch per experimental hypothesis
      - Use clear names: exp/attention-ablation, exp/data-augmentation
      - Short-lived branches: merge or delete after validation
      - Allow “dirty” rapid iteration

    archive/<paper-version>:
      - Archive branches for key milestones such as submission and publication
      - Created from main; never merged back
      - Kept permanently to ensure traceability

### Typical Workflow

#### Scenario 1: Validating a New Hypothesis

1.  Create a new branch from main: `git checkout -b exp/new-loss-function`

2.  Iterate quickly and trial-and-error on the branch; commits can be informal

3.  After obtaining promising results, clean up the code

4.  Create standardized experiment records (config + `run.json`)

5.  Merge back into main: `git checkout main && git merge exp/new-loss-function`

6.  Delete the experiment branch: `git branch -d exp/new-loss-function`

#### Scenario 2: Paper Submission

1.  Ensure all paper experiments on main are reproducible

2.  Create an archive branch: `git checkout -b archive/icml2026-v1`

3.  Create a tag on main: `git tag -a paper-icml2026-v1 -m "ICML 2026 submission version"`

4.  Push the tag: `git push origin paper-icml2026-v1`

#### Scenario 3: Exploring Multiple Directions in Parallel

1.  Create multiple experiment branches simultaneously:

- `exp/architecture-search`

- `exp/data-augmentation`

- `exp/loss-function`

2.  Advance each branch independently without interfering with others

3.  Manage each branch’s experimental artifacts using an independent run_id

4.  Merge valuable changes back into main one by one

5.  Delete branches with no value directly

## Mark Milestones with Tags: Make Paper Results Permanently Traceable

![04 08 tag milestone](images/comics/04_08_tag_milestone.png)
Tags are a severely underestimated feature in Git. For research projects, the value of tags lies in:

- Assigning permanent markers to every key version of the paper;

- Even as the main branch continues to evolve, you can precisely return to historical versions;

- Provide clear version naming to facilitate citation and reproduction.

### Recommended Tag Naming Conventions
    # Paper versions
    paper-<venue>-<version>
    e.g.: paper-icml2026-v1, paper-icml2026-revision

    # Experiment groups
    exp-<experiment-name>
    e.g.: exp-ablation-study, exp-baseline-comparison

    # Primary results
    result-<result-name>
    e.g.: result-table3-main, result-fig2-comparison

    # Milestones
    milestone-<description>
    e.g.: milestone-first-sota, milestone-reproducible-baseline

### Tag Usage Practices
#### Tag each important experiment for the paper:

![提交作为证据](images/comics/04_commit_evidence.png)
    # Tag immediately after finishing the main experiment
    git tag -a result-main-experiment -m \
      "Main results reported in Table 2, config: configs/main.yaml"

    # Record key information in the tag message
    git tag -a result-ablation-study -m \
      "Ablation study results (Table 3)
       Run IDs: 2026-02-01_1030_ablation_*
       Config: configs/ablation_*.yaml
       Key finding: attention mechanism contributes 5% improvement"

#### When reproducing, switch directly to the tag:
    # List all experiment-related tags
    git tag -l "result-*"

    # Switch to a specific experiment version
    git checkout result-main-experiment

    # Reproduce the experiment
    make reproduce CONFIG=configs/main.yaml

## Do Not Commit Experimental Artifacts to Git: Keep the Repository Clean with .gitignore

![04 09 gitignore clean](images/comics/04_09_gitignore_clean.png)
**Core principle:** Git manages source code and configuration, not experimental artifacts.

### What Should Not Be Committed to Git

- **Model weights:** usually large (hundreds of MB to several GB); use dedicated model management tools (e.g., DVC, Git LFS, or cloud storage).

- **Training logs:** all run artifacts under outputs/, organized by run_id and then archived or cleaned up.

- **Intermediate data:** cached features, preprocessing outputs, etc.; these should be regenerable.

- **Datasets:** raw data is typically managed externally; only keep small samples or data pointers (manifests, download scripts) under data/.

- **Virtual environments:** directories such as venv/ and .conda/; use requirements.txt or environment.yaml instead.

### Recommended .gitignore Template
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python

    # Virtual environments
    venv/
    env/
    .conda/

    # Experimental artifacts
    outputs/
    runs/
    checkpoints/
    *.pt
    *.pth
    *.ckpt
    *.h5

    # Data (unless it is a small sample)
    data/raw/
    data/processed/
    *.csv
    *.parquet

    # Logs
    *.log
    logs/
    wandb/

    # Temporary files
    .DS_Store
    *.swp
    *.swo
    *~

    # IDE
    .vscode/
    .idea/
    *.iml

    # Exceptions: keep small sample data and configurations
    !data/samples/
    !configs/

## Frequently Asked Questions and Solutions

### Q1: The code has already changed a lot—how can I recover?

If your repository history is already very messy, do not try to “rewrite history” (unless you are very familiar with Git rebase). The recommended approach is:

1.  **Set a baseline point:** tag the current state: `git tag baseline-before-cleanup`

2.  **Start enforcing conventions from now on:**

- Use an independent branch for each new experiment

- Keep each commit atomic

- Tag important results immediately

3.  **Fix historical issues incrementally:**

- Identify the code versions corresponding to key paper experiments and add tags retroactively

- Record the “mapping between historical versions” in the README or documentation

- Use the standardized workflow for new experiments; trace old experiments as much as possible

### Q2: How do we unify the branching strategy in team collaboration?
- **Write it into the README:** document branch naming conventions and tag usage.

- **Set protection rules:** on GitHub/GitLab, protect the main branch; forbid direct pushes and require PR/MR.

- **Code Review:** before merging into main, check whether the DoD (Chapter 5) is satisfied and whether there is a complete experiment record.

- **Regular cleanup:** hold a weekly meeting to collectively remove useless experiment branches and archive important tags.

### Q3: How should we handle experiments in a “dirty” state?

Sometimes you temporarily modify code to run an experiment but have not had time to commit; this is a “dirty” state.

**Recording strategy:**

- Record `"git_dirty": true` in run.json

- Also record the diff: `git diff > outputs/<run_id>/changes.patch`

- In run.md, note the temporary changes and the reasons

**Post hoc remediation:**

- If the results are valuable, commit the changes immediately and add a tag

- If it is only a temporary trial, recording it in run.md is sufficient; no need to commit

## Practical Case: From Chaos to a Clear Git History

### Before Refactoring (Negative Example)

    * a3f2d1c (HEAD -> main) update
    * f8d9e0a fix
    * 1b2c3d4 add new feature
    * 9e8d7f6 initial commit

No useful information can be inferred from the history, and none of the paper experiments can be matched to a corresponding version.

### After Refactoring (Positive Example)

* d1e2f3g (tag: paper-icml2026-v1, main) Merge exp/final-ablation
    |           Paper results ready for submission
    |\
    | * c4d5e6f (exp/final-ablation) Add ablation study for attention
    | * b3c4d5e Configure ablation experiments
    |/
    * a1b2c3d (tag: result-main-experiment) Main experiment: achieve 95.2% accuracy
               Run ID: 2026-02-01_1030_main_run
               Config: configs/main_experiment.yaml
    * 9a8b7c6 (tag: milestone-baseline) Establish reproducible baseline
               All baseline experiments validated
    * 8f7e6d5 Fix data preprocessing bug in train/val split
    * 7e6d5c4 Add comprehensive smoke test
    * 6d5c4b3 Refactor data loading module

A clear history: every critical milestone is tagged, enabling rollback at any time.

## 10-Minute Action: Establish a Git Baseline for the Current Project

If you do only one thing right now: establish a clear Git baseline for your project.

1.  **Check the current status:**

          git status
          git log --oneline -10

2.  **If there are uncommitted changes, decide how to handle them:**

- Valuable changes: clean them up and commit, with a clear message

- Temporary experiments: record them in run.md, then `git stash`

- Useless changes: revert with `git checkout .`

3.  **Create a baseline tag for the current stable version:**

          git tag -a baseline-$(date +%Y%m%d) -m \
            "Baseline before implementing git workflow"

4.  **Set up a well-structured .gitignore:**

          # Use the template provided earlier
          curl -o .gitignore <template link>
          # Or create it manually
          git add .gitignore
          git commit -m "Add comprehensive .gitignore for research project"

5.  **Document branch naming conventions:** Add a section titled "Git Workflow" to README.md and record:

- The purpose of the main branch

- Naming conventions for exp/ branches

- How to use tag

From this point onward, follow the conventions for branches and tag for every new experiment, so that Git truly becomes your "tool for proving history."