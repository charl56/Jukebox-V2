import axios from 'axios';

const backend = import.meta.env.VITE_BACK_URL || "http://127.0.0.1:5025/"
const isOnServer = import.meta.env.VITE_CUSTOM_MODE || false

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
    getApi(url, params = {}) {
        return api.get('api/' + url, { params });
    },

    // Requête POST
    postApi(url, data = {}, config) {
        if (isOnServer) {
            return Promise.resolve({
                status: "info",
                message: "Certaines fonctionnalités sont limitées pour la version de test",
                data: null
            });
        }

        return api.post('api/' + url, data, config);
    },

    postApiJukebox(url, data = {}, config) {
        if (isOnServer) {
            return Promise.resolve({
                status: "info",
                message: "Certaines fonctionnalités sont limitées pour la version de test",
                data: null
            });
        }

        return api.post('api/jukebox/' + url, data, config);
    },

    // Requête PUT
    putApi(url, data = {}, config) {
        if (isOnServer) {
            return Promise.resolve({
                status: "info",
                message: "Certaines fonctionnalités sont limitées pour la version de test",
                data: null
            });
        }

        return api.put('api/' + url, data, config);
    },

    // Requête DELETE
    deleteApi(url) {
        if (isOnServer) {
            return Promise.resolve({
                status: "info",
                message: "Certaines fonctionnalités sont limitées pour la version de test",
                data: null
            });
        }
        
        return api.delete('api/' + url);
    }
};