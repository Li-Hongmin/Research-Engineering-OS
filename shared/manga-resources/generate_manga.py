#!/usr/bin/env python3
"""
Manga panel generation from YAML storyboards.
Uses Azure OpenAI gpt-image-1.5 with parallel processing.
"""

import argparse
import base64
import os
import sys
import yaml
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    from openai import AzureOpenAI
except ImportError:
    print("Error: pip install openai pyyaml")
    sys.exit(1)

import requests

# Thread-local storage for clients
thread_local = threading.local()

# Default style prefix for all panels
DEFAULT_STYLE = """Japanese manga illustration, clean anime art style,
young Asian female researcher protagonist (casual clothes or lab coat, glasses optional),
expressive anime eyes, dynamic composition, professional digital art,
cel-shading, cinematic lighting, no text or speech bubbles. """


def get_client():
    """Get thread-local Azure OpenAI client."""
    if not hasattr(thread_local, "client"):
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

        if not api_key or not endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set")

        thread_local.client = AzureOpenAI(
            api_key=api_key, api_version=version, azure_endpoint=endpoint
        )
    return thread_local.client


def load_storyboard(yaml_path: Path) -> dict:
    """Load a storyboard YAML file."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_single_panel(task: tuple) -> tuple:
    """Generate a single manga panel image.

    Args:
        task: (panel_id, prompt, output_path, force)

    Returns:
        (panel_id, status, error_message)
    """
    panel_id, prompt, output_path, force = task

    if output_path.exists() and not force:
        return (panel_id, "skip", None)

    try:
        client = get_client()

        # Generate image
        resp = client.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            size="1024x1024",
            n=1
        )

        data = resp.data[0]

        # Handle both base64 and URL responses
        if hasattr(data, 'b64_json') and data.b64_json:
            img_bytes = base64.b64decode(data.b64_json)
        elif hasattr(data, 'url') and data.url:
            img_bytes = requests.get(data.url, timeout=120).content
        else:
            return (panel_id, "fail", "No image data in response")

        # Save image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(img_bytes)

        return (panel_id, "ok", None)

    except Exception as e:
        return (panel_id, "fail", str(e))


def build_tasks_from_storyboard(storyboard: dict, output_dir: Path, force: bool) -> list:
    """Build generation tasks from a storyboard.

    Args:
        storyboard: Loaded YAML storyboard
        output_dir: Base output directory for panels
        force: Whether to regenerate existing images

    Returns:
        List of (panel_id, prompt, output_path, force) tuples
    """
    chapter = storyboard['chapter']
    style_base = storyboard.get('style_base', DEFAULT_STYLE).strip()

    tasks = []
    for panel in storyboard['panels']:
        panel_id = panel['id']
        panel_prompt = panel['prompt'].strip()

        # Combine style base with panel-specific prompt
        full_prompt = f"{style_base}\n\n{panel_prompt}"

        # Output path: output_dir/chapter/panel_id.png
        output_path = output_dir / chapter / f"{panel_id}.png"

        tasks.append((panel_id, full_prompt, output_path, force))

    return tasks


def generate_chapter(storyboard_path: Path, output_dir: Path,
                     workers: int = 8, force: bool = False) -> dict:
    """Generate all panels for a chapter.

    Args:
        storyboard_path: Path to storyboard YAML
        output_dir: Base output directory
        workers: Number of parallel workers
        force: Whether to regenerate existing images

    Returns:
        Dict with generation statistics
    """
    storyboard = load_storyboard(storyboard_path)
    tasks = build_tasks_from_storyboard(storyboard, output_dir, force)

    chapter = storyboard['chapter']
    title = storyboard.get('title_zh', storyboard.get('title_en', chapter))

    print(f"\n📖 Chapter: {chapter} - {title}")
    print(f"   Panels: {len(tasks)}")
    print("=" * 50)

    stats = {"ok": 0, "skip": 0, "fail": 0, "errors": []}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(generate_single_panel, t): t[0] for t in tasks}

        for future in as_completed(futures):
            panel_id = futures[future]
            panel_id, status, error = future.result()

            if status == "ok":
                print(f"  ✅ {panel_id}")
                stats["ok"] += 1
            elif status == "skip":
                print(f"  ⏭️  {panel_id} (exists)")
                stats["skip"] += 1
            else:
                print(f"  ❌ {panel_id}: {error}")
                stats["fail"] += 1
                stats["errors"].append((panel_id, error))

    return stats


def list_storyboards(storyboards_dir: Path) -> list:
    """List all available storyboard files."""
    if not storyboards_dir.exists():
        return []
    return sorted(storyboards_dir.glob("*.yaml"))


def main():
    parser = argparse.ArgumentParser(
        description="Generate manga panels from YAML storyboards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available storyboards
  python generate_manga.py --list

  # Generate prologue chapter
  python generate_manga.py --chapter 00-prologue

  # Generate all chapters
  python generate_manga.py --all

  # Force regenerate with more workers
  python generate_manga.py --chapter 00-prologue --force --workers 10
        """
    )

    parser.add_argument("--list", action="store_true",
                        help="List available storyboards")
    parser.add_argument("--all", action="store_true",
                        help="Generate all chapters")
    parser.add_argument("--chapter", nargs="+", metavar="NAME",
                        help="Chapter names to generate (e.g., 00-prologue 01-why-flip)")
    parser.add_argument("--storyboards-dir", type=Path,
                        default=Path(__file__).parent / "storyboards",
                        help="Directory containing storyboard YAML files")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).parent / "panels",
                        help="Output directory for generated panels")
    parser.add_argument("--workers", type=int, default=128,
                        help="Number of parallel workers (default: 128)")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate existing images")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without actually generating")

    args = parser.parse_args()

    # List mode
    if args.list:
        storyboards = list_storyboards(args.storyboards_dir)
        if not storyboards:
            print(f"No storyboards found in {args.storyboards_dir}")
            return

        print(f"\n📚 Available Storyboards ({args.storyboards_dir}):\n")
        total_panels = 0
        for sb_path in storyboards:
            sb = load_storyboard(sb_path)
            panel_count = len(sb.get('panels', []))
            total_panels += panel_count
            chapter = sb.get('chapter', sb_path.stem)
            title = sb.get('title_zh', sb.get('title_en', ''))
            print(f"  📖 {chapter}: {title} ({panel_count} panels)")

        print(f"\n📊 Total: {len(storyboards)} chapters, {total_panels} panels")
        return

    # Validate environment
    if not args.dry_run:
        if not os.environ.get("AZURE_OPENAI_API_KEY"):
            print("Error: AZURE_OPENAI_API_KEY environment variable not set")
            print("Run: source ~/.azure_openai_config")
            sys.exit(1)
        if not os.environ.get("AZURE_OPENAI_ENDPOINT"):
            print("Error: AZURE_OPENAI_ENDPOINT environment variable not set")
            sys.exit(1)

    # Determine which chapters to generate
    storyboards = list_storyboards(args.storyboards_dir)
    sb_map = {sb.stem: sb for sb in storyboards}

    if args.all:
        chapters_to_generate = list(sb_map.keys())
    elif args.chapter:
        chapters_to_generate = args.chapter
    else:
        parser.print_help()
        return

    # Validate requested chapters
    valid_chapters = []
    for ch in chapters_to_generate:
        if ch in sb_map:
            valid_chapters.append(ch)
        else:
            print(f"⚠️  Warning: Storyboard not found for '{ch}'")

    if not valid_chapters:
        print("No valid chapters to generate")
        return

    # Dry run mode
    if args.dry_run:
        print(f"\n🔍 Dry run - would generate:\n")
        for ch in valid_chapters:
            sb = load_storyboard(sb_map[ch])
            panel_count = len(sb.get('panels', []))
            print(f"  📖 {ch}: {panel_count} panels")
            for panel in sb.get('panels', []):
                output_path = args.output_dir / ch / f"{panel['id']}.png"
                status = "exists" if output_path.exists() else "new"
                if args.force:
                    status = "regenerate" if output_path.exists() else "new"
                print(f"      {panel['id']}: {status}")
        return

    # Generate panels
    print(f"\n🚀 Manga Generation Started")
    print(f"   Chapters: {len(valid_chapters)}")
    print(f"   Workers: {args.workers}")
    print(f"   Output: {args.output_dir}")
    print(f"   Force: {args.force}")

    start_time = datetime.now()
    total_stats = {"ok": 0, "skip": 0, "fail": 0, "errors": []}

    for ch in valid_chapters:
        stats = generate_chapter(
            sb_map[ch],
            args.output_dir,
            workers=args.workers,
            force=args.force
        )
        total_stats["ok"] += stats["ok"]
        total_stats["skip"] += stats["skip"]
        total_stats["fail"] += stats["fail"]
        total_stats["errors"].extend(stats["errors"])

    # Summary
    elapsed = datetime.now() - start_time
    print("\n" + "=" * 50)
    print("📊 Generation Complete!")
    print(f"   ✅ Generated: {total_stats['ok']}")
    print(f"   ⏭️  Skipped: {total_stats['skip']}")
    print(f"   ❌ Failed: {total_stats['fail']}")
    print(f"   ⏱️  Time: {elapsed}")

    if total_stats["errors"]:
        print("\n❌ Errors:")
        for panel_id, error in total_stats["errors"]:
            print(f"   {panel_id}: {error}")


if __name__ == "__main__":
    main()
