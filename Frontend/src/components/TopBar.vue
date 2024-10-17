<template>
  <el-header class="top-bar">
    <div class="logo" @click="goHome">A Toy Semantic Code Search Tool</div>
    <div class="search-container">
      <el-input
        placeholder="Search..."
        v-model="searchQuery"
        class="search-input"
        @keyup.enter="handleSearch"
        clearable
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>

      <div class="select-group" v-if="isSettingsOpen">
        <el-select
          v-model="selectedLanguages"
          multiple
          placeholder="Select Languages"
          @change="handleLanguageChange"
          class="language-select"
        >
          <el-option
            v-for="language in programmingLanguages"
            :key="language.value"
            :label="language.label"
            :value="language.value"
          />
        </el-select>

        <el-select v-model="selectedSort" placeholder="Sort By" class="sort-select">
          <el-option label="Most Popular" value="popular" />
          <el-option label="Newest" value="newest" />
        </el-select>
      </div>
    </div>
    <div class="setting-container">
      <el-icon class="large-icon" @click="handleSettings"><Setting /></el-icon>
    </div>
    <div class="user-container">
      <el-avatar :icon="UserFilled" @click="gotoMyView" style="cursor: pointer" />
      <!-- <div class="name">{{ 'Love' }}</div> -->
    </div>
  </el-header>

  <el-dialog title="Settings" v-model:visible="isSettingsOpen">
    <div class="select-group">
      <el-select
        v-model="selectedLanguages"
        multiple
        placeholder="Select Languages"
        @change="handleLanguageChange"
      >
        <el-option
          v-for="language in programmingLanguages"
          :key="language.value"
          :label="language.label"
          :value="language.value"
        />
      </el-select>

      <el-select v-model="selectedSort" placeholder="Sort By" class="sort-select">
        <el-option label="Most Popular" value="popular" />
        <el-option label="Newest" value="newest" />
      </el-select>
    </div>
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button @click="isSettingsOpen = false">Cancel</el-button>
        <el-button type="primary" @click="saveSettings">Save</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search, UserFilled, Setting } from '@element-plus/icons-vue'
import router from '@/router'

const searchQuery = ref<string>('')
const selectedLanguages = ref<string[]>([])
const selectedSort = ref<string>('popular')
const isSettingsOpen = ref<boolean>(false)

const programmingLanguages = [
  { value: 'javascript', label: 'JavaScript' },
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
  { value: 'csharp', label: 'C#' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
  { value: 'ruby', label: 'Ruby' },
  { value: 'php', label: 'PHP' },
  { value: 'go', label: 'Go' },
  { value: 'none', label: 'None' }
]

const handleLanguageChange = () => {
  if (selectedLanguages.value.includes('none')) {
    selectedLanguages.value = ['none'] // 只保留"none"选项
  }
}

const handleSearch = () => {
  if (searchQuery.value) {
    router.replace({
      name: 'searchResults',
      query: { q: searchQuery.value, languages: selectedLanguages.value, sort: selectedSort.value }
    });
  }
}

const handleSettings = () => {
  console.log('Settings list open')
  isSettingsOpen.value = !isSettingsOpen.value
}

const goHome = () => {
  console.log('goHome')
  router.push('/')
}

const gotoMyView = () => {
  console.log('gotoMyView')
}
</script>

<style scoped>
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  background: linear-gradient(135deg, #3182ce, #63b3ed);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: white;
  width: 100%;
  height: 70px;
  box-sizing: border-box;
}

.logo {
  font-size: 1.75rem;
  font-weight: bold;
  cursor: pointer;
  color: white;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.search-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-input {
  max-width: 48rem;
  width: 100%;
  border-radius: 24px;
  overflow: hidden;
  background-color: white;
}

.search-input .el-input__inner {
  padding: 0.8rem 1rem;
  border-radius: 24px;
  font-size: 1rem;
}

.el-button {
  background-color: #3182ce;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.el-button:hover {
  background-color: #2b6cb0;
}

.language-select {
  margin-left: 1rem;
  min-width: 150px;
}

.setting-container {
  margin-left: 1.5rem;
  width: 50px;
}

.large-icon {
  font-size: 2rem;
  cursor: pointer;
  transition:
    color 0.3s ease,
    transform 0.3s ease;
}

.large-icon:hover {
  color: #e2e8f0;
  transform: rotate(20deg);
}

.user-container {
  display: flex;
  align-items: center;
  margin-left: 1.5rem;
}

.name {
  margin-left: 1rem;
  font-size: 1.2rem;
  font-weight: 500;
  color: #e2e8f0;
}

.el-avatar {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.el-avatar:hover {
  transform: scale(1.1);
}

.select-group {
  display: flex;
  align-items: center;
  gap: 1rem; /* Add spacing between select elements */
}

.language-select,
.sort-select {
  min-width: 150px;
}
</style>
