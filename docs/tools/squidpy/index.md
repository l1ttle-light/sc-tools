# Squidpy 教程

Squidpy 是 scverse 生态中的空间组学分析工具，常用于空间转录组数据的空间邻域、图结构、共定位、空间自相关、配体-受体和图像特征分析。它通常与 Scanpy/AnnData 配合使用：Scanpy 处理表达矩阵，Squidpy 处理空间坐标、组织图像和空间图。

空间分析的关键不是把 UMAP 换成组织图片，而是把“细胞状态在哪里”和“哪些细胞彼此相邻”纳入解释。

<div class="path-grid">
  <a href="/tools/squidpy/spatial-neighborhood">
    <strong>空间邻域与图分析</strong>
    <span>构建空间图，计算邻域富集和空间自相关。</span>
  </a>
  <a href="/biology/sequencing-principles">
    <strong>空间测序原理</strong>
    <span>回到空间转录组平台差异，理解分辨率、捕获效率和坐标含义。</span>
  </a>
  <a href="/tools/anndata/">
    <strong>AnnData 空间字段</strong>
    <span>理解 obsm["spatial"]、uns["spatial"] 和图像元数据如何保存。</span>
  </a>
  <a href="/references/">
    <strong>参考资料</strong>
    <span>查看 Squidpy 官方教程和空间组学实践资料。</span>
  </a>
</div>

## 适合回答的问题

<div class="check-grid">
  <article>
    <strong>哪些细胞类型相邻</strong>
    <span>邻域富集用于判断细胞类型配对是否比随机情况更常相邻。</span>
  </article>
  <article>
    <strong>哪些基因有空间模式</strong>
    <span>Moran's I 等空间自相关指标可用于寻找空间变异基因。</span>
  </article>
  <article>
    <strong>组织区域是否有结构</strong>
    <span>把组织学图像、点位坐标、细胞群和表达放在一起解释。</span>
  </article>
  <article>
    <strong>细胞通讯是否有空间支持</strong>
    <span>配体-受体结果若有空间邻近证据，解释会更稳。</span>
  </article>
</div>

## 资料来源

- [Squidpy documentation](https://squidpy.readthedocs.io/)
- [Squidpy tutorials](https://squidpy.readthedocs.io/en/stable/notebooks/tutorials/index.html)
- [scverse spatial ecosystem](https://scverse.org/)
