# 常用单细胞分析工具清单

除 AnnData、Scanpy、Seurat 和 scvi-tools 之外，单细胞项目常会按任务接入专用工具。下面按分析问题组织一版工具地图，方便决定下一步该学什么。

## 细胞类型注释

<div class="check-grid">
  <article>
    <strong><a href="/tools/celltypist/">CellTypist</a></strong>
    <span>Python 自动注释工具，适合免疫细胞注释迁移。输出需要标志基因和组织背景复核。</span>
  </article>
  <article>
    <strong>SingleR</strong>
    <span>R/Bioconductor 注释工具，基于参考转录组做标签迁移。</span>
  </article>
  <article>
    <strong>Azimuth</strong>
    <span>Seurat 生态的参考映射工具，适合有高质量参考图谱的场景。</span>
  </article>
  <article>
    <strong>Garnett / scmap</strong>
    <span>可用于基于标志基因或基于参考数据的注释，适合和其它结果交叉验证。</span>
  </article>
</div>

## 空间组学

<div class="check-grid">
  <article>
    <strong><a href="/tools/squidpy/">Squidpy</a></strong>
    <span>scverse 空间分析工具，覆盖空间图、邻域富集、图像特征和配体-受体分析。</span>
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
    <span>R 工具，用配体-受体数据库推断细胞群间通讯网络，适合微环境和免疫互作分析。</span>
  </article>
  <article>
    <strong>CellPhoneDB</strong>
    <span>常用配体-受体推断工具，适合细胞群层面的通讯筛查。</span>
  </article>
  <article>
    <strong>NicheNet</strong>
    <span>把配体活性和靶基因程序连接起来，适合问“哪个发送细胞可能驱动接收细胞状态”。</span>
  </article>
  <article>
    <strong>LIANA</strong>
    <span>整合多种细胞间通讯方法的框架，适合比较不同算法输出。</span>
  </article>
</div>

<div class="doc-callout warning">
  <strong>通讯推断不是功能验证</strong>
  <p>CellChat、CellPhoneDB 和 NicheNet 的结果通常是候选互作。更可靠的解释需要空间邻近、配体/受体表达、下游靶基因程序和实验验证共同支持。</p>
</div>

## 轨迹、发育和 RNA 速率

<div class="check-grid">
  <article>
    <strong>Monocle 3</strong>
    <span>R 生态轨迹推断工具，常用于拟时序、轨迹图和分支分析。</span>
  </article>
  <article>
    <strong>Slingshot</strong>
    <span>基于细胞群和低维空间的谱系推断工具，适合较清晰的分化路径。</span>
  </article>
  <article>
    <strong>Palantir</strong>
    <span>用于连续状态、分化潜能和命运概率的轨迹分析。</span>
  </article>
  <article>
    <strong>scVelo</strong>
    <span>RNA 速率工具，用已剪接/未剪接计数推断动态方向，依赖较强模型假设。</span>
  </article>
</div>

## 批次整合与大数据处理

<div class="check-grid">
  <article>
    <strong>Harmony</strong>
    <span>常用批次校正/整合工具，可接 Seurat 或 Scanpy。</span>
  </article>
  <article>
    <strong>BBKNN</strong>
    <span>Scanpy 生态批次平衡邻居图方法，适合快速建立整合基线。</span>
  </article>
  <article>
    <strong>LIGER</strong>
    <span>矩阵分解式整合方法，适合跨数据集和跨模态分析。</span>
  </article>
  <article>
    <strong>scArches</strong>
    <span>基于 scvi-tools 的参考映射/图谱更新框架。</span>
  </article>
</div>

## 双细胞、质量控制和环境 RNA

<div class="check-grid">
  <article>
    <strong>Scrublet</strong>
    <span>Python 双细胞检测工具，常与 Scanpy 搭配。</span>
  </article>
  <article>
    <strong>DoubletFinder</strong>
    <span>Seurat/R 生态常用双细胞检测工具。</span>
  </article>
  <article>
    <strong>scDblFinder</strong>
    <span>Bioconductor 双细胞检测工具，适合 R 流程。</span>
  </article>
  <article>
    <strong>SoupX / CellBender</strong>
    <span>处理环境 RNA 或背景污染。使用前要理解平台和样本背景。</span>
  </article>
</div>

## CNV、肿瘤克隆和恶性细胞识别

<div class="check-grid">
  <article>
    <strong><a href="/tools/infercnv/">inferCNV</a></strong>
    <span>从表达矩阵推断大尺度 CNV，常用于区分恶性与非恶性细胞。</span>
  </article>
  <article>
    <strong>CopyKAT</strong>
    <span>自动识别非整倍体肿瘤细胞和二倍体正常细胞的 R 工具。</span>
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
    <span>Python/R 工具，用调控因子-靶基因关系或通路基因集推断转录因子/通路活性。</span>
  </article>
  <article>
    <strong>AUCell / SCENIC</strong>
    <span>推断调控子活性，适合转录因子调控网络分析。</span>
  </article>
  <article>
    <strong>GSVA / ssGSEA</strong>
    <span>常用于通路评分，但单细胞场景要注意掉落事件和组成偏倚。</span>
  </article>
  <article>
    <strong>PROGENy / DoRothEA</strong>
    <span>常与 decoupler 搭配，用于通路和转录因子活性推断。</span>
  </article>
</div>

## 多组学与模态整合

<div class="check-grid">
  <article>
    <strong>Muon / MuData</strong>
    <span>scverse 多模态容器和分析工具，适合 RNA + ATAC、RNA + 蛋白等数据。</span>
  </article>
  <article>
    <strong>TOTALVI</strong>
    <span>scvi-tools 中处理 CITE-seq RNA + 蛋白的模型。</span>
  </article>
  <article>
    <strong>MULTIVI</strong>
    <span>scvi-tools 中处理配对/非配对多组学的模型。</span>
  </article>
  <article>
    <strong>Signac</strong>
    <span>Seurat 生态的 scATAC-seq 和多组学分析工具。</span>
  </article>
</div>

## 差异表达和组成变化

<div class="check-grid">
  <article>
    <strong>MAST</strong>
    <span>单细胞差异表达常用模型，适合考虑检出率等因素。</span>
  </article>
  <article>
    <strong>edgeR / DESeq2 pseudobulk</strong>
    <span>按样本聚合做伪 bulk 差异表达，通常比细胞层面的差异表达更贴近实验设计。</span>
  </article>
  <article>
    <strong>Milo</strong>
    <span>分析细胞状态/邻域丰度变化，适合差异丰度分析。</span>
  </article>
  <article>
    <strong>muscat</strong>
    <span>多样本多群体单细胞差异状态分析工具。</span>
  </article>
</div>

## 选择原则

1. 先明确任务：注释、整合、RNA 速率、空间分析、细胞通讯、通路分析、CNV、多组学、差异表达或丰度变化。
2. 优先看官方教程，确认输入对象、矩阵要求和版本。
3. 博客和经验帖适合补参数判断，但不能替代官方 API。
4. 自动工具的输出要回到标志基因、样本设计和生物学背景复核。
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
