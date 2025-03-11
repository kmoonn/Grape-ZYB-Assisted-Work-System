const config = {
    // 应用信息
    app: {
      name: import.meta.env.VITE_APP_TITLE,
      env: import.meta.env.VITE_APP_ENV,
      baseUrl: import.meta.env.VITE_APP_BASE_URL,
    },
    
    // API配置
    api: {
      baseUrl: import.meta.env.VITE_APP_API_URL,
      timeout: 10000,
      withCredentials: true
    },
    
    // 其他配置
    settings: {
      // 是否显示设置抽屉
      showSettings: import.meta.env.VITE_APP_ENV !== 'production',
      // 是否固定头部
      fixedHeader: true,
      // 是否显示标签栏
      showTagsView: true,
      // 是否显示侧边栏 Logo
      sidebarLogo: true,
    }
  }
  
  export default config