#!/bin/bash
# 构建中英文双语版本的 mdBook
# 兼容 macOS 和 Linux

set -e
cd "$(dirname "$0")"

# 跨平台 sed -i 函数
sedi() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

echo "🧹 清理旧构建..."
rm -rf book book_zh book_en book_ja

# 保存原始 book.toml
cp book.toml book.toml.original

# 创建不含 gettext 的临时配置（避免依赖问题）
grep -v '\[preprocessor.gettext\]' book.toml.original | grep -v 'after = \["links"\]' > book.toml

echo "🇨🇳 构建中文版..."
mdbook build
# 立即重命名为 book_zh
mv book book_zh

echo "🇺🇸 准备英文版..."
# 临时交换源目录
mv src src_zh
mv src_en src

# 修改语言设置
sedi 's/language = "zh"/language = "en"/' book.toml
sedi 's/description = "把返工压缩成规范 + 模板 + 检查清单"/description = "Compress rework into specifications + templates + checklists"/' book.toml

echo "🇺🇸 构建英文版..."
mdbook build
# 立即重命名为 book_en
mv book book_en

echo "🔄 恢复原始配置..."
# 恢复源目录
mv src src_en
mv src_zh src
# 恢复原始 book.toml
mv book.toml.original book.toml

echo "🇯🇵 准备日文版..."
# 保存原始 book.toml
cp book.toml book.toml.original
grep -v '\[preprocessor.gettext\]' book.toml.original | grep -v 'after = \["links"\]' > book.toml

mv src src_zh
mv src_ja src

# 修改语言设置
sedi 's/language = "zh"/language = "ja"/' book.toml
sedi 's/description = "把返工压缩成规范 + 模板 + 检查清单"/description = "「やり直し」を「規範＋テンプレート＋チェックリスト」に凝縮する"/' book.toml

echo "🇯🇵 构建日文版..."
mdbook build
# 立即重命名为 book_ja
mv book book_ja

echo "🔄 恢复原始配置..."
# 恢复源目录
mv src src_ja
mv src_zh src
# 恢复原始 book.toml
mv book.toml.original book.toml

echo "📦 整合输出..."
mkdir -p book
# 移动语言版本到子目录
mv book_zh book/zh
mv book_en book/en
mv book_ja book/ja

# 创建首页导航（文本版 + 漫画版）
cat > book/index.html << 'HTML'
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Engineering OS - 研究工程操作系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.95;
        }
        .content {
            padding: 40px 30px;
        }
        .editions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        @media (max-width: 600px) {
            .editions { grid-template-columns: 1fr; }
        }
        .edition {
            border: 2px solid #f0f0f0;
            border-radius: 8px;
            padding: 30px 20px;
            text-align: center;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .edition:hover {
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
            transform: translateY(-5px);
        }
        .edition h2 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .edition-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .edition p {
            color: #666;
            font-size: 0.95em;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Research Engineering OS</h1>
            <p>研究工程 操作系统</p>
        </div>

        <div class="content">
            <div class="editions">
                <a href="./zh/" class="edition">
                    <div class="edition-icon">📖</div>
                    <h2>文本版</h2>
                    <p>多语言综合指南 (中 / 英 / 日)</p>
                </a>

                <a href="./manga/" class="edition">
                    <div class="edition-icon">🎨</div>
                    <h2>漫画版</h2>
                    <p>故事驱动的学习 (12章节 · 180+面板)</p>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
HTML

# 添加 .nojekyll 文件到根目录
touch book/.nojekyll

echo ""
echo "✅ 构建完成！"
echo ""
echo "📁 输出结构："
ls -la book/
echo ""
echo "📁 book/zh/："
ls book/zh/ | head -5
echo "..."
echo ""
echo "📁 book/en/："
ls book/en/ | head -5
echo "..."
echo ""
echo "📁 book/ja/："
ls book/ja/ | head -5
echo "..."
echo ""
echo "🌐 本地预览: cd book && python -m http.server 8000"
echo "   然后访问 http://localhost:8000"
