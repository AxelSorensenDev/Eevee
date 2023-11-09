import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/Eevee/',
  plugins: [vue(),VitePWA({registerType: 'prompt', manifest: {
    "icons": [
      {
        "src": "icons/Eevee_app_icon.png",
        "sizes": "512x512",
        "type": "image/png"
      }
    ]
  }})],
  
})
