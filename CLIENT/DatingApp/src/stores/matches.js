// src/stores/matches.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/composables/apiConnection';
import { useAuthStore } from './auth';

export const useMatchesStore = defineStore('matches', () => {
    const matches = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const authStore = useAuthStore();

    const fetchMatches = async () => {
        try {
            loading.value = true;
            error.value = null;
            
            const response = await api.get('/matches/matched', {
                headers: {
                    Authorization: `Bearer ${authStore.user?.token || localStorage.getItem('authToken')}`
                }
            });
            
            matches.value = response.data.matches;
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Failed to fetch matches';
            
            // Auto-logout on 401 Unauthorized
            if (err.response?.status === 401) {
                authStore.logout();
            }
            
            throw err;
        } finally {
            loading.value = false;
        }
    };

    return {
        matches,
        loading,
        error,
        fetchMatches
    };
});