import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth';
import DiscoverView from '@/views/DiscoverView.vue';
import ProfileView from '@/views/ProfileView.vue';
import AuthView from '@/views/AuthView.vue';
import MatchesView from '@/views/MatchesView.vue';
import MessagesView from '@/views/MessageView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/discover',
      name: 'discover',
      component: DiscoverView,
      meta: { requiresAuth: true }
    },
    {
      path: '/matches',
      name: 'matches',
      component: MatchesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView,
      meta: { requiresGuest: true }
    },
    {
      path: '/matches',
      name: 'Matches',
      component: MatchesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/messages',
      name: 'messages', // This should match the name you're using in navigation
      component: MessagesView,
      meta: { requiresAuth: true },
      children: [
        {
          path: ':userId',
          name: 'messages-user', // Give it a distinct name
          component: MessagesView,
          props: true
        },
        {
          path: 'conversation/:conversationId',
          name: 'messages-conversation',
          component: MessagesView,
          props: true
        }
      ]
    }
  ],

});


router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated && localStorage.getItem('authToken')) {
    await authStore.checkAuth();
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth');
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/');
  } else {
    next();
  }
});


export default router;
