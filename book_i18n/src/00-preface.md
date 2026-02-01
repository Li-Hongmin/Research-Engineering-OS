# 前言

![插图](images/00_preface_thinking.png)

AI 时代把研究与开发的边界进一步抹平：从提出假设、搭建原型、跑通实验，到把结果固化为可复现的证据链，这一切都在更短的周期里完成；而 AI 编码助手让"写出能跑的代码"变得前所未有地容易，却也让"写出可信、可追溯、可复现的研究代码"变得更难。

我写这本《Research Engineering OS》，不是想再提供一套抽象的"方法论"，而是把我在学术机器学习/计算生物学研究中反复踩过的坑，压缩成一套可执行的默认行为：用**规范**减少返工、用**模板**降低协作成本、用**检查清单**在每天的节奏里提前消化最后阶段才爆炸的风险。

这本小书的核心观点很朴素：**探索可以野，但产出必须能被清理；结论可以暂时脆弱，但证据链必须牢靠。** 你可以快速试错，但要为每一次"看起来有效"的结果留下足够的信息，使它在一周后、一个月后、换一台机器后依然能被复现、被质疑、被验证。

因此，本书会反复强调三件事：

- **实验是最小单位**：记录的不是"改了哪些代码"，而是"这次实验由哪些版本与配置构成"。

- **默认自动留痕**：让 run_id、commit、config、数据版本、环境摘要成为流水线的一部分。

- **DoD 与清单前置**：把论文阶段才会要求的严谨性，拆成日常可执行的小动作。

如果你正在做的工作属于"AI 时代的研究开发"（research development）：既要保持探索速度、又要对结果负责、还要与合作者高效沟通，希望这本书能成为你桌面旁的一份最小操作系统。

<div style="text-align: right; margin-top: 2em;">

**Li Hongmin（李鸿敏）**<br>
Department of Computational Biology and Medical Sciences<br>
Graduate School of Frontier Sciences, The University of Tokyo<br>
5-1-5 Kashiwanoha, Kashiwa-shi, Chiba 277-8561, Japan<br>
[li-hongmin.github.io](https://li-hongmin.github.io)<br>
[lihongmin@edu.k.u-tokyo.ac.jp](mailto:lihongmin@edu.k.u-tokyo.ac.jp)

</div>
