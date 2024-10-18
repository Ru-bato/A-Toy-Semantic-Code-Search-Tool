<template>
  <div class="search-results-page">
    <el-header style="min-width: 100vw; padding: 0; margin: 0"><TopBar /></el-header>
    <!-- 标题 -->
    <el-row justify="center" class="title-row">
      <h2>Search Results</h2>
    </el-row>

    <!-- 搜索结果的5个部分 -->
    <el-row gutter="20" class="results-grid" style="margin-left: 20px">
      <!-- GitHub Code 结果展示 -->
      <el-col :span="12" :lg="12" :md="12" :sm="24">
        <el-card class="result-card" shadow="hover">
          <h3>GitHub Code Results</h3>
          <el-scrollbar class="result-scroll">
            <ul>
              <li v-for="item in githubCodeResults" :key="item.id">
                <a
                  :href="item.html_url"
                  target="_blank"
                  @click="(event) => handleLinkClick(item.name, item.html_url, event)"
                  >{{ item.name }}</a
                >
                <span
                  class="star"
                  :class="{
                    filled: favorites.find((fav) => fav.title === item.name && fav.isFavorite)
                  }"
                  @click="toggleFavorite(item.name, item.html_url)"
                >
                  ★
                </span>
              </li>
            </ul>
          </el-scrollbar>
        </el-card>
      </el-col>

      <!-- GitHub Repositories 结果展示 -->
      <el-col :span="12" :lg="12" :md="12" :sm="24">
        <el-card class="result-card" shadow="hover">
          <h3>GitHub Repository Results</h3>
          <el-scrollbar class="result-scroll">
            <ul>
              <li v-for="item in githubRepoResults" :key="item.id">
                <a
                  :href="item.html_url"
                  target="_blank"
                  @click="(event) => handleLinkClick(item.name, item.html_url, event)"
                  >{{ item.name }}</a
                >
                <span
                  class="star"
                  :class="{
                    filled: favorites.find((fav) => fav.title === item.name && fav.isFavorite)
                  }"
                  @click="toggleFavorite(item.name, item.html)"
                >
                  ★
                </span>
              </li>
            </ul>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>

    <el-row gutter="20" class="results-grid" style="margin-left: 20px">
      <!-- StackOverflow 结果展示 -->
      <el-col :span="12" :lg="12" :md="12" :sm="24">
        <el-card class="result-card" shadow="hover">
          <h3>StackOverflow Results</h3>
          <el-scrollbar class="result-scroll">
            <ul>
              <li v-for="item in stackoverflowResults" :key="item.question_id">
                <a
                  :href="item.link"
                  target="_blank"
                  @click="(event) => handleLinkClick(item.title, item.link, event)"
                  >{{ item.title }}</a
                >
                <span
                  class="star"
                  :class="{
                    filled: favorites.find((fav) => fav.title === item.title && fav.isFavorite)
                  }"
                  @click="toggleFavorite(item.title, item.link)"
                >
                  ★
                </span>
              </li>
            </ul>
          </el-scrollbar>
        </el-card>
      </el-col>

      <!-- ArXiv 结果展示 -->
      <el-col :span="12" :lg="12" :md="12" :sm="24">
        <el-card class="result-card" shadow="hover">
          <h3>Arxiv Results</h3>
          <el-scrollbar class="result-scroll">
            <ul>
              <li v-for="item in arxivResults" :key="item.id">
                <a
                  :href="item.link"
                  target="_blank"
                  @click="(event) => handleLinkClick(item.title, item.link, event)"
                  >{{ item.title }}</a
                >
                <span
                  class="star"
                  :class="{
                    filled: favorites.find((fav) => fav.title === item.title && fav.isFavorite)
                  }"
                  @click="toggleFavorite(item.title, item.link)"
                >
                  ★
                </span>
              </li>
            </ul>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>

    <el-row gutter="20" class="results-grid" style="margin-left: 20px">
      <!-- YouTube 结果展示 -->
      <el-col :span="24" :lg="24" :md="24" :sm="24">
        <el-card class="youtube-card" shadow="hover">
          <h3>YouTube Tutorials</h3>
          <el-scrollbar class="youtube-scroll">
            <div class="youtube-thumbnails">
              <div
                v-for="item in youtubeResults"
                :key="item.id.videoId || item.id.playlistId"
                class="youtube-video-container"
              >
                <a
                  :href="'https://www.youtube.com/watch?v=' + item.id.videoId || item.id.playlistId"
                  target="_blank"
                  @click="
                    (event) =>
                      handleLinkClick(
                        item.snippet.title,
                        'https://www.youtube.com/watch?v=' + item.id.videoId || item.id.playlistId,
                        event
                      )
                  "
                >
                  <img
                    :src="item.snippet.thumbnails.medium.url"
                    :alt="item.snippet.title"
                    class="youtube-thumbnail"
                  />
                  <div
                    class="youtube-video-title"
                    @click="
                      (event) =>
                        handleLinkClick(
                          item.snippet.title,
                          'https://www.youtube.com/watch?v=' + item.id.videoId ||
                            item.id.playlistId,
                          event
                        )
                    "
                  >
                    {{ item.snippet.title }}
                  </div>
                  <span
                    class="star"
                    :class="{
                      filled: favorites.find(
                        (fav) => fav.title === item.snippet.title && fav.isFavorite
                      )
                    }"
                    @click="toggleFavorite(item.snippet.title, item.snippet.thumbnails.medium.url)"
                  >
                    ★
                  </span>
                </a>
              </div>
            </div>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import axios from 'axios'
