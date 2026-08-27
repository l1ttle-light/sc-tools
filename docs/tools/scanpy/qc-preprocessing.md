# 质控与预处理

质控不是为了把数据“洗干净”到好看，而是为了尽量保留真实生物信号，同时减少低质量细胞、空液滴、双细胞和技术噪声对结论的影响。

## 计算 QC 指标

```python
adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(
    adata,
    qc_vars=["mt"],
    percent_top=None,
    log1p=False,
    inplace=True,
)
```

常看的指标包括：

<div class="flow-strip">
  <span>n_genes_by_counts</span>
  <span>total_counts</span>
  <span>pct_counts_mt</span>
  <span>doublet_score</span>
</div>

<div class="doc-callout important">
  <strong>阈值应该从分布出发</strong>
  <p>官方教程会给出教学阈值，但真实项目中更稳的做法是按样本、组织和实验批次分别画 violin/scatter，再结合背景知识设定过滤逻辑。</p>
</div>

## 过滤低质量细胞和低表达基因

```python
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)

adata = adata[
    (adata.obs.n_genes_by_counts < 2500)
    & (adata.obs.pct_counts_mt < 5)
].copy()
```

`min_genes` 太低容易保留空液滴或破碎细胞；`max_genes` 太低可能误删真实的大细胞或高 RNA 含量细胞；线粒体比例高常提示细胞状态或质量问题，但在某些组织和处理条件下也可能有生物学含义。

## 双细胞检测

Scanpy 官方教程示例中会使用 Scrublet 思路进行双细胞检测。实践上建议把双细胞分数作为证据之一，而不是唯一判决。

```python
sc.pp.scrublet(adata)
```

<div class="doc-callout warning">
  <strong>不要把双细胞和低质量细胞混成一类</strong>
  <p>双细胞常表现为两个细胞类型的标志基因同时偏高；低质量细胞则常伴随低基因数、高线粒体比例或异常总计数。两者排查逻辑不同。</p>
</div>

## 归一化、log 转换和高变基因

```python
adata.layers["counts"] = adata.X.copy()

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(
    adata,
    min_mean=0.0125,
    max_mean=3,
    min_disp=0.5,
)
```

官方基础流程使用总计数归一化加 `log1p`，再选择高变基因。它适合入门和许多常规探索，但大队列、强批次、多样本整合时，可能要考虑更系统的归一化和整合策略。

## Scale 与回归

```python
sc.pp.regress_out(adata, ["total_counts", "pct_counts_mt"])
sc.pp.scale(adata, max_value=10)
```

回归掉总计数或线粒体比例在教程中常见，但不应无脑使用。因为这些技术指标有时和真实细胞状态相关，过度回归可能擦掉生物信号。

## 自检问题

1. 为什么 QC 阈值最好按样本分别检查？
2. `normalize_total` 和 `log1p` 分别解决什么问题？
3. 高变基因选择影响后续哪些步骤？
4. 为什么线粒体比例不能简单等同于“坏细胞比例”？
