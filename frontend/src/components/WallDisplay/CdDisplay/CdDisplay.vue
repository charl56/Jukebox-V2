<script setup>
    const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
</script>
<template>
    <div v-if="cd != undefined" class="div-cd-wall d-flex flex-column justify-space-between align-center" @click="openCdOnWall()" draggable="true" @dragstart="drag(cd)" @drop="onDrop(position, $event)" @dragover="allowDrop($event)">
        <div class="cube-container d-flex align-center justify-center pt-2">
            <div class="cube d-flex align-center justify-center">
                <!-- Les 2 images du cube qui pivote -->
                <div class="display-cd-img d-flex align-center justify-center px-2">
                    <v-img :src="imageSrc" class="album-class rounded" @error="imgSrcNotFound()"></v-img>
                </div>
                <div class="div-btn-play d-flex align-center justify-center">
                    <v-img :src="iconPlay" class="img-play-btn" @click.stop="playThisAlbum()"></v-img>
                </div>
            </div>
        </div>
        <!-- Affichage du nom de l'album et l'artiste -->
        <div class="row-display-cd-data">
            <div>
                <p class="text-subtitle-1 font-weight-bold">{{ cd.albumName }}</p>
            </div>
            <div>
                <p class="text-subtitle-2">{{ cd.artiste }}</p>
            </div>
        </div>
    </div>
    <div v-else class="div-cd-wall" @drop="onDrop(position, $event)" @dragover="allowDrop($event)">
    </div>

</template>
  
<script>
import { eventBus } from '../../../plugins/eventBus'
import axios from 'axios';
import { drag, drop, allowDrop } from '../../../plugins/dragNdrop';

export default {
    name: 'AppCdDisplay',
    props: {
        cd: Object,
        position: Number
    },
    created(){
        try {
            this.imageSrc = this.$backendPort + "images/albums/"+this.cd.albumName.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
        } catch (error) {
            
        }
    },
    data () {
        return {
            imageSrc: ''
        }
    },
    methods:{
        openCdOnWall(){
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {"data":
                    this.cd,
                "function": "Edit"
            }); 
        },
        imgSrcNotFound(){       // Si image album pas trouvée
            this.imageSrc = new URL('../../../assets/albums/default.jpg', import.meta.url).href
        },
        playThisAlbum(){        // C'est le nom de la fonction
            // let confirm = window.confirm("Lancer ce cd ?")
            // if(confirm){
                eventBus.emit("waitCdPause", {"bool" : true, "name": this.cd.albumName, "movement": "Chargement"})      // Active animation du chargemeent de la pause
                axios.post(this.$backendPort + "playThisCd", {"data": this.cd.position})
                    .then(() => {
                        eventBus.emit("waitCdPause", {"bool": false, "name": ''})     // Arrête animation de la pause
                        eventBus.emit("displayPlayer", {"bool": true, "name": this.cd.albumName, "artist": this.cd.artiste})     // Affichage du lecteur cd 
                    })
                    .catch((err) => console.log(err))
            // }
        },
        onDrop(pos){
            // On recupere le cd drag
            let newCd = drop()
            // On recupre la liste de tous les albums
            let listCds = JSON.parse(localStorage.dataList) // On met a jour la liste
            // On check si CD sur cette position
            let index = listCds.findIndex((cd) => cd.position == pos)
            // Si pas de cd à la position, le cd drag prend la position
            if(index == -1){
                let index2 = listCds.findIndex((cd) => cd.albumName == newCd.albumName)
                listCds[index2].position = pos
            } else { // On inverse la position du cd drag, et celui à la place
                // nouvelle position du cd dragNdrop
                let posCdDrag = newCd.position  // Pos du cd drag, avant le drop
                // On récupère d'abord les indexs
                let indexDrop = listCds.findIndex((cd) => cd.albumName == newCd.albumName)
                let indexInverse = listCds.findIndex((cd) => cd.position == pos)
                // Ensuite on met a jour dans la liste
                listCds[indexDrop].position = pos
                listCds[indexInverse].position = posCdDrag
            }
            // On remet la liste en localStorage, pour pouvoir refresh
            localStorage.dataList = JSON.stringify(listCds, null, 2) // On met a jour la liste
            // On actualise la liste dans l'app
            eventBus.emit('updateLists')
        }
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-cd-wall{
    background-color: #181818;
    border-radius: 5px;
    height: 28vh;
}.div-cd-wall:hover{
    cursor: pointer;
    background-color: #282828;
}
.row-display-cd-data{
    width: auto;
}
/* Affichage album */
.album-class, .img-play-btn{
    border-radius: 3px;
    width: 100%;
    height: 100%;
}

/* Effet rotation d'un cube */
.cube-container {
  perspective: 1000px;
  height: 100%;
  width: 100%;
}

.cube {
  position: relative;
  width: 100%; /* Ajustez la taille du cube en fonction de vos besoins */
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.5s;
}

.div-cd-wall:hover .cube {
  transform: rotateY(180deg);
}

.cube div {
  position: absolute;
  width: 95%;
  height: 95%;
  backface-visibility: hidden;
}

.display-cd-img {
  transform: translateZ(100px);
  border-radius: 5px;
}

.div-btn-play {
  transform: rotateY(180deg) translateZ(100px);
  height: 100px;
  width: 100px;
}

</style>