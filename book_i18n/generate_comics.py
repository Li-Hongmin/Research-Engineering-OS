#!/usr/bin/env python3
"""
Generate Marvel-style comics with the young researcher hero for each scenario in the book.

This script parses markdown chapters, identifies story scenarios,
and generates Marvel comic-style illustrations with the young researcher hero as the protagonist.
"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path
from typing import Optional

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

import requests

# Anime manga style prefix - young researcher protagonist
STYLE_PREFIX = """Japanese manga style illustration, dynamic anime art,
clean bold lines and vibrant colors, dramatic lighting,
young Asian researcher as the main character (wearing lab coat or casual clothes, glasses optional),
energetic composition, manga panel aesthetic, expressive anime eyes,
high quality digital art, heroic and determined expressions,
soft cel-shading, clean professional artwork.
No text, speech bubbles, or captions in the image. """

# Scenarios extracted from each chapter - the young researcher hero as a researcher/developer
SCENARIOS = {
    # Chapter 1: Why projects fail at the end
    "01-why-flip": [
        {
            "id": "01_deadline_panic",
            "title": "Deadline Panic",
            "prompt": STYLE_PREFIX + """the young researcher hero in his suit sitting at a messy desk surrounded by
floating papers and code printouts, looking stressed at multiple computer monitors showing errors.
A large clock on the wall shows 11:59 PM. Coffee cups scattered everywhere.
The scene captures the chaos of a deadline approaching, with the young researcher hero's intuition
tingling (shown as wavy lines around his head) warning of impending doom.
Dynamic perspective from slightly above, dramatic lighting from the monitors."""
        },
        {
            "id": "01_three_debts",
            "title": "Three Types of Debt",
            "prompt": STYLE_PREFIX + """the young researcher hero standing heroically while facing three villain-like
shadows labeled representations of technical debt: one shadow made of tangled code (Exploration Debt),
one made of broken test tubes (Validation Debt), one made of scattered puzzle pieces (Reproducibility Debt).
the young researcher hero is in a defensive stance, ready to tackle these challenges.
Dark atmospheric background with dramatic spotlight on the young researcher hero.
Comic book action scene composition."""
        },
        {
            "id": "01_last_minute_chaos",
            "title": "Last Minute Chaos",
            "prompt": STYLE_PREFIX + """the young researcher hero rushing through a cityscape made of falling
documents, crashing servers (depicted as buildings), and exploding deadlines (like bombs).
He's trying to catch and save multiple falling items at once with his webs.
Dynamic action pose mid-swing, motion blur effects, dramatic perspective.
The city represents a research project falling apart at the last minute."""
        },
    ],

    # Chapter 2: Experiment as the basic unit
    "02-experiment-unit": [
        {
            "id": "02_experiment_assembly",
            "title": "Assembling the Experiment",
            "prompt": STYLE_PREFIX + """the young researcher hero carefully assembling glowing experiment components
like a puzzle in his lab (which looks like a high-tech the young researcher hero workshop).
Each piece is labeled with icons: gear (code), database (data), settings (config),
computer chip (environment). He's in a focused, precise pose.
Clean, organized lab setting with web patterns on the walls.
Warm lighting, detailed scientific equipment in background."""
        },
        {
            "id": "02_six_questions",
            "title": "The Six Questions",
            "prompt": STYLE_PREFIX + """the young researcher hero in detective mode, magnifying glass in hand,
examining a holographic display showing six floating question marks, each transforming into
answers: code version, config, data, environment, outputs, metrics.
His intuition connects all six elements with web lines showing their relationships.
Noir-style lighting with dramatic shadows, investigation scene."""
        },
        {
            "id": "02_run_id_naming",
            "title": "Naming Experiments",
            "prompt": STYLE_PREFIX + """the young researcher hero organizing glowing file folders that float in the air,
each labeled with timestamps like "2026-02-01_baseline". He's using his webs to
connect and sort them in chronological order, creating a beautiful organized web pattern.
The folders glow different colors based on their status.
Clean, organized composition showing the power of good naming."""
        },
    ],

    # Chapter 3: Repository structure
    "03-repo-layout": [
        {
            "id": "03_messy_to_clean",
            "title": "From Chaos to Order",
            "prompt": STYLE_PREFIX + """Split panel comic: Left side shows the young researcher hero overwhelmed