import router from '@/router'

const route = useRoute()
const store = useStore()
const githubCodeResults = ref([])
const githubRepoResults = ref([])
const stackoverflowResults = ref([])
const youtubeResults = ref([])
const arxivResults = ref([])
const token = localStorage.getItem('token')
if (token) {
  store.commit('setToken', token)
}
const favorites = ref<{ title: string; link: string; isFavorite: boolean }[]>([])

const searchQuery = ref(route.query.q || '')
const selectedLanguages = ref(
  Array.isArray(route.query.languages)
    ? route.query.languages
    : route.query.languages
      ? [route.query.languages]
      : []
)
const sortOption = ref(route.query.sort || 'popular') // 默认排序方式
const apiUrl = store.getters.apiUrl

const fetchSearchResults = async () => {
  if (!searchQuery.value.trim() && selectedLanguages.value.length === 0) {
    console.warn('No search query or languages selected.')
    return // 不发送请求
  }

  const languageParam =
    selectedLanguages.value.length > 0 && !selectedLanguages.value.includes('none')
      ? `&languages=${selectedLanguages.value.join(',')}`
      : ''
  console.log(
    `${apiUrl}/search/integrated_search?query=${searchQuery.value}${languageParam}&sort=${sortOption.value}`
  )
  const response = await fetch(
    `${apiUrl}/search/integrated_search?query=${searchQuery.value}${languageParam}&sort=${sortOption.value}`,
    {
      method: 'GET', // 默认为 GET，通常可以省略
      headers: {
        // 不添加任何自定义头部
      }
    }
  )

  const data = await response.json()

  githubCodeResults.value = data.github_code
  githubRepoResults.value = data.github_repositories
  stackoverflowResults.value = data.stackoverflow
  youtubeResults.value = data.youtube_tutorials
  arxivResults.value = data.arxiv_results.map(
    (item: { id: any; title: any; link: { [x: string]: any }[] }) => ({
      id: item.id,
      title: item.title,
      link: item.link[0]['@href'] // 使用方括号访问属性
    })
  )
  console.log('you', youtubeResults.value)
}

// 监听路由查询参数变化
watch(
  () => route.query,
  () => {
    searchQuery.value = route.query.q || ''
    selectedLanguages.value = Array.isArray(route.query.languages)
      ? route.query.languages
      : route.query.languages
        ? [route.query.languages]
        : []
    sortOption.value = route.query.sort || 'popular'
    fetchSearchResults()
  }
)

