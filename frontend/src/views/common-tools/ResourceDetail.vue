<template>
  <div class="resource-detail-page" v-loading="loading">
    <template v-if="resource">
      <el-card shadow="hover">
        <div class="detail-header">
          <div class="header-left">
            <div class="resource-icon">
              <el-icon :size="32"><component :is="resource.icon || 'Suitcase'" /></el-icon>
            </div>
            <div>
              <h2>
                {{ resource.name }}
                <el-tag v-if="resource.is_top" type="danger" size="small">置顶</el-tag>
                <el-tag v-if="resource.is_recommend" type="warning" size="small">推荐</el-tag>
              </h2>
              <p class="short-desc">{{ resource.short_desc }}</p>
            </div>
          </div>
          <div class="header-right">
            <el-button v-if="resource.url" type="primary" @click="openLink">
              <el-icon><Link /></el-icon> 访问链接
            </el-button>
            <el-button @click="$router.back()">返回</el-button>
          </div>
        </div>
      </el-card>

      <el-row :gutter="16" style="margin-top: 16px;">
        <el-col :span="16">
          <!-- 使用说明/内容 -->
          <el-card shadow="hover">
            <template #header><span style="font-weight:600;">使用说明</span></template>
            <div class="content-body" v-html="renderedContent"></div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <!-- 基本信息 -->
          <el-card shadow="hover">
            <template #header><span style="font-weight:600;">基本信息</span></template>
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="资源类型">{{ resource.type_display }}</el-descriptions-item>
              <el-descriptions-item label="分类">{{ resource.category_name || '-' }}</el-descriptions-item>
              <el-descriptions-item label="环境类型">{{ resource.env_type_display || '-' }}</el-descriptions-item>
              <el-descriptions-item label="可见范围">{{ resource.visibility_type_display }}</el-descriptions-item>
              <el-descriptions-item label="打开方式">{{ resource.open_mode_display }}</el-descriptions-item>
              <el-descriptions-item label="负责人">{{ resource.owner_name || '-' }}</el-descriptions-item>
              <el-descriptions-item label="联系方式">{{ resource.owner_contact || '-' }}</el-descriptions-item>
              <el-descriptions-item label="访问次数">{{ resource.access_count }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ resource.updated_at?.slice(0, 19).replace('T', ' ') }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 标签 -->
          <el-card shadow="hover" style="margin-top: 12px;">
            <template #header><span style="font-weight:600;">标签</span></template>
            <div>
              <el-tag
                v-for="tag in resource.tags_info || []"
                :key="tag.id" size="default"
                :color="tag.color" style="color:#fff;margin:4px;"
              >{{ tag.name }}</el-tag>
              <span v-if="!resource.tags_info?.length" style="color:#909399;">暂无标签</span>
            </div>
          </el-card>

          <!-- 访问地址 -->
          <el-card v-if="resource.url" shadow="hover" style="margin-top: 12px;">
            <template #header><span style="font-weight:600;">访问地址</span></template>
            <el-link type="primary" :href="resource.url" target="_blank">{{ resource.url }}</el-link>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getResourceDetail, recordAccess } from '@/api/common-tools'
import { Suitcase, Link } from '@element-plus/icons-vue'

const route = useRoute()
const resource = ref(null)
const loading = ref(false)

const renderedContent = computed(() => {
  if (!resource.value?.content) return '<p style="color:#909399;">暂无详细说明</p>'
  // 简易 Markdown 表格和标题渲染
  let text = resource.value.content
  text = text.replace(/^### (.+)$/gm, '<h4>$1</h4>')
  text = text.replace(/^## (.+)$/gm, '<h3>$1</h3>')
  text = text.replace(/^# (.+)$/gm, '<h2>$1</h2>')
  text = text.replace(/\n\n/g, '</p><p>')
  text = text.replace(/\n/g, '<br>')
  text = text.replace(/\|(.+)\|/g, (match) => {
    const cells = match.split('|').filter(c => c.trim())
    if (cells.every(c => c.trim().match(/^[-]+$/))) return ''
    return '<tr>' + cells.map(c => `<td style="border:1px solid #ebeef5;padding:6px 10px;">${c.trim()}</td>`).join('') + '</tr>'
  })
  if (text.includes('<tr>')) {
    text = '<table style="border-collapse:collapse;width:100%;">' + text + '</table>'
  }
  return '<p>' + text + '</p>'
})

const loadDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const res = await getResourceDetail(id)
    resource.value = res.data
    // 记录查看
    try { await recordAccess(id, { access_type: 'view' }) } catch {}
  } catch (e) {
    console.error('加载详情失败', e)
  } finally {
    loading.value = false
  }
}

const openLink = async () => {
  if (resource.value?.url) {
    window.open(resource.value.url, '_blank')
    try { await recordAccess(resource.value.id, { access_type: 'click' }) } catch {}
  }
}

onMounted(loadDetail)
</script>

<style scoped lang="scss">
.resource-detail-page {
  display: flex; flex-direction: column; gap: 0;
}

.detail-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  .header-left {
    display: flex; gap: 16px;
    .resource-icon {
      width: 64px; height: 64px; border-radius: 12px;
      background: #e8f4ff; color: #409eff;
      display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    h2 { font-size: 20px; font-weight: 600; color: #303133; display: flex; align-items: center; gap: 8px; margin: 0; }
    .short-desc { color: #909399; font-size: 14px; margin-top: 6px; }
  }
  .header-right { display: flex; gap: 8px; flex-shrink: 0; }
}

.content-body {
  line-height: 1.8; color: #303133; font-size: 14px;
  :deep(table) { margin: 12px 0; }
  :deep(h3) { margin: 16px 0 8px; font-size: 16px; }
  :deep(h4) { margin: 12px 0 6px; font-size: 14px; }
}
</style>
