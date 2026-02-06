#!/bin/bash
# 构建中英日三语版本的 manga-book
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
sedi 's/title = "研究工程 OS - 漫画版"/title = "Research Engineering OS - Manga Edition"/' book.toml
sedi 's/description = "用漫画讲述研究工程实践的故事"/description = "Research engineering practices told through manga storytelling"/' book.toml

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
sedi 's/title = "研究工程 OS - 漫画版"/title = "研究工学OS - マンガ版"/' book.toml
sedi 's/description = "用漫画讲述研究工程实践的故事"/description = "研究工学の実践をマンガで語る"/' book.toml

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

# 创建根页面重定向至中文版本
cat > book/index.html << 'HTML'
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=./zh/">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究工程 OS - 漫画版</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2em;
        }
        .subtitle {
            color: #666;
            margin: 15px 0;
            font-size: 1.1em;
        }
        .emoji {
            font-size: 3em;
            margin-bottom: 20px;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        a:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">📚✨</div>
        <h1>研究工程 OS</h1>
        <p class="subtitle">漫画版</p>
        <p>正在跳转到中文版...</p>
        <a href="./zh/">如果没有自动跳转，请点击这里</a>
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
