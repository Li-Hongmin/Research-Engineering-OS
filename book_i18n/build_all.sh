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
rm -rf book book_zh book_en

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

echo "📦 整合输出..."
mkdir -p book
# 移动语言版本到子目录
mv book_zh book/zh
mv book_en book/en

# 创建首页重定向（纯跳转，无明文链接）
cat > book/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=zh/">
    <title>Research Engineering OS</title>
</head>
<body></body>
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
echo "🌐 本地预览: cd book && python -m http.server 8000"
echo "   然后访问 http://localhost:8000"
