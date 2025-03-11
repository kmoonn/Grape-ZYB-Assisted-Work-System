import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  
  return defineConfig({
    plugins: [vue()],
    
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    
    // 开发服务器配置
    server: {
      host: '0.0.0.0',
      port: 3000,
      open: true,
      proxy: {
        [env.VITE_APP_API_BASE_URL]: {
          target: env.VITE_APP_API_URL,
          changeOrigin: true,
          rewrite: path => path.replace(new RegExp('^' + env.VITE_APP_API_BASE_URL), '')
        }
      },
      // 开发环境下的错误处理
      hmr: {
        overlay: true
      }
    },
    
    // 生产环境构建配置
    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      // 生产环境移除 console
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      // 构建后的文件分析
      reportCompressedSize: false,
      // 分块策略
      rollupOptions: {
        output: {
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
          manualChunks: {
            'element-plus': ['element-plus'],
            'vue-vendor': ['vue', 'vue-router']
          }
        }
      }
    }
  })
}