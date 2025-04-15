<script setup>
const iconClose = new URL('@/assets/icons/close_white.png', import.meta.url).href
</script>

<template>
    <div v-if="open" class="div-settings">
        <img :src="iconClose" class="icon icon-close" @click="open = false" draggable="false">

        <div class="div-settings-content">
            <div class="div-settings-bluetooth">
                <p>Bluetooth</p>
                <div>
                    <p>Liste des périphériques disponible : </p>
                    <p v-for="periph in listBluetoothPeriph" :key="periph.id">{{ periph }}</p>
                </div>

            </div>

            <div class="div-settings-artists">
                <p>Gestion des images des artises</p>
                <div>
                    <p>Liste des périphériques disponible : </p>
                    <p v-for="artist in listArtists" :key="artist.id">{{ artist }}</p>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus';
import api from '@/plugins/api';

export default {
    name: 'AppSetting',
    mounted() {
        eventBus.on('openSettings', () => {
            this.open = true;
        })
    },
    data() {
        return {
            open: false,
            listArtists: ["Zamdane", "Freeze", "Luv Resval", "Gizo Ecoracci", "Dr .Dre", "Bekar", "Bob Marley", "Zuukou Mayzie", "Youv Dee", "Disiz"],
            listBluetoothPeriph: ["Bose", "CR4XBT", "JBL"],
        }
    },
    methods: {


    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-settings {
    position: fixed;
    top: 0;
    right: 0;

    height: 100vh;
    width: 100vw;

    padding: 10px;
}

.div-settings-content {
    height: 100%;
    width: 100%;

    border-radius: 5px;
    background-color: var(--background-color-black-3);

    
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: column;
}

.div-settings-bluetooth {
    height: 35vh;
    width: 50vw;
}

.div-settings-artists {
    margin-top: 10px;
    height: 60vh;
    width: 50vw;
}

</style>