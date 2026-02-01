#!/usr/bin/env python3
"""
Generate detailed manga-style comics for each section.
Extended version with more granular illustrations.
"""

import argparse
import base64
import os
import sys
from pathlib import Path

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: pip install openai")
    sys.exit(1)

import requests

# Manga style - young researcher protagonist
STYLE = """Japanese manga illustration, clean anime art style,
young Asian researcher as protagonist (lab coat or casual, may have glasses),
expressive anime eyes, dynamic composition, warm colors,
professional digital art, cel-shading, no text or speech bubbles. """

# Extended scenarios - more granular
SCENARIOS = {
    # ===== Chapter 01: Why Projects Fail =====
    "01-why-flip": [
        # Existing
        ("01_01_deadline_panic", "截止日期恐慌",
         STYLE + "Researcher panicking at desk, papers flying, clock showing 11:59, multiple error screens, coffee cups everywhere, dramatic lighting from monitors."),
        ("01_02_three_debts", "三类债务怪物",
         STYLE + "Researcher facing three shadow monsters representing debts: tangled code monster, broken test tubes monster, scattered puzzle monster. Heroic defensive stance."),
        ("01_03_last_minute_chaos", "最后时刻混乱",
         STYLE + "Researcher rushing through falling documents and crashing deadlines like an action scene. Dynamic motion, dramatic perspective."),
        # New detailed scenes
        ("01_04_symptoms", "症状自查",
         STYLE + "Researcher looking in a mirror seeing warning signs reflected: question marks, broken chains, scattered files. Self-reflection scene, concerned expression."),
        ("01_05_exploration_debt", "探索债",
         STYLE + "Researcher surrounded by messy prototype code, quick hacks, temporary solutions piled up. Tangled wires and sticky notes everywhere. Overwhelmed but determined."),
        ("01_06_validation_debt", "验证债",
         STYLE + "Researcher looking at incomplete test tubes, missing control experiments, unchecked boxes. Scientific equipment half-finished. Worried expression."),
        ("01_07_reproducibility_debt", "复现债",
         STYLE + "Researcher trying to rebuild an experiment from scattered pieces, missing configurations, lost environment settings. Puzzle pieces that don't fit."),
        ("01_08_ten_min_action", "10分钟行动",
         STYLE + "Researcher confidently taking small first step, simple checklist in hand, sunrise in background. Hopeful, determined, new beginning mood."),
    ],

    # ===== Chapter 02: Experiment Unit =====
    "02-experiment-unit": [
        ("02_01_experiment_assembly", "组装实验",
         STYLE + "Researcher carefully assembling glowing experiment components like puzzle pieces: code, data, config, environment blocks. Clean organized lab."),
        ("02_02_six_questions", "六个关键问题",
         STYLE + "Researcher examining six floating holographic question marks transforming into answers. Detective investigation style, magnifying glass."),
        ("02_03_run_id_naming", "实验命名",
         STYLE + "Researcher organizing glowing folders with timestamps like 2026-02-01_baseline, creating an ordered timeline. Satisfaction of organization."),
        # New
        ("02_04_code_version", "代码版本追踪",
         STYLE + "Researcher looking at a glowing git commit hash, code history flowing like a river of light. Version control visualization."),
        ("02_05_config_management", "配置管理",
         STYLE + "Researcher adjusting settings dials on a beautiful control panel, each dial labeled (learning rate, batch size). Precision and control."),
        ("02_06_data_version", "数据版本",
         STYLE + "Researcher carefully cataloging data with labels and hashes, data storage like a well-organized library. Data integrity theme."),
        ("02_07_environment_capture", "环境捕获",
         STYLE + "Researcher taking a snapshot of their complete setup: Python version, GPU, dependencies frozen in a crystal. Time capsule feeling."),
        ("02_08_final_chaos", "避免final混乱",
         STYLE + "Researcher rejecting folders named 'final_final_v2' in favor of timestamp-based naming. Comedy scene, clear preference shown."),
    ],

    # ===== Chapter 03: Repository Layout =====
    "03-repo-layout": [
        ("03_01_messy_to_clean", "从混乱到整洁",
         STYLE + "Split scene: left side chaotic messy room with tangled code, right side same researcher in perfectly organized lab. Transformation."),
        ("03_02_folder_tree", "完美目录结构",
         STYLE + "Researcher building a beautiful tree structure in the sky: src/, experiments/, configs/, outputs/ branches. Architectural beauty."),
        ("03_03_fast_slow_variables", "快慢变量",
         STYLE + "Researcher balancing two types: stable blue orbs (slow/src) and fast red orbs (fast/experiments). Juggling act, balance."),
        # New
        ("03_04_early_success", "早期成功假象",
         STYLE + "Researcher celebrating initial working code, but shadows of future problems lurking in background. False confidence scene."),
        ("03_05_collapse_begins", "崩溃开始",
         STYLE + "Researcher realizing the codebase is falling apart, files scattering, can't find which script is current. Panic setting in."),
        ("03_06_rewrite_pain", "重写之痛",
         STYLE + "Researcher reluctantly starting over, throwing away old code, determined but tired. Three days of work symbolized."),
        ("03_07_src_directory", "src目录",
         STYLE + "Researcher polishing a beautiful crystal box labeled 'src/', inside are reusable, tested modules. Quality craftsmanship."),
        ("03_08_experiments_directory", "experiments目录",
         STYLE + "Researcher with disposable notebooks labeled 'experiments/', some being archived, others discarded. Ephemeral nature."),
        ("03_09_makefile_entry", "Makefile入口",
         STYLE + "Researcher at a simple control panel with big buttons: 'make test', 'make train', 'make eval'. Simple, clear interface."),
    ],

    # ===== Chapter 04: Git Proof =====
    "04-git-proof": [
        ("04_01_git_detective", "Git侦探",
         STYLE + "Researcher as detective following trail of glowing git commits through code forest. Noir investigation atmosphere."),
        ("04_02_branch_strategy", "分支策略",
         STYLE + "Researcher navigating between parallel branch paths: main (golden), feature (colorful), experiment (glowing). Navigation map."),
        ("04_03_commit_evidence", "提交作为证据",
         STYLE + "Researcher in courtroom presenting git commits as evidence. Professional, authoritative, proving history."),
        # New
        ("04_04_reviewer_crisis", "审稿危机",
         STYLE + "Researcher receiving reviewer comments demanding reproduction, frantically searching through old commits. Stress and urgency."),
        ("04_05_commit_too_big", "提交粒度太大",
         STYLE + "Researcher looking at one massive commit containing everything, impossible to find specific change. Frustration."),
        ("04_06_experiment_time_mismatch", "实验时间错位",
         STYLE + "Researcher confused by timeline: experiments ran at different times than code commits. Time paradox visualization."),
        ("04_07_branch_chaos", "分支混乱",
         STYLE + "Researcher lost in a maze of tangled branches, main branch polluted with experiments. Lost and confused."),
        ("04_08_tag_milestone", "Tag里程碑",
         STYLE + "Researcher planting a golden flag (tag) at a mountain peak representing paper submission. Achievement moment."),
        ("04_09_gitignore_clean", "gitignore保持干净",
         STYLE + "Researcher filtering out large files and outputs, keeping repository clean and light. Purification ritual."),
    ],

    # ===== Chapter 05: Definition of Done =====
    "05-dod": [
        ("05_01_checklist_hero", "清单英雄",
         STYLE + "Researcher triumphantly checking final item on golden checklist, sparkles of completion. Victory pose, celebration."),
        ("05_02_quality_gate", "质量门",
         STYLE + "Researcher guarding magnificent quality gate with sections: tests, review, docs. Guardian stance."),
        # New
        ("05_03_almost_done_trap", "差不多就行陷阱",
         STYLE + "Researcher stepping on hidden trap labeled '差不多', about to fall into pit of rework. Warning scene."),
        ("05_04_mine_reproduce", "埋雷1:无法复现",
         STYLE + "Researcher discovering a ticking mine labeled 'cannot reproduce' buried under 'working' code. Danger revealed."),
        ("05_05_mine_unknown_why", "埋雷2:不知道为什么",
         STYLE + "Researcher standing on shaky ground, unable to explain why the improvement works. Uncertainty visualization."),
        ("05_06_mine_unfair_eval", "埋雷3:评估不一致",
         STYLE + "Researcher comparing apples and oranges, realizing baseline used different evaluation. Unfair comparison exposed."),
        ("05_07_minimal_dod", "最小DoD清单",
         STYLE + "Researcher with compact but complete 5-item checklist glowing in hand. Essential and sufficient."),
        ("05_08_enhanced_dod", "增强DoD",
         STYLE + "Researcher adding extra shields and armor to basic checklist, going above and beyond. Enhancement."),
        ("05_09_team_dod", "团队DoD标准",
         STYLE + "Team agreeing on shared quality bar, everyone on same page. Unity and agreement."),
    ],

    # ===== Chapter 06: Logging =====
    "06-logging": [
        ("06_01_archaeology", "代码考古",
         STYLE + "Researcher as archaeologist digging through old logs, finding treasure (crucial info). Discovery moment."),
        ("06_02_two_layer_logging", "双层日志",
         STYLE + "Researcher orchestrating two streams: structured JSON (blue, precise) and human notes (orange, warm). Harmony."),
        ("06_03_auto_logging", "自动记录",
         STYLE + "Researcher relaxing while small spider-bots automatically collect experiment data. Automation bliss."),
        # New
        ("06_04_find_logs_struggle", "找日志的挣扎",
         STYLE + "Researcher searching through pile of date-named folders, can't remember which one. Frustration of poor naming."),
        ("06_05_find_config_struggle", "找配置的挣扎",
         STYLE + "Researcher digging through git history, unsure which config was actually used. Detective work."),
        ("06_06_find_data_struggle", "找数据的挣扎",
         STYLE + "Researcher confused by data versions, v2 vs v3, chat history search. Data provenance problem."),
        ("06_07_reviewer_rejection", "审稿人拒稿",
         STYLE + "Researcher receiving harsh rejection letter about inability to reproduce. Devastation but lesson learned."),
        ("06_08_run_json_structure", "run.json结构",
         STYLE + "Researcher admiring a perfect JSON structure floating in air, all fields organized beautifully. Structured data beauty."),
        ("06_09_run_md_template", "run.md模板",
         STYLE + "Researcher quickly filling 5-line template: Hypothesis, Change, Result, Compare, Next. Quick and effective."),
        ("06_10_mlflow_integration", "MLflow集成",
         STYLE + "Researcher connecting their logging to MLflow dashboard, data flowing smoothly. Integration success."),
    ],

    # ===== Chapter 07: AI Workflow =====
    "07-ai-workflow": [
        ("07_01_ai_sidekick", "AI助手协作",
         STYLE + "Researcher working alongside friendly AI robot assistant, collaborative coding. Partnership and teamwork."),
        ("07_02_verify_ai_code", "验证AI代码",
         STYLE + "Researcher carefully scanning AI-generated code with magnifying glass, finding hidden bugs. Quality control."),
        ("07_03_ai_danger", "AI陷阱",
         STYLE + "Researcher dodging pitfalls in maze of AI-generated code, some paths lead to dead ends. Navigation danger."),
        # New
        ("07_04_ai_speed_trap", "AI速度陷阱",
         STYLE + "Researcher running fast with AI help but heading toward cliff edge. Speed without direction danger."),
        ("07_05_hidden_bug", "隐藏的Bug",
         STYLE + "Researcher peeling back layers of working-looking code to reveal bug underneath. Deceptive appearance."),
        ("07_06_unverified_result", "未验证的结果",
         STYLE + "Researcher celebrating apparent success but standing on cracking ice. False confidence danger."),
        ("07_07_ownership_loss", "失去掌控",
         STYLE + "Researcher surrounded by AI-generated code they don't understand, feeling lost. Overwhelmed by complexity."),
        ("07_08_review_discipline", "Review纪律",
         STYLE + "Researcher methodically reviewing each AI suggestion, accepting some, rejecting others. Careful judgment."),
        ("07_09_test_before_trust", "先测试再信任",
         STYLE + "Researcher putting AI code through test gauntlet before accepting. Verification ritual."),
        ("07_10_rollback_ready", "随时准备回退",
         STYLE + "Researcher keeping backup plan ready, git history as safety net. Preparedness and caution."),
    ],

    # ===== Chapter 08: Multi-path Exploration =====
    "08-multi-path": [
        ("08_01_crossroads", "研究十字路口",
         STYLE + "Researcher at dramatic crossroads, multiple glowing paths diverging into different research directions. Decision moment."),
        ("08_02_path_management", "路径管理",
         STYLE + "Researcher at center of organized tracking system, monitoring multiple exploration paths simultaneously. Control center."),
        ("08_03_cleanup", "定期清理",
         STYLE + "Researcher archiving or cleaning old exploration paths, organized maintenance. Housekeeping discipline."),
        # New
        ("08_04_week1_excitement", "第1周兴奋",
         STYLE + "Researcher excitedly starting new paths A, B, C, full of energy and hope. Fresh start enthusiasm."),
        ("08_05_week3_confusion", "第3周混乱",
         STYLE + "Researcher confused by growing paths, some merging, new D and E appearing. Increasing complexity."),
        ("08_06_week6_crisis", "第6周危机",
         STYLE + "Researcher overwhelmed by tangled paths, unable to remember which works, paralysis setting in. Crisis point."),
        ("08_07_path_naming", "路径命名规范",
         STYLE + "Researcher organizing paths with clear names: path_A_dropout, path_B_augment. Order from chaos."),
        ("08_08_path_tracking_table", "路径追踪表",
         STYLE + "Researcher maintaining beautiful tracking table showing all paths, their status, and results. Organization tool."),
        ("08_09_weekly_cleanup", "每周清理仪式",
         STYLE + "Researcher in weekly ritual: archiving completed paths, cleaning failed ones. Regular maintenance."),
        ("08_10_path_comparison", "路径对比",
         STYLE + "Researcher comparing multiple paths side by side, finding the best one objectively. Evaluation scene."),
    ],

    # ===== Chapter: No Boom =====
    "no-boom": [
        ("09_01_bomb_defusal", "拆除截止日期炸弹",
         STYLE + "Researcher heroically defusing cartoon deadline bomb, timer at 00:01. Victory and relief."),
        ("09_02_early_warning", "预警系统",
         STYLE + "Researcher's intuition alerting to problems early, catching issues before they grow. Proactive detection."),
        ("09_03_victory", "成功提交",
         STYLE + "Researcher triumphantly submitting work with time to spare, arms raised, confetti celebration. Pure victory."),
        # New
        ("09_04_monday_crisis", "周一危机",
         STYLE + "Researcher discovering main experiment can't reproduce on Monday morning. Shock and denial."),
        ("09_05_tuesday_baseline", "周二baseline问题",
         STYLE + "Researcher realizing baseline was unfair comparison on Tuesday. Growing concern."),
        ("09_06_wednesday_ablation", "周三消融缺失",
         STYLE + "Researcher finding missing critical ablation experiments on Wednesday. Mounting stress."),
        ("09_07_thursday_data", "周四数据丢失",
         STYLE + "Researcher unable to find original data for figures on Thursday. Desperation."),
        ("09_08_friday_doubt", "周五怀疑人生",
         STYLE + "Researcher in existential crisis on Friday, questioning everything. Rock bottom."),
        ("09_09_weekly_check", "每周自查",
         STYLE + "Researcher doing calm weekly reproducibility check, finding and fixing issues early. Prevention."),
        ("09_10_early_validation", "提前验证",
         STYLE + "Researcher validating results early, not waiting until deadline. Proactive approach."),
    ],

    # ===== Chapter: Team =====
    "team": [
        ("10_01_team_standup", "团队站会",
         STYLE + "Researcher leading team standup, everyone sharing updates around holographic board. Collaboration."),
        ("10_02_code_review", "团队代码审查",
         STYLE + "Team doing code review together, constructive feedback on holographic displays. Learning together."),
        ("10_03_team_victory", "团队胜利",
         STYLE + "Research team celebrating successful project completion together, group high-fives. United achievement."),
        # New
        ("10_04_individual_strong", "个人很强团队很弱",
         STYLE + "Three strong researchers working separately, outputs not connecting, wasted effort. Siloed work."),
        ("10_05_monday_standup", "周一站会混乱",
         STYLE + "Chaotic team meeting, everyone talking past each other, no shared understanding. Communication failure."),
        ("10_06_wednesday_conflict", "周三代码冲突",
         STYLE + "Team members discovering their changes conflict, frustration at wasted work. Integration pain."),
        ("10_07_friday_data_disaster", "周五数据灾难",
         STYLE + "Team discovering shared data was corrupted, finger pointing, blame game. Team crisis."),
        ("10_08_hidden_knowledge", "隐性知识依赖",
         STYLE + "One researcher with all knowledge in their head, others unable to work when they're away. Bus factor."),
        ("10_09_duplicate_work", "重复劳动",
         STYLE + "Two researchers discovering they built the same thing independently. Wasted effort revelation."),
        ("10_10_integration_explosion", "集成成本爆炸",
         STYLE + "Team trying to merge everyone's work at end, incompatibilities everywhere. Integration nightmare."),
        ("10_11_naming_convention", "命名规范",
         STYLE + "Team agreeing on unified naming conventions, everyone's code becoming consistent. Standardization."),
        ("10_12_pr_template", "PR模板",
         STYLE + "Team using beautiful PR template, clear descriptions, reviewable changes. Process improvement."),
    ],
}


