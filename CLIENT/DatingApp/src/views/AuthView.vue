<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import LoginForm from '@/components/auth/LoginForm.vue';
import RegisterForm from '@/components/auth/RegisterForm.vue';




const router = useRouter();
const authStore = useAuthStore();
const isLogin = ref(true);

const handleSuccess = () => {
    router.push('/');
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <h1>{{ isLogin ? 'Login' : 'Register' }}</h1>
        
            <LoginForm
            v-if="isLogin"
            @success="handleSuccess"
            @error="error => authStore.error = error"
            />

            <RegisterForm
            v-else
            @success="isLogin = true"
            @error="error => authStore.error = error"
            />

            <p class="toggle-text">
                {{ isLogin ? "Don`t have an account?" : "Already have an account?" }}
                <button @click="isLogin = !isLogin" class="toggle-btn">
                    {{ isLogin ? 'Register' : 'Login' }}
                </button>
            </p>

            <p v-if="authStore.error" class="error-message">
                {{ authStore.error }}
            </p>
        
        </div>
    </div>


</template>

<style scoped>
.auth-container{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
}

.auth-card{
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

.h1 {
    text-align: center;
    margin-bottom: 1rem;
}

.toggle-text {
    text-align: center;
    margin-top: 1rem;
}

.toggle-btn {
    background: none;
    border: none;
    color: #4a89dc;
    cursor: pointer;
    text-decoration: underline;
}

.error-message {
    color: #e74c3c;
    text-align: center;
    margin-top: 1rem;
}


</style>