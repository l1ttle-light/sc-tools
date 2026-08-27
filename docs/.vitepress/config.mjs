export default {
  lang: 'zh-CN',
  title: 'Single Cell Notes',
  description: '单细胞研究工具与分析路径知识库',
  base: process.env.BASE_PATH || '/',
  cleanUrls: false,
  lastUpdated: true,
  themeConfig: {
    logo: '/brand-mark.svg',
    siteTitle: 'Single Cell Notes',
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '没有结果',
                resetButtonTitle: '清空搜索',
                backButtonTitle: '关闭搜索',
                displayDetails: '显示详情',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭'
                }
              }
            }
          }
        }
      }
    },
    nav: [
      { text: '首页', link: '/' },
      {
        text: '研究主题',
        items: [
          { text: '生物学知识', link: '/biology/' },
          { text: '单细胞相关工具', link: '/tools/' },
          { text: '算法详解', link: '/algorithms/' },
          { text: '实战模拟', link: '/practice/' }
        ]
      },
      { text: '参考资料', link: '/references/' }
    ],
    sidebar: {
      '/tools/anndata/': [
        {
          text: 'AnnData 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/anndata/' },
            { text: '对象结构与读写', link: '/tools/anndata/object-structure-io' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/scanpy/': [
        {
          text: 'Scanpy 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/scanpy/' },
            { text: '环境与数据结构', link: '/tools/scanpy/setup-anndata' },
            { text: '质控与预处理', link: '/tools/scanpy/qc-preprocessing' },
            { text: '降维、聚类与注释', link: '/tools/scanpy/clustering-annotation' },
            { text: '经验与排坑', link: '/tools/scanpy/practical-notes' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/seurat/': [
        {
          text: 'Seurat 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/seurat/' },
            { text: 'PBMC 标准流程', link: '/tools/seurat/pbmc-workflow' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/scvi-tools/': [
        {
          text: 'scvi-tools 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/scvi-tools/' },
            { text: '整合与潜空间', link: '/tools/scvi-tools/integration-latent-space' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/celltypist/': [
        {
          text: 'CellTypist 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/celltypist/' },
            { text: '自动注释流程', link: '/tools/celltypist/annotation-workflow' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/squidpy/': [
        {
          text: 'Squidpy 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/squidpy/' },
            { text: '空间邻域与图分析', link: '/tools/squidpy/spatial-neighborhood' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/infercnv/': [
        {
          text: 'inferCNV 教程',
          collapsed: false,
          items: [
            { text: '教程导读', link: '/tools/infercnv/' },
            { text: 'CNV 推断流程', link: '/tools/infercnv/cnv-workflow' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/biology/': [
        {
          text: '生物学知识',
          collapsed: false,
          items: [
            { text: '知识总览', link: '/biology/' },
            { text: '中心法则与组学层级', link: '/biology/central-dogma-omics' },
            { text: '测序方法与技术原理', link: '/biology/sequencing-principles' },
            { text: '常见细胞类型', link: '/biology/common-cell-types' },
            { text: '免疫系统与微环境', link: '/biology/immunology-microenvironment' },
            { text: 'Janeway 免疫学学习图谱', link: '/biology/immunology-roadmap' },
            { text: '固有免疫', link: '/biology/innate-immunity' },
            { text: '抗原识别与抗原提呈', link: '/biology/antigen-recognition-presentation' },
            { text: '淋巴细胞发育与活化', link: '/biology/lymphocyte-development-activation' },
            { text: '适应性免疫应答', link: '/biology/adaptive-effector-immunity' },
            { text: '黏膜免疫、疾病与治疗', link: '/biology/mucosal-disease-immunotherapy' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/algorithms/': [
        {
          text: '算法详解',
          collapsed: false,
          items: [
            { text: '板块说明', link: '/algorithms/' },
            { text: 'Harmony', link: '/algorithms/harmony/' },
            { text: 'scVI', link: '/algorithms/scvi/' },
            { text: '算法解读模板', link: '/algorithms/template/' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/practice/': [
        {
          text: '实战模拟',
          collapsed: false,
          items: [
            { text: '实战总览', link: '/practice/' },
            { text: 'raw matrix 到报告', link: '/practice/raw-matrix-to-report' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '算法详解', link: '/algorithms/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/tools/': [
        {
          text: '单细胞相关工具',
          collapsed: false,
          items: [
            { text: '工具总览', link: '/tools/' },
            { text: 'AnnData 教程', link: '/tools/anndata/' },
            { text: 'Scanpy 教程', link: '/tools/scanpy/' },
            { text: 'Seurat 教程', link: '/tools/seurat/' },
            { text: 'scvi-tools 教程', link: '/tools/scvi-tools/' },
            { text: 'CellTypist 教程', link: '/tools/celltypist/' },
            { text: 'Squidpy 教程', link: '/tools/squidpy/' },
            { text: 'inferCNV 教程', link: '/tools/infercnv/' },
            { text: '常用工具清单', link: '/tools/common-tools/' }
          ]
        },
        {
          text: '站点入口',
          collapsed: true,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '算法详解', link: '/algorithms/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/references/': [
        {
          text: '站点入口',
          collapsed: false,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '算法详解', link: '/algorithms/' },
            { text: '实战模拟', link: '/practice/' },
            { text: '参考资料', link: '/references/' }
          ]
        }
      ],
      '/': [
        {
          text: '开始',
          collapsed: false,
          items: [
            { text: '首页', link: '/' },
            { text: '生物学知识', link: '/biology/' },
            { text: '单细胞相关工具', link: '/tools/' },
            { text: '算法详解', link: '/algorithms/' },
            { text: '实战模拟', link: '/practice/' }
          ]
        }
      ]
    },
    outline: {
      level: [2, 3],
      label: '本页目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最后更新'
    },
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '返回顶部'
  }
}
