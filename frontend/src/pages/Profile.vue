<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <!-- 左侧个人信息卡片 -->
      <el-col :span="8">
        <el-card class="profile-card">
          <div class="avatar-container">
            <el-avatar 
              :size="120" 
              :src="userInfo.avatar"
              @click="handleAvatarClick"
            />
            <input
              type="file"
              ref="avatarInput"
              style="display: none"
              accept="image/*"
              @change="handleAvatarChange"
            />
          </div>
          <h2 class="username">{{ userInfo.name }}</h2>
          <p class="user-role">{{ userInfo.role }}</p>
          <div class="user-stats">
            <div class="stat-item">
              <h4>工作天数</h4>
              <p>{{ userInfo.workDays }} 天</p>
            </div>
            <div class="stat-item">
              <h4>处理任务</h4>
              <p>{{ userInfo.taskCount }} 个</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息编辑表单 -->
      <el-col :span="16">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>个人信息</h3>
              <el-button type="primary" @click="saveChanges" :loading="saving">
                保存修改
              </el-button>
            </div>
          </template>

          <el-form 
            :model="userForm" 
            label-width="100px"
            :rules="rules"
            ref="formRef"
          >
            <el-form-item label="用户名" prop="username">
              <el-input v-model="userForm.username" />
            </el-form-item>

            <el-form-item label="真实姓名" prop="realName">
              <el-input v-model="userForm.realName" />
            </el-form-item>

            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="userForm.phone" />
            </el-form-item>

            <el-form-item label="邮箱地址" prop="email">
              <el-input v-model="userForm.email" />
            </el-form-item>

            <el-divider>修改密码</el-divider>

            <el-form-item label="原密码" prop="oldPassword">
              <el-input 
                v-model="userForm.oldPassword" 
                type="password" 
                show-password
              />
            </el-form-item>

            <el-form-item label="新密码" prop="newPassword">
              <el-input 
                v-model="userForm.newPassword" 
                type="password" 
                show-password
              />
            </el-form-item>

            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input 
                v-model="userForm.confirmPassword" 
                type="password" 
                show-password
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const avatarInput = ref(null)
const formRef = ref(null)
const saving = ref(false)

// 用户基本信息
const userInfo = reactive({
  avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
  name: '萄萄老师',
  role: '小学英语辅导老师',
  workDays: 0,
  taskCount: 0
})

// 表单数据
const userForm = reactive({
  username: 'taotao',
  realName: '萄萄老师',
  phone: '',
  email: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  newPassword: [
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { 
      validator: (rule, value, callback) => {
        if (value !== userForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 处理头像点击
const handleAvatarClick = () => {
  avatarInput.value.click()
}

// 处理头像变更
const handleAvatarChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    // 这里可以添加上传头像的逻辑
    const reader = new FileReader()
    reader.onload = (e) => {
      userInfo.avatar = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 保存修改
const saveChanges = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    saving.value = true
    
    // 这里添加保存到后端的逻辑
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟请求
    
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('验证失败:', error)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
  text-align: center;
  padding: 20px;
}

.avatar-container {
  margin-bottom: 20px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.avatar-container:hover {
  opacity: 0.8;
}

.username {
  margin: 10px 0;
  font-size: 24px;
  color: #333;
}

.user-role {
  color: #666;
  margin-bottom: 20px;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.stat-item h4 {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.stat-item p {
  margin: 5px 0 0;
  color: #333;
  font-size: 20px;
  font-weight: bold;
}

.info-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

.el-divider {
  margin: 24px 0;
}
</style> 