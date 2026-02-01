# Experiment Logging Automation: What’s Missing Is Not Tools, but Default Behavior
## Story Setup: “Archaeological Work” Three Months Later

Your paper has been accepted, but the reviewers request supplementary materials explaining the exact setup of a particular experiment in Table 4. You open the code repository and begin “archaeology”:

**Step 1: Find the logs**

You remember this experiment was run three months ago. You open the `outputs/` directory and see a pile of date-named folders. The problem is that you cannot recall the exact date. You can only open them one by one to check whether the results correspond to that experiment.

**Step 2: Find the configuration**

You finally locate the result files, but there is no record of the configuration. You comb through the code history, trying to find the hyperparameters used at the time. In one commit you find a configuration that seems plausible, but you are not sure whether it was the final version—you remember temporarily changing the learning rate, but you do not remember what you changed it to.

**Step 3: Find the data**

The data path in the code is `data/v2/`, but your current data directory is `data/v3/`. You do not remember whether you switched dataset versions back then. You search your chat history for “data,” trying to find clues.

**Step 4: Give up**

After an entire afternoon of struggle, you decide to rerun the experiment. However, because the parameters are uncertain, the rerun results do not match what was reported in the paper. In the supplementary materials you can only write: “Due to the long time elapsed, some experimental details may be inaccurate.”

**Reviewer’s reply:** “We cannot accept a paper where the authors cannot reproduce their own results.”

### This tragedy could have been avoided.

If you had spent 2 minutes recording key information at the end of the experiment, you would not have faced a nightmare three months later.

The issue is not a lack of tools (MLflow, W&B, and TensorBoard are all excellent), but rather the **absence of logging as a default behavior**: many people think, “This is just a quick try; no need to record it,” and then they keep trying and forget to log. In the end, even valuable experiments leave no trace.

## A Two-Layer Logging Strategy: Machine-Precise + Human-Concise

![05 Two Layer](images/comics/06_05_two_layer.png)

The core challenge of experiment logging is balancing two needs:

- **Machines require complete and precise information** (for reproducibility and automated analysis);

- **Humans require concise, readable summaries** (for rapid review and decision-making).

With only machine logs (e.g., JSON), it is difficult for humans to quickly understand “what this experiment was trying to verify”; with only human logs (e.g., notes), machines cannot automatically reproduce and compare runs.

**Solution: two layers of logs, each doing its own job.**

### Layer 1: Machine Log (run.json)
**Purpose:** Provide complete, structured information for reproducibility and automation.

**Principles:**

- **Automatically generated:** does not rely on manual input; collected automatically by scripts;

- **Structured:** JSON format, easy for programs to parse and query;

- **Complete:** includes all key information required for reproduction.

**Minimal field set** (can be copied verbatim):

    {
      "run_id": "2026-02-01_1630_ablation_lr",
      "timestamp": {
        "start": "2026-02-01T16:30:45",
        "end": "2026-02-01T18:45:12"
      },
      "git": {
        "commit": "a1b2c3d4e5f6",
        "dirty": false,
        "branch": "exp/ablation-lr",
        "remote": "git@github.com:user/project.git"
      },
      "config": {
        "path": "configs/ablation_lr.yaml",
        "hash": "sha256:abcd1234...",
        "resolved": {
          "model": "transformer",
          "learning_rate": 3e-4,
          "batch_size": 32,
          ...
        }
      },
      "data": {
        "name": "dataset_v3",
        "path": "/data/project/v3",
        "hash": "sha256:ef567890...",
        "split": {
          "train": 8000,
          "val": 1000,
          "test": 1000
        }
      },
      "environment": {
        "python": "3.11.7",
        "cuda": "12.1",
        "platform": "Linux-5.15.0-x86_64",
        "gpu": "NVIDIA A100-SXM4-40GB",
        "pip_freeze_hash": "sha256:12345678..."
      },
      "random": {
        "seed": 42,
        "torch_seed": 42,
        "numpy_seed": 42,
        "python_seed": 42
      },
      "metrics": {
        "val_loss": 0.123,
        "val_acc": 0.943,
        "test_loss": 0.145,
        "test_acc": 0.931,
        "training_time_hours": 2.25
      },
      "artifacts": {
        "model": "outputs/2026-02-01_1630_ablation_lr/model.pt",
        "logs": "outputs/2026-02-01_1630_ablation_lr/train.log",
        "predictions": "outputs/2026-02-01_1630_ablation_lr/predictions.json",
        "plots": "outputs/2026-02-01_1630_ablation_lr/plots/"
      }
    }

#### Explanation of key fields:

- **run_id:** A unique identifier; recommended format is timestamp + short description (see Chapter 2).

