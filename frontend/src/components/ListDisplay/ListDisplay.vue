<script setup>
    const iconAdd = new URL('../../assets/icons/add_white.png', import.meta.url).href
    const iconSync = new URL('../../assets/icons/sync_white.png', import.meta.url).href
</script>
<template>
    <div class="div-list-display d-flex flex-column pa-3 ma-1">
        <!-- Btn ajout cd -->
        <div class="div-btn-add ma-1 pa-1 d-flex justify-center">
            <!-- <v-btn class="btn-add" variant="outlined" @click="addCd()">Ajouter</v-btn> -->
            <v-img title="Ajouter un cd" :src="iconAdd" class="list-icons" @click="addCd()"></v-img>
            <!-- <v-btn class="btn-add" variant="outlined" @click="Sync()">Sync</v-btn> -->
            <v-img title="Syncroniser les données" :src="iconSync" class="list-icons" @click="Sync()"></v-img>
        </div>
        <!-- List des CD en rab, v-for -->
        <div class="div-overflow-list">
            <div v-for="cd in list" class="div-cd-list ma-2 d-flex flex-column align-end" @click="openCd(cd)">
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

export default {
    name: 'AppListDisplay',
    components: {
    },
    props:{
        list: Array,
    },
    created(){
        //   this.iconDl = new URL('../../assets/Icons/download.png', import.meta.url).href
    },
    data () {
        return {
        
        }
    },
    methods:{
        // Ajouter un nv CD
        addCd(){
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {"data":
                    {'albumName': '', 'artiste': '', 'trackNb': '', 'releaseDate': new Date().toISOString().split('T')[0], 'position': 0},
                "function": "Add"
            });   
        },
        // Ouvrir un CD
        openCd(cd){
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {"data":
                    cd,
                "function": "Edit"
            });  
        },
        Sync(){
            // Creation du json qui sera save dans le fichier
            let data = {
                "cd": JSON.parse(localStorage.dataList)
            }
            // Requete vers le back pour save les données du JSON
            axios.post('http://127.0.0.1:5025/syncData', {data: JSON.stringify(data)})
                .then((resp) => {
                    console.log(resp)
                })
                .catch((err) => {
                    console.log(err)
                })
        }
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div du composant */
.div-list-display{
    width: 100%;
    height: 95vh;
    background-color: var(--background-color-black-2);
    border-radius: 5px;
}
/* Row btn add */
.div-btn-add{
    height: fit-content;
}.btn-add:hover{
    color: var(--background-color-black-2);
    background-color: white;
}
/* Liste des cd */
.div-cd-list{
    height: 10vh;
}.div-cd-list:hover{
    cursor: pointer;
    background-color: var(--background-color-black-3);
    border-radius: 5px;
}.div-overflow-list{  /* Scroll bar */
    overflow-y: scroll;
    margin-left: 10px;
}.div-overflow-list::-webkit-scrollbar{             /* Fond de la barre de scroll */
    width: 10px;
    background-color: var(--background-color-black-3);
    border-radius: 5px;
}.div-overflow-list::-webkit-scrollbar-button{      /* Boutons haut/bas */ 
    display: none;
}.div-overflow-list::-webkit-scrollbar-thumb{      /* Bouton de la barre de scroll */
  background-color: var(--background-color-black-4);
  border-radius: 5px;
}


/* Icon */
.list-icons{
    height: 30px;
    width: 30px;
}.list-icons:hover{
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
}



</style>