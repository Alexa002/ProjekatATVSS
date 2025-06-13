<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';


const authStore = useAuthStore()
const emit = defineEmits(['success', 'error']);

const form = ref({
    email:'',
    password:''
});

const isLoading = ref(false);

const handleSubmit = async () => {
    try{
        isLoading.value  = true;
        await authStore.login(form.value);
        emit('success');
    } catch (error) {
        emit('error', error.message);
    } finally {
        isLoading.value = false;
    }
};

</script>

<template>
    <form @submit.prevent="handleSubmit" class="authForm">
        <div class="form-group">
            <label for="email">Email</label>
            <input 
            v-model="form.email"
            type="email"
            id="email"
            required
            placeholder="Enter your email"
            />
        </div>

        <div class="form-group">
            <label for="password">Password</label>
            <input
            v-model="form.password"
            type="password"
            id="password"
            required
            placeholder="Enter yout password"
            />
        </div>

        <button type="submit" :disabled="isLoading" class="submit-btn">
            {{ isLoading ? 'Logging on...' : 'Login' }}
        </button>

    </form>
</template>

<style scoped>

.authForm {
  max-width: 400px;
  margin: 50px auto; /* centers horizontally and adds some top spacing */
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  background: white;
  border-radius: 8px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

label {
    font-weight: 500;
}

input{
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.submit-btn {
    background-color: #4a89dc;
    color: white;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: 1rem;
}


.submit-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>