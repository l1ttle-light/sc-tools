# 免疫系统与微环境

免疫学是单细胞研究最常见、也最容易解释过度的场景之一。一个 T 细胞群不只是一个名字，它背后牵涉发育谱系、抗原刺激、组织定位、细胞互作、炎症环境和代谢状态。

## 免疫系统的两条主线

<div class="check-grid">
  <article>
    <strong>先天免疫</strong>
    <span>巨噬细胞、树突细胞、中性粒细胞、NK 细胞等快速响应病原体、损伤和炎症信号。</span>
  </article>
  <article>
    <strong>适应性免疫</strong>
    <span>T 细胞和 B 细胞通过抗原特异性受体形成更精细的识别、记忆和效应功能。</span>
  </article>
</div>

Janeway 和 Medzhitov 对先天免疫识别、模式识别受体和适应性免疫激活之间的关系做过奠基性阐述 [1]。读免疫单细胞数据时，可以把“细胞谱系”和“激活状态”分开看：谱系回答它是谁，状态回答它正在做什么。

## 免疫细胞速查

<div class="flow-strip">
  <span>T 细胞：杀伤、辅助、调节和记忆</span>
  <span>B 细胞：抗体、抗原呈递和浆细胞分化</span>
  <span>NK 细胞：天然杀伤和应激识别</span>
  <span>单核细胞：循环髓系前体与炎症响应</span>
  <span>巨噬细胞：吞噬、修复、抗原呈递</span>
  <span>树突细胞：抗原呈递和 T 细胞启动</span>
  <span>中性粒细胞：急性炎症和颗粒酶效应</span>
  <span>肥大细胞：过敏、屏障和组织炎症</span>
</div>

## 免疫微环境

微环境指细胞周围的组织生态：免疫细胞、基质细胞、内皮细胞、肿瘤细胞、细胞外基质、细胞因子、代谢条件和空间位置共同决定细胞状态。肿瘤免疫微环境尤其重要，因为免疫浸润、耗竭、抗原呈递、Treg、髓系抑制和空间排斥都会影响治疗响应。

Binnewies 等人在 *Nature Medicine* 综述中把肿瘤免疫微环境整理为动态生态系统，强调免疫细胞、肿瘤细胞和基质成分之间的互作 [2]。单细胞研究常用这个视角解释不同细胞群之间的配体-受体通讯、耗竭状态和炎症程序。

## T 细胞状态不要只靠一个标志基因

<div class="doc-callout warning">
  <strong>PDCD1 高不等于一句话“耗竭”</strong>
  <p>T 细胞耗竭需要结合多个抑制受体、效应分子、转录因子、克隆扩增、组织环境和功能证据。单个标志基因只能提示方向。</p>
</div>

## 单细胞免疫分析的解释路径

<div class="flow-strip">
  <span>先分谱系</span>
  <span>再看亚群</span>
  <span>检查激活/耗竭/干扰素状态</span>
  <span>结合样本和疾病分组</span>
  <span>看空间或组织来源</span>
  <span>用标志基因支撑命名</span>
  <span>保留不确定细胞</span>
  <span>回到功能验证</span>
</div>

## 深入阅读路线

<div class="path-grid">
  <a href="/biology/immunology-roadmap">
    <strong>Janeway 免疫学学习图谱</strong>
    <span>先建立免疫系统整体地图，再进入固有免疫、抗原识别、淋巴细胞发育和疾病免疫。</span>
  </a>
  <a href="/biology/innate-immunity">
    <strong>固有免疫</strong>
    <span>理解 PRR、补体、炎症、干扰素、NK 和 ILC，适合解释髓系与组织炎症状态。</span>
  </a>
  <a href="/biology/adaptive-effector-immunity">
    <strong>适应性免疫应答</strong>
    <span>理解 T/B 细胞如何被启动、分化、产生效应功能和形成记忆。</span>
  </a>
  <a href="/biology/mucosal-disease-immunotherapy">
    <strong>黏膜免疫、疾病与治疗</strong>
    <span>把免疫耐受、炎症性疾病、疫苗和肿瘤免疫治疗放回真实组织场景。</span>
  </a>
</div>

## 自检问题

1. 先天免疫和适应性免疫的主要差异是什么？
2. 为什么细胞类型和细胞状态要分开解释？
3. 肿瘤免疫微环境包含哪些非免疫成分？
4. 为什么单个标志基因不足以给 T 细胞状态下结论？

## 参考文献

[1] Janeway, C. A. Jr. & Medzhitov, R. Innate immune recognition. *Annual Review of Immunology* 20, 197-216 (2002). [Annual Reviews](https://www.annualreviews.org/doi/10.1146/annurev.immunol.20.083001.084359)

[2] Binnewies, M. et al. Understanding the tumor immune microenvironment (TIME) for effective therapy. *Nature Medicine* 24, 541-550 (2018). [Nature Medicine](https://www.nature.com/articles/s41591-018-0014-x)
