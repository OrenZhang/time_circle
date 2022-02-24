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
                    return 'index'
                }
            }
        },
        chunkSizeWarningLimit: 2000
    }
})
