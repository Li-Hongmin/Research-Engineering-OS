#!/bin/bash
# update_health_snapshot.sh - Automatically update .reos/health-snapshot.json
# Part of REOS automation system

set -e

SNAPSHOT_FILE=".reos/health-snapshot.json"
TEMP_HEALTH=$(mktemp)
TEMP_STATS=$(mktemp)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Updating REOS Health Snapshot...${NC}"
echo ""

# 1. Run health check
echo "📊 Running health check..."
bash check_health.sh > "$TEMP_HEALTH" 2>&1
HEALTH_STATUS=$(grep -o "EXCELLENT\|GOOD\|NEEDS_ATTENTION\|CRITICAL" "$TEMP_HEALTH" | head -1)
echo "   Health status: $HEALTH_STATUS"

# 2. Run project stats
echo "📈 Collecting project statistics..."
bash project_stats.sh > "$TEMP_STATS" 2>&1

# 3. Parse statistics
echo "🔍 Parsing metrics..."

# Count markdown files (SOURCE CONTENT ONLY: text-book/src* + manga-book)
# Note: Excludes build output (book/), root docs (README/STATUS), and archives
# Compare with project_stats.sh which counts ALL .md files for total project scope
MD_COUNT=$(find src/ src_en/ src_ja/ manga-book/ -name "*.md" 2>/dev/null | wc -l | xargs)

# Count images
IMG_COUNT=$(find images/ manga/ manga-book/images/ -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" \) 2>/dev/null | wc -l | xargs)

# Count commits
COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo "0")

# Extract documentation words from stats
DOC_WORDS=$(grep "Total documentation:" "$TEMP_STATS" | grep -o "[0-9]\+" | tail -1)

# Count scripts
SHELL_SCRIPTS=$(find . -maxdepth 1 -name "*.sh" -type f | wc -l | xargs)
PYTHON_SCRIPTS=$(find . -maxdepth 1 -name "*.py" -type f | wc -l | xargs)
TOTAL_SCRIPT_LINES=$(grep "Total script lines:" "$TEMP_STATS" | grep -o "[0-9]\+" || echo "0")

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S%z")

echo "   Markdown files: $MD_COUNT"
echo "   Images: $IMG_COUNT"
echo "   Commits: $COMMITS"
echo "   Documentation words: $DOC_WORDS"
echo "   Scripts: $SHELL_SCRIPTS shell + $PYTHON_SCRIPTS python"
echo ""

# 4. Update snapshot JSON
echo "💾 Updating $SNAPSHOT_FILE..."

# Create .reos directory if it doesn't exist
mkdir -p .reos

# Read existing history (if file exists)
if [ -f "$SNAPSHOT_FILE" ]; then
    # Extract existing history using Python (more reliable than jq for JSON manipulation)
    EXISTING_HISTORY=$(python3 -c "
import json
import sys
try:
    with open('$SNAPSHOT_FILE', 'r') as f:
        data = json.load(f)
    history = data.get('history', [])
    # Keep only last 29 entries (we'll add 1 new = 30 total)
    print(json.dumps(history[-29:]))
except:
    print('[]')
" 2>/dev/null || echo '[]')
else
    EXISTING_HISTORY='[]'
fi

# Create new snapshot entry
NEW_ENTRY=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "health": "$HEALTH_STATUS",
  "markdown_files": $MD_COUNT,
  "images": $IMG_COUNT,
  "commits": $COMMITS,
  "doc_words": $DOC_WORDS
}
EOF
)

# Build complete snapshot JSON
python3 -c "
import json
import sys
from datetime import datetime

# Parse inputs
new_entry = json.loads('''$NEW_ENTRY''')
history = json.loads('''$EXISTING_HISTORY''')

# Append new entry to history
history.append(new_entry)

# Build complete snapshot
snapshot = {
    'last_update': '$TIMESTAMP',
    'health_status': '$HEALTH_STATUS',
    'metrics': {
        'markdown_files': $MD_COUNT,
        'images': $IMG_COUNT,
        'commits': $COMMITS,
        'documentation_words': $DOC_WORDS,
        'scripts': {
            'shell': $SHELL_SCRIPTS,
            'python': $PYTHON_SCRIPTS,
            'total_lines': $TOTAL_SCRIPT_LINES
        }
    },
    'history': history
}

# Write to file
with open('$SNAPSHOT_FILE', 'w') as f:
    json.dump(snapshot, f, indent=2)

print('✅ Snapshot updated successfully')
"

# 5. Show summary
echo ""
echo -e "${GREEN}✅ Health snapshot updated${NC}"
echo "   File: $SNAPSHOT_FILE"
echo "   History entries: $(python3 -c "import json; print(len(json.load(open('$SNAPSHOT_FILE')).get('history', [])))")"
echo ""

# Cleanup
rm -f "$TEMP_HEALTH" "$TEMP_STATS"

# 6. Show recent trend (if we have history)
HISTORY_COUNT=$(python3 -c "import json; print(len(json.load(open('$SNAPSHOT_FILE')).get('history', [])))" 2>/dev/null || echo "0")
if [ "$HISTORY_COUNT" -gt 1 ]; then
    echo -e "${BLUE}📊 Recent Trends (last 5 snapshots):${NC}"
    python3 -c "
import json
from datetime import datetime

with open('$SNAPSHOT_FILE', 'r') as f:
    data = json.load(f)
    
history = data.get('history', [])[-5:]  # Last 5 entries

print('  Time                    Health      MD    Images  Commits  Words')
print('  ' + '-' * 70)
for entry in history:
    ts = entry['timestamp'][:16].replace('T', ' ')  # Truncate to minutes
    health = entry['health'][:4]  # Abbreviate
    md = entry['markdown_files']
    img = entry['images']
    commits = entry['commits']
    words = entry['doc_words']
    print(f'  {ts}  {health:8s}  {md:4d}   {img:4d}   {commits:4d}    {words:5d}')
"
fi

echo ""
echo -e "${GREEN}🎯 Ready for next REOS cycle${NC}"
