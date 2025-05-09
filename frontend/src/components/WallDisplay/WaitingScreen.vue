<template>
    <div v-if="waitingScreen" :class="{ active: waitingScreen }"
        class="waiting-screen d-flex align-center justify-center">
        <!-- Animation from : https://codepen.io/ashamallah/pen/YzXdpJy -->
        <div class="loading-animation"></div>
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus';

export default {
    name: 'AppWallDisplay',
    created() {
        eventBus.on('waitingScreen', (data) => {
            this.waitingScreen = data.bool
        })
    },
    data() {
        return {
            waitingScreen: false,
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Ecran de chargement */
.waiting-screen {
    position: fixed;
    top: 0;
    right: 0;

    height: 100vh;
    width: 100vw;

    padding: 10px;
    z-index: 5;
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