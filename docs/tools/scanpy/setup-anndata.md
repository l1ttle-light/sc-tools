# 环境与 AnnData

Scanpy 的第一关不是聚类，而是理解数据被放在哪里。只要 AnnData 的结构熟了，后面的 QC、降维、聚类和注释都会变得可追踪。

## 安装

官方推荐使用独立环境安装。项目分析中建议固定环境文件，至少记录 Python、Scanpy、AnnData、NumPy、SciPy、pandas、matplotlib 的版本。

```bash
conda create -n scverse python=3.11
conda activate scverse
pip install scanpy
```

## 读取 10x 数据

```python
import scanpy as sc

adata = sc.read_10x_mtx(
    "data/filtered_gene_bc_matrices/hg19",
    var_names="gene_symbols",
    cache=True,
)
adata.var_names_make_unique()
```

`var_names_make_unique()` 很常见，因为不同基因 ID 可能映射到相同基因符号。真实项目里更建议同时保留基因 ID 和基因符号，避免后续标志基因对不上。

## AnnData 的几个关键位置

<div class="flow-strip">
  <span>X：表达矩阵</span>
  <span>obs：细胞元数据</span>
  <span>var：基因元数据</span>
  <span>layers：备用矩阵</span>
  <span>obsm：低维坐标</span>
  <span>varm：基因层面的矩阵</span>
  <span>uns：非结构化结果</span>
  <span>raw：常用原始快照</span>
</div>

## 最容易混淆的点

<div class="check-grid">
  <article>
    <strong>adata.X 会被多次改写</strong>
    <span>归一化、对数转换、标准化往往直接作用在 X 上。重要中间结果最好存入 layers 或 raw。</span>
  </article>
  <article>
    <strong>obs 是细胞表</strong>
    <span>样本编号、批次、聚类、细胞类型、QC 指标都应该能在 obs 里找到。</span>
  </article>
  <article>
    <strong>var 是基因表</strong>
    <span>线粒体基因标记、高变基因标记、均值和离散度会写入 var。</span>
  </article>
  <article>
    <strong>uns 保存分析结果</strong>
    <span>PCA 方差、标志基因排名、绘图颜色等经常出现在 uns。</span>
  </article>
</div>

## 自检问题

1. 为什么读取基因符号后还要让 var names 唯一？
2. `adata.obs` 和 `adata.var` 分别代表什么维度？
3. 什么情况下应该把原始计数放到 `layers["counts"]`？
4. 为什么真实项目里需要记录 Scanpy 和 AnnData 版本？
