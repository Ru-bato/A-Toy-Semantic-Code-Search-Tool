<template>
  <div class="container">
    <el-container>
      <el-header style="padding: 0"><TopBar /></el-header>
      <el-main>
        <div class="word-cloud-container">
          <div>
            <canvas id="wordcloud-canvas" style="border: none"></canvas>
          </div>
        </div>
        <div class="article-container">
          <h2>Popular Code Examples</h2>
          <el-loading :loading="loading" text="loading..." />
          <div v-if="!loading && !hasContent">No popular code examples found.</div>
          <div v-else>
            <div class="section-container">
              <h3>Questions (Stack Overflow)</h3>
              <ul v-if="stackOverflowExamples.length">
                <li
                  v-for="(example, index) in stackOverflowExamples"
                  :key="index"
                  class="example-item"
                >
                  <a :href="example.link" target="_blank">{{ example.title }}</a>
                  <span class="star" @click="addToFavorites(example.title, example.link)">★</span>
                </li>
              </ul>
              <div v-else>No questions found.</div>
            </div>

            <!-- GitHub Section -->
            <div class="section-container">
              <h3>Repositories (GitHub)</h3>
              <ul v-if="gitHubExamples.length">
                <li v-for="(example, index) in gitHubExamples" :key="index" class="example-item">
                  <a :href="example.link" target="_blank">{{ example.title }}</a>
                  <!-- <span class="source-label">({{ example.source }})</span> -->
                  <span class="star" @click="addToFavorites(example.title, example.link)">★</span>
                </li>
              </ul>
              <div v-else>No repositories found.</div>
            </div>

            <!-- Dev.to Section -->
            <div class="section-container">
              <h3>Articles (Dev.to)</h3>
              <ul v-if="devToExamples.length">
                <li v-for="(example, index) in devToExamples" :key="index" class="example-item">
                  <a :href="example.link" target="_blank">{{ example.title }}</a>
                  <!-- <span class="source-label">({{ example.source }})</span> -->
                  <span class="star" @click="addToFavorites(example.title, example.link)">★</span>
                </li>
              </ul>
              <div v-else>No articles found.</div>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import WordCloud from 'wordcloud'
import { ElLoading } from 'element-plus'
import router from '@/router'
import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'

const wordCloudImage = ref<string | null>(null)
const tags = ref<string[]>([])
const store = useStore()
const apiUrl = store.getters.apiUrl
const isLoggedIn = computed(()=>store.getters.isLoggedIn)
const loading = ref(false) // Loading state
const favorites = ref<{ title: string; link: string }[]>([]) // 收藏夹

// Save data from Stack Overflow, GitHub and Dev.to separately
const stackOverflowExamples = ref<{ title: string; link: string; source: string }[]>([])
const gitHubExamples = ref<{ title: string; link: string; source: string }[]>([])
const devToExamples = ref<{ title: string; link: string; source: string }[]>([])

// Judge if the content is null
const hasContent = computed(
  () =>
    stackOverflowExamples.value.length > 0 ||
    gitHubExamples.value.length > 0 ||
    devToExamples.value.length > 0
)

// 收藏功能
const addToFavorites = async (title: string, link: string) => {
  const isLoggedIn = store.getters.isLoggedIn
  if (!isLoggedIn) {
    router.push({ name: 'login' })
    return
  }
  favorites.value.push({ title, link })
  console.log(`Added to favorites: ${title} - ${link}`)
  try {
    await axios.post(`${apiUrl}/user/favorites/`, {
      item_title: title,
      item_link: link
    })
    alert('Favour Successfully!')
  } catch (error) {
    console.error('Favour Failed:', error)
  }
}

onMounted(async () => {
  loading.value = true // Start loading
  try {
    const response = await axios.get(`${apiUrl}/wordcloud_generator/generate/`, {
      params: {
        width: 800,
        height: 600
      }
    })
    wordCloudImage.value = response.data.image
    tags.value = response.data.tags

    const canvas = document.getElementById('wordcloud-canvas') as HTMLCanvasElement
    if (canvas) {
      const options = tags.value.map((tag) => [tag, Math.random() * 20])
      canvas.width = 800
      canvas.height = 500
      WordCloud(canvas, {
        list: options,
        gridSize: 0,
        weightFactor: 2,
        shape: 'cardioid',
        backgroundColor: '#efc2dd',
        origin: [400, 100],
        color: (word: any, weight: any) => {
          const colors = ['#FF5733', '#FFB833', '#33FF57', '#33B5FF', '#8E33FF']
          return colors[Math.floor(Math.random() * colors.length)]
        },
        click: (item: any[]) => {
          const tag = item[0]
          window.open(`https://stackoverflow.com/tags/${tag}`, '_blank')
        },
        hover: (item: any[], dimension: any) => {
          if (item) {
            canvas.style.cursor = 'pointer'
          } else {
            canvas.style.cursor = 'default'
          }
        }
      })
    } else {
      console.error('Canvas element not found')
    }

    const examplesResponse = await axios.get(`${apiUrl}/popular_code/get_popular/`)
    const examples = examplesResponse.data.results || []

    stackOverflowExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'Stack Overflow'
    )
    gitHubExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'GitHub'
    )
    devToExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'Dev.to'
    )
  } catch (error) {
    console.error('Error generating word cloud or fetching examples:', error)
  } finally {
    loading.value = false // Stop loading
  }
})
</script>

<style scoped>
.container {
  min-width: 100vw;
  padding: 0;
  background: linear-gradient(135deg, #f3f4f6 30%, #e2e8f0 100%);
  font-family: 'Roboto', sans-serif;
  color: #2d3748;
}

.word-cloud-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #f7edf3;
  padding: 20px;
  margin: 20px 0;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.word-cloud-container h2 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2b6cb0;
  margin-bottom: 20px;
}

.word-cloud-container canvas {
  border: 2px solid #3182ce;
  border-radius: 10px;
}

.article-container {
  margin-top: 20px;
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.article-container h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #2b6cb0;
  text-align: center;
}

.section-container {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 8px;
  background: #f7fafc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.stackoverflow-section {
  background: linear-gradient(135deg, #fbd38d 30%, #f6ad55 100%);
}

.github-section {
  background: linear-gradient(135deg, #b794f4 30%, #9f7aea 100%);
}

.devto-section {
  background: linear-gradient(135deg, #63b3ed 30%, #4299e1 100%);
}

.section-container h3 {
  font-size: 1.6rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 15px;
}

.example-item {
  list-style-type: none;
  margin-bottom: 12px;
  font-size: 1.1rem;
}

.example-item a {
  font-weight: bold;
  color: #2d3748;
  text-decoration: none;
  transition: color 0.3s ease;
}

.example-item a:hover {
  color: #2b6cb0;
}

.source-label {
  font-size: 0.85rem;
  color: #718096;
  margin-left: 8px;
}

.star {
  color: #ffcc00; /* 星号颜色 */
  margin-left: 8px;
  cursor: pointer;
  font-size: 1.2rem; /* 星号大小 */
  transition:
    transform 0.3s ease,
    color 0.3s ease;
}

.star:hover {
  transform: scale(1.2); /* 星号放大效果 */
  color: #f6e05e; /* 鼠标悬停时颜色 */
}

@media (max-width: 768px) {
  .article-container {
    padding: 20px;
  }

  .section-container h3 {
    font-size: 1.4rem;
  }

  .example-item {
    font-size: 1rem;
  }
}
</style>
