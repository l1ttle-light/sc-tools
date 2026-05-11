# inferCNV 教程

inferCNV 是常用于从单细胞 RNA-seq 表达矩阵中推断 large-scale copy number variation 的工具，特别常见于肿瘤单细胞分析。它通过基因在染色体上的位置，对表达信号按染色体区域平滑，比较目标细胞与参考正常细胞的表达偏移，从而推断疑似 CNV 模式。

它的核心用途不是精确替代 DNA CNV calling，而是帮助区分 malignant cells 和 non-malignant reference cells，或观察肿瘤亚克隆结构。结论应尽量与 WGS/WES、拷贝数实验或肿瘤 marker 互相验证。

<div class="path-grid">
  <a href="/tools/infercnv/cnv-workflow">
    <strong>CNV 推断流程</strong>
    <span>准备 counts matrix, cell annotation, gene order file, reference groups，并运行 inferCNV。</span>
  </a>
  <a href="/biology/central-dogma-omics">
    <strong>基因组与转录组关系</strong>
    <span>理解表达推断 CNV 的假设和局限。</span>
  </a>
  <a href="/tools/common-tools/">
    <strong>同类工具</strong>
    <span>CopyKAT, HoneyBADGER, CONICSmat 等也常用于肿瘤 CNV 推断。</span>
  </a>
  <a href="/references/">
    <strong>参考资料</strong>
    <span>查看 inferCNV 官方文档和肿瘤单细胞分析实践资料。</span>
  </a>
</div>

## 适合场景

<div class="check-grid">
  <article>
    <strong>肿瘤上皮细胞识别</strong>
    <span>比较 epithelial-like cells 和 immune/stromal reference cells，识别疑似恶性细胞。</span>
  </article>
  <article>
    <strong>肿瘤亚群结构</strong>
    <span>观察不同 cluster 是否共享 CNV pattern 或呈现亚克隆差异。</span>
  </article>
  <article>
    <strong>质量控制辅助</strong>
    <span>检查疑似 malignant cluster 是否有一致 chromosomal arm-level signal。</span>
  </article>
  <article>
    <strong>论文结果解释</strong>
    <span>许多肿瘤单细胞论文会用 inferCNV 图展示 malignant vs non-malignant。</span>
  </article>
</div>

## 资料来源

- [inferCNV documentation](https://github.com/broadinstitute/infercnv)
- [inferCNV wiki](https://github.com/broadinstitute/infercnv/wiki)
- [Trinity CTAT inferCNV page](https://github.com/broadinstitute/infercnv/wiki)

