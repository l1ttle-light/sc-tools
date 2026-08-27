# 适应性免疫应答

适应性免疫应答的主线是：抗原在次级淋巴器官中被呈递给 naive lymphocytes，特异性克隆扩增并分化为 effector cells，随后一部分细胞死亡以结束反应，另一部分成为 memory cells。T cell 和 B cell 应答相互配合，形成针对不同病原体和组织环境的效应模块 [1]。

## T cell priming

<div class="flow-strip">
  <span>APC 摄取抗原</span>
  <span>APC 成熟迁移</span>
  <span>淋巴结内相遇</span>
  <span>TCR 识别 peptide-MHC</span>
  <span>共刺激</span>
  <span>细胞因子极化</span>
  <span>克隆扩增</span>
  <span>效应/记忆分化</span>
</div>

T cell activation 通常需要三类信息：TCR specificity、costimulation 和 cytokine environment。单细胞数据中如果只看到 `CD3D`、`CD4` 或 `CD8A`，只能说明谱系；判断功能状态还要看 cytokines、transcription factors、cytotoxic genes、checkpoint receptors 和 clonal expansion。

## CD4 T cell 效应模块

| 亚群 | 关键因子 | 典型功能 | 常见 marker / genes |
|---|---|---|---|
| Th1 | IL-12, IFN-gamma, T-bet | 激活 macrophage，对付胞内病原。 | `TBX21`, `IFNG`, `CXCR3` |
| Th2 | IL-4, GATA3 | 驱虫、过敏、屏障修复。 | `GATA3`, `IL4`, `IL5`, `IL13` |
| Th17 | IL-6, IL-23, TGF-beta, RORC | 对付胞外菌和真菌，驱动屏障炎症。 | `RORC`, `IL17A`, `IL17F`, `CCR6` |
| Tfh | BCL6, ICOS, CXCR5 | 帮助 B cell 生发中心反应、类别转换和亲和力成熟。 | `CXCR5`, `ICOS`, `BCL6`, `IL21` |
| Treg | FOXP3, IL2RA, CTLA4 | 抑制过强或自身反应性免疫。 | `FOXP3`, `IL2RA`, `CTLA4`, `IKZF2` |

## CD8 T cell 和细胞毒性

CD8 cytotoxic T cells 通过 perforin/granzyme pathway 或 death receptor pathway 杀伤靶细胞。单细胞中常见 cytotoxic program 包括 `NKG7`, `PRF1`, `GZMB`, `GZMH`, `GNLY`。但 cytotoxic genes 同时可见于 NK cells，所以注释时要结合 TCR/CD3 genes 与 NK receptor genes。

<div class="doc-callout warning">
  <strong>耗竭需要组合证据</strong>
  <p>`PDCD1`、`LAG3`、`TIGIT`、`HAVCR2`、`TOX` 等可以提示 exhaustion-like state，但感染、肿瘤、近期激活和组织驻留都会改变这些基因。最好结合 clonotype、effector genes、样本来源和功能证据。</p>
</div>

## B cell、抗体和生发中心

B cell activation 可以是 T-dependent，也可以是 T-independent。T-dependent response 中，B cell 捕获抗原后向 Tfh 提呈，得到 CD40 和 cytokine help，进入 germinal center，经历 somatic hypermutation、affinity maturation 和 class switch recombination。

| 阶段 | 关键事件 | 单细胞线索 |
|---|---|---|
| activation | antigen binding, T-B linked recognition | `CD69`, `CD83`, `HLA-DRA`, `CD40` |
| germinal center | proliferation, mutation, selection | `BCL6`, `AICDA`, `MKI67` |
| class switching | IgM/IgD 转向 IgG/IgA/IgE | `IGHG*`, `IGHA*`, `IGHE` |
| plasma differentiation | antibody secretion | `XBP1`, `MZB1`, `JCHAIN`, `SDC1` |
| memory formation | rapid secondary response | `CD27`, switched isotypes |

## 免疫记忆

Memory B cells 通常比 naive B cells 更快启动，并可在二次应答中继续亲和力成熟。Memory T cells 可粗略分为 central memory、effector memory 和 tissue-resident memory。单细胞里不要只按 `CCR7` 或 `IL7R` 单基因判断；最好结合 homing receptors、effector genes、tissue residency genes 和样本组织来源。

## 自检问题

1. T cell priming 为什么需要 APC 成熟和共刺激？
2. Th1、Th2、Th17 分别适合应对哪类威胁？
3. Tfh 如何影响 B cell class switching 和 affinity maturation？
4. CD8 T cell 和 NK cell 的 cytotoxic gene program 如何区分？

## 参考资料

[1] Murphy, K. & Weaver, C. *Janeway's Immunobiology*. 9th ed. Garland Science (2017). 中文版：《詹韦免疫生物学：原书第九版》，科学出版社，2022。
