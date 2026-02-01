#!/usr/bin/env python3
"""
Generate anime-style illustrations for Research Engineering OS book chapters.

Usage:
    python generate_illustrations.py --all
    python generate_illustrations.py --chapter 00-preface
    python generate_illustrations.py --chapter 01-why-flip 02-experiment-unit

Requires:
    - OPENAI_API_KEY environment variable
    - openai package: pip install openai
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

import requests

# Base style prefix for all illustrations
STYLE_PREFIX = """Anime-style illustration, soft colors, clean lines,
Studio Ghibli inspired aesthetic, warm and inviting atmosphere,
digital art, high quality, detailed but not cluttered. """

# Chapter definitions with prompts
CHAPTERS = {
    "00-preface": {
        "filename": "00_preface_thinking.png",
        "prompt": STYLE_PREFIX + """A young researcher sitting at a cozy wooden desk
in a warm study room, thoughtfully looking at organized notebooks and papers.
Soft afternoon light coming through the window, a cup of tea nearby.
The researcher has a gentle smile, thinking about how to organize their research work.
Books on shelves in the background, some potted plants adding life to the scene."""
    },
    "01-why-flip": {
        "filename": "01_deadline_panic.png",
        "prompt": STYLE_PREFIX + """A researcher in a state of mild panic near a deadline,
papers and documents flying around in the air, a calendar showing an urgent date circled in red.
The scene is slightly chaotic but still humorous rather than stressful.
Clock showing late hours, coffee cups scattered around, computer screen with error messages.
The researcher is reaching for flying papers with a comical expression."""
    },
    "02-experiment-unit": {
        "filename": "02_experiment_blocks.png",
        "prompt": STYLE_PREFIX + """A scientist carefully organizing colorful experiment
components like building blocks or puzzle pieces. Each block represents different parts:
code, data, config, environment, labeled with cute icons. The scientist is focused and
methodical, arranging pieces on a clean workbench. Soft laboratory background with
equipment, bright and organized workspace."""
    },
    "03-repo-layout": {
        "filename": "03_folder_structure.png",
        "prompt": STYLE_PREFIX + """A visualization of clean organized folder structure
floating in space like a beautiful tree or constellation. Folders represented as
cute colorful houses or containers, connected by glowing pathways. Labels show
'src/', 'experiments/', 'configs/', 'outputs/'. A small character looking up at
the beautiful organization with admiration. Soft glow effects."""
    },
    "04-git-proof": {
        "filename": "04_git_detective.png",
        "prompt": STYLE_PREFIX + """A young detective character following a trail of
glowing git commits like footprints or breadcrumbs. Each commit is represented as
a small glowing orb with a hash number. The detective has a magnifying glass and
a notebook, tracing the evidence chain through a mystical library of code.
Warm lighting, sense of discovery and investigation."""
    },
    "05-dod": {
        "filename": "05_checklist_done.png",
        "prompt": STYLE_PREFIX + """A satisfying scene of a beautiful checklist being
completed with checkmarks. A researcher with a happy expression putting the final
checkmark on a glowing list. Each completed item has a small star or sparkle effect.
The checklist floats in front of a clean desk, golden hour lighting,
sense of accomplishment and completion."""
    },
    "06-logging": {
        "filename": "06_forest_trail.png",
        "prompt": STYLE_PREFIX + """A magical forest path with trail markers and signs
representing logs. A researcher walking along the path, each marker showing timestamps
and messages. The forest is beautiful and welcoming, sunbeams filtering through trees.
Small signposts with 'INFO', 'DEBUG', 'WARNING' labels. Sense of navigation and guidance."""
    },
    "07-ai-workflow": {
        "filename": "07_ai_collaboration.png",
        "prompt": STYLE_PREFIX + """A researcher working happily alongside a friendly
AI robot assistant. The robot is cute and helpful, not threatening, passing tools
or documents to the human. They are at a modern desk with dual monitors.
The AI has a gentle smile displayed on its screen face. Warm collaboration scene,
teamwork between human and AI."""
    },
    "08-multi-path": {
        "filename": "08_branching_paths.png",
        "prompt": STYLE_PREFIX + """An explorer standing at a crossroads with multiple
beautiful branching paths leading to different directions. Each path represents
different exploration branches, marked with signs like 'Approach A', 'Approach B'.
The paths wind through a beautiful landscape with mountains and forests.
Sense of adventure and possibility, each path leading to discovery."""
    },
    "no-boom": {
        "filename": "09_bomb_defused.png",
        "prompt": STYLE_PREFIX + """A triumphant scene where a researcher has just
successfully defused a 'deadline bomb'. The timer is stopped at 00:01, showing
close call success. The researcher is wiping sweat with relief and a smile.
The 'bomb' is cute and cartoonish (labeled 'DEADLINE'), not scary.
Confetti or sparkles indicating victory, dramatic but humorous scene."""
    },
    "team": {
        "filename": "10_team_work.png",
        "prompt": STYLE_PREFIX + """A happy team of diverse researchers collaborating
