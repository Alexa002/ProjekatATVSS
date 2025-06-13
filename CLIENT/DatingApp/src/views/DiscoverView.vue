<script setup>
import api from '@/composables/apiConnection';
import { ref, onMounted } from 'vue';
import ProfileCard from '@/components/profiles/ProfileCard.vue';



const profiles = ref([]);
const isLoading = ref(false);
const error = ref(null);

const fetchProfiles = async () => {
    try {
        isLoading.value = true;
        const response = await api.get('/user/discover');
        profiles.value = response.data.users || [];
    } catch (err) {
        error.value = err.response?.data?.message || "Failed to load profiles"
    } finally {
        isLoading.value = false;
    }
};

const handleLike = async (userId) => {
    try {
        const response  = await api.post(`/user/like/${userId}`);
        if (response.data.is_mutal) {
            alert("It`s a match!");
        }
        console.log(profile)
        profiles.value = profiles.value.filter(profile => profile.Id !== userId) 

    } catch (err) {
        error.value = err.response.data.message || "Failed to like profile";
    }
};

onMounted(() => {
    fetchProfiles(); 
});

</script> 

<template>

    <div class="discover-view">
        <h1>Discover people</h1>

        <div v-if="isLoading" class="loading">
            Loading profiles...
        </div>

        <div v-else-if="error" class="error">
            {{error}}
        </div>

        <div v-else-if="profiles.length === 0" class="empty">
            No more profiles to show. Check back later!
        </div>

        <div v-else class="profiles-grid">
            <ProfileCard
            v-for="profile in profiles"
            :key="profile.user_Id"
            :profile="profile"
            @like="handleLike"
            />
        </div>
    </div>

</template>

<style scoped>
.discover-view {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    margin-bottom: 2rem;
}

.profiles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.loading, .error, .empty{
    text-align: center;
    padding: 2rem;
    font-size: 1.2rem;
}

.error {
    color: #e74c3c;
}

</style>