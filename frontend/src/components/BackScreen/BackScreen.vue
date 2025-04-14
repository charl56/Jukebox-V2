<script setup>
const iconClose = new URL('@/assets/icons/close_white.png', import.meta.url).href
const iconOpen = new URL('@/assets/icons/full_screen_white.png', import.meta.url).href
</script>
<template>
    <div v-if="open" class="div-back-screen d-flex justify-center align-item-center" @keyup="keyup"
        @mousemove="mouseMove" tabindex="0" v-focus :class="{ 'show-mouse': showCloseIcon }">
        <div class="div-image-back pulse-filter">
            <v-img :src="imageBackSrc" cover class="image-back"></v-img>
        </div>
        <div class="back-filter">
            <div class="trail-box"></div>
        </div>
        <div class="div-close-icon" :class="{ 'show-close-icon': showCloseIcon }">
            <v-img :src="iconClose" class="icon" @click="closeModal()"></v-img>
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
        this.artiste = localStorage.artiste

        eventBus.on('backScreen', (data) => {
            this.artiste = data.artiste
            localStorage.artiste = this.artiste
        });

        eventBus.on('backScreenOpen', () => {
            this.open = true
            this.imageBackSrc = this.$backendPort + "images/artists/" + localStorage.artiste.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        })
    },
    data() {
        return {
            open: false,
            imageBackSrc: '',
            showCloseIcon: true,
            artiste: '',
        }
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

            if (window.innerWidth < 800) return;

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
}

.show-mouse {
    cursor: default;
}

.div-back-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 99;
}

@media (max-width: 800px) {
    .div-back-btn {
        top: 36vh;
    }
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

/* Icon close  */
.div-close-icon {
    top: 20px;
    right: 20px;
    position: absolute;
    z-index: 100;
    opacity: 0;
}

.show-close-icon {
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
}
</style>
