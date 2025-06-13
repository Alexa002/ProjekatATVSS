import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/composables/apiConnection';


export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const isAuthenticated = ref(false);
    const error = ref(null);

    const login = async (credentials) => {
        try {
            const response = await api.post('/auth/login', credentials);
            localStorage.setItem('authToken', response.data.access_token);
            console.log(response.data)
            user.value = response.data.user;
            isAuthenticated.value = true;
            error.value = null;
            return response.data;
        } catch (err) {
            error.value = err.response.data.message || 'Login failed';
            throw err;
        }
    };


    const register = async (userData) => {
        try {
            const response = await api.post('/auth/register', userData);
            return response.data;
        } catch (err) {
            error.value = err.response.data.message || 'Registration failed';
            throw err;
        }
    };

    const logout = () => {
        console.log('Logging out')
        localStorage.removeItem('authToken');
        user.value = null;
        isAuthenticated.value = false;
    };

    const checkAuth = async () => {
        const token = localStorage.getItem('authToken');
        if(token){
            try {
                const response = await api.get('/auth/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                
                user.value = { email: response.data.email, id: response.data.id, role: response.data.role };
                isAuthenticated.value = true;
                error.value = null;
            } catch (err) {
                console.error('Error in checkAuth:', err.response?.data || err.message);
                logout();
            }
        }
    };

    return { user, isAuthenticated, error, login, register, logout, checkAuth };

});