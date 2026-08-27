# 经验与排坑

这一页记录一些实践里比代码更重要的判断。它们不是替代官方教程，而是帮助你知道什么时候该停下来检查。

## 常见风险

<div class="check-grid">
  <article>
    <strong>照抄 QC 阈值</strong>
    <span>不同组织、平台、消化条件和测序深度差异很大。阈值必须回到样本分布。</span>
  </article>
  <article>
    <strong>过度过滤</strong>
    <span>过滤太狠会删掉真实稀有细胞或压力状态细胞，后续再漂亮也可能偏。</span>
  </article>
  <article>
    <strong>忽略批次</strong>
    <span>如果 UMAP 主要按样本分开，先别急着解释细胞类型，回头看批次和实验设计。</span>
  </article>
  <article>
    <strong>只看 UMAP</strong>
    <span>UMAP 是可视化，不是统计检验。结论要回到标志基因、差异分析和样本层面。</span>
  </article>
</div>

## 推荐的项目记录

```python
import scanpy as sc

sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, frameon=False)

adata.uns["analysis_notes"] = {
    "qc_strategy": "thresholds chosen per-sample after violin/scatter inspection",
    "normalization": "normalize_total target_sum=1e4 followed by log1p",
    "neighbors": {"n_neighbors": 10, "n_pcs": 40},
    "clustering": {"method": "leiden", "resolution": 1.0},
}

adata.write_h5ad("results/pbmc_scanpy_processed.h5ad")
```

## 做结果汇报时要说清楚

<div class="flow-strip">
  <span>数据来源和样本数</span>
  <span>过滤前后细胞数</span>
  <span>QC 阈值依据</span>
  <span>归一化方法</span>
  <span>HVG 数量</span>
  <span>PCA 与邻居参数</span>
  <span>聚类分辨率</span>
  <span>细胞注释证据</span>
</div>

## 何时查官方文档

当你开始调整参数、改数据结构或接入新函数时，优先查官方 API 和教程。博客适合补经验，但版本差异很常见，尤其是 AnnData、Scanpy 和 scverse 生态的对象结构。
