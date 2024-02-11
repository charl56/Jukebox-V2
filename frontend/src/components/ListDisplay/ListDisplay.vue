<script setup>
const iconAdd = new URL('../../assets/icons/add_white.png', import.meta.url).href
const iconSync = new URL('../../assets/icons/sync_white.png', import.meta.url).href
</script>
<template>
    <div class="div-list-display d-flex flex-column pa-3 ma-1">
        <!-- Btn ajout cd -->
        <div class="div-btn-add ma-1 pb-4 d-flex justify-center">
            <v-img title="Ajouter un cd" :src="iconAdd" class="list-icons" @click="addCd()"></v-img>
            <v-img title="Syncroniser les données" :src="iconSync" class="list-icons" @click="Sync()"></v-img>
        </div>
        <!-- Search bar -->
        <div class="div-search-bar ma-1 pb-3 d-flex justify-center">
            <input type="text" name="searchBar" placeholder="Rechercher" class="pa-2 input-search-bar" v-model="search" @keyup="filtereList">
        </div>
        <!-- List des CD en rab, v-for -->
        <div class="div-overflow-list mt-2" @drop="onDrop(0, $event)" @dragover="allowDrop($event)">
            <div v-for="cd in filteredList" class="div-cd-list ma-2 d-flex flex-column align-end" @click="openCd(cd)"
                draggable="true" @dragstart="drag(cd)">
                <v-row class="my-0 mx-2">
                    <p class="text-subtitle-1 font-weight-bold">{{ cd.albumName }} </p>
                </v-row>
                <v-row class="my-0 mx-2">
                    <p class="text-subtitle-2">{{ cd.artiste }}</p>
                </v-row>
            </div>
        </div>
    </div>
</template>
  
<script>
import { eventBus } from '../../plugins/eventBus';
import axios from 'axios';
import { drag, drop, allowDrop } from '../../plugins/dragNdrop';

export default {
    name: 'AppListDisplay',
    components: {
    },
    props: {
        list: Array,
    },
    watch: {
        list: function(newList, oldList) {
            this.filteredList = newList;
        }
    },
    created() {
        this.filteredList = this.list
    },
    data() {
        return {
            search: '',
            filteredList: []
        }
    },
    methods: {
        // Ajouter un nv CD
        addCd() {
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {
                    "data":
                        { 'albumName': '', 'artiste': '', 'trackNb': '', 'releaseDate': new Date().toISOString().split('T')[0], 'position': 0 },
                    "function": "Add"
                });
        },
        // Ouvrir un CD
        openCd(cd) {
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {
                    "data":
                        cd,
                    "function": "Edit"
                });
        },
        Sync() {
            // Creation du json qui sera save dans le fichier
            let data = {
                "cd": JSON.parse(localStorage.dataList)
            }
            // Requete vers le back pour save les données du JSON
            axios.post(this.$backendPort + "syncData", { data: JSON.stringify(data) })
                .then((resp) => {})
                .catch((err) => {
                    console.log(err)
                })
        },
        onDrop(pos) {
            // On recupère le cd déplacé dans la liste, avec sa position en 0
            let newCd = drop()
            // On recupre la liste de tous les albums
            let listCds = JSON.parse(localStorage.dataList) // On met a jour la liste
            // Puis l'index du cd changé
            let index = listCds.findIndex((cd) => cd.albumName == newCd.albumName)
            // On le modifie dans la liste
            listCds[index].position = 0
            // On remet la liste en localStorage, pour pouvoir refresh
            localStorage.dataList = JSON.stringify(listCds, null, 2) // On met a jour la liste
            // On actualise la liste dans l'app
            eventBus.emit('updateLists')
        },
        filtereList() {
            if(this.search == ''){
                this.filteredList = this.list
            } else {
                // Computed property that filters the list based on the search term
                this.filteredList = this.list.filter(cd => {
                    const albumNameMatch = cd.albumName.toLowerCase().includes(this.search.toLowerCase());
                    const artisteMatch = cd.artiste.toLowerCase().includes(this.search.toLowerCase());
                    return albumNameMatch || artisteMatch;
                });
            }
        }
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div du composant */
.div-list-display {
    width: 100%;
    height: 95vh;
    background-color: var(--background-color-black-2);
    border-radius: 5px;
}

/* Row btn add */
.div-btn-add {
    height: fit-content;
    border-bottom: 1px solid var(--background-color-black-4);
}

.btn-add:hover {
    color: var(--background-color-black-2);
    background-color: white;
}

/* Search barr */
.div-search-bar {
    height: fit-content;
    border-bottom: 1px solid var(--background-color-black-4);
}

.input-search-bar {
    width: 90%;
    height: 100%;
    color: white;
}

.input-search-bar:hover {
    background-color: #282828;
    border-radius: 5px;
}

.input-search-bar:focus {
    outline: none;
}


/* Liste des cd */
.div-cd-list {
    height: 10vh;
}

.div-cd-list:hover {
    cursor: pointer;
    background-color: var(--background-color-black-3);
    border-radius: 5px;
}

.div-cd-list:-moz-drag-over {
    background-color: red;
    color: red;
}

.div-overflow-list {
    /* Scroll bar */
    overflow-y: scroll;
    margin-left: 10px;
}

.div-overflow-list::-webkit-scrollbar {
    /* Fond de la barre de scroll */
    width: 10px;
    background-color: var(--background-color-black-3);
    border-radius: 5px;
}

.div-overflow-list::-webkit-scrollbar-button {
    /* Boutons haut/bas */
    display: none;
}

.div-overflow-list::-webkit-scrollbar-thumb {
    /* Bouton de la barre de scroll */
    background-color: var(--background-color-black-4);
    border-radius: 5px;
}


/* Icon */
.list-icons {
    height: 30px;
    width: 30px;
}

.list-icons:hover {
    cursor: pointer;
    animation: rotate 1.2s infinite;
}

@keyframes rotate {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}</style>