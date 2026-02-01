#!/usr/bin/env python3
"""
Parallel manga comic generation using concurrent.futures.
Generates multiple images simultaneously for faster processing.
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: pip install openai")
    sys.exit(1)

import requests

# Thread-local storage for clients
thread_local = threading.local()

# Manga style
STYLE = """Japanese manga illustration, clean anime art style,
young Asian researcher as protagonist (lab coat or casual, may have glasses),
expressive anime eyes, dynamic composition, warm colors,
professional digital art, cel-shading, no text or speech bubbles. """

# All scenarios (same as v2)
SCENARIOS = {
    "01-why-flip": [
        ("01_01_deadline_panic", "截止日期恐慌", STYLE + "Researcher panicking at desk, papers flying, clock showing 11:59, multiple error screens, coffee cups everywhere, dramatic lighting."),
        ("01_02_three_debts", "三类债务怪物", STYLE + "Researcher facing three shadow monsters: tangled code, broken test tubes, scattered puzzles. Heroic stance."),
        ("01_03_last_minute_chaos", "最后时刻混乱", STYLE + "Researcher rushing through falling documents and deadlines. Dynamic action scene."),
        ("01_04_symptoms", "症状自查", STYLE + "Researcher looking in mirror seeing warning signs. Self-reflection, concerned."),
        ("01_05_exploration_debt", "探索债", STYLE + "Researcher surrounded by messy prototypes, quick hacks, tangled wires. Overwhelmed."),
        ("01_06_validation_debt", "验证债", STYLE + "Researcher with incomplete tests, missing controls. Scientific equipment half-done."),
        ("01_07_reproducibility_debt", "复现债", STYLE + "Researcher rebuilding experiment from scattered pieces. Missing configs."),
        ("01_08_ten_min_action", "10分钟行动", STYLE + "Researcher taking first step with checklist, sunrise background. Hope."),
    ],
    "02-experiment-unit": [
        ("02_01_experiment_assembly", "组装实验", STYLE + "Researcher assembling glowing experiment blocks: code, data, config. Clean lab."),
        ("02_02_six_questions", "六个关键问题", STYLE + "Researcher examining six holographic questions becoming answers. Detective style."),
        ("02_03_run_id_naming", "实验命名", STYLE + "Researcher organizing timestamped folders. Satisfaction of order."),
        ("02_04_code_version", "代码版本追踪", STYLE + "Researcher with glowing git hash, code history flowing. Version control."),
        ("02_05_config_management", "配置管理", STYLE + "Researcher adjusting control panel dials: learning rate, batch size. Precision."),
        ("02_06_data_version", "数据版本", STYLE + "Researcher cataloging data with hashes. Organized library."),
        ("02_07_environment_capture", "环境捕获", STYLE + "Researcher freezing environment snapshot in crystal. Time capsule."),
        ("02_08_final_chaos", "避免final混乱", STYLE + "Researcher rejecting 'final_final_v2' folders. Comedy, clear preference."),
    ],
    "03-repo-layout": [
        ("03_01_messy_to_clean", "从混乱到整洁", STYLE + "Split scene: left chaos, right organized lab. Transformation."),
        ("03_02_folder_tree", "完美目录结构", STYLE + "Researcher building tree: src/, experiments/, configs/. Architectural."),
        ("03_03_fast_slow_variables", "快慢变量", STYLE + "Researcher balancing blue (slow) and red (fast) orbs. Balance."),
        ("03_04_early_success", "早期成功假象", STYLE + "Researcher celebrating but shadows lurking. False confidence."),
        ("03_05_collapse_begins", "崩溃开始", STYLE + "Researcher watching codebase fall apart. Panic setting in."),
        ("03_06_rewrite_pain", "重写之痛", STYLE + "Researcher starting over, throwing old code. Determined but tired."),
        ("03_07_src_directory", "src目录", STYLE + "Researcher polishing crystal 'src/' box with tested modules. Quality."),
        ("03_08_experiments_directory", "experiments目录", STYLE + "Researcher with disposable 'experiments/' notebooks. Ephemeral."),
        ("03_09_makefile_entry", "Makefile入口", STYLE + "Researcher at control panel: 'make test', 'make train'. Simple."),
    ],
    "04-git-proof": [
        ("04_01_git_detective", "Git侦探", STYLE + "Researcher as detective following commit trail. Investigation."),
        ("04_02_branch_strategy", "分支策略", STYLE + "Researcher navigating branch paths: main, feature, experiment. Map."),
        ("04_03_commit_evidence", "提交作为证据", STYLE + "Researcher in courtroom with commits as evidence. Authority."),
        ("04_04_reviewer_crisis", "审稿危机", STYLE + "Researcher receiving demands, searching old commits. Urgency."),
        ("04_05_commit_too_big", "提交粒度太大", STYLE + "Researcher facing massive single commit. Frustration."),
        ("04_06_experiment_time_mismatch", "实验时间错位", STYLE + "Researcher confused by timeline paradox. Confusion."),
        ("04_07_branch_chaos", "分支混乱", STYLE + "Researcher lost in tangled branches. Lost."),
        ("04_08_tag_milestone", "Tag里程碑", STYLE + "Researcher planting golden flag at peak. Achievement."),
        ("04_09_gitignore_clean", "gitignore保持干净", STYLE + "Researcher filtering out large files. Purification."),
    ],
    "05-dod": [
        ("05_01_checklist_hero", "清单英雄", STYLE + "Researcher checking final item on golden list. Victory."),
        ("05_02_quality_gate", "质量门", STYLE + "Researcher guarding quality gate. Guardian."),
        ("05_03_almost_done_trap", "差不多就行陷阱", STYLE + "Researcher stepping on trap, about to fall. Warning."),
        ("05_04_mine_reproduce", "埋雷1:无法复现", STYLE + "Researcher finding hidden mine under code. Danger."),
        ("05_05_mine_unknown_why", "埋雷2:不知道为什么", STYLE + "Researcher on shaky ground, can't explain. Uncertainty."),
        ("05_06_mine_unfair_eval", "埋雷3:评估不一致", STYLE + "Researcher comparing apples and oranges. Unfair."),
        ("05_07_minimal_dod", "最小DoD清单", STYLE + "Researcher with compact 5-item checklist. Essential."),
        ("05_08_enhanced_dod", "增强DoD", STYLE + "Researcher adding extra shields to checklist. Enhancement."),
        ("05_09_team_dod", "团队DoD标准", STYLE + "Team agreeing on shared quality bar. Unity."),
    ],
    "06-logging": [
        ("06_01_archaeology", "代码考古", STYLE + "Researcher as archaeologist finding treasure in logs. Discovery."),
        ("06_02_two_layer_logging", "双层日志", STYLE + "Researcher with two streams: JSON blue, notes orange. Harmony."),
        ("06_03_auto_logging", "自动记录", STYLE + "Researcher relaxing while bots collect data. Automation."),
        ("06_04_find_logs_struggle", "找日志的挣扎", STYLE + "Researcher searching dated folders, frustrated. Poor naming."),
        ("06_05_find_config_struggle", "找配置的挣扎", STYLE + "Researcher in git history, unsure which config. Detective."),
        ("06_06_find_data_struggle", "找数据的挣扎", STYLE + "Researcher confused by data versions. Provenance."),
        ("06_07_reviewer_rejection", "审稿人拒稿", STYLE + "Researcher with rejection letter. Devastation, lesson."),
        ("06_08_run_json_structure", "run.json结构", STYLE + "Researcher admiring perfect JSON floating. Beauty."),
        ("06_09_run_md_template", "run.md模板", STYLE + "Researcher filling 5-line template quickly. Effective."),
        ("06_10_mlflow_integration", "MLflow集成", STYLE + "Researcher connecting to MLflow dashboard. Integration."),
    ],
    "07-ai-workflow": [
        ("07_01_ai_sidekick", "AI助手协作", STYLE + "Researcher with friendly AI robot coding together. Partnership."),
        ("07_02_verify_ai_code", "验证AI代码", STYLE + "Researcher scanning AI code with magnifier, finding bugs. QC."),
        ("07_03_ai_danger", "AI陷阱", STYLE + "Researcher dodging pitfalls in AI code maze. Navigation."),
        ("07_04_ai_speed_trap", "AI速度陷阱", STYLE + "Researcher running fast toward cliff. Speed danger."),
        ("07_05_hidden_bug", "隐藏的Bug", STYLE + "Researcher peeling code layers revealing bug. Deceptive."),
        ("07_06_unverified_result", "未验证的结果", STYLE + "Researcher celebrating on cracking ice. False confidence."),
        ("07_07_ownership_loss", "失去掌控", STYLE + "Researcher surrounded by incomprehensible AI code. Lost."),
        ("07_08_review_discipline", "Review纪律", STYLE + "Researcher methodically reviewing AI suggestions. Judgment."),
        ("07_09_test_before_trust", "先测试再信任", STYLE + "Researcher putting AI code through tests. Verification."),
        ("07_10_rollback_ready", "随时准备回退", STYLE + "Researcher with backup plan ready. Prepared."),
    ],
    "08-multi-path": [
        ("08_01_crossroads", "研究十字路口", STYLE + "Researcher at crossroads, paths diverging. Decision."),
        ("08_02_path_management", "路径管理", STYLE + "Researcher monitoring multiple paths. Control center."),
        ("08_03_cleanup", "定期清理", STYLE + "Researcher archiving and cleaning paths. Maintenance."),
        ("08_04_week1_excitement", "第1周兴奋", STYLE + "Researcher excitedly starting paths A, B, C. Fresh."),
        ("08_05_week3_confusion", "第3周混乱", STYLE + "Researcher confused by growing paths. Complexity."),
        ("08_06_week6_crisis", "第6周危机", STYLE + "Researcher overwhelmed by tangled paths. Crisis."),
        ("08_07_path_naming", "路径命名规范", STYLE + "Researcher organizing paths with clear names. Order."),
        ("08_08_path_tracking_table", "路径追踪表", STYLE + "Researcher with beautiful tracking table. Organization."),
        ("08_09_weekly_cleanup", "每周清理仪式", STYLE + "Researcher in weekly cleanup ritual. Regular."),
        ("08_10_path_comparison", "路径对比", STYLE + "Researcher comparing paths objectively. Evaluation."),
    ],
    "no-boom": [
        ("09_01_bomb_defusal", "拆除截止日期炸弹", STYLE + "Researcher defusing deadline bomb at 00:01. Victory."),
        ("09_02_early_warning", "预警系统", STYLE + "Researcher intuition catching issues early. Proactive."),
        ("09_03_victory", "成功提交", STYLE + "Researcher triumphant, confetti, time to spare. Victory."),
        ("09_04_monday_crisis", "周一危机", STYLE + "Researcher shocked experiment won't reproduce. Denial."),
        ("09_05_tuesday_baseline", "周二baseline问题", STYLE + "Researcher realizing unfair baseline. Concern."),
        ("09_06_wednesday_ablation", "周三消融缺失", STYLE + "Researcher finding missing ablation. Stress."),
        ("09_07_thursday_data", "周四数据丢失", STYLE + "Researcher unable to find data. Desperation."),
        ("09_08_friday_doubt", "周五怀疑人生", STYLE + "Researcher in existential crisis. Rock bottom."),
        ("09_09_weekly_check", "每周自查", STYLE + "Researcher doing calm weekly check. Prevention."),
        ("09_10_early_validation", "提前验证", STYLE + "Researcher validating early. Proactive."),
    ],
    "team": [
        ("10_01_team_standup", "团队站会", STYLE + "Researcher leading standup, sharing updates. Collaboration."),
        ("10_02_code_review", "团队代码审查", STYLE + "Team code review, constructive feedback. Learning."),
        ("10_03_team_victory", "团队胜利", STYLE + "Team celebrating together, high-fives. United."),
        ("10_04_individual_strong", "个人很强团队很弱", STYLE + "Three strong researchers working separately. Siloed."),
        ("10_05_monday_standup", "周一站会混乱", STYLE + "Chaotic meeting, talking past each other. Failure."),
        ("10_06_wednesday_conflict", "周三代码冲突", STYLE + "Team discovering code conflicts. Frustration."),
        ("10_07_friday_data_disaster", "周五数据灾难", STYLE + "Team discovering corrupted data, blame. Crisis."),
        ("10_08_hidden_knowledge", "隐性知识依赖", STYLE + "One person with all knowledge, others stuck. Bus factor."),
        ("10_09_duplicate_work", "重复劳动", STYLE + "Two building same thing independently. Wasted."),
        ("10_10_integration_explosion", "集成成本爆炸", STYLE + "Team merging incompatible work. Nightmare."),
        ("10_11_naming_convention", "命名规范", STYLE + "Team agreeing on naming conventions. Standard."),
        ("10_12_pr_template", "PR模板", STYLE + "Team using PR template, clear descriptions. Process."),
    ],
}


def get_client():
    """Get thread-local client."""
    if not hasattr(thread_local, "client"):
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        thread_local.client = AzureOpenAI(
            api_key=api_key, api_version=version, azure_endpoint=endpoint
        )
    return thread_local.client


def generate_single(task):
    """Generate a single image."""
    fid, title, prompt, output_dir, force = task
    path = output_dir / f"{fid}.png"

    if path.exists() and not force:
        return (fid, title, "skip", None)

    try:
        client = get_client()
        resp = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        data = resp.data[0]
        if hasattr(data, 'b64_json') and data.b64_json:
            img = base64.b64decode(data.b64_json)
        elif hasattr(data, 'url') and data.url:
            img = requests.get(data.url, timeout=120).content
        else:
            return (fid, title, "fail", "No image data")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(img)
        return (fid, title, "ok", None)
    except Exception as e:
        return (fid, title, "fail", str(e))


def main():
    parser = argparse.ArgumentParser(description="Parallel comic generation")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--chapter", nargs="+")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path("src/images/comics"))
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers (default: 5)")
    args = parser.parse_args()

    if args.list:
        total = 0
        for ch, scenes in SCENARIOS.items():
            print(f"📖 {ch}: {len(scenes)} 张")
            total += len(scenes)
        print(f"\n📊 总计: {total} 张")
        return

    # Validate env
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        print("Error: Set AZURE_OPENAI_API_KEY")
        sys.exit(1)

    chapters = list(SCENARIOS.keys()) if args.all else (args.chapter or [])
    if not chapters:
        parser.print_help()
        return

    # Build task list
    tasks = []
    for ch in chapters:
        if ch not in SCENARIOS:
            continue
        for scene in SCENARIOS[ch]:
            fid, title, prompt = scene
            tasks.append((fid, title, prompt, args.output_dir, args.force))

    print(f"🚀 并行生成 {len(tasks)} 张图片，使用 {args.workers} 个线程")
    print("=" * 50)

    ok = fail = skip = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(generate_single, t): t for t in tasks}

        for future in as_completed(futures):
            fid, title, status, error = future.result()
            if status == "ok":
                print(f"✅ {title}")
                ok += 1
            elif status == "skip":
                print(f"⏭️ {title} (已存在)")
                skip += 1
            else:
                print(f"❌ {title}: {error}")
                fail += 1

    print("=" * 50)
    print(f"✅ 成功: {ok} | ⏭️ 跳过: {skip} | ❌ 失败: {fail}")


if __name__ == "__main__":
    main()
