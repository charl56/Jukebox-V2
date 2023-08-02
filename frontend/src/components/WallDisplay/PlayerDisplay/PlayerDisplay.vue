<script setup>
    const iconStop = new URL('../../../assets/icons/stop_white.png', import.meta.url).href
    const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
    const iconPause = new URL('../../../assets/icons/pause_white.png', import.meta.url).href
</script>
<template>
    <div class="div-player-display d-flex flex-column justify-space-between">
        <v-row class="display-cd d-flex align-center justify-center pa-0">
            <v-img v-if="cdInPlayer" :src="imageSrc" class="cd-in-player" @error="imgSrcNotFound()"></v-img>
        </v-row>
        <v-row class="display-btns d-flex align-end pb-2 px-5 mt-0">
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconStop" class="display-icon" @click="closeModal()" title="Remettre le cd à sa place"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPlay" class="display-icon" @click="closeModal()" title="Lancer le cd en place"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPause" class="display-icon" @click="closeModal()" title="Mettre en pause le cd en place"></v-img>
            </v-col>
        </v-row>
    </div>
</template>
  
<script>
import { eventBus } from '../../../plugins/eventBus';

export default {
    name: 'AppPlayerDisplay',
    components: {
    },
    props: {
        id: Number,
    },
    created(){
        eventBus.on("displayPlayer", (data) => {
            this.cdInPlayer = data.bool
            this.imageSrc = new URL("../../../assets/albums/"+data.name.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e") + ".jpg", import.meta.url).href
        })
    },
    data () {
        return {
            imageSrc: '',
            cdInPlayer: false,
        }
    },
    methods:{
        
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-player-display{
    width: 100%;
    height: 28vh;
    background-color: #121212;
}
/* Icons play/pause/stop */
.display-btns{
    height: min-content;
}
.col-display-btns{
    height: min-content;
}
.display-icon{
    width: 40px;
    height: 40px;
}.display-icon:hover{
    cursor: pointer;
    background-color: rgba(107, 107, 107, 0.4);
    border-radius: 5px;
    margin-bottom: 3px;
}
/* Affichae cd in player */
.display-cd{
    height: 100%;
    width: 100%;
}.cd-in-player{
    height: 60%;
    width: 60%;
}
</style>