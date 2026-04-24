<template>
  <div class="common-tools-dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background:#e8f4ff;color:#409eff;">
              <el-icon :size="28"><Suitcase /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboard.total_count || 0 }}</div>
              <div class="stat-label">资源总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background:#f0f9eb;color:#67c23a;">
              <el-icon :size="28"><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ (dashboard.recommend || []).length }}</div>
              <div class="stat-label">推荐资源</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background:#fdf6ec;color:#e6a23c;">
              <el-icon :size="28"><FolderOpened /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ (dashboard.categories || []).length }}</div>
              <div class="stat-label">分类数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background:#f9f0ff;color:#722ed1;">
              <el-icon :size="28"><QuestionFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ (dashboard.faq || []).length }}</div>
              <div class="stat-label">FAQ条目</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类导航 -->
    <el-card shadow="hover" class="section-card">
      <template #header>
        <div class="section-header">
          <span>分类导航</span>
          <el-button text type="primary" @click="$router.push('/common-tools/list')">查看全部</el-button>
        </div>
      </template>
      <div class="category-grid">
        <div
          v-for="cat in dashboard.categories || []"
          :key="cat.id"
          class="category-item"
          @click="goCategory(cat)"
        >
          <el-icon :size="24"><component :is="cat.icon || 'FolderOpened'" /></el-icon>
          <div class="category-name">{{ cat.name }}</div>
          <div class="category-count">{{ cat.resource_count }}个资源</div>
        </div>
      </div>
    </el-card>

    <!-- 推荐工具 -->
    <el-card shadow="hover" class="section-card">
      <template #header>
        <div class="section-header">
          <span>推荐工具</span>
        </div>
      </template>
      <div class="resource-grid">
        <div
          v-for="item in dashboard.recommend || []"
          :key="item.id"
          class="resource-card"
          @click="handleClick(item)"
        >
          <div class="resource-icon">
            <el-icon :size="28"><component :is="item.icon || 'Suitcase'" /></el-icon>
          </div>
          <div class="resource-info">
            <div class="resource-name">
              {{ item.name }}
              <el-tag v-if="item.is_top" type="danger" size="small">置顶</el-tag>
            </div>
            <div class="resource-desc">{{ item.short_desc || '暂无描述' }}</div>
          </div>
          <div class="resource-meta">
            <el-tag size="small" type="info">{{ item.type_display }}</el-tag>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 热门工具 -->
    <el-card shadow="hover" class="section-card">
      <template #header>
        <div class="section-header">
          <span>热门工具</span>
        </div>
      </template>
      <div class="resource-grid">
        <div
          v-for="item in dashboard.hot || []"
          :key="item.id"
          class="resource-card"
          @click="handleClick(item)"
        >
          <div class="resource-icon hot-icon">
            <el-icon :size="28"><component :is="item.icon || 'Suitcase'" /></el-icon>
          </div>
          <div class="resource-info">
            <div class="resource-name">{{ item.name }}</div>
            <div class="resource-desc">{{ item.short_desc || '暂无描述' }}</div>
          </div>
          <div class="resource-meta">
            <span class="access-count">{{ item.access_count }}次访问</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- FAQ入口 -->
    <el-card v-if="dashboard.faq && dashboard.faq.length" shadow="hover" class="section-card">
      <template #header>
        <div class="section-header">
          <span>常见问题</span>
        </div>
      </template>
      <div class="faq-list">
        <div
          v-for="item in dashboard.faq"
          :key="item.id"
          class="faq-item"
          @click="goDetail(item)"
        >
          <el-icon color="#e6a23c"><QuestionFilled /></el-icon>
          <span>{{ item.name }}</span>
          <el-icon class="faq-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getDashboard, recordAccess } from '@/api/common-tools'
import {
  Suitcase, Star, FolderOpened, QuestionFilled, ArrowRight
} from '@element-plus/icons-vue'

const router = useRouter()
const dashboard = ref({})

const loadDashboard = async () => {
  try {
    const res = await getDashboard()
    dashboard.value = res.data
  } catch (e) {
    console.error('加载首页数据失败', e)
  }
}

const handleClick = async (item) => {
  if (item.url && item.open_mode === '_blank') {
    window.open(item.url, '_blank')
    try { await recordAccess(item.id, { access_type: 'click' }) } catch {}
  } else {
    router.push(`/common-tools/detail/${item.id}`)
  }
}

const goDetail = (item) => {
  router.push(`/common-tools/detail/${item.id}`)
}

const goCategory = (cat) => {
  router.push({ path: '/common-tools/list', query: { category: cat.id } })
}

onMounted(loadDashboard)
</script>

<style scoped lang="scss">
.common-tools-dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-row {
  .stat-card {
    .stat-content {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .stat-icon {
      width: 56px; height: 56px;
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
    }
    .stat-info {
      .stat-value { font-size: 24px; font-weight: 700; color: #303133; }
      .stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
    }
  }
}

.section-card {
  .section-header {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 16px; font-weight: 600;
  }
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;

  .category-item {
    display: flex; flex-direction: column; align-items: center;
    padding: 16px 8px; border-radius: 8px; cursor: pointer;
    transition: background 0.2s;
    &:hover { background: #f5f7fa; }
    .category-name { margin-top: 8px; font-size: 14px; font-weight: 500; color: #303133; }
    .category-count { font-size: 12px; color: #909399; margin-top: 4px; }
  }
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;

  .resource-card {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; border-radius: 8px; border: 1px solid #ebeef5;
    cursor: pointer; transition: all 0.2s;
    &:hover { border-color: #409eff; box-shadow: 0 2px 8px rgba(64,158,255,0.1); }

    .resource-icon {
      width: 48px; height: 48px; border-radius: 10px;
      background: #e8f4ff; color: #409eff;
      display: flex; align-items: center; justify-content: center; flex-shrink: 0;
      &.hot-icon { background: #fdf6ec; color: #e6a23c; }
    }
    .resource-info {
      flex: 1; min-width: 0;
      .resource-name { font-size: 14px; font-weight: 500; color: #303133; display: flex; align-items: center; gap: 6px; }
      .resource-desc { font-size: 12px; color: #909399; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    }
    .resource-meta {
      flex-shrink: 0;
      .access-count { font-size: 12px; color: #909399; }
    }
  }
}

.faq-list {
  .faq-item {
    display: flex; align-items: center; gap: 8px;
    padding: 12px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer;
    &:last-child { border-bottom: none; }
    &:hover { color: #409eff; }
    span { flex: 1; font-size: 14px; }
    .faq-arrow { color: #c0c4cc; }
  }
}
</style>