in a chaotic room with tangled code webs everywhere, files scattered.
Right side shows the same the young researcher hero proudly standing in a perfectly organized lab
with clean folder structures visualized as a beautiful web pattern on the wall.
Before/after transformation, dramatic contrast in lighting and mood."""
        },
        {
            "id": "03_folder_tree",
            "title": "The Perfect Structure",
            "prompt": STYLE_PREFIX + """the young researcher hero building a magnificent web structure in the sky
that forms a perfect folder tree: src/, experiments/, configs/, outputs/, tests/.
Each branch of the web is labeled and glows with different colors.
He's perched at the center like a spider in its web, proud of his creation.
Dramatic sky background, architectural web design."""
        },
        {
            "id": "03_fast_slow_variables",
            "title": "Fast vs Slow",
            "prompt": STYLE_PREFIX + """the young researcher hero juggling two types of orbs while balancing on a web:
stable blue orbs labeled 'src/' (slow, careful) on one side,
and fast-moving red orbs labeled 'experiments/' (fast, disposable) on the other.
Dynamic action pose showing balance and control.
Motion trails on the fast orbs, stability on the slow ones."""
        },
    ],

    # Chapter 4: Git as proof
    "04-git-proof": [
        {
            "id": "04_git_detective",
            "title": "Git Detective",
            "prompt": STYLE_PREFIX + """the young researcher hero as a detective, following a glowing trail of
git commits through a dark cityscape. Each commit is a glowing orb with a hash.
He's using his intuition to trace the history, magnifying glass examining commits.
Noir detective atmosphere, dramatic shadows, investigation scene.
The trail of commits tells a story of changes over time."""
        },
        {
            "id": "04_branch_strategy",
            "title": "Branch Strategy",
            "prompt": STYLE_PREFIX + """the young researcher hero swinging between different parallel web structures
representing git branches: main (golden, stable), feature branches (colorful, experimental),
and experiment branches (glowing, scientific). Each branch has its own distinct visual style.
Dynamic rushing pose connecting all branches.
Architectural diagram come to life as a 3D cityscape."""
        },
        {
            "id": "04_commit_evidence",
            "title": "Commit as Evidence",
            "prompt": STYLE_PREFIX + """the young researcher hero in a courtroom-like setting, presenting holographic
git commits as evidence. Each commit floats like an exhibit, showing code changes.
He's in a confident presenting pose, the commits glow with authenticity.
Dramatic courtroom lighting, professional presentation scene.
The commits prove the history and authenticity of his work."""
        },
    ],

    # Chapter 5: Definition of Done
    "05-dod": [
        {
            "id": "05_checklist_hero",
            "title": "Checklist Hero",
            "prompt": STYLE_PREFIX + """the young researcher hero triumphantly checking off the final item on a
giant glowing checklist floating in the air. Each checked item sparkles with completion.
He's in a victory pose, one arm raised, the checklist behind him like a trophy.
Celebration effects: sparkles, light rays, heroic atmosphere.
The satisfaction of completing a Definition of Done."""
        },
        {
            "id": "05_quality_gate",
            "title": "Quality Gate",
            "prompt": STYLE_PREFIX + """the young researcher hero standing guard at a magnificent gate made of
quality standards. The gate has sections: Tests Pass, Code Review, Documentation.
He's in a protective stance, ensuring nothing passes without meeting standards.
Architectural gate design, guardian pose, determined expression.
The gate glows with quality assurance energy."""
        },
    ],

    # Chapter 6: Logging
    "06-logging": [
        {
            "id": "06_archaeology",
            "title": "Code Archaeology",
            "prompt": STYLE_PREFIX + """the young researcher hero as an archaeologist, digging through layers of
old log files and experiment records. He's found a crucial piece of information
that glows like treasure. Ancient temple aesthetic but with computer themes.
Dramatic discovery moment, light shining from the found artifact.
The importance of keeping good records visualized."""
        },
        {
            "id": "06_two_layer_logging",
            "title": "Two Layer Logging",
            "prompt": STYLE_PREFIX + """the young researcher hero managing two parallel streams of information:
