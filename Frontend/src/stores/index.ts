// src/store.js
import { createStore } from 'vuex';

const store = createStore({
  state: {
    apiUrl: import.meta.env.VUE_APP_API_URL || 'http://127.0.0.1:8000/api', // API 地址
    isLoggedIn: false,
  },
  mutations: {
    setApiUrl(state: { apiUrl: string; }, url: string) {
      state.apiUrl = url;
    },
    setLoginState(state: { isLoggedIn: any; }, status: any){
      state.isLoggedIn = status
    }
  },
  actions: {
    // 其他 actions...
  },
  getters: {
    apiUrl: (state: { apiUrl: any; }) => state.apiUrl,
    isLoggedIn: (state: { isLoggedIn: any; })=>state.isLoggedIn,
  },
});

export default store;
