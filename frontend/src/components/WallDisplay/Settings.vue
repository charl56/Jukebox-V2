<script setup>
const iconClose = new URL('@/assets/icons/close_white.png', import.meta.url).href
</script>

<template>
    <div v-if="open" class="div-settings">
        <img :src="iconClose" class="icon icon-close" @click="open = false" draggable="false">

        <div class="div-settings-content">

            <h3>Contrôle manuel</h3>
            <div class="div-settings-manual-movements">
                <div class="control">
                    <h5>Axe X</h5>
                    <button @click="move('X', 'cw')">-</button>
                    <button @click="move('X', 'ccw')">+</button>
                </div>

                <!-- Axe Y -->
                <div class="control">
                    <h5>Axe Y</h5>
                    <button @click="move('Y', 'cw')">-</button>
                    <button @click="move('Y', 'ccw')">+</button>
                </div>

                <!-- Axe Z -->
                <div class="control">
                    <h5>Axe Z</h5>
                    <button @click="move('Z', '30')">-</button>
                    <button @click="move('Z', '80')">+</button>
                </div>

                <!-- Axe Z -->
                <div class="control">
                    <h5>Aimant</h5>
                    <button @click="toggleMagnet()">On/Off</button>
                </div>
            </div>

            
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
import api from '@/plugins/api.js';

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
            electromagnetState: false,
            listBluetoothPeriph: ["Bose", "CR4XBT", "JBL"],
            listArtists: ["Zamdane", "Freeze", "Luv Resval", "Gizo Ecoracci", "Dr .Dre", "Bekar", "Bob Marley", "Zuukou Mayzie", "Youv Dee", "Disiz"],
        }
    },
    methods: {
        move(axis, direction) {
            let command = `MOVE_${axis}_${direction}`;
            api.postApiManual('command', { command: command })
                .then((resp) => {
                    console.log(`Command ${command} sent successfully.`);
                })
                .catch((error) => {
                    console.error(`Error sending command ${command}:`, error);
                });
        },
        toggleMagnet() {
            let command = `TOGGLE_MAGNET_${this.electromagnetState}`;
            this.electromagnetState = !this.electromagnetState;
            api.postApiManual('command', { command: command })
                .then((resp) => {
                    console.log(`Command ${command} sent successfully.`);
                })
                .catch((error) => {
                    console.error(`Error sending command ${command}:`, error);
                });
        },
      


    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.div-settings {
    position: fixed;
    top: 0;
    right: 0;

    height: 100vh;
    width: 100vw;

    padding: 10px;
    z-index: 2;
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


.div-settings-manual-movements{
    display: flex;
    flex-wrap: wrap;
    margin: 2vh 0 5vh 0;
    justify-content: center;

    div {
        width: 150px;
    }
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


button {
    margin: 0 5px;
    padding: 5px 10px;

    border: none;
    border-radius: 5px;
    background-color: var(--background-color-black-2);
    color: var(--text-color-white);

    font-size: 1rem;
    cursor: pointer;
}
button:hover {
    background-color: var(--background-color-black-1);
    transform: scale(1.05);
    transition: transform 0.2s;
}
button:active {
    transform: scale(0.95);
    transition: transform 0.1s;
}

</style>