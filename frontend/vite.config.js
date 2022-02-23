import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        vue()
    ],
    base: '/',
    publicDir: 'public',
    server: {
        host: 'dev.time.incv.net',
        port: 8080
    },
    css: {
        preprocessorOptions:
            {
                scss:
                    {
                        charset: false // 禁用 Charset 提醒
                    }
            }
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules/tdesign-vue-next')) {
                        return 'tdesign-vue-next'
                    }
                    if (id.includes('node_modules/echarts')) {
                        return 'echarts'
                    }
                }
            }
        },
        chunkSizeWarningLimit: 2000
    }
})
