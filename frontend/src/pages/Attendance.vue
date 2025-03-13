<template>
  <div class="attendance-container">
    <el-card class="attendance-card">
      <template #header>
        <div class="card-header">
          <h2>缺勤统计</h2>
          <div class="header-actions">
            <el-button type="primary" @click="showAddDialog = true">添加记录</el-button>
            <el-button type="success" @click="exportToExcel">导出Excel</el-button>
            <el-button type="danger" @click="handleClearData">清空数据</el-button>
          </div>
        </div>
      </template>

      <!-- 日期筛选 -->
      <div class="filter-container">
        <el-date-picker
          v-model="filterDate"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
          @change="fetchAttendance"
        />
      </div>

      <!-- 考勤记录表格 -->
      <el-table :data="filteredAttendanceList" style="width: 100%">
        <el-table-column prop="date" label="日期" width="240" sortable
      :sort-method="sortDate" />
        <el-table-column prop="name" label="学生姓名" width="240" sortable/>
        <el-table-column prop="reason" label="缺勤原因" sortable/>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="danger" size="small" @click="deleteRecord(row)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加记录弹窗 -->
    <el-dialog v-model="showAddDialog" title="添加缺勤记录" width="30%">
      <el-form :model="newRecord" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker
            v-model="newRecord.date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <!-- 姓名：支持首字母匹配选择 -->
      <el-form-item label="姓名">
        <el-autocomplete
          v-model="newRecord.name"
          :fetch-suggestions="queryName"
          placeholder="请输入学生姓名"
          value-key="name"
          @select="handleNameSelect"
        />
      </el-form-item>

      <!-- 原因：支持下拉选择或手动输入 -->
      <el-form-item label="原因">
        <el-select
          v-model="newRecord.reason"
          filterable
          placeholder="请选择或输入缺勤原因"
        >
          <el-option
            v-for="reason in reasonOptions"
            :key="reason"
            :label="reason"
            :value="reason"
          />
        </el-select>
      </el-form-item>
    </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRecord">提交</el-button>
      </template>
    </el-dialog>

    <!-- 添加确认对话框 -->
    <el-dialog
      v-model="showClearConfirm"
      title="确认清空"
      width="30%"
    >
      <span>确定要清空所有考勤记录吗？此操作不可恢复！</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showClearConfirm = false">取消</el-button>
          <el-button type="danger" @click="clearData">确定清空</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import request from '@/utils/request'
import * as XLSX from 'xlsx'
import { pinyin } from 'pinyin-pro'
import { ElMessage } from 'element-plus'

// 声明响应式数据
const attendanceList = ref([])
const studentNames = ref([])
const showAddDialog = ref(false)
const filterDate = ref('')
const showClearConfirm = ref(false)

// 预设的缺勤原因选项
const reasonOptions = [
  '失联',
  '回放',
  '请假',
]

// 计算属性：根据日期筛选考勤记录
const filteredAttendanceList = computed(() => {
  if (!filterDate.value) {
    return attendanceList.value
  }
  return attendanceList.value.filter(record => record.date === filterDate.value)
})

// 姓名搜索建议
const queryName = (queryString, cb) => {
  if (!queryString) {
    cb(studentNames.value.map(name => ({ name })))
    return
  }

  const results = studentNames.value.filter(name => {
    // 全名匹配
    if (name.includes(queryString)) {
      return true
    }

    // 获取姓名的每个字的首字母
    const firstLetters = name.split('').map(char => {
      return pinyin(char, { pattern: 'first', toneType: 'none' })
    }).join('')

    // 全拼匹配
    const fullPinyin = pinyin(name, { toneType: 'none' }).replace(/\s/g, '')

    // 查询字符串转小写
    const query = queryString.toLowerCase()

    return firstLetters.includes(query) || fullPinyin.toLowerCase().includes(query)
  })

  cb(results.map(name => ({ name })))
}

// 姓名选择处理
const handleNameSelect = (item) => {
  newRecord.value.name = item.name
}

// 日期排序方法
const sortDate = (a, b) => {
  return new Date(a.date) - new Date(b.date)
}

// 导出Excel功能
const exportToExcel = () => {
  const data = attendanceList.value.map(({ date, name, reason }) => ({
    日期: date,
    姓名: name,
    原因: reason
  }))
  
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '考勤记录')
  XLSX.writeFile(wb, '考勤记录.xlsx')
}

// 获取学生姓名列表
const fetchStudentNames = async () => {
  try {
    const response = await request({
      url: '/api/student',
      method: 'get'
    })
    studentNames.value = Array.isArray(response) 
      ? response.map(student => student.name)
      : response
  } catch (error) {
    console.error('获取学生姓名失败:', error)
    ElMessage.error('获取学生名单失败')
  }
}

// 获取考勤记录
const fetchAttendance = async () => {
  try {
    const response = await request({
      url: '/api/attendance',
      method: 'get'
    })
    attendanceList.value = response.map((record) => ({
      ...record,
      date: record.date.split('T')[0]
    }))
  } catch (error) {
    console.error('获取考勤记录失败:', error)
  }
}

// 获取当前日期的函数
const getCurrentDate = () => {
  const date = new Date()
  return date.toISOString().split('T')[0]  // 返回 'YYYY-MM-DD' 格式
}

// 声明响应式数据时使用当前日期
const newRecord = ref({
  date: getCurrentDate(),  // 默认使用当前日期
  name: '',
  reason: '',
})

// 修改 submitRecord 方法中的重置逻辑
const submitRecord = async () => {
  if (!newRecord.value.date || !newRecord.value.name || !newRecord.value.reason) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    const response = await request({
      url: '/api/attendance',
      method: 'post',
      data: newRecord.value
    })
    attendanceList.value.push(response)
    showAddDialog.value = false
    // 重置时使用当前日期
    newRecord.value = { 
      date: getCurrentDate(),
      name: '', 
      reason: '', 
    }
    ElMessage.success('添加成功')
  } catch (error) {
    console.error('添加考勤记录失败:', error)
    ElMessage.error('添加失败')
  }
}

// 删除考勤记录
const deleteRecord = async (row) => {
  try {
    await request({
      url: `/api/attendance/${row.id}`,
      method: 'delete'
    })
    const index = attendanceList.value.indexOf(row)
    attendanceList.value.splice(index, 1)
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除考勤记录失败:', error)
    ElMessage.error('删除失败')
  }
}

// 处理清空数据按钮点击
const handleClearData = () => {
  showClearConfirm.value = true
}

// 清空数据的方法
const clearData = async () => {
  try {
    await request({
      url: '/api/attendance/clear',
      method: 'delete',
      headers: {}
    })
    
    // 清空本地数据
    attendanceList.value = []
    
    // 关闭确认对话框
    showClearConfirm.value = false
    
    // 显示成功消息
    ElMessage.success('数据已清空')
  } catch (error) {
    console.error('清空数据失败:', error)
    ElMessage.error('清空数据失败')
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchStudentNames(),
    fetchAttendance()
  ])
})
</script>

<style scoped>
.attendance-container {
  padding: 20px;
}

.attendance-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-container {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>