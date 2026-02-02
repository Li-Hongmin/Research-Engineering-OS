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

# 创建根页面重定向至英文版本
cat > book/index.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=./en/">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Engineering OS</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .container {
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        p {
            color: #666;
            margin: 10px 0;
        }
        a {
            color: #0d9488;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Redirecting...</h1>
        <p>Research Engineering OS</p>
        <p>If not redirected automatically, <a href="./en/">click here</a>.</p>
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
