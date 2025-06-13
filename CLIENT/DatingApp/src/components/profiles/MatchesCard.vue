<template>
  <div class="match-card">
    <div class="match-header">
      <img 
        v-if="match.profile.photo" 
        :src="match.profile.photo" 
        class="profile-pic"
        alt="Profile"
      >
      <div v-else class="initials">
        {{ match.profile.first_name.charAt(0) }}{{ match.profile.last_name.charAt(0) }}
      </div>
      <h3>{{ match.profile.first_name }} {{ match.profile.last_name }}</h3>
      <p class="meta">{{ match.profile.age }} • {{ match.profile.location }}</p>
    </div>
    
    <p v-if="match.profile.bio" class="bio">{{ match.profile.bio }}</p>
    
    <div class="match-actions">
      <button @click="$emit('view', match.user.id)">View</button>
      <button @click="$emit('message', match.user.id)">Message</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  match: {
    type: Object,
    required: true
  }
});

defineEmits(['view', 'message']);
</script>

/* src/components/MatchCard.vue - style section */
<style scoped>
.match-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.match-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.match-header {
  padding: 1.5rem;
  text-align: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.profile-pic {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 1rem;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.initials {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6e8efb 0%, #4a6cf7 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto 1rem;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.match-header h3 {
  margin: 0.5rem 0 0;
  color: #2c3e50;
  font-size: 1.25rem;
}

.meta {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0.25rem 0 0;
}

.bio {
  padding: 1rem 1.5rem;
  color: #34495e;
  font-size: 0.95rem;
  line-height: 1.5;
  border-bottom: 1px solid #ecf0f1;
  flex-grow: 1;
}

.match-actions {
  display: flex;
  border-top: 1px solid #ecf0f1;
}

.match-actions button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.match-actions button:first-child {
  color: #3498db;
  border-right: 1px solid #ecf0f1;
}

.match-actions button:last-child {
  color: #2ecc71;
}

.match-actions button:hover {
  background: #f8f9fa;
}

.match-actions button:active {
  transform: scale(0.98);
}

/* For the matches grid container */
.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

/* Loading and error states */
.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.error {
  color: #e74c3c;
}

.error button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error button:hover {
  background: #c0392b;
}
</style>