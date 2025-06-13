<script setup>
import { RouterView } from 'vue-router';
import NavBar from '@/components/common/NavBar.vue'; // Ensure NavBar is imported
import { useAuthStore } from './stores/auth';
import { onMounted, computed } from 'vue';

const authStore = useAuthStore();

// Call checkAuth only if needed
onMounted(async () => {

});

// Reactive isAuthenticated state for conditional rendering
const isAuthenticated = computed(() => authStore.isAuthenticated);
</script>

<template>
  <div class="app-container">
    <!-- Show Navbar only for authenticated users -->
    <NavBar v-if="isAuthenticated" />

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
}
</style>
