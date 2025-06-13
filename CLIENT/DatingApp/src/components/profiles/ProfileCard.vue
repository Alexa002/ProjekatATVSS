<script setup>
import userImage from '@/assets/user.png';

defineProps({
    profile: {
        type: Object,
        required: true
    }
});

 const emit = defineEmits(['like']);

</script>

<template>
<div class="profile-card">
    <div class="profile-image">
        <img 
        :src="profile.photo || userImage" 
        :alt="profile.name"
        />
    </div>

    <div class="profile-info">
        <h2>{{ profile.name }}, {{ profile.age }}</h2>
        <p class="loaction"> {{ profile.location }}</p>
        <p class="bio"> {{ profile.bio }}</p>

        <button @click="emit('like', profile.id)" class="like-btn">
            Like ❤️
        </button>
    </div>
</div>

</template>

<style scoped>

.profile-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.profile-card:hover {
    transform: translateY(-5px);
}

.profile-image img {
    width: 100%;
    height: 300px;
    object-fit: cover;
}

.profile-info {
    padding: 1rem;
}

h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
}

.location {
    color: #666;
    margin: 0 0  1rem 0;
}

.bio {
    margin: 0 0 1rem 0;
    line-height: 1.5;
}

.like-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.like-btn:hover {
  background-color: #ff6b81;
}
</style>