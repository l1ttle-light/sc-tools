# 中心法则与组学层级

中心法则给单细胞研究一个最重要的坐标系：遗传信息从 DNA 传到 RNA，再通过翻译进入蛋白质层面，并被调控网络、表观遗传状态、细胞环境和代谢状态不断改写。Crick 在 1970 年对中心法则做过经典阐述，强调序列信息在核酸和蛋白之间的传递规则，而现代组学则把这个框架扩展成可测量的多层系统 [1]。

## 一句话地图

<div class="flow-strip">
  <span>基因组：有什么编码潜力</span>
  <span>表观组：哪些区域可被调控</span>
  <span>转录组：当前表达了什么</span>
  <span>蛋白组：真正执行什么功能</span>
  <span>代谢组：细胞状态的化学读出</span>
  <span>宏基因组：群落里有哪些生物</span>
  <span>空间组学：这些状态在哪里</span>
  <span>多组学：层与层如何耦合</span>
</div>

## 基因组

基因组回答的是“遗传信息和变异在哪里”。人类基因组计划的初始论文为后续高通量测序、变异解释和功能基因组学奠定了坐标系 [2]。在单细胞研究中，基因组层面常见问题包括拷贝数变异、克隆结构、体细胞突变和肿瘤演化。

<div class="doc-callout example">
  <strong>单细胞里的基因组问题</strong>
  <p>肿瘤样本中，如果某些 cluster 同时表现出异常 CNV 信号和特定转录状态，就要区分“细胞类型差异”和“恶性克隆差异”。</p>
</div>

## 转录组

转录组回答的是“此时此地哪些 RNA 被表达”。RNA-seq 的高通量测量框架在 2008-2009 年快速成熟，Wang、Gerstein 和 Snyder 的综述系统总结了 RNA-seq 如何用于转录本结构、表达量和可变剪接分析 [3]。

单细胞 RNA-seq 进一步把 bulk 平均信号拆到单细胞分辨率，但也带来 dropout、捕获效率、批次效应和解离偏倚。读 scRNA-seq 结果时要记住：表达量是细胞状态的观测，不是细胞身份的全部。

## 蛋白组

蛋白组回答的是“哪些分子真正承担结构、催化、信号和调控功能”。Aebersold 和 Mann 总结过现代质谱蛋白组学如何从大规模鉴定走向定量、互作和系统生物学解释 [4]。对单细胞研究而言，CITE-seq 等方法把表面蛋白和 RNA 同时测量，让免疫细胞注释更稳。

## 代谢组

代谢组更接近细胞状态的即时读出，常用于解释营养、缺氧、炎症、肿瘤代谢和免疫细胞功能转换。代谢物变化不总能从 mRNA 直接推断，因为酶活性、底物可用性和细胞环境都会介入调控。

## 宏基因组

宏基因组关注微生物群落的组成和功能潜力。Human Microbiome Project 展示了人体不同部位微生物群落的结构和个体差异，为疾病、免疫和代谢研究提供了群落层面的参照 [5]。如果研究肠道、皮肤、呼吸道或肿瘤微生物环境，宏基因组和单细胞宿主转录组可以形成互补。

## 多组学的关键问题

多组学不是把多个数据表简单拼起来，而是问层级之间如何耦合：染色质开放是否解释转录变化？RNA 是否对应蛋白变化？代谢通路是否支撑细胞状态？空间位置是否决定细胞互作？Nature Reviews Genetics 和 Nature Reviews Molecular Cell Biology 的综述都强调，单细胞与空间多组学正在把基因组、表观组、转录组、蛋白组和代谢组放到同一细胞或同一空间坐标中解释，但整合分析必须同时处理技术噪声、模态缺失、尺度差异和生物学先验 [6,7]。

## 自检问题

1. 为什么 RNA 高表达不一定代表蛋白高活性？
2. 基因组、转录组和蛋白组分别更适合回答什么问题？
3. 为什么单细胞 RNA-seq 不能单独证明细胞功能？
4. 多组学整合最常见的技术难点是什么？

## 参考文献

[1] Crick, F. Central dogma of molecular biology. *Nature* 227, 561-563 (1970). [Nature](https://www.nature.com/articles/227561a0)

[2] International Human Genome Sequencing Consortium. Initial sequencing and analysis of the human genome. *Nature* 409, 860-921 (2001). [Nature](https://www.nature.com/articles/35057062)

[3] Wang, Z., Gerstein, M. & Snyder, M. RNA-Seq: a revolutionary tool for transcriptomics. *Nature Reviews Genetics* 10, 57-63 (2009). [Nature Reviews Genetics](https://www.nature.com/articles/nrg2484)

[4] Aebersold, R. & Mann, M. Mass-spectrometric exploration of proteome structure and function. *Nature* 537, 347-355 (2016). [Nature](https://www.nature.com/articles/nature19949)

[5] Human Microbiome Project Consortium. Structure, function and diversity of the healthy human microbiome. *Nature* 486, 207-214 (2012). [Nature](https://www.nature.com/articles/nature11234)

[6] Thienpont, B. et al. Methods and applications for single-cell and spatial multi-omics. *Nature Reviews Genetics* 24, 494-515 (2023). [Nature Reviews Genetics](https://www.nature.com/articles/s41576-023-00580-2)

[7] Baysoy, A. et al. The technological landscape and applications of single-cell multi-omics. *Nature Reviews Molecular Cell Biology* (2023). [Nature Reviews Molecular Cell Biology](https://www.nature.com/articles/s41580-023-00615-w)
