<script setup>
const iconPlay = new URL('@/assets/icons/play_white.png', import.meta.url).href
const iconPause = new URL('@/assets/icons/pause_white.png', import.meta.url).href
const iconNext = new URL('@/assets/icons/next_white.png', import.meta.url).href
const iconClose = new URL('@/assets/icons/close_white.png', import.meta.url).href
</script>

<template>
    <div v-if="cd != undefined" class="div-cd-player">
        <img :src="imageSrc" class="album-class_img" id="album_played" @error="imgSrcNotFound()"
            @click.stop="openBackScreen()" draggable="false">
        <div class="div-cd-player-icons">
            <img :src="iconNext" class="icon icon-player icon-prev" @click="prev()" draggable="false">
            <img v-if="isPlaying" :src="iconPause" class="icon icon-player" @click="pause()" draggable="false">
            <img v-else :src="iconPlay" class="icon icon-player" @click="play()" draggable="false">
            <img :src="iconNext" class="icon icon-player" @click="next()" draggable="false">
            <!-- <button>Barre niveau de son</button> -->
            <div class="volume-slider">
                <input type="range" min="0" max="100" step="1" v-model="soundValue" @change="updateSoundValue"
                    class="slider" />
            </div>
        </div>
        <img :src="iconClose" class="icon icon-close" @click="stop()" draggable="false">
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus'
import api from '@/plugins/api';

export default {
    name: 'AppCdPlayer',
    props: {
        cd: Object,
    },
    mounted() {
        try {
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        } catch (error) {
            // Fermer, et ouvrir le toast avec message erreur
        }

        this.soundValue = localStorage.soundValue == undefined ? 30 : localStorage.soundValue

        // Permet de lancer la rotation si le cd était joué
        this.isPlaying = localStorage.isPlaying == undefined ? false : localStorage.isPlaying == 'true' ? true : false

        if (this.isPlaying || localStorage.previousCd != localStorage.cdPlaying) this.startTurningCd()
        localStorage.previousCd = localStorage.cdPlaying

        eventBus.emit('backScreen', { "artiste": this.cd.artiste }) // On met à jour l'artiste sur le backScreen

    },
    data() {
        return {
            imageSrc: '',
            cdPlaying: 0,
            isPlaying: true,
            soundValue: 0
        }
    },
    methods: {
        imgSrcNotFound() {
            this.imageSrc = new URL('@/assets/albums/default.webp', import.meta.url).href
        },
        openBackScreen() {
            eventBus.emit('backScreenOpen', { "isOpen": true }) // On met à jour l'artiste sur le backScreen
        },
        stop() {
            eventBus.emit("waitingScreen", { "bool": true })      // Active animation du chargemeent de la pause
            api.postApiJukebox('pause')
                .then((res) => {
                    localStorage.cdPlaying = 0
                    eventBus.emit("waitingScreen", { "bool": false })     // Arrête animation de la pause
                    eventBus.emit('backScreen', { "artiste": '' }) // On met à jour l'artiste sur le backScreen
                })
        },
        play() {
            api.postApiJukebox(`play/${this.cdPlaying}`)
                .then((res) => this.startTurningCd())
                .catch((err) => console.log(err))
        },
        pause() {
            api.postApiJukebox('pause')
                .then((res) => this.stopTurningCd())
                .catch((err) => console.log(err))
        },
        next() {
            api.postApiJukebox('next')
                .catch((err) => console.log(err))
        },
        prev() {
            api.postApiJukebox('prev')
                .catch((err) => console.log(err))
        },
        startTurningCd() {
            this.isPlaying = true
            localStorage.isPlaying = true

            try {
                document.getElementById('album_played').classList.add('zooming-cd')
            } catch (error) {

            }
        },
        stopTurningCd() {
            this.isPlaying = false
            localStorage.isPlaying = false

            try {
                document.getElementById('album_played').classList.remove('zooming-cd')
            } catch (error) {

            }
        },
        updateSoundValue() {
            localStorage.soundValue = this.soundValue
            api.postApiJukebox(`sound_update/${this.soundValue}`)
                // .then((res) => this.startTurningCd())
                .catch((err) => console.log(err))
        }

    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-cd-player {
    width: 100%;
    height: 100%;

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    z-index: 50;
}

/* Affichage album */
.album-class_img {
    width: 50vh;
    height: 50vh;

    /* border-radius: 50%; */
    border-radius: 5%;
    transition: 0.3s;
}

@media (max-width: 800px) {
    .div-cd-player {
        position: absolute;
        top: 0;
        left: 0;

        height: 100vh;
        width: 100vw;

        background-color: var(--background-color-black-2);
    }

    .album-class_img {
        height: auto !important;
        width: 80vw !important;
    }

}

@media (min-width: 800px) {
    .album-class_img:hover {
        animation: none;    /* Permet a la transformation au hover de se faire */
        transform: scale(1.03);
        cursor: pointer;
    }
}




.zooming-cd {
    animation: zoomInOut 3s ease-in-out infinite;
}

@keyframes zoomInOut {
    0% {
        transform: scale(1);
    }
    25% {
        transform: scale(1.02);
    }
    50% {
        transform: scale(1);
    }
}


.div-cd-player-icons {
    width: max-content;
    margin: 25px 0px;
    margin-top: 100px;

}

.icon-player {
    width: 40px !important;
    height: 40px !important;
    margin: 0px 10px;
}

.icon-prev {
    rotate: 180deg;
}

.icon-close {
    position: absolute;
    top: 20px;
    right: 20px;
}


.slider {
    accent-color: var(--background-color-black-4);
}
</style>