around a large table. They are sharing ideas, pointing at documents and screens,
some high-fiving. The atmosphere is warm and supportive, with everyone contributing.
Whiteboards with diagrams in background, coffee cups, laptops open.
Sense of camaraderie and productive teamwork."""
    },
    "appendix-templates": {
        "filename": "11_template_treasure.png",
        "prompt": STYLE_PREFIX + """A treasure chest overflowing with useful templates
and tools. Scrolls, checklists, and documents with golden edges spilling out.
A researcher discovering the chest with excitement. Each template glows softly,
labeled with things like 'PR Template', 'Experiment Log', 'Makefile'.
Magical discovery scene, valuable resources found."""
    },
    "appendix-ai-disasters": {
        "filename": "12_ai_lessons.png",
        "prompt": STYLE_PREFIX + """A thoughtful scene showing a researcher studying
case files of AI failures, learning from mistakes. Documents spread on a desk
with 'Case Study' labels. The researcher has a contemplative expression,
taking notes. Small illustrations on the documents show cautionary tales.
Learning atmosphere, wisdom from experience, not doom but education."""
    }
}


def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_image(client: OpenAI, prompt: str, output_path: Path) -> bool:
    """
    Generate an image using DALL-E 3 and save it to the specified path.

    Args:
        client: OpenAI client instance
        prompt: Image generation prompt
        output_path: Path to save the generated image

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Generating image...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # Download the image
        print(f"  Downloading image...")
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_response.content)

        print(f"  Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"  Error: {e}")
        return False


def generate_chapter_illustration(client: OpenAI, chapter: str, output_dir: Path) -> bool:
    """
    Generate illustration for a specific chapter.

    Args:
        client: OpenAI client instance
        chapter: Chapter identifier (e.g., '00-preface')
        output_dir: Directory to save images

    Returns:
        True if successful, False otherwise
    """
    if chapter not in CHAPTERS:
        print(f"Error: Unknown chapter '{chapter}'")
        print(f"Available chapters: {', '.join(CHAPTERS.keys())}")
        return False

    chapter_info = CHAPTERS[chapter]
    output_path = output_dir / chapter_info["filename"]

    print(f"\n[{chapter}]")
    print(f"  Output: {chapter_info['filename']}")

    # Check if file already exists
    if output_path.exists():
        print(f"  File already exists. Use --force to regenerate.")
        return True

    return generate_image(client, chapter_info["prompt"], output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime-style illustrations for book chapters using DALL-E 3"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate illustrations for all chapters"
    )
    parser.add_argument(
        "--chapter",
        nargs="+",
        metavar="CHAPTER",
        help="Generate illustrations for specific chapter(s)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available chapters"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if file already exists"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "src" / "images",
        help="Output directory for images (default: src/images/)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without making API calls"
    )

    args = parser.parse_args()

    # List chapters if requested
    if args.list:
        print("Available chapters:")
        for chapter, info in CHAPTERS.items():
            print(f"  {chapter}: {info['filename']}")
        return

    # Determine which chapters to process
    if args.all:
        chapters_to_process = list(CHAPTERS.keys())
    elif args.chapter:
        chapters_to_process = args.chapter
    else:
        parser.print_help()
        print("\nError: Specify --all or --chapter CHAPTER_NAME")
        sys.exit(1)

    # Validate chapters
    invalid_chapters = [c for c in chapters_to_process if c not in CHAPTERS]
    if invalid_chapters:
        print(f"Error: Unknown chapter(s): {', '.join(invalid_chapters)}")
        print(f"Available chapters: {', '.join(CHAPTERS.keys())}")
        sys.exit(1)

    # Dry run mode
    if args.dry_run:
        print("Dry run mode - no API calls will be made\n")
        print(f"Output directory: {args.output_dir}")
        print(f"Chapters to process: {len(chapters_to_process)}")
        for chapter in chapters_to_process:
            info = CHAPTERS[chapter]
            output_path = args.output_dir / info["filename"]
            exists = output_path.exists()
            status = "[EXISTS]" if exists else "[WILL GENERATE]"
            if exists and args.force:
                status = "[WILL REGENERATE]"
            print(f"  {chapter}: {info['filename']} {status}")
        return

    # Initialize client
    client = get_openai_client()

    print(f"Output directory: {args.output_dir}")
    print(f"Chapters to process: {len(chapters_to_process)}")

    # Process chapters
    success_count = 0
    fail_count = 0
    skip_count = 0

    for chapter in chapters_to_process:
        chapter_info = CHAPTERS[chapter]
        output_path = args.output_dir / chapter_info["filename"]

        print(f"\n[{chapter}]")
        print(f"  Output: {chapter_info['filename']}")

        # Check if file already exists
        if output_path.exists() and not args.force:
            print(f"  Skipped (file exists). Use --force to regenerate.")
            skip_count += 1
            continue

        if generate_image(client, chapter_info["prompt"], output_path):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Generated: {success_count}")
    print(f"  Skipped:   {skip_count}")
    print(f"  Failed:    {fail_count}")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
