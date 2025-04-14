<template>
    <div class="div-wall-display">
        <div v-if="waitingScreen" :class="{ active: waitingScreen }" class="waiting-screen d-flex align-center justify-center">
            <!-- Animation from : https://codepen.io/ashamallah/pen/YzXdpJy -->
            <div class="loading-animation"></div>
        </div>

        <CdPlayer v-if="cdPlayingPosition != 0" :cd="list.find(cd => cd.position == cdPlayingPosition)"/>
        <!-- Affiche grille avec CDs et lecteur -->
        <div v-else class="col-display" v-for="n in 3">
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 2))" :position="(3 * n - 2)" :key="keyUpdate" />
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 1))" :position="(3 * n - 1)" :key="keyUpdate" />
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n))" :position="(3 * n)" :key="keyUpdate" />
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
            if (data.bool) {
                this.waitingScreen = data.bool
            } else {
                this.waitingScreen = data.bool
            }
            this.cdPlayingPosition = localStorage.cdPlaying
        })
    },
    data() {
        return {
            keyUpdate: 0,
            waitingScreen: false,
            cdPlayingPosition: 0,
        }
    },
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


/* Ecran de chargement */
.waiting-screen {
    position: absolute;
    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    z-index: 999;
    backdrop-filter: blur(0px) saturate(100%) brightness(100%);
}

.waiting-screen.active {
    backdrop-filter: blur(15px);
    transition: backdrop-filter 1s ease;
}

.loading-animation {
    width: 150px;
    height: 150px;

    background: url('@/assets/gifs/loader.gif') center no-repeat;
}
</style>