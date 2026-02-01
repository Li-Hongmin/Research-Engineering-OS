#!/usr/bin/env python3
"""Insert comics into English markdown files based on section keywords."""

import re
from pathlib import Path

# Mapping: (filename, keyword_in_heading) -> comic_image
# More specific patterns first to avoid duplicates
COMIC_MAPPINGS = [
    # Chapter 01 - Why Flip
    ("01-why-flip.md", r"Story Setup.*Deadline", "01_deadline_panic.png"),
    ("01-why-flip.md", r"Why This Happens.*Three Types", "01_three_debts.png"),
    ("01-why-flip.md", r"Symptom Checklist", "01_04_symptoms.png"),
    ("01-why-flip.md", r"Late-Stage Explosion.*Inevitable", "01_last_minute_chaos.png"),
    ("01-why-flip.md", r"### Exploration Debt", "01_05_exploration_debt.png"),
    ("01-why-flip.md", r"### Validation Debt", "01_06_validation_debt.png"),
    ("01-why-flip.md", r"### Reproducibility Debt", "01_07_reproducibility_debt.png"),
    ("01-why-flip.md", r"10-Minute Actions", "01_08_ten_min_action.png"),

    # Chapter 02 - Experiment Unit
    ("02-experiment-unit.md", r"Six.*Questions", "02_01_six_questions.png"),
    ("02-experiment-unit.md", r"Naming.*Experiment", "02_02_experiment_naming.png"),
    ("02-experiment-unit.md", r"Code.*Version", "02_03_code_version.png"),
    ("02-experiment-unit.md", r"Config", "02_04_config.png"),
    ("02-experiment-unit.md", r"Data.*Version", "02_05_data_version.png"),
    ("02-experiment-unit.md", r"Environment", "02_06_environment.png"),
    ("02-experiment-unit.md", r"Assemble", "02_07_assemble.png"),

    # Chapter 03 - Repo Layout
    ("03-repo-layout.md", r"Illusion.*Success", "03_01_early_success.png"),
    ("03-repo-layout.md", r"Ideal.*Structure", "03_02_ideal_structure.png"),
    ("03-repo-layout.md", r"Fast.*Slow", "03_03_fast_slow.png"),
    ("03-repo-layout.md", r"`src/`", "03_04_src_dir.png"),
    ("03-repo-layout.md", r"`experiments/`", "03_05_experiments_dir.png"),
    ("03-repo-layout.md", r"final", "03_06_avoid_final.png"),
    ("03-repo-layout.md", r"Collapse", "03_08_collapse.png"),

    # Chapter 04 - Git Proof
    ("04-git-proof.md", r"Git.*Evidence", "04_01_git_detective.png"),
    ("04-git-proof.md", r"Branch.*Strategy", "04_02_branch_strategy.png"),
    ("04-git-proof.md", r"Commit.*Atomic", "04_03_commit_evidence.png"),
    ("04-git-proof.md", r"Makefile", "04_04_makefile.png"),
    ("04-git-proof.md", r"Reviewer.*Asks", "04_05_reviewer_crisis.png"),
    ("04-git-proof.md", r"Tag.*Milestone", "04_07_tag_milestone.png"),
    ("04-git-proof.md", r"\.gitignore", "04_10_gitignore.png"),

    # Chapter 05 - DoD
    ("05-dod.md", r"Hero", "05_01_checklist_hero.png"),
    ("05-dod.md", r"Quality.*Gate", "05_02_quality_gate.png"),
    ("05-dod.md", r"Trap.*Cannot.*Reproduce", "05_03_trap1.png"),
    ("05-dod.md", r"Trap.*Don.*Know.*Why", "05_04_trap2.png"),
    ("05-dod.md", r"Trap.*Inconsistent", "05_05_trap3.png"),
    ("05-dod.md", r"Good Enough", "05_06_good_enough_trap.png"),
    ("05-dod.md", r"Minimal.*DoD", "05_07_minimal_dod.png"),
    ("05-dod.md", r"Enhanced.*DoD", "05_08_enhanced_dod.png"),
    ("05-dod.md", r"Archaeology", "05_09_code_archaeology.png"),
    ("05-dod.md", r"Team.*Standard", "05_10_team_dod.png"),

    # Chapter 06 - Logging
    ("06-logging.md", r"Two.*Layer", "06_05_two_layer.png"),
    ("06-logging.md", r"`run\.md`", "06_06_run_md.png"),
    ("06-logging.md", r"`run\.json`", "06_07_run_json.png"),
    ("06-logging.md", r"Auto.*Record", "06_08_auto_record.png"),
    ("06-logging.md", r"MLflow", "06_09_mlflow.png"),

    # Chapter 07 - AI Workflow
    ("07-ai-workflow.md", r"Speed.*Trap", "07_01_ai_speed_trap.png"),
    ("07-ai-workflow.md", r"Unverified", "07_02_unverified.png"),
    ("07-ai-workflow.md", r"Hidden.*Bug", "07_03_hidden_bug.png"),
    ("07-ai-workflow.md", r"Lost.*Control", "07_04_lost_control.png"),
    ("07-ai-workflow.md", r"AI.*Collaborat", "07_06_ai_collaboration.png"),
    ("07-ai-workflow.md", r"Verify.*AI", "07_07_verify_ai.png"),
    ("07-ai-workflow.md", r"Test.*Trust", "07_08_test_first.png"),
    ("07-ai-workflow.md", r"Rollback", "07_09_rollback.png"),
    ("07-ai-workflow.md", r"Review.*Discipline", "07_10_review.png"),

    # Chapter 08 - Multi Path
    ("08-multi-path.md", r"Crossroad", "08_01_crossroads.png"),
    ("08-multi-path.md", r"Week 1", "08_02_week1.png"),
    ("08-multi-path.md", r"Week 3", "08_03_week3.png"),
    ("08-multi-path.md", r"Week 6", "08_04_week6.png"),
    ("08-multi-path.md", r"Path.*Management", "08_05_path_management.png"),
    ("08-multi-path.md", r"Naming.*Convention", "08_06_path_naming.png"),
    ("08-multi-path.md", r"Path.*Tracking", "08_07_path_tracking.png"),
    ("08-multi-path.md", r"Path.*Comparison", "08_08_path_compare.png"),
    ("08-multi-path.md", r"Weekly.*Clean", "08_09_weekly_cleanup.png"),

    # No-Boom
    ("no-boom.md", r"Defuse.*Bomb", "09_01_defuse_bomb.png"),
    ("no-boom.md", r"Warning.*System", "09_02_warning_system.png"),
    ("no-boom.md", r"Self.*Check", "09_03_self_check.png"),
    ("no-boom.md", r"Validate.*Early", "09_04_validate_early.png"),
    ("no-boom.md", r"Success.*Submit", "09_05_success_submit.png"),
    ("no-boom.md", r"Monday", "09_06_monday_crisis.png"),
    ("no-boom.md", r"Tuesday", "09_07_tuesday_baseline.png"),
    ("no-boom.md", r"Wednesday", "09_08_wednesday_ablation.png"),
    ("no-boom.md", r"Thursday", "09_09_thursday_data.png"),
    ("no-boom.md", r"Friday", "09_10_friday_doubt.png"),

    # Team
    ("team.md", r"Strong.*Weak", "10_01_strong_weak.png"),
    ("team.md", r"Monday.*Standup", "10_02_monday_standup.png"),
    ("team.md", r"Wednesday.*Conflict", "10_03_wednesday_conflict.png"),
    ("team.md", r"Friday.*Disaster", "10_04_friday_disaster.png"),
    ("team.md", r"Duplicate.*Work", "10_05_duplicate_work.png"),
    ("team.md", r"Hidden.*Knowledge", "10_06_hidden_knowledge.png"),
    ("team.md", r"Integration.*Cost", "10_07_integration_cost.png"),
    ("team.md", r"Team.*Standup", "10_08_team_standup.png"),
    ("team.md", r"Code.*Review", "10_09_code_review.png"),
    ("team.md", r"PR.*Template", "10_10_pr_template.png"),
    ("team.md", r"Naming.*Convention", "10_11_naming_convention.png"),
    ("team.md", r"Team.*Victory", "10_12_team_victory.png"),
]

