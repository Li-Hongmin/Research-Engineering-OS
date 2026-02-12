#!/bin/bash
# generate_dashboard.sh - Generate REOS Project Health Dashboard
# Part of REOS automation system

set -e

OUTPUT="dashboard.html"
SNAPSHOT=".reos/health-snapshot.json"

echo "🎨 Generating REOS Project Health Dashboard..."

# Check if snapshot exists
if [ ! -f "$SNAPSHOT" ]; then
    echo "❌ Error: $SNAPSHOT not found"
    echo "   Run: make snapshot"
    exit 1
fi

# Generate HTML dashboard
python3 << 'EOF'
import json
from datetime import datetime

# Load snapshot data
with open('.reos/health-snapshot.json', 'r') as f:
    data = json.load(f)

# Extract current metrics
metrics = data['metrics']
history = data['history']
last_update = data['last_update']

# Calculate trends
if len(history) >= 2:
    prev = history[-2]
    curr = history[-1]
    commits_trend = curr['commits'] - prev['commits']
    words_trend = curr['doc_words'] - prev['doc_words']
    md_trend = curr['markdown_files'] - prev['markdown_files']
    img_trend = curr['images'] - prev['images']
else:
    commits_trend = words_trend = md_trend = img_trend = 0

# Generate chart data for last 30 snapshots
chart_history = history[-30:] if len(history) > 30 else history
timestamps = [h['timestamp'][:16].replace('T', ' ') for h in chart_history]
commits_data = [h['commits'] for h in chart_history]
words_data = [h['doc_words'] for h in chart_history]
md_data = [h['markdown_files'] for h in chart_history]
img_data = [h['images'] for h in chart_history]

# Get health status color
health_colors = {
    'EXCELLENT': '#10b981',
    'GOOD': '#3b82f6',
    'NEEDS_ATTENTION': '#f59e0b',
    'CRITICAL': '#ef4444'
}
health_color = health_colors.get(data['health_status'], '#6b7280')

# HTML template
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REOS Project Health Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }}
        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        header p {{
            font-size: 1rem;
            opacity: 0.9;
        }}
        .health-badge {{
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: {health_color};
            color: white;
            border-radius: 2rem;
            font-weight: bold;
            font-size: 1.2rem;
            margin: 1rem 0;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .metric-card h3 {{
            font-size: 0.9rem;
            color: #6b7280;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        .metric-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 0.5rem;
        }}
        .metric-card .trend {{
            font-size: 0.9rem;
            color: #6b7280;
        }}
        .trend.positive {{
            color: #10b981;
        }}
        .trend.negative {{
            color: #ef4444;
        }}
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
        }}
        .chart-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .chart-card h3 {{
            font-size: 1.2rem;
            color: #1f2937;
            margin-bottom: 1rem;
        }}
        footer {{
            text-align: center;
            color: white;
            margin-top: 2rem;
            opacity: 0.8;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🪷 REOS Project Health Dashboard</h1>
            <p>Research Engineering Operating System - Real-time Metrics</p>
            <div class="health-badge">{data['health_status']}</div>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;">Last updated: {last_update}</p>
        </header>

        <div class="metrics">
            <div class="metric-card">
                <h3>📊 Total Commits</h3>
                <div class="value">{metrics['commits']}</div>
                <div class="trend {'positive' if commits_trend > 0 else 'negative' if commits_trend < 0 else ''}">
                    {'+' if commits_trend > 0 else ''}{commits_trend} from last snapshot
                </div>
            </div>
            <div class="metric-card">
                <h3>📝 Documentation Words</h3>
                <div class="value">{metrics['documentation_words']:,}</div>
                <div class="trend {'positive' if words_trend > 0 else 'negative' if words_trend < 0 else ''}">
                    {'+' if words_trend > 0 else ''}{words_trend} from last snapshot
                </div>
            </div>
            <div class="metric-card">
                <h3>📄 Markdown Files</h3>
                <div class="value">{metrics['markdown_files']}</div>
                <div class="trend {'positive' if md_trend > 0 else 'negative' if md_trend < 0 else ''}">
                    {'+' if md_trend > 0 else ''}{md_trend} from last snapshot
                </div>
            </div>
            <div class="metric-card">
                <h3>🖼️ Images</h3>
                <div class="value">{metrics['images']}</div>
                <div class="trend {'positive' if img_trend > 0 else 'negative' if img_trend < 0 else ''}">
                    {'+' if img_trend > 0 else ''}{img_trend} from last snapshot
                </div>
            </div>
            <div class="metric-card">
                <h3>🔧 Shell Scripts</h3>
                <div class="value">{metrics['scripts']['shell']}</div>
                <div class="trend">Automation tools</div>
            </div>
            <div class="metric-card">
                <h3>🐍 Python Scripts</h3>
                <div class="value">{metrics['scripts']['python']}</div>
                <div class="trend">{metrics['scripts']['total_lines']:,} total lines</div>
            </div>
        </div>

        <div class="charts">
            <div class="chart-card">
                <h3>📈 Commits Growth</h3>
                <canvas id="commitsChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>📊 Documentation Growth</h3>
                <canvas id="wordsChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>📄 Content Files</h3>
                <canvas id="filesChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>🖼️ Images</h3>
                <canvas id="imagesChart"></canvas>
            </div>
        </div>

        <footer>
            <p>Generated by REOS Automation System | Data source: .reos/health-snapshot.json</p>
        </footer>
    </div>

    <script>
        const chartConfig = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{ display: false }}
            }},
            scales: {{
                y: {{ beginAtZero: false }}
            }}
        }};

        // Commits chart
        new Chart(document.getElementById('commitsChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(timestamps)},
                datasets: [{{
                    label: 'Commits',
                    data: {json.dumps(commits_data)},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: chartConfig
        }});

        // Words chart
        new Chart(document.getElementById('wordsChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(timestamps)},
                datasets: [{{
                    label: 'Words',
                    data: {json.dumps(words_data)},
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: chartConfig
        }});

        // Files chart
        new Chart(document.getElementById('filesChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(timestamps)},
                datasets: [{{
                    label: 'Markdown Files',
                    data: {json.dumps(md_data)},
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: chartConfig
        }});

        // Images chart
        new Chart(document.getElementById('imagesChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(timestamps)},
                datasets: [{{
                    label: 'Images',
                    data: {json.dumps(img_data)},
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: chartConfig
        }});
    </script>
</body>
</html>
'''

# Write HTML file
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Dashboard generated successfully: dashboard.html")
print(f"📊 Current status: {data['health_status']}")
print(f"📈 History entries: {len(history)}")
print("\n🌐 Open in browser:")
print(f"   file://{__import__('os').path.abspath('dashboard.html')}")

EOF

chmod +x "$OUTPUT"
echo ""
echo "✅ Dashboard generation complete!"
echo "   File: $OUTPUT"
echo "   Command: open $OUTPUT"
