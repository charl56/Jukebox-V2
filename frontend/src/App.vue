<template>
    <ListDisplay v-if="dataLoad" :list="listCds" />
    <WallDisplay v-if="dataLoad" :list="wallCds" />
    <ServerUnreachable v-else-if="serverUnreachable" />
    <CdPopUp />
    <Toast />
    <Settings />
    <WaitingScreen />
    <BackScreen />

</template>

<script>
import WallDisplay from '@/components/WallDisplay/WallDisplay.vue';
import Settings from '@/components/WallDisplay/Settings.vue';
import WaitingScreen from '@/components/WallDisplay/WaitingScreen.vue';

import ListDisplay from '@/components/ListDisplay/ListDisplay.vue';
import CdPopUp from '@/components/CdPopUp/CdPopUp.vue';
import ServerUnreachable from '@/components/ServerUnreachable/ServerUnreachable.vue';
import Toast from '@/components/Toast/Toast.vue';
import BackScreen from '@/components/BackScreen/BackScreen.vue';

import { eventBus } from './plugins/eventBus';
import { SyncronizeCdWithBack } from './plugins/syncronization';
import api from './plugins/api.js';

export default {
    name: 'App',
    components: {
        Toast,
        WallDisplay,
        ListDisplay,
        CdPopUp,
        ServerUnreachable,
        Settings,
        WaitingScreen,
        BackScreen

    },
    created() {
        if(localStorage.firstVisit == undefined) {
            localStorage.firstVisit = false
            localStorage.dataList = null
            localStorage.cdPlaying = 0
            localStorage.localStorage = 0
            localStorage.artiste = ''
        }

        // On récupère les données du JSON dans le back 
        api.getApi('cd')
            .then((resp) => {
                let Data = JSON.parse(resp.data.data)
                this.dataList = []
                // On commence par mettre les données du JS dans une liste, pour mieux manipuler
                // Pour recupe l'index des object dans le JS
                const keys = Object.keys(Data.cd);
                // Pour chaques items
                for (const index of keys) {
                    const cd = Data.cd[index];
                    this.dataList.push(cd)
                }
                localStorage.dataList = JSON.stringify(this.dataList, null, 2)
                this.serverUnreachable = false
                this.dataLoad = true
                // Puis on trie ente les 2 listes : cd en rab ou sur le mur
                this.setLists()
            })
            .catch((err) => {
                this.serverUnreachable = true
                console.log(err)
            })
        // Permet de mettre à jour les listes
        eventBus.on('updateLists', () => {
            this.dataList = JSON.parse(localStorage.dataList) // On met a jour les données dans la liste
            this.wallCds = []              // On vide les listes
            this.listCds = []
            this.setLists()
            SyncronizeCdWithBack()

        });

    },
    data() {
        return {
            dataList: [],
            wallCds: [],
            listCds: [],
            dataLoad: false,
            serverUnreachable: true,
        }
    },
    methods: {
        setLists() {
            this.dataList.forEach((cd) => {
                // On trie les cd entre ceux du mur, et ceux de la liste
                if (cd.position == 0) {
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
    --background-color-black-2-1: #1D1D1D;
    --background-color-black-3: #282828;
    --background-color-black-4: #484848;
    --border-color-cd-popup: white;
    --div-cd-color: #181818;
    --div-cd-color-hover: #282828;
}

/* Hide scrollbar for Chrome, Safari and Opera */
html::-webkit-scrollbar {
    display: none;
}

html {
    /* Hide scrollbar for IE, Edge and Firefox */
    -ms-overflow-style: none;
    /* IE and Edge */
    scrollbar-width: none;
    /* Firefox */
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

    height: 100svh;
    width: 100%;
    display: flex;
    padding: 10px;
}

/* Surlignage du texte */
::selection {
    background-color: #ebe5dc;
    color: #7eb3e8;
}

::-moz-selection {
    background-color: #ebe5dc;
    color: #2c3e50;
}

.icon {
    height: 30px;
    width: 30px;
}

.icon:hover {
    cursor: pointer;
    transform: scale(1.06);
    transition: transform 0.2s ease;
}

.icon:active{
    transform: scale(0.9);
}

</style>
