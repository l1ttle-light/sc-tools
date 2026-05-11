# 常用单细胞分析工具清单

除 AnnData, Scanpy, Seurat, and scvi-tools 之外，单细胞项目常会按任务接入专用工具。下面按分析问题组织一版工具地图，方便决定下一步该学什么。

## 细胞类型注释

<div class="check-grid">
  <article>
    <strong><a href="/tools/celltypist/">CellTypist</a></strong>
    <span>Python 自动注释工具，适合 immune cell annotation transfer。输出需要 marker gene 和组织背景复核。</span>
  </article>
  <article>
    <strong>SingleR</strong>
    <span>R/Bioconductor 注释工具，基于 reference transcriptome 做 label transfer。</span>
  </article>
  <article>
    <strong>Azimuth</strong>
    <span>Seurat 生态 reference mapping 工具，适合有高质量 reference atlas 的场景。</span>
  </article>
  <article>
    <strong>Garnett / scmap</strong>
    <span>可用于 marker-based 或 reference-based annotation，适合和其它结果交叉验证。</span>
  </article>
</div>

## 空间组学

<div class="check-grid">
  <article>
    <strong><a href="/tools/squidpy/">Squidpy</a></strong>
    <span>scverse 空间分析工具，覆盖 spatial graph, neighborhood enrichment, image features, and ligand-receptor。</span>
  </article>
  <article>
    <strong>Giotto</strong>
    <span>空间转录组综合分析框架，常用于空间可视化、空间模式和细胞互作分析。</span>
  </article>
  <article>
    <strong>Seurat spatial</strong>
    <span>Seurat 生态中的 Visium/空间分析流程，适合 R 用户。</span>
  </article>
  <article>
    <strong>stLearn</strong>
    <span>空间转录组分析工具，强调组织图像、空间邻域和细胞通讯。</span>
  </article>
</div>

## 细胞通讯与微环境

<div class="check-grid">
  <article>
    <strong>CellChat</strong>
    <span>R 工具，用 ligand-receptor database 推断细胞群间通讯网络，适合微环境和免疫互作分析。</span>
  </article>
  <article>
    <strong>CellPhoneDB</strong>
    <span>常用 ligand-receptor 推断工具，适合 cluster-level communication screening。</span>
  </article>
  <article>
    <strong>NicheNet</strong>
    <span>把 ligand activity 和 target gene program 连接起来，适合问“哪个发送细胞可能驱动接收细胞状态”。</span>
  </article>
  <article>
    <strong>LIANA</strong>
    <span>整合多种 cell-cell communication 方法的框架，适合比较不同算法输出。</span>
  </article>
</div>

<div class="doc-callout warning">
  <strong>通讯推断不是功能验证</strong>
  <p>CellChat, CellPhoneDB, and NicheNet 的结果通常是候选互作。更可靠的解释需要空间邻近、配体/受体表达、下游 target program 和实验验证共同支持。</p>
</div>

## 轨迹、发育和 RNA velocity

<div class="check-grid">
  <article>
    <strong>Monocle 3</strong>
    <span>R 生态轨迹推断工具，常用于 pseudotime, trajectory graph, and branch analysis。</span>
  </article>
  <article>
    <strong>Slingshot</strong>
    <span>基于 cluster 和低维空间的 lineage inference 工具，适合较清晰的分化路径。</span>
  </article>
  <article>
    <strong>Palantir</strong>
    <span>用于连续状态、分化潜能和 fate probability 的轨迹分析。</span>
  </article>
  <article>
    <strong>scVelo</strong>
    <span>RNA velocity 工具，用 spliced/unspliced counts 推断动态方向，依赖较强模型假设。</span>
  </article>
</div>

## 批次整合与大数据处理

<div class="check-grid">
  <article>
    <strong>Harmony</strong>
    <span>常用 batch correction/integration 工具，可接 Seurat 或 Scanpy。</span>
  </article>
  <article>
    <strong>BBKNN</strong>
    <span>Scanpy 生态批次平衡邻居图方法，适合快速 integration baseline。</span>
  </article>
  <article>
    <strong>LIGER</strong>
    <span>矩阵分解式整合方法，适合跨数据集和跨模态分析。</span>
  </article>
  <article>
    <strong>scArches</strong>
    <span>基于 scvi-tools 的 reference mapping/atlas update 框架。</span>
  </article>
</div>

## Doublet、质量控制和环境 RNA

