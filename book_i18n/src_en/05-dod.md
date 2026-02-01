# From “It Runs” to “Trustworthy”: Only a Definition of Done Away

## Story: The Cost of “Good Enough”

![06 Good Enough Trap](images/comics/05_06_good_enough_trap.png)

At 2 a.m., you finally get a “pretty good-looking” result—test accuracy 94.3%, 3 percentage points higher than the baseline. Excited, you take a screenshot and post it to the team chat: “The new method works!”

Three days later, when you are ready to write the paper, you want to rerun the experiment to verify the result. You open the code and hesitate:

- Which configuration file did I use? There are three similar yaml files; I can’t remember.
- Which version of the data did I use? I think I temporarily changed the split once.
- What was the random seed? I forgot to record it.
- Was the code committed at the time? Or were there temporary local edits?

You bite the bullet and rerun it. The result comes out: 92.7%. That is 1.6 percentage points lower than before.

Your heart sinks—so which run is correct? Or are both unreliable?

**The problem in this scenario is: you do not have a clear standard for judging whether “an experiment is done.”**

In software engineering, there is a concept called **Definition of Done (DoD)**—the definition of completion. It answers: “When can I say this task is truly finished?”

In research, we also need a DoD, but with different standards:

- Engineering DoD: the code runs, tests pass, documentation is complete.
- Research DoD: results are trustworthy, reproducible, and comparable.

## Why “It Runs” ≠ “Done”

In research, there are many situations that “look finished but actually plant landmines”:

### Landmine 1: “Got a result” but cannot reproduce it
**Symptom:** You see a good result, but lack complete records of the environment, configuration, and data version. A few days later, you try to rerun it and the numbers do not match.

**Real cost:**

- You panic when reviewers ask for reproducibility;
- Teammates cannot build on your results;
- Worst case: the paper is rejected because the “results are not reproducible.”

### Landmine 2: “Improvement works” but you do not know why

**Symptom:** You changed three things at once. The result did improve, but you do not know which change mattered, and you did not run ablation experiments.

**Real cost:**

- You cannot answer when reviewers ask for a mechanistic explanation;
- You do not know what to keep or discard in subsequent iterations;
- You may mistakenly treat ineffective or even harmful changes as the key contribution.

### Landmine 3: “Comparative experiments” but inconsistent evaluation protocol
**Symptom:** Your method and the baseline use different evaluation scripts, or different post-processing. Your method appears better, but the comparison is actually unfair.

**Real cost:**

- Reviewers point out the unfair evaluation and ask you to redo it;
- After rerunning, the advantage disappears;
- You waste substantial time “equalizing” the evaluation.

## DoD Checklist for Paper-Candidate Conclusions

The following checklist applies to any experimental result that “might go into the paper.” It is recommended to paste it verbatim into the project README as a team consensus.

### Minimal DoD (5 mandatory items)

![07 Minimal Dod](images/comics/05_07_minimal_dod.png)

1.  **Reproduce the primary metric with a single command**

          # For example:
          make reproduce RUN=2026-02-01_1030_main_experiment
          # Or:
          python reproduce.py --run_id=2026-02-01_1030_main_experiment

    Starting from scratch (given the environment and data), it must be possible to reproduce the metrics reported in the paper with a single command (allowing minor fluctuations).

2.  **Complete run records**

    Each important experiment must have complete run records, including at least:

- Git commit hash (code version)
- Config file path and content (all hyperparameters)
- Random seed
- Data version (dataset version number, hash, or manifest file)
- Environment summary (Python version, key library versions, GPU model, etc.)

    A recommended format is the `run.json` template in Chapter 6.

3.  **Baseline and ablation use the same evaluation script**

    All comparative experiments must:

- Use exactly the same evaluation code;
- Use exactly the same data split;
- Use exactly the same post-processing;
- Use consistent metric computation logic (e.g., the same thresholds and the same averaging scheme).

    **Acceptance criterion:** you can point to a single unified evaluation script, and all methods’ metrics come from that script.

4.  **At least one smoke test runs in 1–3 minutes**

    A smoke test is a quick test that validates the core pipeline, aiming to catch obvious errors as early as possible.

    Key components that must be covered:

- Data loading (can read correctly and return data with correct shapes)
- Model forward pass (does not crash; output shapes are correct)
- Loss computation (values are reasonable; no NaN)
- Evaluation pipeline (metrics are computed correctly)

    **Implementation suggestion:** use a tiny data subset (e.g., 10 samples), run 2–3 iterations, and ensure the end-to-end pipeline is intact.

5.  **Figures are generated by scripts, not manual drag-and-drop**

    All figures in the paper must be automatically generated from the raw data in `outputs/`.

    Prohibited practices:

