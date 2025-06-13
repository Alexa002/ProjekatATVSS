import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    } else {
        delete config.headers.Authorization;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});


api.interceptors.response.use(
    response => response,
    error => {
        if (error.response.status === 401 && error.response.data.message === 'Token expired') {

            return axios.post('http://127.0.0.1:5000/api/refresh', {}, {
                headers: { Authorization: `Bearer ${localStorage.getItem('authToken')}` }
            })
                .then(response => {
                    localStorage.setItem('authToken', response.data.token);
                    error.config.headers.Authorization = `Bearer ${response.data.token}`;
                    return axios(error.config);
                })
                .catch(refreshError => {
                    localStorage.removeItem('authToken');
                    window.location = '/login';
                    return Promise.reject(refreshError);
                });
        }
        return Promise.reject(error);
    }
);


export default api;