- **git.commit:** Code version; obtain via `git rev-parse HEAD`.

- **git.dirty:** Whether there are uncommitted changes; check via `git diff-index --quiet HEAD --`. If true, it is recommended to save the diff: `git diff > changes.patch`.

- **config.resolved:** The fully expanded final configuration, including all default values. This is important because defaults may change as the code evolves.

- **data.hash:** A hash of the data version to ensure the data are exactly identical. You can compute a hash for the entire data directory with `sha256sum`, or use tools such as DVC.

- **environment.pip_freeze_hash:** A hash of dependency versions, computed with `pip freeze | sha256sum`. Avoid storing the full `pip freeze` output (too long); store only the hash and the path to the original file.

- **random.seed:** All random seeds. Ensure that seeds are set for PyTorch, NumPy, and Python’s built-in `random`.

### Layer 2: Human Log (run.md)
**Purpose:** Provide a concise summary of the experiment for humans (including your future self) to enable rapid understanding.

**Principles:**

- **Concise:** No more than 10 lines; key information should be immediately clear.

- **Structured:** Organize using a fixed set of five elements.

- **Handwritten:** Allow subjective judgment and insights.

**Five-element template** (5 lines are enough):

    # Run: 2026-02-01_1630_ablation_lr

    ## Hypothesis
    Test the effect of learning rate on convergence speed and final performance. Expectation: a smaller learning rate (1e-4) will be more stable.

    ## Change
    Compared with the baseline (lr=3e-4), reduce the learning rate to 1e-4; keep other hyperparameters unchanged.

    ## Result
- Slower convergence (from 50 epochs to 80 epochs)
- Slightly improved final performance (val_acc: 0.943 vs 0.938)
- More stable training; no obvious oscillations in the loss curve

    ## Next
    Try an intermediate value of 2e-4, which may balance speed and performance.
    Consider a learning rate warmup strategy.

    ## Risk/Anomalies
    No obvious anomalies. Data augmentation may need coordinated adjustment (currently fixed).

#### Why only 5 lines?

- **Lower the logging barrier:** If you have to write a long document, you will procrastinate; with 5 lines, you can finish in 2 minutes.

- **Force distillation of the core:** Compels you to think about “what exactly did this experiment validate,” rather than producing a chronological narrative.

- **Fast review:** Months later, a 5-line summary is more useful than a full log.

## Automation Tools: Make Logging a Zero-Cost Behavior
**Core idea:** Logging should not depend on “remembering to do it”; it should happen automatically.

### Automatically Generate run.json in the Training Script
#### Example implementation (Python):

    import json
    import subprocess
    import hashlib
    from pathlib import Path
    from datetime import datetime

    def log_run(run_id, config, metrics, output_dir):
        """
        Automatically log experiment information to run.json

        Args:
            run_id: Unique experiment identifier
            config: Configuration dictionary (resolved/expanded)
            metrics: Final metrics dictionary
            output_dir: Output directory path
        """
        run_info = {
            "run_id": run_id,
            "timestamp": {
                "start": datetime.now().isoformat(),
            },
            "git": get_git_info(),
            "config": {
                "resolved": config,
                "hash": hash_dict(config),
            },
            "data": get_data_info(config.get("data_path")),
            "environment": get_env_info(),
            "random": get_random_seeds(config),
            "metrics": metrics,
            "artifacts": {
                "model": str(output_dir / "model.pt"),
                "logs": str(output_dir / "train.log"),
            }
        }

        # Save to file
        run_file = output_dir / "run.json"
        with open(run_file, "w") as f:
            json.dump(run_info, f, indent=2)

        print(f"Run info logged to {run_file}")

    def get_git_info():
        """Retrieve git information"""
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            ).decode().strip()

            # Check for uncommitted changes
            subprocess.check_call(
                ["git", "diff-index", "--quiet", "HEAD", "--"]
            )
            dirty = False
        except subprocess.CalledProcessError:
            dirty = True

        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).decode().strip()

