# Your Repository Structure Is Your Second Brain

The “messiness” of research code is often not due to lack of ability, but because research is inherently parallel exploration: at the same time, you must maintain multiple hypotheses, multiple implementations, multiple experimental entry points, multiple outputs, and multiple plots.

When these things are piled together without structure, your brain is forced to act as an index: **Which script still runs? Which output is trustworthy? Which change affected the metrics?**

The purpose of a repository structure is not to look nice, but to **reduce cognitive load**: so that you can judge—without relying on memory—“Can this code be deleted? Is this output reliable? Is this path reproducible?”

## Real Case: The Cost of Rapidly Piling Up Code

![从混乱到整洁](../images/comics/03_messy_to_clean.png)

When I first started using AI coding assistants, I learned this lesson the hard way. To quickly validate an idea, I had Copilot generate a large amount of “runnable” code—data loading, model definitions, training loops, evaluation scripts, and so on. Within a few hours, I had built what looked like a complete framework.

### Early “success”:

![03 04 early success](../images/comics/03_04_early_success.png)

The code did run, and the experiments produced results. Excited, I continued iterating, repeatedly asking the AI to add new features: data augmentation, different model variants, various evaluation metrics... Each change had an “immediate effect,” and the codebase expanded rapidly.

#### The beginning of the collapse:

![03 05 collapse begins](../images/comics/03_05_collapse_begins.png)
Two weeks later, when I needed to prepare ablation and comparison experiments for a paper, the problems surfaced:

- I could not tell which script was the latest and which was obsolete;

- The same data-loading logic had been copy-pasted into five different files, each with slight differences;

- The baseline and the new method used different evaluation code, so the results were not comparable at all;

- I wanted to reproduce a “very good result,” but could not find the configuration and data version used at the time.

#### Starting over:

![03 06 rewrite pain](../images/comics/03_06_rewrite_pain.png)

In the end, I had to stop all new experiments and spend three full days **rewriting almost all the code**. This rewrite was not because the AI-generated code had bugs, but because of **a lack of structure**: reusable core logic and one-off experimental scripts were mixed together; quick-and-dirty trial code was not cleaned up in time; outputs were scattered everywhere and hard to trace.

This experience made me deeply understand: AI can help you produce code quickly, but **the structure must be designed by humans**. If, from the beginning, you separate “stable” from “exploratory,” and organize outputs by run_id, you will not fall into this kind of chaos later.

#### Case references:

This is not an isolated issue. When you use AI to quickly pile up a “runnable” repository but fail to isolate reusable code from one-off experimental entry points, the common ending is: every module must be rewritten, and almost all AI-generated fragments are replaced. **Structure is the first line of defense against this kind of rework.**

## A Copy-and-Paste Directory Layout (Research-Friendly)

![完美的目录结构](../images/comics/03_folder_tree.png)

    repo/
      src/                 # Core library: reusable, testable, maintainable (slow variables)
      experiments/         # Experimental entry points: one-off glue code (fast variables, disposable)
      configs/             # Unified configuration: yaml/json (diffable, traceable)
      data/                # Only pointers or small samples; manage large data externally
      outputs/             # Run artifacts: organized by run_id (cleanable/archivable)
      reports/             # Paper figures and conclusions: auto-generated from outputs
      scripts/             # Utility scripts for data prep/download/evaluation, etc.
      tests/               # Unit tests + smoke tests (hold the line)
      Makefile             # Common entry points: train/eval/reproduce/test
      README.md
      CLAUDE.md            # AI coding rules (recommended)

## Fast Variables vs. Slow Variables: Separate “Stability” from “Exploration”

![快慢变量分离](../images/comics/03_fast_slow_variables.png)
It is recommended to divide the contents of a repository into two categories:

- **Slow variables (stable):** parts that will be maintained long-term, reused repeatedly, and require test coverage.

- **Fast variables (explore):** entry scripts for quickly testing a hypothesis, short-lived glue, and one-off analyses.

In this book’s terminology: `src/` contains slow variables, and `experiments/` contains fast variables.

**Rule of thumb:** exploration can be dirty, but the core library must be clean; exploration can be fast, but evaluation must be stable.

### Why is this separation so important?

In my rewrite experience, the biggest pain point was **being unable to distinguish assets from consumables**. When all code is mixed together, you dare not delete anything (for fear of removing important functionality), and you also dare not refactor aggressively (for fear of affecting other experiments). Once you clearly define `src/` as assets and `experiments/` as consumables, the psychological burden is greatly reduced:

- Changes to `src/` must be made cautiously and require tests;

- Changes to `experiments/` can be made freely—after the trial, delete it.

## Definition of Done (DoD) for Each Directory

A directory name only truly reduces chaos when “what should go in” and “what should not go in” are sufficiently clear.

### src/: Core Library (Reusable, Testable)

![03 07 src directory](../images/comics/03_07_src_directory.png)
- Store reusable modules: data loading, model components, losses, evaluation, general utilities.

- Must be testable: at minimum, have smoke tests covering key pipelines.

- No hard-coding: do not include paths/parameters that are only useful for a particular run.

#### Anti-example:

In my rewrite case, the original “data loading” code hard-coded the path and preprocessing for a specific experiment, forcing new experiments to copy-paste and modify it. If the paths and parameters had been passed in as function arguments from the start, this problem would not have occurred.

### experiments/: Experimental Entry Points (Disposable)

![03 08 experiments directory](../images/comics/03_08_experiments_directory.png)
- Store only entry points and glue: **short-lived is allowed**; delete after use.

- Any logic proven valuable and reusable should be migrated to `src/` once it stabilizes.

#### Practical advice:

Name each experiment script by date or run_id, e.g., `2026-02-01_baseline.py`. This makes it immediately obvious which experiments are old and which are new. Regularly (e.g., weekly) clean up scripts older than one month that have no value.

### configs/: Configuration (Traceable)

- Every “paper-candidate conclusion” must correspond to a config (or a traceable way to generate it).

- A config must expand to the final parameters (avoid drift in default values).

### outputs/: Artifacts (Cleanable/Archivable)

- Store only run artifacts, and organize them **by run_id**.

- No overwriting: do not reuse or manually modify the same run_id directory.

- Archive important artifacts: move them into long-term storage; the repository should not carry large binaries.

### reports/: Figures and Conclusions (Regenerable)

- As much as possible, store only script-generated figures/tables and draft conclusions.

- All figures and tables in the paper must be reproducible from `outputs/`, avoiding manual drag-and-drop.

### tests/: Testing (Hold the Line)

- At least one 1–3 minute smoke test: run through data loading $\rightarrow$ forward pass $\rightarrow$ loss $\rightarrow$ evaluation.

- Add assertions for critical functions: shape, NaN, value ranges, signals of data leakage, etc.

## Converge Entry Points: Make “How to Run” Obvious

![03 09 makefile entry](../images/comics/03_09_makefile_entry.png)

The most common waste in research is that others (including your future self) do not know how to run the code.

It is recommended to converge all commonly used entry points into a `Makefile` (or an equivalent task tool):

- `make test`

- `make train CONFIG=...`

- `make eval RUN=...`

- `make reproduce RUN=...`

When entry points are few enough and stable enough, you can keep complexity internal while exposing reproducibility externally.

## Progressive Refactoring: Migrating from a Messy Project to a Sound Structure

If you already have a “messy” legacy project, do not try to tear it down and rebuild everything at once. Below is a step-by-step refactoring process:

### Step 1: Identify and Separate Slow Variables vs. Fast Variables

1.  **Review the existing code:** Scan the entire project and mark which modules are core functionality (to be maintained long-term and reused repeatedly) and which are one-off experimental scripts.

2.  **Create new directories:**

- Create `src/` and migrate modules that you are sure will be reused into it;

- Create `experiments/` and move assorted run scripts and temporary code into it.

3.  **Complete a coarse layering:** After this step, the project structure will begin to look clearer, and the indexing burden in your head will be reduced accordingly. Perfection is not required; simply separate the obvious parts first.

### Step 2: Extract Configurations and Parameters

1.  **Find hard-coded values:** Scan the code and identify all hard-coded key parameters (learning rate, batch size, paths, etc.).

2.  **Create configuration files:** Under `configs/`, create YAML or JSON files to manage parameters centrally.

3.  **Replace incrementally:** Do not modify all code at once. Instead, refactor one script at a time, and proceed to the next only after confirming it runs correctly.

#### Practical experience:

During my refactoring, extracting configurations alone helped me uncover three hidden bugs—the “seemingly identical” parameters in different scripts actually had different values, making results incomparable.

### Step 3: Standardize Output Paths

1.  **Define a convention:** Decide to use the `outputs/<run_id>/` structure.

2.  **Modify the code:** Adjust all experiment entry points so that outputs are archived by run_id.