one stream of structured JSON data (mechanical, precise, blue),
one stream of human-readable notes (organic, personal, warm orange).
He's orchestrating both streams like a conductor, balanced pose.
The harmony of machine and human logging working together."""
        },
        {
            "id": "06_auto_logging",
            "title": "Automatic Logging",
            "prompt": STYLE_PREFIX + """the young researcher hero relaxing while his spider-bots automatically
collect and organize experiment data around him. The bots are small spider-drones
gathering information into organized containers. Automated efficiency scene.
Futuristic lab setting, peaceful automation, the young researcher hero supervising."""
        },
    ],

    # Chapter 7: AI Workflow
    "07-ai-workflow": [
        {
            "id": "07_ai_sidekick",
            "title": "AI Sidekick",
            "prompt": STYLE_PREFIX + """the young researcher hero working alongside a friendly AI robot assistant
in his lab. They're collaborating on code, the AI suggesting while the young researcher hero reviews.
Partnership pose, both looking at holographic code displays.
Warm collaborative atmosphere, mutual respect between hero and AI.
The power of human-AI teamwork."""
        },
        {
            "id": "07_verify_ai_code",
            "title": "Verifying AI Code",
            "prompt": STYLE_PREFIX + """the young researcher hero using his intuition to scan AI-generated code,
detecting potential bugs visualized as small glowing warning signs.
He's in an analytical pose, magnifying glass examining code carefully.
The importance of human oversight over AI-generated content.
Detective and quality assurance scene combined."""
        },
        {
            "id": "07_ai_danger",
            "title": "AI Pitfalls",
            "prompt": STYLE_PREFIX + """the young researcher hero dodging pitfalls and traps in a maze made of
AI-generated code. Some paths look good but lead to dead ends or traps.
His intuition guides him through the correct path.
Action scene navigating dangers, dynamic dodging poses.
The risks of blindly trusting AI without verification."""
        },
    ],

    # Chapter 8: Multi-path exploration
    "08-multi-path": [
        {
            "id": "08_crossroads",
            "title": "Research Crossroads",
            "prompt": STYLE_PREFIX + """the young researcher hero at a dramatic crossroads where multiple paths
diverge into different research directions. Each path glows with different potential.
He's in a thoughtful pose, considering which paths to explore.
Dramatic sky, multiple glowing pathways, decision moment.
The excitement and uncertainty of research exploration."""
        },
        {
            "id": "08_path_management",
            "title": "Managing Paths",
            "prompt": STYLE_PREFIX + """the young researcher hero using his webs to keep track of multiple
parallel exploration paths, each represented as a glowing thread.
He's at the center of his web, monitoring all paths simultaneously.
Control center aesthetic, organized chaos, masterful management.
The art of managing multiple research directions."""
        },
        {
            "id": "08_cleanup",
            "title": "Path Cleanup",
            "prompt": STYLE_PREFIX + """the young researcher hero archiving or cleaning up old exploration paths,
some paths being carefully stored (archived), others being responsibly discarded.
Organized cleanup scene, decision-making about what to keep.
The importance of regular maintenance and cleanup."""
        },
    ],

    # Chapter: No Boom (Avoiding explosions)
    "no-boom": [
        {
            "id": "09_bomb_defusal",
            "title": "Deadline Bomb Defusal",
            "prompt": STYLE_PREFIX + """the young researcher hero heroically defusing a cartoon-style 'DEADLINE' bomb,
the timer stopped at 00:01. Sweat drops, focused expression, careful hands.
Dramatic close-up of the defusal moment, tension and relief.
The bomb is labeled with research deadline imagery.
Victory over last-minute disasters through good planning."""
        },
        {
            "id": "09_early_warning",
            "title": "Early Warning System",
            "prompt": STYLE_PREFIX + """the young researcher hero's intuition alerting him to problems early,
visualized as glowing warning waves around his head. He's catching issues
before they become disasters, represented as small problems he's webbing up.
Proactive problem detection, prevention over reaction.
The value of early testing and validation."""
        },
        {
            "id": "09_victory",
            "title": "Successful Submission",
            "prompt": STYLE_PREFIX + """the young researcher hero triumphantly submitting his research paper/project,
