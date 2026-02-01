#!/usr/bin/env python3
"""
Generate anime-style illustrations for Research Engineering OS book chapters.

This script uses Azure OpenAI's gpt-image-1.5 API to generate Studio Ghibli-inspired
illustrations for each chapter of the book.

Usage:
    python generate_illustrations.py --all
    python generate_illustrations.py --chapter 00-preface
    python generate_illustrations.py --chapter 01-why-flip 02-experiment-unit
    python generate_illustrations.py --list
    python generate_illustrations.py --dry-run --all

Environment Variables Required:
    AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
    AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL

Requires:
    - openai package: pip install openai
    - requests package: pip install requests
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

import requests

# Base style prefix for all illustrations - Studio Ghibli inspired anime style
STYLE_PREFIX = """Studio Ghibli inspired anime illustration style, soft watercolor-like colors,
warm and inviting atmosphere, gentle lighting, clean lines with subtle details,
digital art with hand-drawn aesthetic, high quality, cozy and peaceful mood,
Japanese animation style with warm color palette (soft oranges, greens, blues).
No text or words in the image. """

# Chapter definitions with prompts designed for research engineering book
CHAPTERS = {
    "00-preface": {
        "filename": "00_preface_thinking.png",
        "title": "Preface - Introduction",
        "prompt": STYLE_PREFIX + """A young researcher (Asian appearance) sitting at a cozy wooden desk
in a warm study room filled with soft afternoon sunlight streaming through large windows.
The researcher is thoughtfully looking at neatly organized notebooks, papers, and a laptop.
A warm cup of tea sits nearby on the desk. The researcher has a gentle, contemplative smile,
thinking deeply about how to organize research work. Bookshelves filled with academic books
line the walls. Potted plants and small succulents add life to the peaceful scene.
The overall mood is calm, focused, and inspiring."""
    },
    "01-why-flip": {
        "filename": "01_deadline_panic.png",
        "title": "Chapter 1 - Why Projects Fail at the End",
        "prompt": STYLE_PREFIX + """A researcher in a state of mild, humorous panic near a deadline.
Papers and documents are floating and flying gently in the air around them.
A calendar on the wall shows an urgent date circled in red ink.
The scene has a comedic rather than stressful atmosphere.
A clock on the wall shows late evening hours, coffee cups are scattered around
a messy desk, and a computer screen shows colorful error messages.
The researcher is reaching for the flying papers with a comical, exaggerated expression.
Despite the chaos, the scene maintains a warm, lighthearted Ghibli-style charm."""
    },
    "02-experiment-unit": {
        "filename": "02_experiment_blocks.png",
        "title": "Chapter 2 - Experiment as the Basic Unit",
        "prompt": STYLE_PREFIX + """A young scientist carefully and methodically organizing colorful
experiment components like magical building blocks or glowing puzzle pieces.
Each block is a different pastel color and represents different parts: one labeled
with a small gear icon (code), one with a document icon (data), one with a settings
cog (config), one with a leaf (environment). The scientist is focused and precise,
arranging the pieces on a clean, light wooden workbench. Soft laboratory background
with gentle lighting, test tubes with colorful liquids, and plants on windowsills.
The workspace is bright, organized, and inviting."""
    },
    "03-repo-layout": {
        "filename": "03_folder_tree.png",
        "title": "Chapter 3 - Repository Structure",
        "prompt": STYLE_PREFIX + """A beautiful visualization of a clean, organized folder structure
floating in a dreamy sky space like a magical tree or constellation.
Folders are represented as cute, colorful little houses or treasure boxes
connected by softly glowing golden pathways. Small signs near each house show
folder names like 'src/', 'experiments/', 'configs/', 'outputs/'.
A small curious character (young researcher) stands at the base looking up at
the beautiful organization with wonder and admiration.
Soft glow effects, floating particles of light, ethereal atmosphere."""
    },
    "04-git-proof": {
        "filename": "04_git_detective.png",
        "title": "Chapter 4 - Git as Proof of History",
        "prompt": STYLE_PREFIX + """A young detective character with a cozy scarf following a trail of
glowing git commits like magical footprints or golden breadcrumbs through a forest path.
Each commit is represented as a small glowing orb or lantern with tiny symbols.
The detective carries a magnifying glass and a small notebook, carefully tracing
the evidence chain through a mystical library of code represented as ancient trees.
Warm lighting filters through the canopy, creating a sense of discovery and investigation.
The path winds through the forest, showing the journey of tracking history."""
    },
    "05-dod": {
        "filename": "05_checklist_complete.png",
        "title": "Chapter 5 - Definition of Done",
        "prompt": STYLE_PREFIX + """A satisfying, heartwarming scene of a beautiful golden checklist
being completed with sparkling checkmarks. A young researcher with a genuinely happy
expression is putting the final glowing checkmark on a magical floating list.
Each completed item has a small star or sparkle effect emanating from it.
The checklist floats gently in front of a clean, organized desk bathed in
golden hour lighting from a nearby window. The scene conveys a deep sense of
accomplishment, completion, and satisfaction. Soft confetti or sparkles in the air."""
    },
    "06-logging": {
        "filename": "06_forest_path.png",
        "title": "Chapter 6 - Experiment Logging",
        "prompt": STYLE_PREFIX + """A magical forest path with charming trail markers and wooden signs