3.  **Clean up old outputs:** Organize or delete scattered legacy output files to keep the outputs directory clean.

### Step 4: Add Basic Tests

1.  **Write a smoke test:** Create a 1–3 minute quick test to verify that the core pipeline runs end-to-end.

2.  **Run after each refactor:** Ensure changes do not break basic functionality.

3.  **Increase coverage gradually:** As refactoring progresses, gradually add unit tests for critical functions.

#### Key principle:

Progressiveness matters. Do not attempt to finish all refactoring in one go; instead, ensure existing functionality remains intact at each step before moving on. My rewrite took three days, but if I had adopted progressive refactoring from the start, it could have been spread over a week without affecting the normal pace of experiments.

## Directory Hierarchy Management for Multi-Task / Multi-Project Work

When facing multiple related but independent research tasks, how to organize directories becomes an important question.

### Principle: Prefer Separate Repositories

**Best practice:** Use an independent code repository for each research project. This helps to:

- Avoid dependency conflicts across projects;

- Ensure independence in version control;

- Simplify reproduction (each project has its own environment and dependencies).

#### Rule of thumb:

If two projects differ substantially in dependency versions, datasets, or runtime environments, **strongly consider splitting into separate repositories**.

### Layered Structure for Multiple Projects in a Single Repository

If you truly need to manage multiple related tasks within one repository (e.g., multiple experiments for the same paper, or subprojects that share a large amount of code), you can adopt the following structure:

    repo/
      projectA/
        src/
        experiments/
        configs/
        outputs/
        README.md
      projectB/
        src/
        experiments/
        configs/
        outputs/
        README.md
      common/
        src/               # Core code shared across projects
        tests/             # Tests for shared functionality
        scripts/           # General-purpose utility scripts
      README.md            # Overall description
      Makefile             # Cross-project common commands

### Naming Conventions and Environment Isolation

- **Configuration file naming:** Use project prefixes, e.g., `configs/projectA_baseline.yaml`, `configs/projectB_ablation.yaml`.

- **Output directories:** You may maintain outputs within each project subdirectory, or unify them at the repository root while using the project name as a prefix: `outputs/projectA/<run_id>/`.

- **Environment management:** Even if the code lives in one repository, it is still recommended to maintain separate virtual environments or Docker containers for different projects to prevent dependency conflicts.

### When to Share Code vs. When to Copy Code

**When to share code into common/:**

- Basic utility functions needed by multiple projects;

- General data loading or preprocessing logic;

- Standardized evaluation metric computation.

**When to copy code:**

- The code is still changing rapidly and requirements may diverge across projects;

- Sharing would cause excessive coupling and harm independence;

- The project is nearing completion and future synchronized updates are unlikely.

#### Practical recommendation:

At the beginning, prefer copying; extract into common/ only after the code is truly stable and you are confident it needs to be shared. Premature abstraction leads to frequent modifications of shared code and increases maintenance burden.

## Quick Start: Use AI to Generate Your Repository Template

To speed up this process, your advisor suggests using an AI assistant. Simply describe the directory structure and files you need—for example, in one sentence to Claude:

> "Generate a standard research project template with directories: src/, experiments/, configs/, outputs/, data/, reports/, scripts/, tests/. Include a README.md explaining each directory's purpose and a Makefile with targets for test, train, eval, and reproduce."

Within a minute, a complete project structure with all essential files is generated. You now have a solid foundation before writing a single line of code—a perfect example of "standing on the shoulders of giants." Going forward, you decide to initialize every new project this way.

### Why This Matters

Using AI to generate boilerplate is not lazy; it is **structural wisdom**. By outsourcing the tedious template creation, you ensure every project starts with best practices. The human effort is then focused on the unique science, not on redoing infrastructure.

## A 10-Minute Action: "Layer Once" Your Current Project

If you do only one thing right now: roughly split the current repository into slow variables and fast variables.

1.  Create `src/` and move in modules you are sure will be reused.

2.  Create `experiments/` and move all entry scripts into it, allowing them to be short-lived.

3.  Create `configs/` and extract key parameters from scripts.

4.  Standardize all outputs into `outputs/<run_id>/`.

You will immediately feel an increase in “controllability,” because you begin to distinguish what is an asset versus what is a one-off consumable.

### From personal experience:

If I had established this structure when I first started using an AI coding assistant, the three-day rewrite could have been entirely avoided. A good structure is not for aesthetics; it is to **stop forcing your brain to remember every detail**, and to make the repository itself your reliable “second brain.”