<template>
  <div class="attendance-container">
    <el-card class="attendance-card">
      <template #header>
        <div class="card-header">
          <h2>缺勤统计</h2>
          <div class="header-actions">
            <el-button type="success" @click="exportToExcel">导出 Excel</el-button>
            <el-button type="primary" @click="showAddDialog = true">添加记录</el-button>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx'; // 导入 xlsx 库
import { pinyin } from 'pinyin-pro'; // 导入 pinyin-pro 库

// 将中文姓名转换为拼音首字母
const getInitials = (name) => {
  return pinyin(name, {
    pattern: 'first', // 只获取首字母
    toneType: 'none', // 不包含声调
  })
    .replace(/\s+/g, '') // 去除空格
    .toLowerCase(); // 转换为小写
};

// 获取当前日期并格式化为 YYYY-MM-DD
const getCurrentDate = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从 0 开始，需要 +1
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 将日期转换为周几
const getDayOfWeek = (date) => {
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const dayIndex = new Date(date).getDay(); // 获取周几的索引（0-6）
  return days[dayIndex]; // 返回对应的周几
};

// 按日期排序
const sortDate = (a, b) => {
  return new Date(a.date) - new Date(b.date);
};

// 考勤记录列表
const attendanceList = ref([]);
// 筛选日期
const filterDate = ref('');
// 是否显示添加记录弹窗
const showAddDialog = ref(false);
// 新记录表单数据
const newRecord = ref({
  date: getCurrentDate(), // 默认使用当前日期
  name: '',
  reason: '',
  status: '未处理',
});

// 学生姓名列表（从接口获取）
const studentNames = ref([]);

// 缺勤原因选项（示例数据）
const reasonOptions = ref(['病假', '事假', '迟到', '早退', '其他']);

// 获取学生姓名列表
const fetchStudentNames = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/student');
    studentNames.value = response.data;
  } catch (error) {
    console.error('获取学生姓名失败:', error);
  }
};

// 姓名自动补全查询
const queryName = (queryString, cb) => {
  console.log('用户输入:', queryString);
  const results = queryString
    ? studentNames.value.filter((item) => {
        const initials = getInitials(item.name);
        return initials.startsWith(queryString.toLowerCase());
      })
    : studentNames.value;
  console.log('匹配结果:', results);
  cb(results);
};

const handleNameSelect = (item) => {
  newRecord.value.name = item.name;
};

// 获取考勤记录
const fetchAttendance = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/attendance');
    attendanceList.value = response.data.map((record) => ({
      ...record,
      date: record.date.split('T')[0], // 确保日期格式为 YYYY-MM-DD
    }));
  } catch (error) {
    console.error('获取考勤记录失败:', error);
  }
};

// 添加考勤记录
const submitRecord = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/attendance', {
      ...newRecord.value,
      date: newRecord.value.date, // 直接使用已格式化的日期
    });
    attendanceList.value.push(response.data); // 将新记录添加到列表
    showAddDialog.value = false; // 关闭弹窗
    newRecord.value = { date: '', name: '', reason: '', status: '未处理' }; // 重置表单
  } catch (error) {
    console.error('添加考勤记录失败:', error);
  }
};

// 删除考勤记录
const deleteRecord = async (row) => {
  try {
    await axios.delete(`http://localhost:8000/api/attendance/${row.id}`);
    const index = attendanceList.value.indexOf(row);
    attendanceList.value.splice(index, 1); // 从列表中移除记录
  } catch (error) {
    console.error('删除考勤记录失败:', error);
  }
};

// 导出为 Excel
const exportToExcel = () => {
  // 定义表头
  const headers = ['日期', '学生姓名', '缺勤原因', '处理状态'];

  // 将数据转换为 Excel 需要的格式
  const data = attendanceList.value.map((record) => [
    record.date,
    record.name,
    record.reason,
    record.status,
  ]);

  // 创建工作簿
  const workbook = XLSX.utils.book_new();

  // 创建工作表
  const worksheet = XLSX.utils.aoa_to_sheet([headers, ...data]);

  // 将工作表添加到工作簿
  XLSX.utils.book_append_sheet(workbook, worksheet, '缺勤记录');

  // 生成文件名
  const currentDate = getCurrentDate(); // 获取当前日期
  const dayOfWeek = getDayOfWeek(currentDate); // 获取周几
  const fileName = `${currentDate}_${dayOfWeek}_缺勤记录.xlsx`; // 拼接文件名

  // 生成 Excel 文件并触发下载
  XLSX.writeFile(workbook, fileName);
};

// 根据筛选日期过滤考勤记录
const filteredAttendanceList = computed(() => {
  if (!filterDate.value) return attendanceList.value;
  return attendanceList.value.filter((record) => record.date === filterDate.value);
});

// 组件挂载时获取考勤记录
onMounted(() => {
  fetchAttendance();
  fetchStudentNames();
});
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
</style>