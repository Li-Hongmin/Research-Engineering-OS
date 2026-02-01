# The Smallest Unit of a Project Is Not “Code,” but an “Experiment”

In research projects, if you treat the smallest unit as “code,” you will naturally tend to use Git to organize everything: commits, branches, merges, rollbacks, and so on. This habit is highly effective in engineering development, but it often fails in research work. The reason is that the ultimate output of research is not a piece of code itself, but a verifiable conclusion or discovery. In other words, code is merely one means to reach a research conclusion; experimental results are the outcomes we truly care about.

Conclusions come from experiments. An experiment is driven by a set of traceable input conditions and produces reviewable output results. Therefore, this book defines “experiment” as the minimal unit of project operations, and organizes directory structure, logging, automation workflows, and acceptance criteria around it. By treating experiments as the fundamental unit, we can ensure that every result is well-grounded, improving the reproducibility and reliability of research.

## Definition of an Experiment: Turning “I Changed Something” into a Comparable Object

Simply put, **an experiment = code version + configuration + data version + environment + outputs + metrics**. More plainly: **any result you obtain must be able to answer “Where exactly did it come from?”** In other words, whenever you “change something” in code or configuration and produce a result, that run should form an independent, comparable experimental object.

### Six Questions That Must Be Answerable

![01 Six Questions](images/comics/02_01_six_questions.png)

To ensure traceability and comparability of experimental results, each experiment must be able to answer at least the following six key questions:

1. **What code was used?** — Specify the code version, such as the Git commit hash, and whether the repository had uncommitted changes at the time (dirty). This ensures we know exactly which version of the code was used to run the experiment.

2. **What configuration was used?** — Specify the set of configuration parameters used, such as the configuration file path and the final parameter values after parsing and expansion. Configuration determines hyperparameters and runtime options and must be recorded explicitly.

3. **What data was used?** — Specify the dataset version or hash, as well as how the data was split (train/validation/test split). Different data directly affects results, so the data source and version must be described precisely. Ideally, data consistency can be proven via a data hash or a manifest file.

4. **What environment was used?** — Describe the environment information required for execution, such as the Python version, dependency versions, driver versions, and key hardware configuration (CPU/GPU model, etc.). Environmental differences may affect reproducibility; if someone reruns the experiment elsewhere, they need to know the original environment.

5. **Where are the outputs stored?** — Clearly record the locations of all files produced by the experiment, such as model weights, logs, prediction results, cached intermediate features, and so on. Outputs are the basis for subsequent analysis and verification; they must be preserved and retrievable.

6. **What are the metrics, and how are they computed?** — Provide the metrics used for evaluation and their computation methods, including evaluation scripts and any post-processing details. Different metric conventions make results incomparable; metric definitions must be transparent and consistent.

None of these six elements can be omitted. If any one question cannot be answered, the experiment is not fully reproducible, and any conclusion drawn will lack persuasiveness. Only when all six are satisfied can we say “we know where this result came from,” and only then can we precisely reproduce it later or compare it against other experiments.

#### Case: AI Generates “Seemingly Complete” Code That Cannot Run

In cross-language migration (“code translation”) scenarios, API hallucination frequently occurs: the model generates functions that look reasonable but do not actually exist in the target language’s libraries, causing the generated code to be non-executable. Researchers ultimately have to rewrite and fix files one by one.. If we mistakenly treat “code” as the smallest unit of a project, we may fall into the trap of focusing only on how many files or lines of code were generated. The significance of using “experiment” as the smallest unit is that our acceptance criterion is not how many files were produced, but whether we produced **runnable deliverables and metrics that can be evaluated comparatively**. In other words, whether an experiment succeeds does not depend on how many lines of code were changed, but on whether you obtained an executable model or result, along with clear evaluation metrics to demonstrate the effect of the change.

## The Experimental Object Model: Decomposing the Research Process into Stable “Five Elements”

To make each stage of the research workflow clear, controllable, easy to compose, and convenient for tool automation, we can describe the elements of the experimental process using a fixed set of conceptual objects. Each experiment involves the following five objects:

- **config (configuration):** All key parameter settings for a single run. It should be serializable (for saving and recording), support partial overrides (for modifying defaults), and be easy to diff. A config defines how the experiment should run—e.g., model architecture parameters, learning rate, number of training epochs—and serves as the blueprint of the experiment.

- **dataset:** The data version used and the splitting strategy. The dataset object should clearly identify the data used, for example via a version number, data hash, or manifest file to prove data consistency. This ensures that different experiments share the same data basis, or that data differences are explicitly understood.

- **run:** A concrete code execution process. A run typically records a unique run_id, timestamp, the commit version of the code used, the corresponding config, random seed (seed), and runtime logs. A run represents an experiment that actually occurred—the process record of putting configuration and code into practice to obtain results.

- **artifact:** All output files generated by a run. For example, trained model weight files, model predictions on the test set, cached intermediate features, and intermediate data produced during evaluation are all artifacts. Artifacts are the direct outputs of an experiment; subsequent analysis, comparison, and reporting are built on them. Preserving artifacts allows us to inspect or reuse results at any time without repeating expensive computation.

