import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/my',
      name: 'my',
      component: () => import('../views/MyView.vue')
    },
    {
      path: '/searchResults',
      name: 'searchResults',
      component: () => import('../views/SearchResultsView.vue'),
      props: true
    }
  ]
})

export default router