- Manually copying numbers from logs into Excel;
- Manually adjusting chart styles and then taking screenshots;
- Being unable to locate the source data files for figures.

    Recommended practices:

- Place generation scripts in the `reports/` directory (e.g., `plot_main_results.py`);
- Scripts read `outputs/<run_id>/metrics.json` and generate figures;
- Save figures in an editable format (e.g., PDF) and save source data (e.g., CSV);
- Add `make plots` to the Makefile to generate all figures with one command.

### Enhanced DoD (recommended additional items)

![08 Enhanced Dod](images/comics/05_08_enhanced_dod.png)

After meeting the minimal DoD, the following items can further improve result credibility:

1.  **Statistics over multiple runs**

    For experiments with substantial randomness, a single run is insufficient to demonstrate effectiveness. Recommended:

- Run with at least 3–5 different random seeds;
- Report mean and standard deviation (or confidence intervals);
- List the run_id corresponding to each seed in the run records.

2.  **Failure case analysis**

    Honestly document the limitations of the method:

- Under what conditions does the method perform poorly?
- Are there clear failure examples?
- How sensitive is it to hyperparameters?

    This not only increases credibility but also points the way for future improvements.

3.  **Complete ablation study**

    For methods that include multiple improvements, an ablation study must answer:

- How much does each improvement contribute on its own?
- Which improvements are critical and which are marginal?
- Are there interaction effects among improvements?

4.  **Code quality checks**

    Use automated tools to check code quality:

- Linter (e.g., flake8, pylint): code style checks
- Type checker (e.g., mypy): type checking
- Unit test coverage: key functions must have tests

    Run these checks automatically in CI.

5.  **Data leakage checks**

    Ensure strict separation between the training set and the test set:

- Print sample counts before splitting and verify totals are consistent;
- Check whether the training and test sets overlap (using sample IDs or hashes);

- Time-series data: ensure the test set is temporally later than the training set.

## DoD Checklist: Operational Steps from “It Runs” to “It’s Trustworthy”

### Do Immediately After Finishing an Experiment (5 minutes)

1. **Record run information**

          # Automatically generate run.json (see Chapter 6 tools)
          python log_run.py --run_id <id>

2. **Manually write key information in run.md** (no more than 5 lines)

- What is the hypothesis of this experiment?
- What are the main changes?
- What are the results (summarize in one sentence)?
- What is the next step?
- Are there any noteworthy risks or anomalies?

### Do Before Starting to Write the Paper (30 minutes)

1. **Reproducibility verification**

    Run the reproduction command in a new terminal (or a new environment):

          make reproduce RUN=<run_id of the paper-candidate result>

    Check:

- Does it run smoothly (without errors)?
- Are the results within a reasonable range (difference no more than 1–2% or one standard deviation)?
- If the discrepancy is large, investigate the cause (environment, data, randomness).

2. **Comparative experiment check**

    Check all methods to be compared:

          ls outputs/
          # Find all baseline and ablation run_id

    Confirm:

- Did they use the same evaluation script? (This can be confirmed via the script path or hash in run.json.)
- Is the data split consistent?
- Are the evaluation parameters consistent?

    If inconsistencies are found, you must rerun some experiments to unify the evaluation protocol.

3. **Run smoke tests**

          make test
          # Or:
          pytest tests/test_smoke.py

    Ensure the core pipeline has not been broken by subsequent changes.

4. **Generate plots**

          make plots

    Check the generated plots:

- Do they reflect the latest experimental results?
- Are the numbers consistent with the run records?
- Are the axes and legends clear?

### Do Before Paper Submission (1 hour)

1. **Completeness self-check**

    Cross-check the DoD list item by item:

- Every experiment cited in the paper has a run_id
- Every run_id has a complete run.json
- All comparative experiments use the same evaluation script
- Smoke tests pass
- All plots can be generated via scripts

2. **Create Git tags for key experiments**

          # Main experiment
          git tag -a result-main-table2 -m \
            "Main results in Table 2, run_id: 2026-02-01_1030_main"

          # Ablation experiments
          git tag -a result-ablation-table3 -m \
            "Ablation study in Table 3, run_ids: 2026-02-01_14*"

          # Push tags
          git push origin --tags

3. **Write reproduction documentation**

    In the README or a separate REPRODUCE.md, clearly specify:

