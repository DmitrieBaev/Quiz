import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/sign-in',
    name: 'sign-in',
    component: () => import('../views/SignInView.vue')
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: () => import('../views/SignUpView.vue')
  },
  {
    path: '/questionary/:id',
    component: () => import('../views/QuestionaryView.vue'),
    name: 'questionary-by-id',
    props: true
  },
  {
    path: '/questionary/:id/results',
    component: () => import('../views/QuestionaryResultsView.vue'),
    name: 'questionary-by-id-results',
    props: true
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
