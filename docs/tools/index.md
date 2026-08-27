# 单细胞相关工具

单细胞工具很多，但学习时不应该从“软件名”开始堆列表。更稳的方式是先问：这个工具接管了分析链路里的哪一段？当前主线按数据容器、Python 分析、R 分析、深度生成模型和专用任务工具组织。

<div class="tool-grid">
  <a href="/tools/anndata/">
    <strong>AnnData</strong>
    <span>Python/scverse 生态的数据容器，承载 X、obs、var、layers、obsm、varm、obsp 和 uns。</span>
  </a>
  <a href="/tools/scanpy/">
    <strong>Scanpy</strong>
    <span>Python 单细胞分析主力工具，围绕 AnnData 管理矩阵、元数据、降维、聚类和可视化。</span>
  </a>
  <a href="/tools/seurat/">
    <strong>Seurat</strong>
    <span>R 生态经典工具，适合和 Scanpy 形成互相校验的分析视角。</span>
  </a>
  <a href="/tools/scvi-tools/">
    <strong>scvi-tools</strong>
    <span>面向整合、批次校正、潜变量建模和概率解释的现代工具链。</span>
  </a>
  <a href="/tools/celltypist/">
    <strong>CellTypist</strong>
    <span>自动细胞类型注释工具，适合注释迁移和免疫细胞初筛。</span>
  </a>
  <a href="/tools/squidpy/">
    <strong>Squidpy</strong>
    <span>空间组学分析工具，覆盖空间图、邻域富集和空间模式。</span>
  </a>
  <a href="/tools/infercnv/">
    <strong>inferCNV</strong>
    <span>从 scRNA-seq 表达矩阵推断大尺度 CNV，常用于肿瘤恶性细胞识别。</span>
  </a>
  <a href="/tools/common-tools/">
    <strong>常用工具清单</strong>
    <span>自动注释、空间组学、细胞通讯、RNA 速率、双细胞、通路活性和 CNV 推断工具。</span>
  </a>
</div>

## 第一阶段

先纳入 AnnData、Scanpy、Seurat 和 scvi-tools。AnnData 是 Python 数据容器，Scanpy 是 Python 常规分析主线，Seurat 是 R 生态主线，scvi-tools 负责更现代的整合和概率建模。

<div class="doc-callout important">
  <strong>学习目标</strong>
  <p>不是只跑通一份笔记本，而是能解释每一步为什么要做、参数改变会影响什么、图上异常应该回到哪一步排查。</p>
</div>
