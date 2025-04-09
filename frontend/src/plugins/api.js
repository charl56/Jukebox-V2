// // src/api.js
// import axios from 'axios';

// // Configuration de base pour axios
// const api = axios.create({
//     baseURL: this.$backend,
//     timeout: 10000,
//     headers: {
//         'Content-Type': 'application/json',
//         'Accept': 'application/json'
//     }
// });

// // Intercepteur pour ajouter automatiquement le token d'authentification si disponible
// api.interceptors.request.use(config => {
//     const token = localStorage.getItem('auth_token');
//     if (token) {
//         config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
// });

// // Les 4 types de requêtes de base
// export default {
//     // Requête GET
//     get(url, params = {}) {
//         return api.get(url, { params });
//     },

//     // Requête POST
//     post(url, data = {}) {
//         return api.post(url, data);
//     },

//     // Requête PUT
//     put(url, data = {}) {
//         return api.put(url, data);
//     },

//     // Requête DELETE
//     delete(url) {
//         return api.delete(url);
//     }
// };