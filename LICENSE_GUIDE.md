# LICENSE Selection Guide for REOS

**Created**: 2026-02-07 15:06 JST  
**Purpose**: 帮助项目维护者选择合适的开源许可证

---

## 🚨 为什么需要 LICENSE？

没有明确许可证的开源项目会导致：
- ❌ 法律风险：默认版权保护意味着他人无法合法使用
- ❌ 贡献者顾虑：不清楚能否安全地 fork/修改/分发
- ❌ 专业度降低：成熟项目都有明确的许可证
- ❌ GitHub 警告：缺失许可证会在仓库页面显示警告

**REOS 当前状态**：⚠️ 无 LICENSE 文件（在 README.md 中标记为 `[Specify license information here]`）

---

## 🎯 REOS 项目特点（许可证选择依据）

### 项目性质
- 📚 **教育资源**：Research Engineering OS 教学材料
- 🌍 **多语言内容**：中/英/日三语言版本
- 📖 **双形态呈现**：text-book（技术文档） + manga-book（漫画教程）
- 🛠️ **包含代码**：自动化脚本（Shell + Python）
- 🖼️ **包含创意内容**：插图、漫画面板（671 张图片）

### 目标受众
- 🎓 研究人员、工程师、学生
- 🤝 可能的贡献者（翻译、插图、代码改进）
- 📚 教育机构（可能用于教学）

---

## 📋 推荐许可证对比

| 许可证 | 类型 | 适合场景 | 主要特点 | 推荐度 |
|--------|------|----------|----------|--------|
| **CC-BY-4.0** | 创作共用 | 📚 教育内容、文档、教材 | - 允许商用<br>- 要求署名<br>- 不要求开源衍生品 | ⭐⭐⭐⭐⭐ |
| **CC-BY-SA-4.0** | 创作共用 | 📚 希望衍生品也开源 | - 允许商用<br>- 要求署名<br>- 衍生品需相同许可证（类似 GPL） | ⭐⭐⭐⭐ |
| **MIT** | 软件许可 | 💻 代码工具、脚本库 | - 极度宽松<br>- 允许闭源使用<br>- 仅保留版权声明 | ⭐⭐⭐ |
| **Apache-2.0** | 软件许可 | 💻 企业级项目、专利考量 | - 明确专利授权<br>- 要求标注修改<br>- 更详细的法律条款 | ⭐⭐ |
| **GPL-3.0** | Copyleft | 💻 强制开源传播 | - 衍生品必须开源<br>- 可能限制教育灵活性 | ⭐ |

---

## 🏆 **推荐方案：CC-BY-4.0**

### 理由
1. ✅ **教育友好**：教育机构可自由使用、修改、分发
2. ✅ **商用允许**：不阻止合理的商业应用（如出版、培训）
3. ✅ **贡献者友好**：贡献者知道他们的工作将被广泛传播
4. ✅ **双重内容适配**：同时覆盖文档和创意内容（插图）
5. ✅ **国际标准**：广泛认可，被众多教育项目使用

### 示例项目
- [Carpentries](https://carpentries.org/) 教学材料
- [O'Reilly Open Books](https://www.oreilly.com/openbook/)
- Coursera 部分课程资料

### 不足
- ⚠️ 衍生品可以闭源（如果希望强制开源，选 CC-BY-SA-4.0）

---

## 🔄 **替代方案：双许可证**

如果希望区分代码和内容：

```
REOS 项目采用双许可证：
- 📄 **内容（文档/图片）**：CC-BY-4.0
- 💻 **代码（脚本/工具）**：MIT License

详见各目录下的 LICENSE 文件。
```

**优点**：
- ✅ 代码可直接用于闭源项目（降低开发者顾虑）
- ✅ 内容保持教育友好性
- ✅ 明确区分不同类型资产

**缺点**：
- ❌ 复杂度增加（需要管理两个许可证）
- ❌ 新手可能困惑

---

## 📝 实施步骤（选定后）

### 1. 创建 LICENSE 文件
```bash
# 下载官方许可证文本
wget https://creativecommons.org/licenses/by/4.0/legalcode.txt -O LICENSE

# 或者手动从 https://choosealicense.com/licenses/cc-by-4.0/ 复制
```

### 2. 更新 README.md
```markdown
## ⚖️ License

This project is licensed under [Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE).

You are free to:
- 📚 **Share** — copy and redistribute the material
- 🔧 **Adapt** — remix, transform, and build upon the material
- 💼 **Commercial use** — for any purpose

Under the following terms:
- 📛 **Attribution** — You must give appropriate credit and indicate if changes were made

See the [LICENSE](LICENSE) file for details.
```

### 3. 添加版权声明到关键文件
在每个 Markdown 文件头部可选添加：
```markdown
---
# Copyright (c) 2024-2026 Hongmin Li
# Licensed under CC-BY-4.0
---
```

### 4. 更新 GitHub 仓库设置
- Settings → General → License → 选择对应许可证
- 触发 GitHub 的许可证徽章显示

### 5. 添加徽章到 README
```markdown
![License](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)
```

---

## 🔗 参考资源

- [Choose a License](https://choosealicense.com/) - GitHub 官方许可证选择指南
- [Creative Commons Licenses](https://creativecommons.org/licenses/) - CC 许可证详解
- [SPDX License List](https://spdx.org/licenses/) - 标准许可证标识符
- [Open Source Guide](https://opensource.guide/legal/) - 开源法律指南

---

## ❓ 决策检查清单

在最终决定前，考虑：

- [ ] 是否允许商业使用？
  - ✅ Yes → CC-BY-4.0 或 MIT
  - ❌ No → CC-BY-NC-4.0（不推荐，限制教育机构）
  
- [ ] 是否要求衍生品也开源？
  - ✅ Yes → CC-BY-SA-4.0 或 GPL-3.0
  - ❌ No → CC-BY-4.0 或 MIT
  
- [ ] 是否需要区分代码和内容？
  - ✅ Yes → 双许可证（MIT + CC-BY-4.0）
  - ❌ No → 单一许可证
  
- [ ] 是否关心专利保护？
  - ✅ Yes → Apache-2.0（代码部分）
  - ❌ No → MIT（更简洁）

---

**建议**：基于 REOS 的教育性质，**CC-BY-4.0** 是最佳选择，除非有特殊需求。

**下一步**：在 TODO.md 中标记此任务，等待用户决策后实施。
