<script setup>
const iconPlay = new URL('@/assets/icons/play_white.png', import.meta.url).href
const iconPause = new URL('@/assets/icons/pause_white.png', import.meta.url).href
const iconNext = new URL('@/assets/icons/next_white.png', import.meta.url).href
</script>

<template>
    <div v-if="cd != undefined" class="div-cd-player">
        <img :src="imageSrc" class="album-class_img" id="album_played" @error="imgSrcNotFound()" @click.stop="stop()">
        <div class="div-cd-player-icons">
            <img :src="iconNext" class="icon icon-player icon-prev" @click="prev()">
            <img v-if="isPlaying" :src="iconPause" class="icon icon-player" @click="pause()">
            <img v-else :src="iconPlay" class="icon icon-player" @click="play()">
            <img :src="iconNext" class="icon icon-player" @click="next()">
        </div>
        <button>Barre niveau de son</button>
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus'
import api from '@/plugins/api';

export default {
    watch: {
    },
    name: 'AppCdPlayer',
    props: {
        cd: Object,
    },
    mounted() {
        try {
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        } catch (error) {
        }

        this.startTurningCd()
    },
    data() {
        return {
            imageSrc: '',
            cdPlaying: 0,
            isPlaying: true,
        }
    },
    methods: {
        imgSrcNotFound() {
            this.imageSrc = new URL('@/assets/albums/default.webp', import.meta.url).href
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
            console.log("play")
            api.postApiJukebox(`play/${this.cdPlaying}`)
                .then((res) => this.startTurningCd())
                .catch((err) => console.log(err))
        },
        pause() {
            console.log("plause")

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

            try {
                document.getElementById('album_played').classList.add('turning-cd')
            } catch (error) {

            }
        },
        stopTurningCd() {
            this.isPlaying = false

            try {
                document.getElementById('album_played').classList.remove('turning-cd')
            } catch (error) {

            }
        },

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
}

@media (max-width: 800px) {
    .div-cd-player {
        width: 14vh;
        height: 14vh;
    }

}

@media (min-width: 800px) {
    .album-class_img:hover {
        transform: scale(1.03);
        cursor: pointer;
    }
}


/* Affichage album */
.album-class_img {
    border-radius: 50%;
    width: 100%;
    height: 100%;
    transition: 0.3s;

    width: 50vh;
    height: 50vh;
}


.turning-cd {
    animation: turn 12s infinite linear forwards;
}

@keyframes turn {
    to {
        rotate: 1turn
    }
}

.div-cd-player-icons {
    margin: 25px 0px;
}

.icon-player {
    width: 5vh;
    height: 5vh;
    margin: 0px 10px;
}

.icon-prev {
    rotate: 180deg;
}
</style>