arms raised in victory, confetti and celebration effects around him.
The deadline clock shows time to spare, everything is organized and complete.
Pure celebration and success moment, heroic victory pose.
The reward of good research engineering practices."""
        },
    ],

    # Chapter: Team collaboration
    "team": [
        {
            "id": "10_team_standup",
            "title": "Team Standup",
            "prompt": STYLE_PREFIX + """the young researcher hero leading a team standup meeting with other heroes
(generic superhero teammates, not specific Marvel characters).
They're gathered around a holographic project board, sharing updates.
Collaborative team meeting scene, everyone engaged and contributing.
The importance of regular team communication."""
        },
        {
            "id": "10_code_review",
            "title": "Team Code Review",
            "prompt": STYLE_PREFIX + """the young researcher hero and teammates doing code review together,
pointing at holographic code displays, giving constructive feedback.
Collaborative and supportive atmosphere, learning together.
The value of peer review and knowledge sharing."""
        },
        {
            "id": "10_team_victory",
            "title": "Team Victory",
            "prompt": STYLE_PREFIX + """the young researcher hero and his research team celebrating a successful
project completion together, group victory pose, high-fives and celebration.
United team achievement, everyone contributed to success.
The power of good teamwork and collaboration."""
        },
    ],
}


def get_azure_client() -> AzureOpenAI:
    """Initialize Azure OpenAI client."""
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    if not api_key or not endpoint:
        print("Error: Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        sys.exit(1)

    return AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=endpoint)


def generate_image(client: AzureOpenAI, prompt: str, output_path: Path,
                   model: str = "gpt-image-1.5") -> bool:
    """Generate image using Azure OpenAI."""
    try:
        print(f"  🎨 Generating with {model}...")
        response = client.images.generate(model=model, prompt=prompt, size="1024x1024", n=1)

        image_data = response.data[0]
        if hasattr(image_data, 'b64_json') and image_data.b64_json:
            image_bytes = base64.b64decode(image_data.b64_json)
        elif hasattr(image_data, 'url') and image_data.url:
            image_bytes = requests.get(image_data.url, timeout=120).content
        else:
            print(f"  ❌ No image data")
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"  ✅ Saved: {output_path.name}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def list_scenarios():
    """List all scenarios."""
    total = 0
    for chapter, scenes in SCENARIOS.items():
        print(f"\n📖 {chapter}:")
        for s in scenes:
            print(f"   🎬 {s['id']}: {s['title']}")
            total += 1
    print(f"\n📊 Total: {total} scenarios")


def main():
    parser = argparse.ArgumentParser(description="Generate Marvel the young researcher hero comics")
    parser.add_argument("--all", action="store_true", help="Generate all comics")
    parser.add_argument("--chapter", nargs="+", help="Generate for specific chapter(s)")
    parser.add_argument("--list", action="store_true", help="List all scenarios")
    parser.add_argument("--force", action="store_true", help="Regenerate existing")
    parser.add_argument("--output-dir", type=Path, default=Path("src/images/comics"))
    parser.add_argument("--dry-run", action="store_true", help="Show prompts only")
    args = parser.parse_args()

    if args.list:
        list_scenarios()
        return

    chapters = list(SCENARIOS.keys()) if args.all else (args.chapter or [])
    if not chapters:
        parser.print_help()
        return

    if args.dry_run:
        for ch in chapters:
            if ch in SCENARIOS:
                print(f"\n{'='*60}\n📖 {ch}\n{'='*60}")
                for s in SCENARIOS[ch]:
                    print(f"\n🎬 {s['title']}:\n{s['prompt'][:200]}...")
        return

    client = get_azure_client()
    success = fail = skip = 0

    for ch in chapters:
        if ch not in SCENARIOS:
            print(f"⚠️ Unknown chapter: {ch}")
            continue
        print(f"\n📖 Chapter: {ch}")
        for scene in SCENARIOS[ch]:
            output_path = args.output_dir / f"{scene['id']}.png"
            print(f"\n  🎬 {scene['title']}")
            if output_path.exists() and not args.force:
                print(f"  ⏭️ Skipped (exists)")
                skip += 1
                continue
            if generate_image(client, scene["prompt"], output_path):
                success += 1
            else:
                fail += 1

    print(f"\n{'='*40}\n✅ Generated: {success} | ⏭️ Skipped: {skip} | ❌ Failed: {fail}")


if __name__ == "__main__":
    main()
