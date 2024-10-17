<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">Register</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="registerForm.email"
            placeholder="Enter Email"
            required
            @input="validateEmail"
          />
          <p v-if="registerForm.emailError" class="error-message">{{ registerForm.emailError }}</p>
        </div>
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="registerForm.username"
            placeholder="Enter Username"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="registerForm.password"
            @input="validatePassword"
            placeholder="Set password"
            required
          />
          <p v-if="registerForm.passwordValidationMessage" class="error-message">
            {{ registerForm.passwordValidationMessage }}
          </p>
        </div>
        <div class="form-group">
          <label for="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            v-model="registerForm.confirmPassword"
            placeholder="Repeat password"
            @input="checkPasswords"
            required
          />
          <p v-if="registerForm.passwordError" class="error-message">
            {{ registerForm.passwordError }}
          </p>
        </div>
        <p v-if="registerForm.errorMessage" class="error-message">
          {{ registerForm.errorMessage }}
        </p>
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="!!registerForm.passwordError || !!registerForm.emailError"
        >
          Register
        </button>
        <div class="extra-options">
          <router-link :to="{ name: 'login' }" class="btn"
            >Already have an account? Back to Login</router-link
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const router = useRouter()
const store = useStore()

const apiUrl = store.getters.apiUrl

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  passwordValidationMessage: '',
  passwordError: '',
  errorMessage: '',
  emailError: ''
})

const handleRegister = () => {
  if (registerForm.value.passwordError || registerForm.value.emailError) {
    return
  }

  axios
    .post(`${apiUrl}/user/register/`, {
      username: registerForm.value.username,
      password: registerForm.value.password,
      email: registerForm.value.email
    })
    .then((response) => {
      console.log(response.data)
      router.push({ name: 'login' })
    })
    .catch((error) => {
      if (error.response) {
        console.log(error)
        switch (error.response.status) {
          case 400:
            registerForm.value.errorMessage = 'Register failed, please check your input'
            break
          case 409:
            registerForm.value.errorMessage = 'Phone Number or Email has been registered'
            break
          default:
            registerForm.value.errorMessage = 'Register page error'
        }
      }
    })
}

const validateEmail = () => {
  const email = registerForm.value.email
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // 简单的邮箱格式验证
  registerForm.value.emailError = emailPattern.test(email) ? '' : 'Incorrect Email format'
}

const validatePassword = () => {
  const password = registerForm.value.password
  const hasMinimumLength = password.length >= 10
  const hasDigit = /\d/.test(password)
  const hasLowerCase = /[a-z]/.test(password)
  const hasUpperCase = /[A-Z]/.test(password)
  const hasSpecialCharacter = /[!@#$%^&*(),.?":{}|_<>]/.test(password) // 修正特殊字符验证

  if (!hasMinimumLength) {
    registerForm.value.passwordValidationMessage = 'Password should at least be 10 characters'
  } else if (!hasDigit) {
    registerForm.value.passwordValidationMessage = 'Password must contain at least 1 number'
  } else if (!hasLowerCase) {
    registerForm.value.passwordValidationMessage = 'Password must contain at least 1 lowercase'
  } else if (!hasUpperCase) {
    registerForm.value.passwordValidationMessage = 'Password must contain at least 1 capital'
  } else if (!hasSpecialCharacter) {
    registerForm.value.passwordValidationMessage =
      'Password must contain at least 1 special character'
  } else {
    registerForm.value.passwordValidationMessage = ''
  }
}

const checkPasswords = () => {
  if (registerForm.value.password && registerForm.value.confirmPassword) {
    if (registerForm.value.password !== registerForm.value.confirmPassword) {
      registerForm.value.passwordError = 'Password mismatch'
    } else {
      registerForm.value.passwordError = ''
    }
  }
}
</script>

<style scoped>
/* 与登录界面相同的样式 */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #4a90e2, #50b3ff);
  /* 蓝色渐变背景 */
}

.register-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

.register-title {
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}

.register-form {
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
  border-color: #4a90e2;
  /* 聚焦时的蓝色边框 */
  outline: none;
}

.btn {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4a90e2;
  /* 蓝色按钮 */
  color: white;
}

.btn-primary:hover {
  background-color: #357abd;
  /* 悬停时更深的蓝色 */
}

.extra-options {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.extra-options a {
  font-size: 14px;
  color: #4a90e2;
  /* 蓝色链接 */
  text-decoration: none;
  transition: color 0.3s;
}

.extra-options a:hover {
  color: #357abd;
  /* 悬停时更深的蓝色 */
}

.error-message {
  color: red;
}
</style>
