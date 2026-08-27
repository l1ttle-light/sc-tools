# 黏膜免疫、疾病与治疗

免疫系统既要清除威胁，也要避免对自身组织、食物抗原和共生微生物产生过度反应。黏膜免疫、免疫缺陷、过敏、自身免疫、移植、疫苗和肿瘤免疫治疗，本质上都围绕这个平衡展开 [1]。

## 黏膜免疫

黏膜是免疫系统最繁忙的界面之一：它持续接触食物、空气、共生菌和病原体。黏膜免疫的重点不是“一直强烈炎症”，而是屏障保护、IgA、组织驻留细胞、微生物群调控和 oral tolerance 的平衡。

| 模块 | 功能 | 单细胞线索 |
|---|---|---|
| epithelial barrier | 物理隔离、抗菌分子、危险信号释放。 | epithelial stress, `DEFA*`, `REG*`, interferon genes。 |
| secretory IgA | 中和和限制微生物黏附，降低炎症性清除需求。 | `JCHAIN`, `IGHA1`, `IGHA2`, plasma cells。 |
| tissue-resident lymphocytes | 快速局部保护与组织监视。 | `ITGAE`, `CXCR6`, `ZNF683`, `CD69`。 |
| microbiota regulation | 塑造局部和系统免疫状态。 | myeloid activation, Th17/ILC3 program, barrier genes。 |

## 免疫防御失败

免疫缺陷可以来自遗传缺陷、感染、药物、营养、年龄或治疗造成的继发性免疫抑制。不同缺陷对应不同感染谱：

| 缺陷类型 | 易感问题 | 机制理解 |
|---|---|---|
| T cell / combined immunodeficiency | viral, fungal, opportunistic infections | T cell help、细胞毒性和免疫协调不足。 |
| B cell / antibody deficiency | extracellular bacteria, some viruses | 中和、opsonization 和 complement activation 不足。 |
| phagocyte defects | bacterial and fungal dissemination | 摄取、氧爆发或趋化迁移不足。 |
| complement defects | encapsulated bacteria, immune complex disease | opsonization、裂解和免疫复合物清除不足。 |

## 过敏和超敏反应

过敏可以理解为免疫系统对无害抗原产生了过强或错误类型的效应应答。IgE-mediated allergy 中，Th2/Tfh 信号推动 IgE 产生；IgE 固定在 mast cells 和 basophils 的 Fc epsilon receptor 上，再次遇到 allergen 时快速脱颗粒。

<div class="check-grid">
  <article>
    <strong>IgE / mast cell axis</strong>
    <span>快速释放 histamine、lipid mediators 和 cytokines，造成鼻炎、哮喘、荨麻疹或 anaphylaxis。</span>
  </article>
  <article>
    <strong>Eosinophils</strong>
    <span>参与寄生虫防御，也可在过敏性炎症中造成组织损伤。</span>
  </article>
  <article>
    <strong>Immune complex</strong>
    <span>大量难清除抗原-抗体复合物可诱发补体和炎症损伤。</span>
  </article>
  <article>
    <strong>Delayed-type hypersensitivity</strong>
    <span>Th1 和 CD8 T cells 可介导迟发型组织炎症。</span>
  </article>
</div>

## 自身免疫和移植

自身免疫来自耐受机制被突破：遗传易感、MHC、感染、组织损伤、分子模拟、免疫豁免区暴露、随机克隆事件都可能参与。移植免疫则是免疫系统把同种异体 MHC 或其呈递的 peptide 识别为危险信号。

| 场景 | 核心机制 | 单细胞关注点 |
|---|---|---|
| organ-specific autoimmunity | 自身抗原局部靶向。 | autoreactive T/B cells, tissue-resident inflammation。 |
| systemic autoimmunity | immune complex、广泛炎症和多器官损伤。 | plasmablast expansion, interferon program, myeloid activation。 |
| acute rejection | T cell-mediated alloreactivity。 | cytotoxic T cells, APC activation, endothelial inflammation。 |
| chronic rejection | 持续低度损伤、血管和纤维化改变。 | macrophage/fibroblast/endothelial states。 |

## 疫苗和肿瘤免疫治疗

疫苗的目标是安全地产生长期保护性免疫，通常需要抗原、合适的递送方式、佐剂和记忆细胞形成。肿瘤免疫治疗则利用或增强抗肿瘤免疫，包括 monoclonal antibodies、checkpoint blockade、CAR-T cells 和 cancer vaccines。

<div class="doc-callout important">
  <strong>肿瘤免疫治疗看的是系统</strong>
  <p>checkpoint blockade 是否有效，不只取决于 T cell 是否表达 PD-1，还取决于 antigen presentation、T cell infiltration、Treg 和 myeloid suppression、肿瘤抗原负荷、空间排斥和组织代谢环境。</p>
</div>

## 自检问题

1. 黏膜免疫为什么必须同时容忍共生菌和清除病原体？
2. 不同免疫缺陷为什么对应不同感染谱？
3. IgE-mediated allergy 的致敏阶段和效应阶段有什么区别？
4. checkpoint blockade 为什么不是只看 `PDCD1` 或 `CD274` 表达？

## 参考资料

[1] Murphy, K. & Weaver, C. *Janeway's Immunobiology*. 9th ed. Garland Science (2017). 中文版：《詹韦免疫生物学：原书第九版》，科学出版社，2022。
