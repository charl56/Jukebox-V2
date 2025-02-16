<template>
    <div class="div-wall-display">
        <div v-if="waitCdPause" class="waiting-screen d-flex align-center justify-center">
            <div class="d-flex align-center justify-center">
                <p class="text-subtitle-1">Chargement de {{ albumNameLoad }}</p>
            </div>
        </div>
        <!-- Afficha grille avec CDs et lecteur -->
        <div class="col-display" v-for="n in 3">
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 2))" :position="(3 * n - 2)" :key="keyUpdate" />
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n - 1))" :position="(3 * n - 1)" :key="keyUpdate" />
            <CdDisplay :cd="list.find(cd => cd.position == (3 * n))" :position="(3 * n)" :key="keyUpdate" />
        </div>
    </div>
</template>

<script>
import CdDisplay from './CdDisplay/CdDisplay.vue';
import PlayerDisplay from './PlayerDisplay/PlayerDisplay.vue'
import { eventBus } from '../../plugins/eventBus';

export default {
    name: 'AppWallDisplay',
    components: {
        CdDisplay,
        PlayerDisplay,
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
        eventBus.on('waitCdPause', (data) => {
            if (data.bool) {
                this.waitCdPause = data.bool
                this.movement = data.movement
                this.albumNameLoad = data.name
            } else {
                this.waitCdPause = data.bool
                this.movement = data.movement
            }
        })
    },
    data() {
        return {
            keyUpdate: 0,
            waitCdPause: false,
            albumNameLoad: '',
            movement: '',
        }
    },
    methods: {

    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div component */
.div-wall-display {
    display: flex;
    height: 100%;
    width: -webkit-fill-available;

    display: flex;
    justify-content: center;

    background-color: var(--background-color-black-2);
    border-radius: 5px;
    padding: 10px;
}




.col-display {
    height: 100%;
    width: fit-content;
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    justify-content: center;
}

.col-display:nth-child(even) {
    padding-bottom: 100px;
}

.col-display:nth-child(odd) {
    padding-top: 100px;
}

/* Ecran de chargement */
.waiting-screen {
    z-index: 999;
    border-radius: 5px;
    backdrop-filter: blur(2px) invert(80%);
    width: 72vw;
    height: 93vh;
    position: absolute;
}

/* Rond de chargement en attendant les photos
.lds-dual-ring {
    display: inline-block;
    width: 150px;
    height: 150px;
    animation: change-size 2.5s linear infinite;
}

@keyframes change-size {
    0% {
        width: 150px;
        height: 150px;
    }

    50% {
        width: 185px;
        height: 185px;
    }

    100% {
        width: 150px;
        height: 150px;
    }
}

.lds-dual-ring div {
    content: "";
    display: flex;
    width: 100%;
    height: 100%;
    border: 6px solid #fff;
    border-radius: 50%;
    border-color: var(--background-color-black-4) transparent var(--background-color-black-4) transparent;
    color: var(--background-color-black-4);
    animation: lds-dual-ring 4s linear infinite;
}

@keyframes lds-dual-ring {
    0% {
        transform: rotate(0deg);
        border-radius: 50%;
    }

    50% {
        border-radius: 0px;
    }

    100% {
        transform: rotate(360deg);
        border-radius: 50%;
    }
} */
</style>