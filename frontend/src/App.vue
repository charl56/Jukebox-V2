<template>
    <div v-if="dataLoad" class="d-flex">
        <!-- Col affichage CD en plus -->
        <v-col cols="3"  class="col-list-display pa-1">
          <ListDisplay :list="listCds" />
        </v-col>
        <!-- Col affichage CD en places -->
        <v-col cols="9" class="col-wall-display pa-1">
          <WallDisplay :list="wallCds" />
        </v-col>

        <!-- Popup CD -->
        <CdPopUp />
    </div>
</template>

<script>
import WallDisplay from './components/WallDisplay/WallDisplay.vue';
import ListDisplay from './components/ListDisplay/ListDisplay.vue';
import CdPopUp from './components/CdPopUp/CdPopUp.vue';
import data from "./assets/data.json"
import { eventBus } from './plugins/eventBus';

export default {
    name: 'App',
    components: {
      WallDisplay,
      ListDisplay,
      CdPopUp
    },
    created(){   
        // On récupère les données du JSON dans le back 
        let Data = JSON.parse(data) 
    
        // On commence par mettre les données du JS dans une liste, pour mieux manipuler
        // Pour recupe l'index des object dans le JS
        const keys = Object.keys(Data.cd);
        // Pour chaques items
        for (const index of keys) {
            const cd = Data.cd[index];
            this.dataList.push(cd)
        }
        localStorage.dataList = JSON.stringify(this.dataList, null, 2)
        this.dataLoad = true
        // Puis on trie ente les 2 listes : cd en rab ou sur le mur
        this.setLists()
        // Permet de mettre à jour les listes
        eventBus.on('updateLists', () => {
            this.dataList = JSON.parse(localStorage.dataList) // On met a jour les données dans la liste
            this.wallCds = []              // On vide les listes
            this.listCds = []                 
            this.setLists()
        });
    },
    data () {
        return {
          dataList: [],
          wallCds: [],
          listCds: [],
          dataLoad: false,
        }
    },
    methods:{
        setLists(){
            this.dataList.forEach((cd) => { 
                // On trie les cd entre ceux du mur, et ceux de la liste
                if(cd.position == 0){
                    this.listCds.push(cd)
                } else {
                    this.wallCds.push(cd)
                }
            })
        }
    },
}

</script>

<style>
/* Equivalent var global mais pour couleurs CSS */
:root {
   --background-color-black-1: #000000;
   --background-color-black-2: #121212;
   --background-color-black-3: #282828;
   --background-color-black-4: #484848;
   --border-color-cd-popup: white;
}

/* Hide scrollbar for Chrome, Safari and Opera */
html::-webkit-scrollbar {
    display: none;
}

html {
    margin: 0;
    height: 100%;
    background-color: var(--background-color-black-1);
    /* Hide scrollbar for IE, Edge and Firefox */
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
}
#app {
    font-family: Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: white;
    background-color: var(--background-color-black-1) !important;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
/* Surlignage du texte */
::selection{
    background-color: #ebe5dc;
    color: #7eb3e8;
}
::-moz-selection{
    background-color: #ebe5dc;
    color: #2c3e50;
}
/* Cols affichage */
.col-list-display, .col-wall-display{
    width: 100%;
    height: 100%;
}
</style>
