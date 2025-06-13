<!-- src/views/MatchesView.vue -->
<template>
  <div class="matches-view">
    <h1>Your Matches</h1>
    
    <div v-if="loading" class="loading">
      <p>Loading matches...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchMatches">Try Again</button>
    </div>
    
    <div v-else-if="!matches.length" class="empty">
      <p>No matches found</p>
    </div>
    
    <div v-else class="matches-grid">
      <MatchCard
        v-for="match in matches"
        :key="match.match_id"
        :match="match"
        @view="viewProfile"
        @message="sendMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMatchesStore } from '@/stores/matches';
import MatchCard from '@/components/profiles/MatchesCard.vue';
import { useRouter } from 'vue-router';

const matchesStore = useMatchesStore();
const router = useRouter()


const matches = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchMatches = async () => {
  try {
    loading.value = true;
    error.value = null;
    await matchesStore.fetchMatches();
    matches.value = matchesStore.matches;
  } catch (err) {
    error.value = matchesStore.error;
  } finally {
    loading.value = false;
  }
};

const viewProfile = (userId) => {
  // Navigate to profile view
  console.log('View profile:', userId);
};

const sendMessage = (userId) => {
  router.push({ name: 'messages-user', params: { userId } });
  console.log('Message user:', userId);
};

onMounted(() => {
  fetchMatches();
});
</script>