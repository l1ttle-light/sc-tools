# 实战模拟

这一部分把教程内容落成一个真实项目模板。默认使用 Scanpy 内置的公开 PBMC3k 数据集，也可以切换成你自己的 10x `raw_feature_bc_matrix` 路径。目标是输出可复查、可复跑、可交付的结果：

<div class="flow-strip">
  <span>processed.h5ad</span>
  <span>QC report</span>
  <span>UMAP figures</span>
  <span>标志基因表</span>
  <span>analysis log</span>
  <span>parameters.yaml</span>
  <span>environment.yaml</span>
  <span>README</span>
</div>

<div class="lesson-feature">
  <span class="feature-index">P1</span>
  <div>
    <h2>从 raw_feature_bc_matrix 到最终报告</h2>
    <p>推荐以脚本化流程而不是手动笔记本为主线：笔记本用于探索，脚本用于复现，报告用于沟通。</p>
    <a href="/practice/raw-matrix-to-report">进入实战模板</a>
  </div>
</div>

## 为什么这么设计

<div class="check-grid">
  <article>
    <strong>目录结构先行</strong>
    <span>项目一开始就分清 raw、interim、processed、figures、tables 和 reports，后续不会到处找文件。</span>
  </article>
  <article>
    <strong>参数外置</strong>
    <span>QC 阈值、HVG 参数、PCA 维度、聚类 resolution 都写进配置文件，结果才可追踪。</span>
  </article>
  <article>
    <strong>输出物明确</strong>
    <span>每一步应该产出什么文件提前定义，便于检查失败位置。</span>
  </article>
  <article>
    <strong>报告可复查</strong>
    <span>QC 图、过滤前后数量、标志基因表和 UMAP 统一进入报告。</span>
  </article>
</div>

## 本地模板位置

项目根目录已经补好一套可运行骨架：

```text
config/
  parameters.yaml
  samples.tsv
scripts/
  00_check_inputs.py
  01_create_h5ad.py
  02_qc_filter.py
  03_normalize_hvg.py
  04_pca_neighbors_umap.py
  05_markers_annotation.py
  06_export_report_assets.py
  run_pbmc_pipeline.sh
environment.yml
```

运行方式：

```bash
conda env create -f environment.yml
conda activate sc-tools-pbmc
bash scripts/run_pbmc_pipeline.sh
```
