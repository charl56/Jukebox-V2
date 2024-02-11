<script setup>
    const iconStop = new URL('../../../assets/icons/stop_white.png', import.meta.url).href
    const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
    const iconPause = new URL('../../../assets/icons/pause_white.png', import.meta.url).href
</script>
<template>
    <div class="div-player-display d-flex flex-column align-center justify-space-between">
        <div class="div-display-cd d-flex align-center justify-center ">
            <v-img v-if="cdInPlayer" :src="imageSrc" cover class="cd-in-player rotate" id="rotate-effect" @error="imgSrcNotFound()" @click="backScreen()"></v-img>
            <div v-if="cdInPlayer" class="round-middle"></div>
        </div>
        <div class="row-display-btns d-flex align-end pb-0 px-2 mx-4 mt-2">
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconStop" class="display-icon" @click="stop()" title="Remettre le cd à sa place"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPlay" class="display-icon" @click="play()" title="Lancer le cd en place"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPause" class="display-icon" @click="pause()" title="Mettre en pause le cd en place"></v-img>
            </v-col>
        </div>
        <BackScreen />
    </div>
</template>
  
<script>
import { eventBus } from '../../../plugins/eventBus';
import axios from 'axios';
import BackScreen from './BackScreen/BackScreen.vue'

export default {
    name: 'AppPlayerDisplay',
    components: {
        BackScreen,
    },
    created(){
        eventBus.on("displayPlayer", (data) => {
            this.cdInPlayer = data.bool
            this.albumName = data.name
            this.artist = data.artist
            this.imageSrc = this.$backendPort + "images/albums/"+this.albumName.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
        })
    },
    data () {
        return {
            imageSrc: '',
            cdInPlayer: false,
            albumName: '',
            artist: '',
        }
    },
    methods:{
        play(){
            if(this.cdInPlayer){
                axios.post(this.$backendPort + "playMusic")
                .then((resp) => {
                    this.setAnimation(true)
                })
                .catch((err) => console.log(err))
            }
        },
        pause(){    // Mettre en pause le cd actuel
            if(this.cdInPlayer){
                axios.post(this.$backendPort + "pauseMusic")
                .then((resp) => {
                    this.setAnimation(false)
                })
                .catch((err) => console.log(err))
            }
        },
        stop(){
            if(this.cdInPlayer){
                eventBus.emit("waitCdPause", {"bool" : true, "name": this.albumName, "movement": "Enlèvement" })      // Active animation du chargemeent de la pause
                axios.post(this.$backendPort + "removeFromPlayer")
                .then(() => {
                    this.imageSrc = ''      // On enleve la src de l'image
                    this.cdInPlayer = false;    // Plus de cd dans le lecteur
                    eventBus.emit("waitCdPause", {"bool" : false, "name": '' })      // Desactive animation du chargemeent de la pause
                })
                .catch((err) => console.log(err))
            }
        },
        setAnimation(bool){
            let element = document.getElementById("rotate-effect")
            bool ? element.classList.add("rotate") : element.classList.remove("rotate")
        },
        backScreen(){
            let data = {"albumName": this.albumName, "artist": this.artist}
            eventBus.emit("backScreen", data)
        }
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
.row-display-btns{
    height: 4vh;
}
.col-display-btns{
    height: 100%;
}
.display-icon{
    width: 40px;
    height: 40px;
}.display-icon:hover{
    cursor: pointer;
    border-radius: 5px;
    transform: scale(1.1);
}
/* Affichae cd in player */
.div-display-cd{
    height: 24vh !important;
    width: 24vh !important;
}.div-display-cd:hover{
    transform: scale(1.03);
}.cd-in-player{
    height: 100%;
    width: 100%;
    border-radius: 50%;
}.cd-in-player:hover{
    cursor: pointer;
}.rotate{
    animation: rotate-cd 5s linear 200ms infinite; 
}@keyframes rotate-cd {
    0%{
        transform: rotate(0deg);
    }
    100%{
        transform: rotate(360deg);
    }
}
/* Round au milieu de  */
.round-middle{
    z-index: 10;
    position: fixed;
    background-color: var(--background-color-black-4);
    width: 20px;
    height: 20px;
    border-radius: 50%;
}.round-middle:hover{
    cursor: pointer;
}
</style>