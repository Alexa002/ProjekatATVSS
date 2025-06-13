<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';


const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
    authStore.logout();
    router.push('/auth');
};

</script>

<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <router-link to="/">Dating App</router-link>
        </div>

        <div class="navbar-links">
            <router-link to="/discover">Discover</router-link>
            <router-link to="/matches">Matches</router-link>
            <router-link to="/profile">Profile</router-link>
            <router-link to="/messages">Messages</router-link>

            <a @click.prevent="logout" class="logout-link">Logout</a>
        </div>
    </nav>
</template>


<style scoped>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #4a89dc;
    color: white;
}

.navbar-brand a {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

.navbar-links {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.navbar-links a { 
    color: white;
    text-decoration: none;
    font-size: 1.1rem;
}

.navbar-links a:hover {
    text-decoration: underline;
}

.logout-link {
    color: white;
    text-decoration: none;
    font-size: 1.1rem;
    cursor: pointer;
}

.logout-link:hover {
    text-decoration: underline;
}
</style>
