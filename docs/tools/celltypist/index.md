# CellTypist 教程

CellTypist 是常用的自动细胞类型注释工具，适合把 query single-cell RNA-seq 数据映射到已有 reference model。它在免疫细胞注释场景里尤其常见，因为官方和社区模型覆盖了不少免疫细胞状态。

CellTypist 的定位不是替代人工注释，而是给出一个可复核的第一版标签：它能帮助快速发现主要细胞类型、检查 cluster 是否合理、辅助发现疑似 doublet 或 ambiguous cluster。最终结论仍要回到 marker gene、组织背景和实验设计。

<div class="path-grid">
  <a href="/tools/celltypist/annotation-workflow">
    <strong>自动注释流程</strong>
    <span>从 AnnData 输入、模型选择、annotate 到 majority voting 和结果回写。</span>
  </a>
  <a href="/tools/scanpy/clustering-annotation">
    <strong>与 marker 注释对照</strong>
    <span>把 CellTypist labels 和 Leiden clusters、marker genes 一起检查。</span>
  </a>
  <a href="/tools/common-tools/">
    <strong>其它注释工具</strong>
    <span>SingleR, Azimuth, Garnett, scmap 等工具也可用于 annotation transfer。</span>
  </a>
  <a href="/references/">
    <strong>参考资料</strong>
    <span>查看 CellTypist 官方文档和细胞注释实践资料。</span>
  </a>
</div>

## 什么时候适合使用

<div class="check-grid">
  <article>
    <strong>初步细胞类型注释</strong>
    <span>快速给 cluster 或 cell-level annotation 一个候选标签。</span>
  </article>
  <article>
    <strong>免疫细胞数据</strong>
    <span>许多公开模型对 immune cell atlas 比较友好，但仍需 marker 验证。</span>
  </article>
  <article>
    <strong>批量检查项目</strong>
    <span>多个样本或多个数据集做初筛时，可以快速发现异常样本和混合群。</span>
  </article>
  <article>
    <strong>参考映射辅助</strong>
    <span>适合和手工 marker、Seurat/Azimuth、SingleR 等结果互相校验。</span>
  </article>
</div>

## 资料来源

- [CellTypist documentation](https://celltypist.readthedocs.io/)
- [CellTypist models](https://www.celltypist.org/models)
- [CellTypist GitHub](https://github.com/Teichlab/celltypist)

