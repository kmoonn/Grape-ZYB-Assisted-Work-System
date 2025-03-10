<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <img src="../assets/logo.png" alt="logo" class="logo">
        <h2>萄萄作业帮工作辅助工具</h2>
      </div>
      
      <el-form :model="loginForm" class="login-form">
        <el-form-item>
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleLogin" class="login-button">
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        class="error-alert"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const errorMessage = ref('')
const loginForm = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/login', loginForm)
    if (response.data.success) {
      localStorage.setItem('token', response.data.access_token)
      await router.push('/home')
    }
  } catch (error) {
    errorMessage.value = '用户名或密码错误'
  }
}
</script>

<style scoped>
:root {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.login-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: fixed;  /* 添加这行 */
  top: 0;          /* 添加这行 */
  left: 0;         /* 添加这行 */
  overflow: hidden; /* 添加这行 */
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  max-height: 90vh;    /* 添加这行 */
  overflow-y: auto;    /* 添加这行，如果内容过多时可以滚动 */
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  border-radius: 50%;  /* 添加这行使logo变成圆形 */
  object-fit: cover;   /* 确保图片填充方式正确 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* 添加阴影效果 */
  border: 3px solid #fff;  /* 添加白色边框 */
  transition: transform 0.3s ease;  /* 添加过渡效果 */
}

.logo:hover {
  transform: scale(1.05);  /* 鼠标悬停时轻微放大效果 */
}

.login-header h2 {
  color: #333;
  font-size: 24px;
  margin: 0;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
  margin-top: 20px;
}

.error-alert {
  margin-top: 16px;
}

</style>
