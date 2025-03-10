<template>
  <div class="deepseek-container">
    <el-card class="chat-card">
      <template #header>
        <div class="card-header">
          <h2>DeepSeek 助手</h2>
          <el-button type="primary" @click="clearChat">清空对话</el-button>
        </div>
      </template>

      <div class="chat-content" ref="chatContent">
        <div v-for="(msg, index) in chatMessages" :key="index" 
             :class="['message', msg.role === 'user' ? 'user-message' : 'ai-message']">
          <div class="message-content">{{ msg.content }}</div>
        </div>
      </div>

      <div class="input-area">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter.ctrl="sendMessage"
        />
        <el-button type="primary" @click="sendMessage" :loading="loading">
          发送
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const chatContent = ref(null)
const userInput = ref('')
const loading = ref(false)
const chatMessages = ref([
  { role: 'ai', content: '你好！我是 DeepSeek 助手，有什么可以帮你的吗？' }
])

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  // 添加用户消息
  chatMessages.value.push({
    role: 'user',
    content: userInput.value
  })
  
  loading.value = true
  try {
    // 这里添加与后端的通信逻辑
    const response = '这是一个模拟的 AI 回复'
    chatMessages.value.push({
      role: 'ai',
      content: response
    })
  } catch (error) {
    console.error('Error:', error)
  } finally {
    loading.value = false
    userInput.value = ''
    scrollToBottom()
  }
}

const clearChat = () => {
  chatMessages.value = [{
    role: 'ai',
    content: '你好！我是 DeepSeek 助手，有什么可以帮你的吗？'
  }]
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContent.value) {
    chatContent.value.scrollTop = chatContent.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.deepseek-container {
  padding: 20px;
  height: calc(100vh - 100px);
}

.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 20px;
  max-width: 80%;
}

.user-message {
  margin-left: auto;
  text-align: right;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  display: inline-block;
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #f4f4f5;
}

.user-message .message-content {
  background-color: #95c2f3;
  color: white;
}

.input-area {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.input-area .el-input {
  flex: 1;
}
</style> 