<script>
export default {
  name: "Home"
}
</script>

<template>
  <div class="home-container">
    <el-aside class="sidebar" width="220px">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="logo" class="logo">
        <h3>萄萄</h3>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="menu"
        background-color="transparent"
        text-color="#fff"
        active-text-color="#ffd04b"
        router
      >
        <el-menu-item index="/home/attendance">
          <el-icon><List /></el-icon>
          <span>缺勤统计</span>
        </el-menu-item>

        <el-menu-item index="/home/phrases">
          <el-icon><ChatDotRound /></el-icon>
          <span>常用话术</span>
        </el-menu-item>

        <el-menu-item index="/home/deepseek">
          <el-icon><Sunny /></el-icon>
          <span>DeepSeek</span>
        </el-menu-item>
      </el-menu>

      <!-- 底部用户信息 -->
      <div class="user-info">
        <el-dropdown>
          <span class="user-dropdown">
            <el-avatar :size="32" :src="userAvatar" />
            <span class="username">{{ username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleProfile">个人信息</el-dropdown-item>
              <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-aside>

    <!-- 主要内容区 -->
    <el-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {Calendar, List, ChatDotRound, Sunny} from '@element-plus/icons-vue'

const router = useRouter()
const activeMenu = ref('/home/')
const username = ref('我的')
const userAvatar = ref('https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png')

const handleProfile = () => {
  router.push('/home/profile')
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
  background-color: #f5f7fa;
}

.sidebar {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 8px rgba(0, 0, 0, 0.1);
}

.logo-container {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.logo-container h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.menu {
  flex: 1;
  border: none;
  margin-top: 20px;
}

.user-info {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.username {
  color: white;
  font-size: 14px;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

</style>