// 获取收藏夹
const fetchFavorites = async () => {
  try {
    const response = await axios.get(`${apiUrl}/user/favorites/`)
    favorites.value = response.data.map((fav: any) => ({
      title: fav.item_title,
      link: fav.item_link,
      isFavorite: true
    }))
  } catch (error) {
    console.error('Error fetching favorites:', error)
  }
}

// 收藏功能
const toggleFavorite = async (title: string, link: string) => {
  const existingFavorite = favorites.value.find((fav) => fav.title === title)
  if (existingFavorite) {
    // 取消收藏
    existingFavorite.isFavorite = false
    await deleteFavorite(title)
  } else {
    // 添加收藏
    favorites.value.push({ title, link, isFavorite: true })
    await addFavorite(title, link)
  }
}

const addFavorite = async (title: string, link: string) => {
  try {
    const headers = {
      Authorization: `Bearer ${token}`
    }
    await axios
      .post(
        `${apiUrl}/user/favorites/`,
        {
          item_title: title,
          item_link: link
        },
        { headers }
      )
      .catch((error) => {
        if (error.response.status === 401) {
          alert('Have not login yet')
          router.push({ name: 'login' })
        }
      })
  } catch (error) {
    console.error('Error adding to favorites:', error)
  }
}

const deleteFavorite = async (title: string) => {
  try {
    const headers = {
      Authorization: `Bearer ${token}`
    }
    await axios
      .delete(`${apiUrl}/user/favorites/${encodeURIComponent(title)}/`, { headers })
      .catch((error) => {
        if (error.response.status === 401) {
          alert('Have not login yet')
          router.push({ name: 'login' })
        }
      })
    console.log('Deleted from favorites:', title)
    // 更新本地 favorites 状态
  } catch (error) {
    console.error('Error deleting favorite:', error)
  }
}

const recordSearchHistory = async (title: string, link: string, event: any) => {
  try {
    const headers = {
      Authorization: `Bearer ${token}`
    }
    await axios.post(
      `${apiUrl}/user/search_records/`,
      {
        search_query: title,
        search_link: link
      },
      { headers }
    )
  } catch (error) {
    console.error('Error recording search history:', error)
  }
}

// 在链接点击时调用
const handleLinkClick = (title: string, link: string, event: any) => {
  recordSearchHistory(title, link, event)
}

onMounted(() => {
  fetchSearchResults()
})
</script>

<style scoped>
.search-results-page {
  min-width: 100vw;
  overflow-x: hidden !important;
  background-color: #f4f7fa; /* 页面背景色 */
}

.title-row {
  margin-top: 40px;
  margin-bottom: 20px;
  text-align: center;
}

h2 {
  font-size: 2.5rem;
  color: #333;
  font-weight: bold;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
  margin-left: 0;
}

@media (max-width: 768px) {
  .results-grid {
    grid-template-columns: 1fr; /* 小屏幕时占用100% */
  }
}

.result-card {
  border-radius: 15px;
  background-color: #ffffff;
  height: 300px; /* 固定高度 */
  min-width: 700px; /* 其他框的宽度 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  transition:
    transform 0.3s,
    box-shadow 0.3s; /* 动画效果 */
}

.result-card:hover {
  transform: translateY(-5px); /* 悬停上升效果 */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); /* 悬停时阴影变强 */
}

.youtube-card {
  border-radius: 15px;
  background-color: #ffffff;
  height: 400px; /* 固定高度 */
  min-width: 1460px; /* YouTube框的宽度是其他框的两倍 */
  width: 1460px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}

.youtube-card:hover {
  transform: translateY(-5px); /* 悬停上升效果 */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); /* 悬停时阴影变强 */
}

.result-scroll {
  max-height: 250px; /* 限制内容的最大高度 */
  overflow-y: auto; /* 允许滚动 */
}