def get_client():
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    if not api_key or not endpoint:
        print("Error: Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        sys.exit(1)
    return AzureOpenAI(api_key=api_key, api_version=version, azure_endpoint=endpoint)


def generate(client, prompt, path, model="gpt-image-1.5"):
    try:
        print(f"  🎨 生成中...")
        resp = client.images.generate(model=model, prompt=prompt, size="1024x1024", n=1)
        data = resp.data[0]
        if hasattr(data, 'b64_json') and data.b64_json:
            img = base64.b64decode(data.b64_json)
        elif hasattr(data, 'url') and data.url:
            img = requests.get(data.url, timeout=120).content
        else:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(img)
        print(f"  ✅ {path.name}")
        return True
    except Exception as e:
        print(f"  ❌ {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate detailed manga comics")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--chapter", nargs="+")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path("src/images/comics"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.list:
        total = 0
        for ch, scenes in SCENARIOS.items():
            print(f"\n📖 {ch}: {len(scenes)} 张")
            for s in scenes:
                print(f"   🎬 {s[0]}: {s[1]}")
                total += 1
        print(f"\n📊 总计: {total} 张插图")
        return

    chapters = list(SCENARIOS.keys()) if args.all else (args.chapter or [])
    if not chapters:
        parser.print_help()
        return

    if args.dry_run:
        for ch in chapters:
            if ch in SCENARIOS:
                for s in SCENARIOS[ch]:
                    print(f"📖 {ch}/{s[0]}: {s[1]}")
        return

    client = get_client()
    ok = fail = skip = 0

    for ch in chapters:
        if ch not in SCENARIOS:
            continue
        print(f"\n📖 {ch}")
        for scene in SCENARIOS[ch]:
            fid, title, prompt = scene
            path = args.output_dir / f"{fid}.png"
            print(f"  🎬 {title}")
            if path.exists() and not args.force:
                print(f"  ⏭️ 跳过")
                skip += 1
                continue
            if generate(client, prompt, path):
                ok += 1
            else:
                fail += 1

    print(f"\n{'='*40}\n✅ {ok} | ⏭️ {skip} | ❌ {fail}")


if __name__ == "__main__":
    main()
