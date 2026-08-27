# Seurat 教程

Seurat 是 R 生态中最常用的单细胞分析框架之一。官方教程以 PBMC 数据为入口，展示从读取 10x 数据、创建 Seurat 对象、QC、归一化、特征选择、PCA、邻居图、聚类、UMAP 到标志基因的标准流程。

如果 Scanpy 是 Python/scverse 主线，Seurat 就是 R 生态主线。许多公开数据、论文补充代码和湿实验团队仍大量使用 Seurat。因此学习 Seurat 的价值不仅在于会跑 R 代码，也在于能读懂他人的分析对象和中间结果。

<div class="path-grid">
  <a href="/tools/seurat/pbmc-workflow">
    <strong>PBMC 标准流程</strong>
    <span>参考官方 PBMC 教程，整理 CreateSeuratObject、QC、NormalizeData、PCA、UMAP、细胞群和标志基因。</span>
  </a>
  <a href="/tools/scanpy/">
    <strong>与 Scanpy 对照</strong>
    <span>把 Seurat 对象和 AnnData 对照起来，理解元数据、降维结果、assay 和 layer。</span>
  </a>
  <a href="/tools/common-tools/">
    <strong>后续工具</strong>
    <span>细胞注释、空间组学、CNV 推断和通路活性分析可以接在 Seurat 或 Scanpy 后面。</span>
  </a>
  <a href="/references/">
    <strong>参考资料</strong>
    <span>查看 Seurat 官方教程和单细胞最佳实践资料。</span>
  </a>
</div>

## 实践判断

<div class="doc-callout important">
  <strong>Seurat 的对象版本很重要</strong>
  <p>Seurat v5 引入 layer 概念后，旧教程和旧对象的字段习惯可能不同。复现论文代码时，先记录 Seurat 版本、Assay 类型和数据所在 layer。</p>
</div>

## 资料来源

- [Seurat official website](https://satijalab.org/seurat/)
- [Seurat PBMC 3K guided tutorial](https://satijalab.org/seurat/articles/pbmc3k_tutorial)
- [Seurat essential commands](https://satijalab.org/seurat/articles/essential_commands)