.youtube-scroll {
  overflow-x: auto; /* 仅允许水平滚动 */
  overflow-y: auto; /* 隐藏垂直滚动 */
  white-space: nowrap; /* 使子元素横向排列 */
  max-height: 400px; /* 固定最大高度以避免上下滚动 */
  height: 400px;
}

.youtube-thumbnails {
  display: flex; /* 使用 Flexbox 进行水平排列 */
  align-items: flex-start; /* 顶部对齐 */
  overflow-x: auto; /* 允许横向滚动 */
}

.youtube-video-container {
  display: flex; /* 使视频图像和标题在同一行 */
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 水平居中 */
  margin-right: 10px; /* 视频之间的间距 */
}

.youtube-thumbnail {
  cursor: pointer; /* 鼠标悬停效果 */
  height: 180px; /* 固定高度 */
  width: auto; /* 宽度自适应 */
  transition: transform 0.2s; /* 添加平滑过渡效果 */
}

.youtube-thumbnail:hover {
  transform: scale(1.05); /* 悬停放大效果 */
}

.youtube-video-container a {
  background-color: transparent; /* 取消背景颜色变化 */
  text-decoration: none; /* 去掉下划线 */
}

.youtube-video-container a:hover {
  background-color: transparent; /* 确保在鼠标悬停时背景保持透明 */
}
.youtube-video-title {
  font-size: 1rem; /* 调整标题字体大小 */
  font-weight: bold; /* 加粗标题 */
  color: #007bff; /* 标题颜色 */
  margin-top: 5px; /* 标题与视频图像之间的间距 */
  max-width: 100%; /* 限制最大宽度为100% */
  overflow: hidden; /* 隐藏超出部分 */
  white-space: normal; /* 允许换行 */
  text-overflow: ellipsis; /* 超出部分显示省略号 */
  text-decoration: none; /* 去掉下划线 */
  transition: transform 0.2s; /* 添加平滑过渡效果 */
}

.youtube-video-title:hover {
  text-decoration: none; /* 鼠标悬停时去掉下划线 */
  transform: scale(1.05); /* 鼠标悬停时轻微放大 */
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #409eff; /* 修改标题颜色 */
  text-align: center; /* 标题居中 */
}

ul {
  padding-left: 0;
  list-style-type: none;
}

ul li {
  margin-bottom: 10px;
}

ul li a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s; /* 添加链接颜色过渡效果 */
}

ul li a:hover {
  color: #409eff; /* 悬停时颜色变化 */
}

.el-card {
  padding: 20px;
}

/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 10px; /* 垂直滚动条的宽度 */
  height: 10px; /* 水平滚动条的高度 */
}

::-webkit-scrollbar-track {
  background: #f4f7fa; /* 滚动条的轨道背景颜色 */
  border-radius: 10px; /* 轨道的圆角 */
}

::-webkit-scrollbar-thumb {
  background: #e3d4f2; /* 滚动条的颜色 */
  border-radius: 10px; /* 滚动条的圆角 */
}

::-webkit-scrollbar-thumb:hover {
  background: #d9aef3; /* 鼠标悬停时滚动条的颜色 */
}

/* Firefox */
.scrollable {
  scrollbar-width: thin; /* 滚动条的宽度（Firefox） */
  scrollbar-color: #409eff #f4f7fa; /* 滚动条的颜色和轨道颜色（Firefox） */
}

.star {
  color: transparent; /* 初始透明 */
  position: relative;
  display: inline-block;
  margin-left: 8px;
  font-size: 1.2rem; /* 星号大小 */
  cursor: pointer;
  transition:
    transform 0.3s ease,
    color 0.3s ease;
}

.star:hover {
  transform: scale(1.2); /* 星号放大效果 */
  color: #f6e05e; /* 鼠标悬停时颜色 */
}

.star:before {
  content: '★'; /* 星形字符 */
  position: absolute;
  left: 0;
  top: 0;
  color: transparent; /* 初始透明 */
  -webkit-text-stroke: 1px #ffcc00; /* 边框颜色 */
}

.star.filled:before {
  color: #ffcc00; /* 点击后填充颜色 */
}
</style>
