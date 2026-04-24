<template>
  <div class="common-tools-container">
    <!-- 页面头部 -->
    <el-card class="header-card">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Suitcase /></el-icon>
          工具导航
        </h1>
        <p class="page-subtitle">快速查找和使用常用工具资源</p>
        <div class="header-actions">
          <el-input
            v-model="searchText"
            placeholder="搜索工具名称、描述..."
            clearable
            prefix-icon="Search"
            class="search-input"
            @input="handleSearch"
          />
          <el-select v-model="filterCategory" placeholder="全部分类" clearable class="category-select">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
          <el-select v-model="filterType" placeholder="资源类型" clearable class="type-select" @change="handleFilterChange">
            <el-option v-for="t in typeOptions" :key="t.value" :label="t.label" :value="t.value" />
          </el-select>
        </div>
      </div>
    </el-card>

    <!-- 分类导航视图 -->
    <div v-loading="loading" class="category-view">
      <template v-if="groupedResources.length">
        <div
          v-for="group in groupedResources"
          :key="group.categoryId || 'none'"
          class="category-section"
        >
          <el-card class="category-card">
            <template #header>
              <div class="category-header">
                <el-icon class="category-icon" :style="{ color: getCategoryColor(group.categoryId) }">
                  <component :is="group.icon || 'FolderOpened'" />
                </el-icon>
                <span class="category-title">{{ group.categoryName }}</span>
                <el-tag size="small">{{ group.tools.length }}个工具</el-tag>
              </div>
            </template>
            <div class="tools-grid">
              <div
                v-for="tool in group.tools"
                :key="tool.id"
                class="tool-item"
                @click="handleClick(tool)"
              >
                <div class="tool-icon">
                  <el-icon><component :is="tool.icon || 'Suitcase'" /></el-icon>
                </div>
                <div class="tool-info">
                  <h4 class="tool-name">
                    {{ tool.name }}
                    <el-tag v-if="tool.is_top" type="danger" size="small">置顶</el-tag>
                    <el-tag v-if="tool.is_recommend" type="warning" size="small">推荐</el-tag>
                  </h4>
                  <p class="tool-desc">{{ tool.short_desc || '暂无描述' }}</p>
                </div>
                <el-icon class="tool-arrow"><ArrowRight /></el-icon>
              </div>
            </div>
          </el-card>
        </div>
      </template>
      <el-empty v-else description="暂无匹配的工具" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getResourceList, getCategories, recordAccess } from '@/api/common-tools'
import { Suitcase, ArrowRight, FolderOpened } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const resources = ref([])
const categories = ref([])
const loading = ref(false)
const searchText = ref('')
const filterType = ref('')
const filterCategory = ref(null)

let searchTimer = null

const typeOptions = [
  { label: '工具链接', value: 'tool_link' },
  { label: '网站地址', value: 'website' },
  { label: '文档链接', value: 'doc_link' },
  { label: 'Mock平台', value: 'mock_platform' },
  { label: '环境地址', value: 'env_address' },
  { label: '备忘信息', value: 'memo' },
  { label: 'FAQ', value: 'faq' },
  { label: '其他', value: 'other' },
]

// 分类配色
const categoryColors = [
  '#409eff', '#67c23a', '#e6a23c', '#f56c6c',
  '#909399', '#722ed1', '#13c2c2', '#eb2f96',
]
const getCategoryColor = (categoryId) => {
  if (!categoryId) return '#909399'
  return categoryColors[categoryId % categoryColors.length]
}

// 按分类分组
const groupedResources = computed(() => {
  let filtered = resources.value

  // 前端搜索过滤
  if (searchText.value) {
    const kw = searchText.value.toLowerCase()
    filtered = filtered.filter(r =>
      (r.name || '').toLowerCase().includes(kw) ||
      (r.short_desc || '').toLowerCase().includes(kw) ||
      (r.content || '').toLowerCase().includes(kw)
    )
  }

  // 分类过滤
  if (filterCategory.value) {
    filtered = filtered.filter(r => r.category === filterCategory.value)
  }

  // 类型过滤
  if (filterType.value) {
    filtered = filtered.filter(r => r.type === filterType.value)
  }

  // 按分类分组
  const groupMap = new Map()
  const catMap = new Map()
  categories.value.forEach(c => catMap.set(c.id, c))

  // 先把分类中已有的按顺序排
  categories.value.forEach(cat => {
    const tools = filtered.filter(r => r.category === cat.id)
    if (tools.length) {
      groupMap.set(cat.id, {
        categoryId: cat.id,
        categoryName: cat.name,
        icon: cat.icon || 'FolderOpened',
        tools,
      })
    }
  })

  // 未分类的工具
  const uncategorized = filtered.filter(r => !r.category)
  if (uncategorized.length) {
    groupMap.set('none', {
      categoryId: null,
      categoryName: '未分类',
      icon: 'FolderOpened',
      tools: uncategorized,
    })
  }

  return Array.from(groupMap.values())
})

const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {}, 300)
}

const handleFilterChange = () => {}

const handleClick = async (tool) => {
  if (tool.url && tool.open_mode === '_blank') {
    window.open(tool.url, '_blank')
    try { await recordAccess(tool.id, { access_type: 'click' }) } catch {}
  } else {
    router.push(`/common-tools/detail/${tool.id}`)
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const [res, catRes] = await Promise.all([
      getResourceList({ page_size: 200, is_enabled: true }),
      getCategories(),
    ])
    resources.value = res.data.results || res.data
    categories.value = (catRes.data.results || catRes.data).filter(c => c.is_enabled !== false)
  } catch (e) {
    console.error('加载工具数据失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query.type) filterType.value = route.query.type
  if (route.query.category) filterCategory.value = Number(route.query.category)
  loadData()
})
</script>

<style scoped lang="scss">
.common-tools-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background: #f5f7fa;
}

.header-card {
  margin-bottom: 20px;

  .header-content {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .page-title {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0;

    .title-icon {
      font-size: 32px;
      color: #409eff;
    }
  }

  .page-subtitle {
    font-size: 16px;
    color: #7f8c8d;
    margin: 0;
  }

  .header-actions {
    display: flex;
    gap: 10px;

    .search-input {
      max-width: 400px;
    }

    .category-select {
      width: 150px;
    }

    .type-select {
      width: 150px;
    }
  }
}

.category-view {
  display: flex;
  flex-direction: column;
  gap: 20px;

  .category-section {
    .category-card {
      .category-header {
        display: flex;
        align-items: center;
        gap: 10px;

        .category-icon {
          font-size: 24px;
        }

        .category-title {
          flex: 1;
          font-size: 18px;
          font-weight: 600;
        }
      }
    }
  }

  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
    margin-top: 15px;
  }

  .tool-item {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 12px;

    &:hover {
      background: #fff;
      border-color: #409eff;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
      transform: translateY(-2px);
    }

    .tool-icon {
      width: 40px;
      height: 40px;
      background: #e6f7ff;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #409eff;
      font-size: 20px;
      flex-shrink: 0;
    }

    .tool-info {
      flex: 1;
      min-width: 0;

      .tool-name {
        font-size: 14px;
        font-weight: 600;
        margin: 0 0 5px 0;
        color: #2c3e50;
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .tool-desc {
        font-size: 12px;
        color: #7f8c8d;
        margin: 0;
        line-height: 1.4;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }

    .tool-arrow {
      color: #c0c4cc;
      transition: transform 0.3s;
      flex-shrink: 0;
    }

    &:hover .tool-arrow {
      transform: translateX(5px);
      color: #409eff;
    }
  }
}
</style>