- **report:** A human-readable summary, including plots, tables, key conclusion statements derived from experiments, and analyses of failure cases. A report can be viewed as transforming quantitative experimental results into qualitative insights; it often aggregates metrics and artifacts from multiple runs and provides references for readers or decision-makers. It is the final form in which experimental outcomes are presented.

The relationships among these objects can be summarized in one sentence:

> config + dataset + env (environment), executed by code, produces a run; that run yields several artifacts; based on artifacts and computed metrics, we write a report.

With this object model, we decompose a complex research process into several stable “noun” objects, making it easier to think and communicate. For example, when discussing an experiment, we can clearly distinguish “which config and dataset were used,” “which artifacts were produced,” and “how the final report is written.” More importantly, this partitioning lays the foundation for subsequent tooling: we can define conventions for each object type (e.g., managing config with YAML files, storing artifacts in specific directories), thereby standardizing and automating the experimental workflow.

## run_id: Making Every Run Unambiguously Referable

When writing a paper or report, you may need to frequently cite results produced under a specific configuration, e.g., “our best result under a certain setting is …”. If that experiment does not have a stable and unambiguous name, your description will be vague, which hinders reader understanding and can easily lead to confusion across experiments. To avoid this, we recommend generating a unique run_id for every run, and making this ID as readable and time-ordered as possible.

A practical approach is to combine a timestamp with a short description to form an ordered and interpretable name. For example, you can name runs by date and start time, then add a brief summary of the experiment:

    2026-02-01_0930_baseline          (baseline experiment started at 09:30 on Feb 01, 2026)
    2026-02-01_1130_ablation_noaug    (ablation experiment started at 11:30 on Feb 01, 2026 — removing data augmentation)
    2026-02-02_0045_sweep_lr3e-4      (hyperparameter grid experiment started at 00:45 on Feb 02, 2026 — learning rate 3e-4)

With this naming convention, lexicographic ordering of files corresponds to chronological ordering, making it easy to see the sequence and approximate content at a glance. Each run_id is both unique and readable, avoiding vague and non-comparable names such as “experiment1” and “experiment2”.

For file organization, you can use the run_id as the directory name and centrally store all outputs of that experiment. For example:

    outputs/<run_id>/
        run.json        # Metadata about this run (e.g., code version, start time, parameter configuration)
        run.md          # Optional: a log recording the description, observations, and preliminary conclusions for this run
        metrics.json    # Metric results for this experiment
        artifacts/      # Subfolder containing models, predictions, and other files produced by this run

With this structure, we can conveniently manage and query experimental results. For instance, when you want to compare multiple experiments, you can directly open metrics.json under the corresponding run_id directory to inspect metrics, or load models from artifacts for analysis.

### Avoiding “final” chaos:

Many people like to use the word “final” when naming experiments, but a common situation is that after completing “experiment_final” they discover a small improvement is needed, leading to “experiment_final_v2” or even “final_final”. In the end, even the author cannot tell which one is truly the final result, causing confusion and misunderstanding. This is a typical consequence of non-standard naming. With the run_id approach, you no longer rely on such vague labels to mark the final outcome; instead, you identify each attempt with clear time and content descriptors. As for which experiment is ultimately adopted, you can simply state in the report which run_id is used. In short, do not let words like “final” interfere with experiment management; with a unified run naming scheme, every experiment is well-grounded—run N is run N—and confusion disappears.

## A practical principle: put “comparability” as the top priority

In research, what often determines the pace of progress is not the physical time spent training models, but the repetition and uncertainty caused by a lack of comparability across experiments. If experimental conditions are inconsistent, then even after you obtain numerical results, it is difficult to determine where differences come from, and you may even end up discarding and redoing work. Common negative examples include:

- **Inconsistent evaluation criteria:** The baseline and your new method use different evaluation scripts, resulting in different measurement conventions and making direct comparison impossible. This forces you to spend extra time re-evaluating both under the same standard.

- **Inconsistent post-processing:** Experiment A and Experiment B use different post-processing or filtering strategies, causing metrics to be on different scales. For example, one result applies additional threshold filtering while the other does not; without unified processing, it is hard to clearly argue which method is better.

- **Inconsistent data splits:** Experiment B temporarily switched datasets or splitting schemes without recording it; comparing its results with Experiment A is then inherently unfair—B may have used an easier test set while claiming superior performance. In such cases, even “better” results are meaningless because the comparison is not made on the same baseline.

For these reasons, we should always keep in mind: **any important conclusion must come from the same evaluation pipeline, ensuring comparability between experiments**. That is, when comparing two experiments, aside from the intentionally changed variable (e.g., model architecture, hyperparameters), all other components—data, evaluation criteria, post-processing methods, random seeds, etc.—should be kept as consistent as possible or at least be traceable. Once an inconsistency is found, either correct it in a new experiment and rerun, or explicitly document the differences in the report and avoid direct comparison.

Prioritizing comparability may require additional effort to align conditions when designing experiments, but it actually accelerates overall research progress. You avoid repeated trials and debates caused by unfair comparisons, and the conclusions from a single experiment become genuinely defensible and withstand scrutiny.

Starting from this chapter, all subsequent chapters—including repository structure, Git workflow, DoD (Definition of Done), logging practices, and AI-assisted workflows—will revolve around two core goals: “experiment traceability” and “result comparability”. The principles established in this chapter will run through the entire methodology of research management.