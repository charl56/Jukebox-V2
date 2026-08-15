<template>
    <div v-if="cd != undefined" class="div-cd-display">
        <img :src="imageSrc" class="album-class rotation" @error="imgSrcNotFound()"
            @click.stop="removeThisAlbum()" draggable="false">
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus'
import api from '@/plugins/api';

export default {
    name: 'AppWallPlayer',
    props: {
        cd: Object,
    },
    mounted() {
        try {
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        } catch (error) {
            // Fermer, et ouvrir le toast avec message erreur
        }

        // // Permet de lancer la rotation si le cd était joué
        this.isPlaying = localStorage.isPlaying == undefined ? false : localStorage.isPlaying == 'true' ? true : false
    },
    data() {
        return {
            imageSrc: '',
        }
    },
    methods: {
          removeThisAlbum() {
            eventBus.emit("waitingScreen", { "bool": true })      // Active animation du chargemeent de la pause

            api.postApiJukebox(`play/${localStorage.cdPlaying}`)
                .then((res) => {
                        localStorage.cdPlaying = 0
                        localStorage.isPlaying = false
                        localStorage.isPlayerOpen = false
                })
                .catch((err) => console.log(err))
                .finally(() => eventBus.emit("waitingScreen", { "bool": false }))
        },
        imgSrcNotFound() {
            this.imageSrc = new URL('@/assets/albums/default.webp', import.meta.url).href
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.rotation {
    animation: rotate 8s linear infinite;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
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





</style>