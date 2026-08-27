# 固有免疫

固有免疫是免疫系统的快速响应层。它先通过屏障阻止入侵；一旦病原体或组织损伤突破屏障，补体、吞噬细胞、模式识别受体、炎症因子、干扰素、NK 细胞和固有淋巴样细胞会在小时级别启动防御 [1]。

## 一张地图

<div class="flow-strip">
  <span>上皮屏障</span>
  <span>抗菌分子</span>
  <span>补体标记</span>
  <span>吞噬杀伤</span>
  <span>PRR 感知</span>
  <span>炎症募集</span>
  <span>干扰素抗病毒</span>
  <span>NK / ILC 效应</span>
</div>

## 屏障与补体

| 机制 | 关键组成 | 主要作用 | 单细胞解读线索 |
|---|---|---|---|
| 物理屏障 | skin, mucosal epithelium, mucus, tight junction | 阻止微生物进入组织。 | epithelial stress, interferon-stimulated genes, antimicrobial genes。 |
| 化学防御 | defensins, lysozyme, antimicrobial peptides | 直接抑制或杀伤微生物。 | 上皮细胞和髓系细胞的 antimicrobial program。 |
| 补体 | classical, lectin, alternative pathways | opsonization, inflammation, membrane attack complex。 | `C1QA`, `C1QB`, `C1QC`, `C3`, complement receptor genes。 |
| 吞噬 | neutrophils, macrophages, monocytes | 摄取并清除病原体和碎片。 | `LYZ`, `S100A8`, `S100A9`, `FCGR3A`, `MARCO`, `MRC1` 等。 |

补体可以理解为血浆中的“快速标记和放大系统”：C3b 把目标标记给吞噬细胞，C3a/C5a 招募和激活炎症细胞，终末通路可在部分病原体膜上形成孔道 [1]。

## 模式识别受体

固有免疫不是“非特异”的简单反射，而是通过 PRR 识别 PAMP 和 DAMP。常见模式包括：

| 受体家族 | 常见识别对象 | 典型下游 | 单细胞常见现象 |
|---|---|---|---|
| TLR | bacterial LPS, flagellin, CpG DNA, viral RNA | NF-kB, AP-1, IRF | inflammatory cytokines, type I interferon program。 |
| NLR | bacterial products, cellular stress | inflammasome, IL-1 family | `IL1B`, `NLRP3`, `CASP1` 相关炎症状态。 |
| RLR | cytosolic viral RNA | MAVS, IRF3/7 | `IFIT1`, `ISG15`, `MX1`, `OAS1`。 |
| cGAS-STING | cytosolic DNA | TBK1, IRF3 | DNA damage, viral infection, tumor inflammation。 |

## 炎症与细胞募集

炎症的逻辑是“定位问题，招募细胞，限制损伤，清除威胁，启动修复”。巨噬细胞和树突细胞产生 cytokines 和 chemokines；内皮细胞上调 adhesion molecules；中性粒细胞和单核细胞穿过血管壁进入组织。

<div class="check-grid">
  <article>
    <strong>TNF / IL-1 / IL-6</strong>
    <span>驱动局部炎症、急性期反应和内皮活化；过强时可导致系统性炎症损伤。</span>
  </article>
  <article>
    <strong>CXCL / CCL chemokines</strong>
    <span>决定不同白细胞进入组织的路线，例如中性粒细胞、单核细胞、T cells 的募集。</span>
  </article>
  <article>
    <strong>Type I interferon</strong>
    <span>诱导抗病毒状态，也可在自身免疫和肿瘤微环境中形成长期炎症背景。</span>
  </article>
  <article>
    <strong>NK cells</strong>
    <span>通过 activating/inhibitory receptors 识别缺失 self MHC 或应激配体的靶细胞。</span>
  </article>
</div>

## NK 和 ILC

NK 细胞偏向细胞毒杀伤和 IFN-gamma 产生；ILC1、ILC2、ILC3 则与 Th1、Th2、Th17 类似，分别参与胞内病原、寄生虫/组织修复、黏膜屏障和胞外菌/真菌应答。单细胞数据中，ILC 与 T cell marker 可能部分重叠，需要结合 `TRAC`, `CD3D`, `KLRD1`, `KIT`, `IL7R`, `RORC`, `GATA3`, `TBX21` 等组合判断。

## 自检问题

1. PAMP 和 DAMP 的区别是什么？
2. 补体的三类主要效应是什么？
3. 为什么 type I interferon program 不能简单等同于病毒感染？
4. NK 细胞如何避免攻击健康细胞？

## 参考资料

[1] Murphy, K. & Weaver, C. *Janeway's Immunobiology*. 9th ed. Garland Science (2017). 中文版：《詹韦免疫生物学：原书第九版》，科学出版社，2022。
