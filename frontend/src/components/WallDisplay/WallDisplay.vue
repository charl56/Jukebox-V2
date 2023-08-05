<template>
    <div class="div-wall-display d-flex flex-column pa-3 ma-1">
        <div v-if="waitCdPause" class="waiting-screen d-flex align-center justify-center">
            <div class="lds-dual-ring">
                <div class="d-flex align-center justify-center">
                    <p class="text-subtitle-1">{{ movement }} de {{ albumNameLoad }}</p>
                </div>
            </div>        
        </div>
        <!-- Afficha grille avec CDs et lecteur -->
        <v-row v-for="n in 3" :key="keyUpdate">
            <v-col>
                <CdDisplay :cd="list.find(cd => cd.position == (3*n - 2))" :position="(3*n - 2)"/>
            </v-col>
            <v-col>
                <PlayerDisplay v-if="(3*n - 1 == 5)" />
                <CdDisplay v-else :cd="list.find(cd => cd.position == (3*n - 1))" :position="(3*n - 1)"/>
            </v-col>
            <v-col>
                <CdDisplay :cd="list.find(cd => cd.position == (3*n))" :position="(3*n)"/>
            </v-col>
        </v-row>
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
        list: function() { // watch it
            this.keyUpdate ++
        }
    },
    created(){
        eventBus.on('waitCdPause', (data) => {
            if(data.bool){
                this.waitCdPause = data.bool
                this.movement = data.movement
                this.albumNameLoad = data.name
            } else {
                this.waitCdPause = data.bool
                this.movement = data.movement
            }
        })
    },
    data () {
        return {
            keyUpdate: 0,
            waitCdPause: false,
            albumNameLoad: '',
            movement: '',
        }
    },
    methods:{
        
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div component */
.div-wall-display{
    height: 96vh;
    background-color: var(--background-color-black-2);
    border-radius: 5px;
}
/* Ecran de chargement */
.waiting-screen{
    z-index: 999;
    border-radius: 5px;
    backdrop-filter: blur(2px) invert(80%);
    width: 72vw;
    height: 93vh;
    position: absolute;
}
/* Rond de chargement en attendant les photos */
.lds-dual-ring {
  display: inline-block;
  width: 150px;
  height: 150px;
  animation: change-size 2.5s linear infinite;
}@keyframes change-size {
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
}@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
    border-radius: 50%;
  }
  50%{
    border-radius: 0px;
  }
  100% {
    transform: rotate(360deg);
    border-radius: 50%;
  }
}
</style>