representing experiment logs. A young researcher walks peacefully along the sunlit path,
each marker showing timestamps and friendly messages. The forest is beautiful and
welcoming with dappled sunlight filtering through the leaves. Small wooden signposts
along the path have cute icons representing 'INFO' (blue), 'DEBUG' (green),
'WARNING' (yellow). The path is well-maintained and clear, conveying a sense of
navigation, guidance, and not getting lost. Mushrooms and flowers dot the path edges."""
    },
    "07-ai-workflow": {
        "filename": "07_ai_collaboration.png",
        "title": "Chapter 7 - AI-Assisted Workflow",
        "prompt": STYLE_PREFIX + """A researcher working happily alongside a friendly, cute AI robot assistant
in a cozy study. The robot is small, round, and adorable with a gentle smile
displayed on its simple screen face. The robot is helpfully passing tools or
documents to the human with its small mechanical arms. They are at a modern but
warm wooden desk with dual monitors showing code. The scene is filled with
warm collaboration energy, showing genuine teamwork between human and AI.
Plants, books, and warm lighting create a comfortable atmosphere."""
    },
    "08-multi-path": {
        "filename": "08_branching_paths.png",
        "title": "Chapter 8 - Multi-path Exploration",
        "prompt": STYLE_PREFIX + """An explorer character standing at a magical crossroads in a beautiful
landscape where multiple glowing paths branch out in different directions.
Each winding path is marked with small wooden signs like 'Path A', 'Path B', 'Path C'
and leads through different beautiful terrain - one through flower fields,
one through gentle hills, one through a peaceful forest. The paths are illuminated
with soft, different colored lights. The scene conveys a sense of adventure,
possibility, and the excitement of exploration. Mountains and clouds in the
dreamy background."""
    },
    "no-boom": {
        "filename": "09_bomb_defused.png",
        "title": "Chapter 9 - Avoiding Last-Minute Explosions",
        "prompt": STYLE_PREFIX + """A triumphant, celebratory scene where a young researcher has just
successfully defused a cartoonish 'deadline bomb'. The timer is stopped at 00:01,
showing a close call victory. The researcher is wiping sweat from their brow
with visible relief and a big smile. The 'bomb' is cute and cartoonish
(a round ball with 'DEADLINE' written on it), not scary at all.
Colorful confetti and sparkles fill the air indicating victory.
The scene is dramatic but humorous and heartwarming, with warm sunset lighting."""
    },
    "team": {
        "filename": "10_team_work.png",
        "title": "Chapter 10 - Team Collaboration",
        "prompt": STYLE_PREFIX + """A happy, diverse team of researchers collaborating warmly around
a large wooden table in a bright, plant-filled meeting room. They are sharing ideas,
pointing at documents and screens, some giving high-fives or thumbs up.
The atmosphere is warm, supportive, and energetic with everyone actively contributing.
Large whiteboards with colorful diagrams decorate the walls, coffee cups and laptops
are scattered on the table. Sunlight streams through large windows.
The scene conveys genuine camaraderie, productive teamwork, and positive energy."""
    },
    "appendix-templates": {
        "filename": "11_template_treasure.png",
        "title": "Appendix - Templates",
        "prompt": STYLE_PREFIX + """A magical treasure chest overflowing with useful, glowing templates
and tools on a desk. Beautiful scrolls, checklists with golden edges, and
document pages with sparkles are gently floating out of the open chest.
A young researcher is discovering the chest with an expression of wonder and excitement.
Each template glows softly with warm light. The scene suggests valuable resources
being discovered. The room is a cozy study with bookshelves and warm lighting.
Small magical particles float in the air around the treasure."""
    },
    "appendix-ai-disasters": {
        "filename": "12_ai_lessons.png",
        "title": "Appendix - AI Failure Cases",
        "prompt": STYLE_PREFIX + """A thoughtful, studious scene showing a young researcher carefully studying