```python
remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"]
        ).decode().strip()

        return {
            "commit": commit,
            "dirty": dirty,
            "branch": branch,
            "remote": remote
        }

    def get_data_info(data_path):
        """Retrieve dataset information"""
        data_path = Path(data_path)

        # Compute a hash of the data directory (simplified; in practice, DVC can be used)
        # This is only an example; in real scenarios, it is recommended to use a dedicated data versioning tool

        return {
            "name": data_path.name,
            "path": str(data_path.absolute()),
            # "hash": compute_dir_hash(data_path),  # Optional
        }

    def get_env_info():
        """Retrieve environment information"""
        import sys
        import platform

        env = {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        }

        # Retrieve the CUDA version (if available)
        try:
            import torch
            env["cuda"] = torch.version.cuda
            env["pytorch"] = torch.__version__
            if torch.cuda.is_available():
                env["gpu"] = torch.cuda.get_device_name(0)
        except ImportError:
            pass

        # Save pip freeze to a separate file
        pip_freeze = subprocess.check_output(
            ["pip", "freeze"]
        ).decode()
        pip_file = Path("requirements_freeze.txt")
        pip_file.write_text(pip_freeze)

        env["pip_freeze_hash"] = hashlib.sha256(
            pip_freeze.encode()
        ).hexdigest()[:16]

        return env

    def get_random_seeds(config):
        """Extract random seeds"""
        return {
            "seed": config.get("seed", None),
            "torch_seed": config.get("torch_seed", None),
            "numpy_seed": config.get("numpy_seed", None),
        }

    def hash_dict(d):
        """Compute a hash of a dictionary"""
        import json
        return hashlib.sha256(
            json.dumps(d, sort_keys=True).encode()
        ).hexdigest()[:16]
```

#### Usage in the training script:

```python
    # train.py

    import argparse
    from pathlib import Path
    from run_logger import log_run  # The utility above

    def main():
        args = parse_args()

        # Create run_id and the output directory
        run_id = f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_{args.exp_name}"
        output_dir = Path("outputs") / run_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # Load and resolve the configuration
        config = load_config(args.config)
        config = resolve_config(config, args)  # Resolve all default values

        # Set random seeds
        set_random_seeds(config["seed"])

        # Train the model
        model, metrics = train_model(config, output_dir)

        # Automatically log experiment information
        log_run(
            run_id=run_id,
            config=config,
            metrics=metrics,
            output_dir=output_dir
        )

        # Prompt to write run.md
        print(f"\n{'='*60**")
        print(f"[OK] Experiment completed: {run_id}")
        print(f"[NOTE] Please write a brief summary in:")
        print(f"    {output_dir / 'run.md'}")
        print(f"{'='*60**\n")

    if __name__ == "__main__":
        main()
```

### Simplify run.md writing with a template
Automatically generate a `run.md` template in the output directory:

```python
def create_run_md_template(output_dir, run_id):
    """Create a run.md template"""
    template = f"""# Run: {run_id}

## Hypothesis
[What does this experiment aim to validate? What are the expected results?]

## Change
[Compared with the previous experiment, what was changed?]

## Result
[What were the experimental results? Any unexpected findings?]

## Next
[Based on these results, what is the next step?]

## Risk/Anomaly
[Are there any notable anomalies or risks?]
"""

    md_file = output_dir / "run.md"
    if not md_file.exists():
        md_file.write_text(template)
        print(f"[NOTE] run.md template created at {md_file}")
```

In this way, after each experiment ends, you only need to fill in the blanks rather than writing from scratch.

## Integration with Existing Tools

### Integration with MLflow

![09 Mlflow](images/comics/06_09_mlflow.png)

If you are already using MLflow, you can synchronize the run.json information to MLflow:

```python
import mlflow

def log_to_mlflow(run_info):
    """Log run.json information to MLflow"""
    with mlflow.start_run(run_name=run_info["run_id"]):
        # Log parameters
        mlflow.log_params(run_info["config"]["resolved"])

        # Log metrics
        mlflow.log_metrics(run_info["metrics"])

        # Log environment information
        mlflow.log_dict(run_info["environment"], "environment.json")

        # Log git information
        mlflow.set_tag("git.commit", run_info["git"]["commit"])
        mlflow.set_tag("git.branch", run_info["git"]["branch"])
        mlflow.set_tag("git.dirty", run_info["git"]["dirty"])

        # Log artifacts
        mlflow.log_artifact(run_info["artifacts"]["model"])
```

### Integration with Weights & Biases

```python
import wandb

def log_to_wandb(run_info):
    """Log run.json information to W&B"""
    wandb.init(
        project="my-research",
        name=run_info["run_id"],
        config=run_info["config"]["resolved"],
        tags=[run_info["git"]["branch"]]
    )

    # Log metrics
    wandb.log(run_info["metrics"])

    # Log environment and git information
    wandb.config.update({
        "git_commit": run_info["git"]["commit"],
        "git_dirty": run_info["git"]["dirty"],
        "python_version": run_info["environment"]["python"],
    **)

    # Save the model
    wandb.save(run_info["artifacts"]["model"])
```

**Key point:** Tools are auxiliary; the core is the **standardization of recording**. Even without MLflow/W&B, run.json and run.md are sufficient.

## Log Querying and Analysis

With a structured run.json, you can quickly query and compare experiments:

### Finding the Best Experiments

