<template>
  <div class="phrases-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="category-card">
          <template #header>
            <div class="card-header">
              <h3>话术分类</h3>
              <el-button type="primary" size="small" @click="addCategory">
                添加分类
              </el-button>
            </div>
          </template>
          
          <el-menu
            :default-active="activeCategory"
            @select="handleCategorySelect"
          >
            <el-menu-item v-for="category in categories" :key="category.id" :index="category.id">
              {{ category.name }}
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card class="phrases-card">
          <template #header>
            <div class="card-header">
              <h3>话术列表</h3>
              <el-button type="primary" size="small" @click="addPhrase">
                添加话术
              </el-button>
            </div>
          </template>
          
          <div class="phrases-list">
            <el-card v-for="phrase in phrases" :key="phrase.id" class="phrase-item">
              <div class="phrase-content">
                {{ phrase.content }}
              </div>
              <div class="phrase-actions">
                <el-button type="primary" size="small" @click="copyPhrase(phrase)">复制</el-button>
                <el-button type="danger" size="small" @click="deletePhrase(phrase)">删除</el-button>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeCategory = ref('1')
const categories = ref([
  { id: '1', name: '作业批改' },
  { id: '2', name: '学习建议' },
  { id: '3', name: '家长沟通' }
])

const phrases = ref([
  { id: '1', content: '作业完成得很好，继续保持！' },
  { id: '2', content: '建议多做课后练习，巩固知识点。' }
])

const handleCategorySelect = (index) => {
  activeCategory.value = index
  // 加载对应分类的话术
}

const addCategory = () => {
  // 添加分类逻辑
}

const addPhrase = () => {
  // 添加话术逻辑
}

const copyPhrase = (phrase) => {
  navigator.clipboard.writeText(phrase.content)
  ElMessage.success('复制成功')
}

const deletePhrase = (phrase) => {
  const index = phrases.value.indexOf(phrase)
  phrases.value.splice(index, 1)
}
</script>

<style scoped>
.phrases-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.category-card, .phrases-card {
  margin-bottom: 20px;
}

.phrases-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.phrase-item {
  margin-bottom: 10px;
}

.phrase-content {
  margin-bottom: 10px;
}

.phrase-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 