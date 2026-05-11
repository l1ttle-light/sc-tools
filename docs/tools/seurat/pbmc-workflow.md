# PBMC 标准流程

这一页按 Seurat 官方 PBMC 3K tutorial 的逻辑组织。代码用 R，概念尽量和 Scanpy 对照。

## 读取数据与创建对象

```r
library(Seurat)

pbmc.data <- Read10X(data.dir = "data/raw/pbmc3k/filtered_gene_bc_matrices/hg19/")
pbmc <- CreateSeuratObject(
  counts = pbmc.data,
  project = "pbmc3k",
  min.cells = 3,
  min.features = 200
)
```

对应 Scanpy 里大致是 `sc.read_10x_mtx()` 加 AnnData 的 `obs` 和 `var` 元数据。

## QC 指标

```r
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

VlnPlot(pbmc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")

pbmc <- subset(pbmc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
```

<div class="doc-callout warning">
  <strong>不要直接照抄阈值</strong>
  <p>PBMC3K 的 <code>nFeature_RNA < 2500</code> 和 <code>percent.mt < 5</code> 是教学示例。真实项目应按 sample, tissue, chemistry, and sequencing depth 分开检查 QC 分布。</p>
</div>

## 归一化、高变基因和 scale

```r
pbmc <- NormalizeData(pbmc, normalization.method = "LogNormalize", scale.factor = 10000)
pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)

all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)
```

Scanpy 中对应 `normalize_total()`, `log1p()`, `highly_variable_genes()`, and `scale()`。

## PCA、neighbors、clusters、UMAP

```r
pbmc <- RunPCA(pbmc, features = VariableFeatures(object = pbmc))
pbmc <- FindNeighbors(pbmc, dims = 1:10)
pbmc <- FindClusters(pbmc, resolution = 0.5)
pbmc <- RunUMAP(pbmc, dims = 1:10)

DimPlot(pbmc, reduction = "umap")
```

Seurat 的 `FindNeighbors()` + `FindClusters()` 和 Scanpy 的 `pp.neighbors()` + `tl.leiden()` 在分析语义上相似：先建图，再在图上找社区。

## Marker gene

```r
cluster.markers <- FindAllMarkers(
  pbmc,
  only.pos = TRUE,
  min.pct = 0.25,
  logfc.threshold = 0.25
)
```

实践中不要只用 marker 表自动命名。更可靠的命名需要结合经典 marker、组织背景、样本分组、是否存在 doublet、是否是 cell cycle 或 stress 状态。

## Seurat object 和 AnnData 对照

<div class="check-grid">
  <article>
    <strong>counts/data/scale.data</strong>
    <span>大致对应 AnnData 中 counts layer, normalized/log X, and scaled matrix 的角色。</span>
  </article>
  <article>
    <strong>meta.data</strong>
    <span>对应 AnnData 的 obs，用来保存 sample, QC metrics, clusters, and cell type。</span>
  </article>
  <article>
    <strong>reductions</strong>
    <span>对应 AnnData 的 obsm/uns，保存 PCA, UMAP, and related loadings。</span>
  </article>
  <article>
    <strong>assays/layers</strong>
    <span>Seurat v5 里 layer 更重要，整合和多样本分析时要确认 active assay and layer。</span>
  </article>
</div>

## 自检问题

1. `nFeature_RNA`, `nCount_RNA`, and `percent.mt` 分别对应什么 QC 含义？
2. `FindVariableFeatures()` 会影响后续哪些步骤？
3. `resolution` 变大时 cluster 数会如何变化？
4. Seurat object 和 AnnData 互转时最容易丢哪些信息？

