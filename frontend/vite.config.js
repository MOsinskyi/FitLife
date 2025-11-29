import {fileURLToPath, URL} from 'node:url'

import vueDevTools from 'vite-plugin-vue-devtools'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from 'bootstrap-vue-next/resolvers'

export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
        Components({
            resolvers: [BootstrapVueNextResolver()],
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
})