def clean_duplicate_images(content: str) -> str:
    """Remove duplicate consecutive image lines."""
    lines = content.split("\n")
    new_lines = []
    prev_image = None

    for line in lines:
        # Check if this is an image line
        match = re.match(r'!\[.*\]\((images/comics/[^)]+)\)', line)
        if match:
            img_path = match.group(1)
            if img_path == prev_image:
                continue  # Skip duplicate
            prev_image = img_path
        else:
            if line.strip():  # Reset on non-empty non-image line
                prev_image = None
        new_lines.append(line)

    return "\n".join(new_lines)

def insert_comics(src_dir: Path):
    """Insert comics into English markdown files."""
    comics_dir = "images/comics"
    inserted_count = 0
    used_patterns = set()

    for md_file in sorted(src_dir.glob("*.md")):
        filename = md_file.name
        content = md_file.read_text(encoding="utf-8")

        # First clean any duplicate images from previous runs
        content = clean_duplicate_images(content)

        # Remove all existing comic images to start fresh
        content = re.sub(r'\n*!\[.*\]\(images/comics/[^)]+\)\n*', '\n', content)

        lines = content.split("\n")
        new_lines = []
        file_insertions = 0

        for i, line in enumerate(lines):
            new_lines.append(line)

            # Check if this is a heading line
            if line.startswith("#"):
                # Find matching comic for this heading
                for fn, pattern, comic in COMIC_MAPPINGS:
                    if fn != filename:
                        continue

                    # Create unique key for this pattern
                    pattern_key = f"{fn}:{pattern}"
                    if pattern_key in used_patterns:
                        continue

                    if re.search(pattern, line, re.IGNORECASE):
                        # Mark pattern as used
                        used_patterns.add(pattern_key)

                        # Extract alt text from comic filename
                        alt_text = comic.replace(".png", "").split("_", 1)[-1].replace("_", " ").title()
                        img_line = f"\n![{alt_text}]({comics_dir}/{comic})\n"
                        new_lines.append(img_line)
                        file_insertions += 1
                        print(f"  ✅ {filename}: {alt_text}")
                        break

        if file_insertions > 0:
            # Clean up extra blank lines
            result = "\n".join(new_lines)
            result = re.sub(r'\n{3,}', '\n\n', result)
            md_file.write_text(result, encoding="utf-8")
            inserted_count += file_insertions
            print(f"📄 {filename}: {file_insertions} images inserted")

    return inserted_count

if __name__ == "__main__":
    src_en = Path(__file__).parent / "src_en"
    print("🎨 Inserting comics into English markdown files...")
    print("=" * 50)
    total = insert_comics(src_en)
    print("=" * 50)
    print(f"✅ Total: {total} images inserted")
