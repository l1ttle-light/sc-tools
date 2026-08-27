# 空间邻域与图分析

Squidpy 的基本工作流是：读取空间 AnnData，确认坐标字段，构建空间图，然后计算邻域富集或空间自相关。

## 读取空间数据

```python
import scanpy as sc
import squidpy as sq

adata = sq.datasets.visium_hne_adata()
```

真实项目中，10x Visium 数据通常可以通过 Scanpy/Squidpy 读入，并把空间坐标存入 `adata.obsm["spatial"]`。

## 构建空间邻接图

```python
sq.gr.spatial_neighbors(
    adata,
    coord_type="grid",
)
```

`coord_type` 要和平台匹配。Visium 点位接近网格结构；更接近单细胞坐标的平台可能用通用坐标。构图策略会影响后续富集分析和空间统计。

## 邻域富集

```python
sq.gr.nhood_enrichment(adata, cluster_key="cluster")
sq.pl.nhood_enrichment(adata, cluster_key="cluster")
```

这个结果回答的是：某些细胞群配对是否比随机置换更常相邻。它不是直接证明配体-受体通讯，但能提供空间邻近证据。

## 空间自相关

```python
sq.gr.spatial_autocorr(
    adata,
    mode="moran",
    genes=["CXCL13", "MS4A1", "CD3D"],
)
```

Moran's I 可用于判断基因表达是否有空间聚集模式。实践中应结合组织切片、点位/细胞类型组成和测序深度检查。

<div class="doc-callout warning">
  <strong>空间分辨率决定解释边界</strong>
  <p>Visium 点位往往包含多个细胞，不能简单把一个点位等同于一个细胞。单细胞分辨率平台也会有捕获效率、分割和坐标误差。</p>
</div>

## 常见输出

<div class="check-grid">
  <article>
    <strong>空间图</strong>
    <span>通常保存在 obsp/uns 中，用于后续邻域和空间统计。</span>
  </article>
  <article>
    <strong>邻域富集</strong>
    <span>细胞群配对的空间相邻富集结果。</span>
  </article>
  <article>
    <strong>空间变异基因</strong>
    <span>具有空间自相关的基因或通路。</span>
  </article>
  <article>
    <strong>空间图</strong>
    <span>把细胞群、基因表达和组织学图像放回组织坐标。</span>
  </article>
</div>

## 自检问题

1. `adata.obsm["spatial"]` 里的坐标代表点位还是单细胞？
2. 空间图的邻居定义是否适合你的平台？
3. 邻域富集能否单独证明细胞间通讯？
4. 空间自相关高的基因是否可能由组织区域组成驱动？
