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
import { eventBus } from '@/plugins/eventBus';

export default {
    name: 'AppWallDisplay',
    components: {
        CdDisplay,
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
    z-index: 999;
    border-radius: 5px;
    backdrop-filter: blur(2px) invert(80%);
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}
</style>