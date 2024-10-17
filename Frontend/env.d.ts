/// <reference types="vite/client" />
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 声明环境变量的类型
declare global {
  interface ImportMetaEnv {
    VUE_APP_API_URL: string
  }
}
