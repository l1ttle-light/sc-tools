# 淋巴细胞发育与活化

适应性免疫的能力来自一个看似矛盾的过程：先通过 V(D)J recombination 制造大量随机受体，再通过发育选择和外周调控清除危险的自身反应性克隆。这个过程决定了 T/B cell repertoire 的广度，也决定了免疫耐受的底线 [1]。

## 受体库如何产生

<div class="flow-strip">
  <span>造血干细胞</span>
  <span>淋巴祖细胞</span>
  <span>V(D)J 重排</span>
  <span>受体表达测试</span>
  <span>阳性选择</span>
  <span>阴性选择</span>
  <span>外周成熟</span>
  <span>抗原激活</span>
</div>

| 机制 | 发生对象 | 作用 | 分析提示 |
|---|---|---|---|
| V(D)J recombination | BCR heavy/light chain, TCR alpha/beta/gamma/delta | 产生受体多样性。 | VDJ-seq 可连接 clonotype 与转录状态。 |
| junctional diversity | 重排连接处核苷酸增减 | 主要扩展 CDR3 多样性。 | CDR3 是 clonotype 分析核心区域。 |
| allelic exclusion | B cells and T cells | 让单个细胞主要表达一个特异性受体。 | 双重受体或 ambient contamination 需要谨慎判断。 |
| class switch recombination | activated B cells | 改变 antibody isotype，不改变抗原特异性。 | `IGHM`, `IGHD`, `IGHG`, `IGHA`, `AICDA`。 |

## B cell 发育

B cell 在骨髓中完成早期发育：重链重排、pre-BCR 检查、轻链重排、自身反应性检查，然后进入外周继续成熟。单细胞中常见状态包括 immature B, naive B, memory B, germinal center B, plasmablast, plasma cell。

| 状态 | 常见 marker | 功能解释 |
|---|---|---|
| naive B cell | `MS4A1`, `CD79A`, `CD79B`, `IGHD`, `IGHM` | 未充分经历抗原驱动分化。 |
| germinal center B | `BCL6`, `AICDA`, `MKI67` | 体细胞高频突变、选择和亲和力成熟。 |
| memory B cell | `CD27`, switched `IGHG`/`IGHA` | 再次应答更快，常有类别转换。 |
| plasma cell | `MZB1`, `XBP1`, `JCHAIN`, `SDC1` | 大量分泌抗体。 |

## T cell 发育

T cell 起源于骨髓，但关键发育发生在胸腺。Notch signaling 推动 T lineage commitment；pre-TCR 检查 beta chain；阳性选择保留能识别 self-MHC 的细胞；阴性选择清除高亲和识别自身抗原的细胞。部分自身反应性细胞会进入 Treg 或 innate-like T cell fate。

<div class="doc-callout important">
  <strong>选择不是越强越好</strong>
  <p>TCR 信号太弱，细胞无法通过阳性选择；太强，可能触发阴性选择或 Treg fate。免疫系统是在识别能力和自身耐受之间找平衡。</p>
</div>

## TCR/BCR 信号和共刺激

| 模块 | 关键分子 | 作用 | 单细胞解释 |
|---|---|---|---|
| TCR signal | `CD3D/E/G`, `LCK`, `ZAP70`, `LAT` | 抗原识别后启动胞内级联。 | `FOS`, `JUN`, `NR4A1`, `IL2RA` 可提示近期激活。 |
| BCR signal | `CD79A/B`, `SYK`, `BLNK` | 抗原结合后促进 B cell activation。 | 与 antigen uptake、Tfh help、class switching 联合解释。 |
| costimulation | CD28, CD40, ICOS | 提供完全激活信号。 | T cell priming、T-B interaction、Tfh response。 |
| coinhibition | CTLA-4, PD-1, phosphatase recruitment | 限制过强免疫反应。 | exhaustion、Treg function、checkpoint therapy response。 |

## 自检问题

1. 为什么 V(D)J recombination 必须配套中枢和外周耐受？
2. 阳性选择和阴性选择分别筛选什么？
3. CD28、CTLA-4 和 PD-1 在免疫调控中有什么差异？
4. 单细胞 TCR clonotype 扩增一定代表抗原特异性吗？

## 参考资料

[1] Murphy, K. & Weaver, C. *Janeway's Immunobiology*. 9th ed. Garland Science (2017). 中文版：《詹韦免疫生物学：原书第九版》，科学出版社，2022。
