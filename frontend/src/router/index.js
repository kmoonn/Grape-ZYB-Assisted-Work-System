import { createRouter, createWebHistory } from 'vue-router';
import Login from '../pages/Login.vue';
import Home from '../pages/Home.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [
      {
        path: 'attendance',
        name: 'Attendance',
        component: () => import('../pages/Attendance.vue')
      },
      {
        path: 'phrases',
        name: 'Phrases',
        component: () => import('../pages/Phrases.vue')
      },
      {
        path: 'deepseek',
        name: 'Deepseek',
        component: () => import('../pages/Deepseek.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../pages/Profile.vue')
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.path !== '/login' && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
