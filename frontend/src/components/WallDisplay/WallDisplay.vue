<script setup>
const iconSettings = new URL('@/assets/icons/settings_white.png', import.meta.url).href
const isOnServer = import.meta.env.VITE_CUSTOM_MODE || false

</script>

<template>
    <div class="div-wall-display">
        <CdPlayer v-if="cdPlayingPosition != 0" :cd="list.find(cd => cd.position == cdPlayingPosition)" />
            
        
            <!-- <div v-else class="col-display" v-for="n in 3" :key="n"> -->
            <!-- <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 2))" :position="(3 * n - 2)" :key="keyUpdate" /> -->
            <!-- <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 1))" :position="(3 * n - 1)" :key="keyUpdate" /> -->
            <!-- <CdDisplay :cd="list.find(cd => cd.position == (3 * n))" :position="(3 * n)" :key="keyUpdate" /> -->
        
        
        <!-- Affiche grille avec CDs et lecteur -->
        <div v-else class="col-display" v-for="n in 2" :key="n">
            <CdDisplay :cd="list.find(cd => cd.position == (2 * n - 1))" :position="(2 * n - 1)" :key="keyUpdate" />
            <CdDisplay v-if="(2 * n) != 2" :cd="list.find(cd => cd.position == (2 * n))" :position="(2 * n)" :key="keyUpdate" />
            <CdDisplay v-else :active="false" />
        </div>

        <div v-if="!isOnServer && cdPlayingPosition == 0" class="settings">
            <img :src="iconSettings" class="icon" @click="openSettings()" draggable="false">
        </div>

    </div>
</template>

<script>
import CdDisplay from './CdDisplay.vue';
import CdPlayer from './CdPlayer.vue';

import { eventBus } from '@/plugins/eventBus';

export default {
    name: 'AppWallDisplay',
    components: {
        CdDisplay,
        CdPlayer,
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
    padding: 10px;

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