<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="loginForm.email"
            placeholder="Enter Email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            placeholder="Enter Password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
        <p v-if="loginForm.errorMessage" class="error-message">{{ loginForm.errorMessage }}</p>
        <div class="extra-options">
          <router-link :to="{ name: 'register' }" class="btn">Register</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

const loginForm = ref({
  email: '',
  password: '',
  errorMessage: ''
})

const apiUrl = store.getters.apiUrl

const login = () => {
  axios
    .post(`${apiUrl}/user/login/`, {
      email: loginForm.value.email,
      password: loginForm.value.password
    })
    .then((response) => {
      // login success
      const token = response.data.access
      // store.commit('setToken', token);
      localStorage.setItem('token', token) // 存储到 localStorage
      router.push('/')
    })
    .catch((error) => {
      // 错误处理
      if (error.response) {
        switch (error.response.status) {
          case 401:
            loginForm.value.errorMessage = 'Email or Password error'
            break
          default:
            loginForm.value.errorMessage = 'Login page error'
        }
      }
    })
}
const logout = () => {
  localStorage.removeItem('token') // 清除 token
  store.commit('clearToken') // 清空 Vuex 中的 token
  // 其他退出处理
}
</script>

<style scoped>
/* 整体容器样式 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  /* background: linear-gradient(135deg, #74ebd5, #acb6e5); */
  background: linear-gradient(135deg, #3c89e1, #7bc4fc);
  /* 蓝色渐变背景 */
  /* overflow: hidden !important; */
}

/* 登录卡片样式 */
.login-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

/* 标题样式 */
.login-title {
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}

/* 表单样式 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.form-group label {
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  /* border-color: #74ebd5; */
  border-color: #4a90e2;
  /* 聚焦时的蓝色边框 */
  outline: none;
}

/* 按钮样式 */
.btn {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-primary {
  /* background-color: #74ebd5; */
  background-color: #4a90e2;
  /* 蓝色按钮 */
  color: white;
}

.btn-primary:hover {
  /* background-color: #5cc6b4; */
  background-color: #357abd;
  /* 悬停时更深的蓝色 */
}

/* 额外选项样式 */
.extra-options {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.extra-options a {
  font-size: 14px;
  /* color: #74ebd5; */
  color: #4a90e2;
  /* 蓝色链接 */
  text-decoration: none;
  transition: color 0.3s;
}

.extra-options a:hover {
  /* color: #5cc6b4; */
  color: #357abd;
  /* 悬停时更深的蓝色 */
}

.error-message {
  color: red;
}
</style>
