// src/api.js
import axios from 'axios';

const backend = import.meta.env.VITE_BACK_URL || "http://127.0.0.1:5025/"

// Configuration de base pour axios
const api = axios.create({
    baseURL: backend,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});


// Intercepteur pour ajouter automatiquement le token d'authentification si disponible
api.interceptors.request.use(config => {
    const token = localStorage.getItem('auth_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Les 4 types de requêtes de base
export default {
    // Requête GET
    get(url, params = {}) {
        return api.get(url, { params });
    },

    getApi(url, params = {}) {
        return api.get('api/' + url, { params });
    },

    // Requête POST
    post(url, data = {}) {
        return api.post(url, data);
    },

    postApi(url, data = {}) {
        return api.post('api/' + url, data);
    },

    // Requête PUT
    put(url, data = {}) {
        return api.put(url, data);
    },

    // Requête DELETE
    delete(url) {
        return api.delete(url);
    },

    deleteApi(url) {
        return api.delete('api/' + url);
    }
};