- Environment setup steps (a single command or script)
- Data preparation steps (download, preprocessing)
- Commands to reproduce each table/figure
- Expected runtime and resource requirements

    Example:

          # Reproduction Instructions

          ## Environment Setup
          conda env create -f environment.yaml
          conda activate research-env

          ## Data Preparation
          bash scripts/download_data.sh
          python scripts/preprocess.py

          ## Reproduce Main Experiment (Table 2)
          make reproduce RUN=2026-02-01_1030_main
          # Expected time: 2 hours (single V100 GPU)
          # Expected metric: accuracy 94.3% ± 0.5%

          ## Reproduce Ablation Experiments (Table 3)
          bash scripts/reproduce_ablation.sh
          # Expected time: 6 hours (single V100 GPU)

## How Teams Use DoD
### As a Merge Criterion

In team collaboration, DoD can serve as the threshold for merging code into the main branch:

1. An experiment branch must meet the minimum DoD to be merged into main;
2. During code review, the reviewer checks against the DoD checklist;
3. Code that does not meet DoD cannot be merged and must be completed.

### As a Handover Standard

When a project needs to be handed over (e.g., student graduation, team member departure), DoD ensures that knowledge is not lost:

- All important experiments have complete records, so new members can reproduce them;
- Code quality is ensured (tests and documentation);
- Data and models have clear storage and access instructions.

### As a Self-Audit Standard

Even for individual projects, DoD helps you avoid “fooling yourself”:

- Regularly (e.g., weekly) check experiments that have not completed DoD and fill in missing records;
- Perform batch checks before writing the paper to avoid last-minute scrambling;
- Once the habit is formed, DoD becomes a natural workflow rather than an extra burden.

## Common Obstacles and Solutions

### Obstacle 1: “I’m just exploring right now; there’s no need to be so strict.”

**Rebuttal:** During exploration, you may **lower the DoD standard**, but you cannot have no standard at all.

Recommended “simplified DoD for the exploration phase”:

- No requirement for multiple-run statistics;
- No requirement for complete ablation studies;
- **But must**: record commit, config, and seed to ensure it can be rerun.

Once an experiment “seems valuable,” immediately upgrade to the full DoD.

### Obstacle 2: “Meeting DoD takes too much time.”

**Response:** A one-time investment of 30 minutes yields:

- No need for emergency patch-ups during review (saves days);
- A clear baseline for subsequent improvements (saves repeated work);
- No anxiety about “not being reproducible” at submission time (reduces psychological burden).

**Practical suggestions:**

- Script the DoD checks to reduce manual operations;
- Add checks in Git pre-commit hooks (see Chapter 7);
- With proficiency, DoD will integrate into daily workflows and no longer be an extra cost.

### Obstacle 3: “We already have experiment management tools (e.g., MLflow, W&B).”

**Response:** Tools are great, but DoD is a **standard**, not a tool.

Tools can help you:

- Automatically record run information (save time);
- Visualize experimental results (easy comparison);
- Store models and artifacts (convenient management).

But tools cannot replace:

- Your definition of “what counts as done”;

- Your checks on “whether the evaluation is fair”;

- Your verification of “whether the code is reproducible”.

**Recommendation:** Combine the DoD checklist with tooling; for example, record a “DoD compliance status” field in the MLflow run.

## 10-Minute Action: Perform a DoD Check on the Current Best Result

If you do only one thing right now: perform a complete DoD check on your currently “most promising” experimental result.

1. **Find the run_id for this experiment** (if it does not exist, create one now)

2. **Inspect the run records**

          # Check whether run.json exists
          ls outputs/<run_id>/run.json

          # If not, remediate immediately:
          # 1. Record the git commit: git log -1 --format="%H"
          # 2. Record the config file path
          # 3. Record the seed (if you remember it)
          # 4. Record the data version (check the data directory or logs)
          # 5. Record the environment: pip freeze > requirements_<run_id>.txt

3. **Attempt reproduction**

          # Switch to the recorded commit
          git checkout <commit_hash>

          # Re-run with the recorded config
          python train.py --config <config_path> --seed <seed>

          # Check whether the results are within a reasonable range

4. **Record the check results**

   Record the following in `outputs/<run_id>/dod_check.md`:

- Are the records complete?

- Reproducible? (result discrepancy: )

- Is the evaluation fair?

- Are there tests?

- Can the figures be generated?

5. **If issues are found, fix them immediately**

- Incomplete records: supplement run.json

- Not reproducible: investigate discrepancies and rerun

- Unfair evaluation: unify the evaluation script and rerun all comparative experiments

After completing this check, you will have a clear understanding of the credibility of this result. If it passes the DoD, you can confidently include it in the paper; if it does not, it is still early enough to fix it now.

**Remember: finding problems early is better than finding them before submission; finding them before submission is better than finding them during review; finding them during review is better than being questioned after publication.**