<div class="check-grid">
  <article>
    <strong>Scrublet</strong>
    <span>Python doublet 检测工具，常与 Scanpy 搭配。</span>
  </article>
  <article>
    <strong>DoubletFinder</strong>
    <span>Seurat/R 生态常用 doublet 检测工具。</span>
  </article>
  <article>
    <strong>scDblFinder</strong>
    <span>Bioconductor doublet detection 工具，适合 R pipeline。</span>
  </article>
  <article>
    <strong>SoupX / CellBender</strong>
    <span>处理 ambient RNA 或 background contamination。使用前要理解平台和样本背景。</span>
  </article>
</div>

## CNV、肿瘤克隆和恶性细胞识别

<div class="check-grid">
  <article>
    <strong><a href="/tools/infercnv/">inferCNV</a></strong>
    <span>从表达矩阵推断 large-scale CNV，常用于 malignant vs non-malignant 区分。</span>
  </article>
  <article>
    <strong>CopyKAT</strong>
    <span>自动识别 aneuploid tumor cells 和 diploid normal cells 的 R 工具。</span>
  </article>
  <article>
    <strong>HoneyBADGER</strong>
    <span>从 scRNA-seq 推断 CNV 和 LOH 的工具。</span>
  </article>
  <article>
    <strong>CONICSmat</strong>
    <span>基于表达矩阵识别 CNV 相关模式，适合肿瘤单细胞场景。</span>
  </article>
</div>

## 通路、转录因子和功能活性

<div class="check-grid">
  <article>
    <strong>decoupler</strong>
    <span>Python/R 工具，用 regulator-target 或 pathway-gene sets 推断 TF/pathway activity。</span>
  </article>
  <article>
    <strong>AUCell / SCENIC</strong>
    <span>推断 regulon activity，适合转录因子调控网络分析。</span>
  </article>
  <article>
    <strong>GSVA / ssGSEA</strong>
    <span>常用于 pathway score，但单细胞场景要注意 dropout 和 composition bias。</span>
  </article>
  <article>
    <strong>PROGENy / DoRothEA</strong>
    <span>常与 decoupler 搭配，用于 pathway 和 TF activity 推断。</span>
  </article>
</div>

## 多组学与模态整合

<div class="check-grid">
  <article>
    <strong>Muon / MuData</strong>
    <span>scverse 多模态容器和分析工具，适合 RNA + ATAC, RNA + protein 等数据。</span>
  </article>
  <article>
    <strong>TOTALVI</strong>
    <span>scvi-tools 中处理 CITE-seq RNA + protein 的模型。</span>
  </article>
  <article>
    <strong>MULTIVI</strong>
    <span>scvi-tools 中处理 paired/unpaired multiome 的模型。</span>
  </article>
  <article>
    <strong>Signac</strong>
    <span>Seurat 生态的 scATAC-seq 和 multiome 分析工具。</span>
  </article>
</div>

## 差异表达和组成变化

<div class="check-grid">
  <article>
    <strong>MAST</strong>
    <span>单细胞差异表达常用模型，适合考虑 detection rate 等因素。</span>
  </article>
  <article>
    <strong>edgeR / DESeq2 pseudobulk</strong>
    <span>按 sample 聚合做 pseudobulk DE，通常比 cell-level DE 更贴近实验设计。</span>
  </article>
  <article>
    <strong>Milo</strong>
    <span>分析细胞状态/邻域 abundance changes，适合 differential abundance。</span>
  </article>
  <article>
    <strong>muscat</strong>
    <span>多样本多群体单细胞差异状态分析工具。</span>
  </article>
</div>

## 选择原则

1. 先明确任务：annotation, integration, velocity, spatial, communication, pathway, CNV, multiome, DE, or abundance。
2. 优先看官方教程，确认输入对象、矩阵要求和版本。
3. 博客和经验帖适合补参数判断，但不能替代官方 API。
4. 自动工具的输出要回到 marker、样本设计和生物学背景复核。
5. 涉及微环境和通讯时，最好结合空间邻近或实验验证。

## 资料入口

- [CellTypist documentation](https://celltypist.readthedocs.io/)
- [Squidpy documentation](https://squidpy.readthedocs.io/)
- [inferCNV documentation](https://github.com/broadinstitute/infercnv)
- [CellChat tutorial](https://htmlpreview.github.io/?https://github.com/sqjin/CellChat/blob/master/tutorial/CellChat-vignette.html)
- [CellPhoneDB documentation](https://cellphonedb.readthedocs.io/)
- [NicheNet tutorial](https://github.com/saeyslab/nichenetr)
- [LIANA documentation](https://liana-py.readthedocs.io/)
- [scVelo documentation](https://scvelo.readthedocs.io/)
- [Muon documentation](https://muon.readthedocs.io/)
- [decoupler documentation](https://decoupler.readthedocs.io/)
- [Scrublet repository](https://github.com/swolock/scrublet)