```python
# find_best_run.py

import json
from pathlib import Path

def find_best_runs(metric="test_acc", top_k=5):
    """Find experiments with the best metric values"""
    runs = []

    for run_dir in Path("outputs").iterdir():
        if not run_dir.is_dir():
            continue

        run_json = run_dir / "run.json"
        if not run_json.exists():
            continue

        with open(run_json) as f:
            run_info = json.load(f)

        if metric in run_info.get("metrics", {**):
            runs.append({
                "run_id": run_info["run_id"],
                metric: run_info["metrics"][metric],
                "config": run_info["config"]["resolved"]
            **)

    # Sort
    runs.sort(key=lambda x: x[metric], reverse=True)
```

```python
print(f"Top {top_k} runs by {metric}:")
        for i, run in enumerate(runs[:top_k], 1):
            print(f"{i}. {run['run_id']}: {run[metric]:.4f}")
            print(f"   Config: lr={run['config'].get('learning_rate')}, "
                  f"bs={run['config'].get('batch_size')}")

        return runs[:top_k]

    if __name__ == "__main__":
        find_best_runs()
```

## Comparing Configuration Differences Between Two Experiments

```python
# compare_runs.py

import json
from pathlib import Path

def compare_runs(run_id1, run_id2):
    """Compare the configurations and results of two experiments"""
    run1 = load_run(run_id1)
    run2 = load_run(run_id2)

    print(f"Comparing {run_id1} vs {run_id2}\n")

    # Compare configurations
    config1 = run1["config"]["resolved"]
    config2 = run2["config"]["resolved"]

    print("Configuration differences:")
    for key in set(config1.keys()) | set(config2.keys()):
        val1 = config1.get(key, "N/A")
        val2 = config2.get(key, "N/A")
        if val1 != val2:
            print(f"  {key}: {val1} -> {val2}")

    # Compare metrics
    print("\nMetrics:")
    metrics1 = run1.get("metrics", {})
    metrics2 = run2.get("metrics", {})
    for key in set(metrics1.keys()) & set(metrics2.keys()):
        val1 = metrics1[key]
        val2 = metrics2[key]
        diff = val2 - val1
        print(f"  {key}: {val1:.4f} -> {val2:.4f} "
              f"({diff:+.4f}, {diff/val1*100:+.2f}%)")

def load_run(run_id):
    """Load experiment information"""
    run_json = Path("outputs") / run_id / "run.json"
    with open(run_json) as f:
        return json.load(f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_runs.py <run_id1> <run_id2>")
        sys.exit(1)

    compare_runs(sys.argv[1], sys.argv[2])
```

## Frequently Asked Questions and Solutions

### Q1: What if run.json is too large?
**Problem:** If you save the full config (including model definitions, data preprocessing details, etc.), run.json may become very large.

**Solutions:**

- Save only the “key hyperparameters” in run.json (e.g., learning rate, batch size);

- Save the full config to a separate file: `config_resolved.yaml`;

- In run.json, record only the config file path and its hash.

### Q2: What if you forgot to write run.md?
**Solutions:**

- Add a check in the Makefile or scripts:

```sh
if [ ! -f outputs/$RUN_ID/run.md ]; then
    echo "Warning: run.md not found for $RUN_ID"
    echo "Please write a summary before continuing."
fi
```

- Periodically (e.g., every Friday) check which experiments are missing run.md and fill them in in a batch.

- If you truly cannot recall, write “forgotten”—it is still better than having no record.

### Q3: What if the data version is too large to compute a hash?

**Solutions:**

- Use a data versioning tool (e.g., DVC, Git LFS);

- Or record only a “manifest file” of the data:

```sh
# Generate a manifest
find data/ -type f | xargs sha256sum > data_manifest.txt

# Compute the manifest hash
sha256sum data_manifest.txt
```

- Record the manifest file path and hash in run.json.

## 10-Minute Action: Set Up Automatic Logging for Your Next Experiment
If you do only one thing right now: build a minimal system for automatic logging.

1.  **Copy run_logger.py**

    Copy the earlier `log_run` function into your project.

2.  **Call it at the end of the training script**

```python
# After training finishes
log_run(run_id, config, metrics, output_dir)
```

3.  **Create a run.md template**

```python
create_run_md_template(output_dir, run_id)
```

4.  **Run one experiment as a test**

    Run an experiment and confirm:

- outputs/\<run_id\>/run.json is generated automatically

- The `outputs/<run_id>/run.md` template has been generated.

- The information in `run.json` is complete (git, config, env, metrics).

5. **Fill in `run.md`**

   Spend 2 minutes completing the five-element template.

Starting from the next experiment, logging will be automatic and zero-cost. The only thing you need to do is spend 2 minutes writing a 5-line summary—an investment that will yield a hundredfold return three months later.