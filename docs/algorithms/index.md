# 算法详解

这个板块用于系统拆解单细胞和生物信息学算法。等你提供具体文献后，每个算法会单独成页，按照统一模板整理：先读论文，再读 GitHub 仓库代码，必要时补充官方文档、issue、教程和复现实验记录。

## 解读目标

<div class="check-grid">
  <article>
    <strong>算法作用</strong>
    <span>回答它解决什么问题、适用什么数据、相比传统方法解决了什么痛点。</span>
  </article>
  <article>
    <strong>输入输出</strong>
    <span>精确到文件格式、矩阵维度、字段名、metadata 要求和输出结果类型。</span>
  </article>
  <article>
    <strong>模型结构</strong>
    <span>参考论文模型图，拆解 encoder, decoder, graph module, attention, loss, and inference head。</span>
  </article>
  <article>
    <strong>代码逻辑</strong>
    <span>阅读 GitHub 仓库，记录数据加载、模型定义、训练循环、推理入口和配置文件。</span>
  </article>
</div>

## 我会按这个流程处理文献

<div class="flow-strip">
  <span>确认论文任务</span>
  <span>提取输入输出</span>
  <span>定位 GitHub 仓库</span>
  <span>阅读 README 和 examples</span>
  <span>追踪 data loader</span>
  <span>拆解 model modules</span>
  <span>梳理 loss 和 training</span>
  <span>写成可复现说明</span>
</div>

## 页面模板

<div class="lesson-feature">
  <span class="feature-index">ALG</span>
  <div>
    <h2>算法解读模板</h2>
    <p>模板已经包含作用、输入输出、示意图、模型结构、代码仓库阅读记录、复现流程和常见误区。你给文献后，我会以它为骨架填充。</p>
    <a href="/algorithms/template/">查看模板</a>
  </div>
</div>

## 已整理算法

<div class="path-grid">
  <a href="/algorithms/harmony/">
    <strong>Harmony</strong>
    <span>从论文 Algorithm 1 到官方 R/C++ 实现，拆解 maximum diversity clustering 和 mixture-of-experts ridge correction。</span>
  </a>
  <a href="/algorithms/scvi/">
    <strong>scVI</strong>
    <span>拆解 VAE、ZINB/NB likelihood、library size、batch covariate、ELBO 和 scvi-tools 代码实现。</span>
  </a>
</div>

## 待填算法列表

后续每篇文献会继续在这里加入入口。建议每次给一篇论文或一组强相关论文，这样可以把论文、代码和复现逻辑读透。
