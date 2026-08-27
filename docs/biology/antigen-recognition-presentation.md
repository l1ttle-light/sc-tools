# 抗原识别与抗原提呈

适应性免疫的精细识别依赖两套受体逻辑：B 细胞受体（BCR）和抗体可以直接识别天然抗原表面；T 细胞受体（TCR）通常识别肽-MHC 复合物。抗原提呈则把细胞内外蛋白加工成 T 细胞能读懂的信号 [1]。

## BCR 和 TCR 的差异

| 维度 | BCR / 抗体 | TCR |
|---|---|---|
| 识别对象 | 天然蛋白、糖、脂质或复杂构象表面。 | 多数为 MHC 呈递的抗原肽。 |
| 抗原形式 | 可识别可溶或细胞表面抗原。 | 需要抗原提呈细胞（APC）或靶细胞表面的肽-MHC 复合物。 |
| 后续效应 | 分化为浆细胞、产生抗体、形成记忆 B 细胞。 | 分化为 CD4 辅助 T 细胞、CD8 细胞毒性 T 细胞、Treg 等效应群。 |
| 单细胞线索 | `MS4A1`, `CD79A`, `CD79B`, `IGH*`, `JCHAIN`。 | `CD3D`, `CD3E`, `TRAC`, `CD4`, `CD8A`, 克隆型。 |

## MHC-I 和 MHC-II

| 通路 | 抗原来源 | 表达细胞 | 识别细胞 | 关键意义 |
|---|---|---|---|---|
| MHC-I | 细胞质蛋白、病毒蛋白、肿瘤抗原 | 几乎所有有核细胞 | CD8 T 细胞 | 让 CD8 T 细胞监视细胞内部异常。 |
| MHC-II | 胞吞、吞噬、自噬来源的蛋白 | 专职抗原提呈细胞 | CD4 T 细胞 | 让 CD4 T 细胞感知外源病原和组织抗原。 |
| 交叉提呈 | 外源抗原进入 MHC-I 通路 | 树突细胞 | CD8 T 细胞 | 让树突细胞激活初始 CD8 T 细胞。 |
| 非经典提呈 | 脂质或微生物代谢物 | CD1、MR1 等 | NKT、MAIT 等 | 连接屏障组织、微生物群和快速 T 样应答。 |

## 抗原加工路线

<div class="flow-strip">
  <span>内源蛋白</span>
  <span>蛋白酶体切割</span>
  <span>TAP 转运入 ER</span>
  <span>MHC-I 装载</span>
  <span>外源蛋白</span>
  <span>内吞体/溶酶体降解</span>
  <span>MHC-II 肽交换</span>
  <span>CD4/CD8 T 细胞识别</span>
</div>

## 单细胞中的抗原提呈细胞判断

<div class="check-grid">
  <article>
    <strong>抗原呈递能力</strong>
    <span>看 `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `B2M`, `HLA-A/B/C` 等，不只看细胞类型名字。</span>
  </article>
  <article>
    <strong>成熟树突细胞</strong>
    <span>抗原摄取、迁移、共刺激和细胞因子程序共同决定 T 细胞启动能力。</span>
  </article>
  <article>
    <strong>B 细胞作为抗原提呈细胞</strong>
    <span>B 细胞可高效提呈其 BCR 捕获的抗原，尤其在 T-B 连锁识别中重要。</span>
  </article>
  <article>
    <strong>肿瘤微环境</strong>
    <span>MHC-I 降低、抗原提呈细胞缺失或共刺激不足都可能削弱 T 细胞介导的杀伤。</span>
  </article>
</div>

## 自检问题

1. 为什么 CD8 T 细胞通常读 MHC-I，而 CD4 T 细胞通常读 MHC-II？
2. 交叉提呈解决了什么免疫学问题？
3. BCR 识别抗原和 TCR 识别抗原的本质差异是什么？
4. 在单细胞数据中，为什么 HLA 高表达不一定意味着有效 T 细胞启动？

## 参考资料

[1] Murphy, K. & Weaver, C. *Janeway's Immunobiology*. 9th ed. Garland Science (2017). 中文版：《詹韦免疫生物学：原书第九版》，科学出版社，2022。
