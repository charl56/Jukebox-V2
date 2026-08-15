<script setup>
const iconSettings = new URL('@/assets/icons/settings_white.png', import.meta.url).href
const isOnServer = import.meta.env.VITE_CUSTOM_MODE || false

</script>

<template>
    <div class="div-wall-display">
        <BorderPlayer v-if="!getLocalStorageIsPlayerOpen() && getLocalStorageIsPlaying()" :cd="list.find(cd => cd.position == cdPlayingPosition)" />

        <CdPlayer v-if="getLocalStorageIsPlayerOpen()" :cd="list.find(cd => cd.position == cdPlayingPosition)" :key="keyUpdate"/>
        <!-- Affiche grille avec CDs et lecteur -->
        <div v-else class="col-display" v-for="n in 2" :key="n">
            <WallPlayer v-if="n == 2 && getLocalStorageIsPlaying()" :cd="list.find(cd => cd.position == (getLocalStorageCdPlaying()))" />
            <CdDisplay v-else-if="n != 2 && n != getLocalStorageCdPlaying()" :cd="list.find(cd => cd.position == (n))" :position="(n)" :key="keyUpdate" />
            <CdDisplay v-else :active="false"/>

            <CdDisplay v-if="getLocalStorageIsPlaying() && getLocalStorageCdPlaying() == (2 + n)" :active="false" />
            <CdDisplay v-else :cd="list.find(cd => cd.position == (2 + n))" :position="(2 + n)" :key="keyUpdate" />
        </div>

        <div v-if="!isOnServer && cdPlayingPosition == 0" class="settings">
            <img :src="iconSettings" class="icon" @click="openSettings()" draggable="false">
        </div>

    </div>
</template>

<script>
import CdDisplay from './CdDisplay.vue';
import CdPlayer from './CdPlayer.vue';
import WallPlayer from './WallPlayer.vue';
import BorderPlayer from './BorderPlayer.vue';

import { eventBus } from '@/plugins/eventBus';

export default {
    name: 'AppWallDisplay',
    components: {
        CdDisplay,
        CdPlayer,
        WallPlayer,
        BorderPlayer
    },
    props: {
        list: Array,
    },
    watch: {
        list: function () { // watch it
            this.keyUpdate++
        }
    },
    created() {
        if (localStorage.cdPlaying != 0) {
            this.cdPlayingPosition = localStorage.cdPlaying
        }

        eventBus.on('waitingScreen', (data) => {
            this.cdPlayingPosition = localStorage.cdPlaying
            this.keyUpdate++
        })

        eventBus.on('refresh', (data) => {
            this.keyUpdate++
        })
    },
    data() {
        return {
            keyUpdate: 0,
            cdPlayingPosition: 0,
        }
    },
    methods: {
        openSettings() {
            eventBus.emit('openSettings')
        },
        getLocalStorageCdPlaying() {
            return localStorage.cdPlaying == undefined ? 0 : localStorage.cdPlaying
        },
        getLocalStorageIsPlaying() {
            return localStorage.isPlaying == undefined ? false : localStorage.isPlaying == 'true' ? true : false
        },
        getLocalStorageIsPlayerOpen() {
            return localStorage.isPlayerOpen == undefined ? false : localStorage.isPlayerOpen == 'true' ? true : false
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div component */
.div-wall-display {
    height: 100%;
    width: -webkit-fill-available;

    display: flex;
    justify-content: center;

    background-color: var(--background-color-black-2);
    border-radius: 5px;
    padding: 0 10px;

    z-index: 0;
}

@media (max-width: 800px) {
    .div-wall-display {
        height: auto;
        margin-top: 34vh;
    }
}

.col-display {
    height: 100%;
    width: fit-content;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 0px 5px;
    align-items: center;
    justify-content: center;
}


.settings {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 1;
}
</style>