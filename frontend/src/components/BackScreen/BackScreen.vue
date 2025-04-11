<!-- Utilisation du composant : 

On l'importe dans le composant d'ou on l'appelle, puis une fonction qui se declenche au click par exemple

backScreen(){
    let data = {"artist": this.artist}
    eventBus.emit("backScreen", data)
} -->





<!-- Popup -->
<script setup>
const iconClose = new URL('@/assets/icons/close_white.png', import.meta.url).href
</script>
<template>
    <div v-if="open" class="div-back-screen d-flex justify-center align-item-center" @keyup="keyup" @mousemove="mouseMove" tabindex="0" v-focus :class="{ 'show-mouse': showCloseIcon }">
        <div class="div-image-back pulse-filter">
            <v-img :src="imageBackSrc" cover class="image-back"></v-img>
        </div>
        <div class="back-filter">
            <div class="trail-box"></div>
        </div>
        <div class="div-close-icon" :class="{ 'show-close-icon': showCloseIcon }">
            <v-img :src="iconClose" class="img-close-icon" @click="closeModal()"></v-img>
        </div>
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus';

export default {
    directives: {
        focus: {
            inserted: function (el) {
                el.focus()
            }
        }
    },
    created() {
        eventBus.on('backScreen', (data) => {
            this.open = true
            this.imageBackSrc = this.$backendPort + "images/artists/" + data.artist.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
        });
    },
    data() {
        return {
            open: false,
            imageBackSrc: '',
            showCloseIcon: true,
        }
    },
    beforeMount() {                 // Lance la fonction au chargement de la page

    },
    methods: {
        closeModal() {
            this.open = false
            this.imageBackSrc = ''
        },
        keyup(e) {
            if (e.key === 'Escape') {
                this.closeModal()
            }
        },
        mouseMove() {
            this.showCloseIcon = true;

            // Clear existing timer (if any)
            clearTimeout(this.hideCloseIconTimer);

            // Set a new timer to hide the close icon after 2 seconds
            this.hideCloseIconTimer = setTimeout(() => {
                this.showCloseIcon = false;
            }, 2000);
        },
    }
}
</script>

<style scoped>
/* Popup de fond */
.div-back-screen {
    z-index: 99;
    top: 0;
    left: 0;
    position: absolute;
    width: 100vw;
    height: 100vh;
    cursor: none;
}.show-mouse{
    cursor: default;
}

/* Image de fond */
.div-image-back {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
}

.image-back {
    width: 100%;
    height: 100%;
}

.album-back {
    width: 100px;
    height: 100px;
    border-radius: 5px;
}

.album-back:hover {
    transform: scale(1.1);
    cursor: none;
}

/* Filtre de 'gris' */
.back-filter {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}

.trail-box {
    position: absolute;
    /* top: 50%; */
    right: 0;
    width: 30px;
    height: 100%;
    /* Épaisseur du trait */
    background-color: rgba(0, 0, 0, 0.3);
    box-shadow: 0 0 10px 5px rgba(0, 0, 0, 0.3);
    animation: rotateTrail 5s infinite linear;
}

@keyframes rotateTrail {

    0% {
        transform: translateX(-100vw);
    }
}

/* Pusle effect */
.pulse-filter {
    animation: pulse 5s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.01);
    }
}

/* Image album */
.col-image-back {
    width: 10vw;
    height: 17vh;
}

/* Affichage des données */
.back-display {
    position: absolute;
    width: auto;
    height: auto;
    bottom: -3vh;
    left: 20vw;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
}

.col-display-data {
    width: 100%;
}

.max-content {
    width: max-content;
}

/* Texts */
.text-album {
    font-size: 5vh;
    font-weight: 600;
}

.text-album:hover {
    transform: scale(1.1);
    cursor: none;
}

.text-artist {
    font-size: 4vh;
    font-weight: 600;
}

.text-artist:hover {
    transform: scale(1.1);
    cursor: none;
}

/* Icon close  */
.div-close-icon {
    top: 30px;
    right: 30px;
    position: absolute;
    z-index: 100;
    opacity: 0;
}
.show-close-icon {
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
}
.img-close-icon {
    width: 30px;
    height: 30px;
}

.img-close-icon:hover {
    cursor: pointer;
    transform: scale(1.1);
}
</style>