case files and learning from past mistakes at a desk. Documents spread on the desk
have 'Case Study' labels with small illustrations of cautionary tales.
The researcher has a contemplative, focused expression while taking notes in a journal.
Small thought bubbles show simplified diagrams of what went wrong.
The atmosphere is one of learning and gaining wisdom, not doom or fear.
Warm desk lamp lighting, books stacked nearby, a cup of tea for comfort."""
    }
}


def get_azure_client() -> AzureOpenAI:
    """
    Initialize Azure OpenAI client with API key and endpoint from environment.

    Returns:
        AzureOpenAI client instance

    Raises:
        SystemExit: If required environment variables are not set
    """
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    if not api_key:
        print("Error: AZURE_OPENAI_API_KEY environment variable not set.")
        print("Set it with: export AZURE_OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    if not endpoint:
        print("Error: AZURE_OPENAI_ENDPOINT environment variable not set.")
        print("Set it with: export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'")
        sys.exit(1)

    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )


def generate_image(client: AzureOpenAI, prompt: str, output_path: Path,
                   deployment_name: str = "gpt-image-1.5") -> bool:
    """
    Generate an image using Azure OpenAI and save it to the specified path.

    Args:
        client: Azure OpenAI client instance
        prompt: Image generation prompt
        output_path: Path to save the generated image
        deployment_name: Azure deployment name for image generation

    Returns:
        True if successful, False otherwise
    """
    import base64

    try:
        print(f"  Generating image with {deployment_name}...")
        response = client.images.generate(
            model=deployment_name,
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        # Try to get image data - could be URL or base64
        image_data = response.data[0]

        if hasattr(image_data, 'b64_json') and image_data.b64_json:
            print(f"  Decoding base64 image...")
            image_bytes = base64.b64decode(image_data.b64_json)
        elif hasattr(image_data, 'url') and image_data.url:
            print(f"  Downloading image from URL...")
            image_response = requests.get(image_data.url, timeout=120)
            image_response.raise_for_status()
            image_bytes = image_response.content
        else:
            print(f"  Error: No image data returned. Response: {response}")
            return False

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        print(f"  ✅ Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def list_chapters():
    """List all available chapters with their titles and filenames."""
    print("Available chapters:")
    print("-" * 70)
    for chapter, info in CHAPTERS.items():
        title = info.get("title", chapter)
        print(f"  {chapter:<25} -> {info['filename']}")
        print(f"    Title: {title}")
    print("-" * 70)
    print(f"Total: {len(CHAPTERS)} chapters")


def show_prompts(chapters: list, output_dir: Path, force: bool = False):
    """
    Show prompts for specified chapters (dry-run mode).

    Args:
        chapters: List of chapter identifiers
        output_dir: Output directory for images
        force: Whether to regenerate existing files
    """
    print("=" * 70)
    print("DRY RUN MODE - No API calls will be made")
    print("=" * 70)
    print(f"\nOutput directory: {output_dir}")
    print(f"Chapters to process: {len(chapters)}")
    print()

    for chapter in chapters:
        info = CHAPTERS[chapter]
        output_path = output_dir / info["filename"]
        exists = output_path.exists()

        if exists and not force:
            status = "[EXISTS - will skip]"
        elif exists and force:
            status = "[EXISTS - will regenerate]"
        else:
            status = "[WILL GENERATE]"

        print("=" * 70)
        print(f"Chapter: {chapter}")
        print(f"Title: {info.get('title', chapter)}")
        print(f"Output: {info['filename']} {status}")
        print("-" * 70)
        print("PROMPT:")
        print(info["prompt"])
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate anime-style illustrations for book chapters using Azure OpenAI gpt-image-1.5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all available chapters
    python generate_illustrations.py --list

    # Show prompts without generating (dry run)
    python generate_illustrations.py --dry-run --all

    # Generate all illustrations
    python generate_illustrations.py --all

    # Generate specific chapters
    python generate_illustrations.py --chapter 00-preface 01-why-flip

    # Regenerate existing illustrations
    python generate_illustrations.py --chapter 00-preface --force

Environment Variables:
    AZURE_OPENAI_API_KEY     Your Azure OpenAI API key
    AZURE_OPENAI_ENDPOINT    Your Azure OpenAI endpoint URL
        """
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
    parser.add_argument(
        "--deployment",
        type=str,
        default="gpt-image-1.5",
        help="Azure OpenAI deployment name for gpt-image-1.5 (default: gpt-image-1.5)"
    )

    args = parser.parse_args()

    # List chapters if requested
    if args.list:
        list_chapters()
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
        print(f"\nAvailable chapters:")
        for ch in CHAPTERS.keys():
            print(f"  - {ch}")
        sys.exit(1)

    # Dry run mode
    if args.dry_run:
        show_prompts(chapters_to_process, args.output_dir, args.force)
        return

    # Initialize Azure OpenAI client
    client = get_azure_client()

    print("=" * 70)
    print("Azure OpenAI gpt-image-1.5 Illustration Generator")
    print("=" * 70)
    print(f"Output directory: {args.output_dir}")
    print(f"Deployment: {args.deployment}")
    print(f"Chapters to process: {len(chapters_to_process)}")
    print()

    # Process chapters
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, chapter in enumerate(chapters_to_process, 1):
        chapter_info = CHAPTERS[chapter]
        output_path = args.output_dir / chapter_info["filename"]

        print(f"\n[{i}/{len(chapters_to_process)}] {chapter}")
        print(f"  Title: {chapter_info.get('title', chapter)}")
        print(f"  Output: {chapter_info['filename']}")

        # Check if file already exists
        if output_path.exists() and not args.force:
            print(f"  Skipped (file exists). Use --force to regenerate.")
            skip_count += 1
            continue

        if generate_image(client, chapter_info["prompt"], output_path, args.deployment):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  Generated: {success_count}")
    print(f"  Skipped:   {skip_count}")
    print(f"  Failed:    {fail_count}")
    print("=" * 70)

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
