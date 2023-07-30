<script setup>
    const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
</script>
<template>
    <div v-if="cd != undefined" class="div-cd-wall d-flex flex-column justify-space-between align-center" @click="openCdOnWall()">
        <div class="cube-container">
            <div class="cube d-flex align-center justify-center">
                <!-- Mettez ici les deux images que vous souhaitez afficher -->
                <div class="display-cd-img d-flex align-center justify-center">
                    <v-img :src="imageSrc" class="album-class" @error="imgSrcNotFound()"></v-img>
                </div>
                <div class="div-btn-play d-flex align-center justify-center">
                    <v-img :src="iconPlay" class="img-play-btn" @click.stop="playThisAlbum()"></v-img>
                    <!-- <img :src="Logo" alt="Logo" /> -->
                </div>
            </div>
        </div>

        <div class="row-display-cd-data">
            <div>
                <p class="text-subtitle-1 font-weight-bold">{{ cd.albumName }}</p>
            </div>
            <div>
                <p class="text-subtitle-2">{{ cd.artiste }}</p>
            </div>
        </div>
    </div>

</template>
  
<script>
import { eventBus } from '../../../plugins/eventBus'
// import Logo from "../../../assets/icons/play.svg"; // Assurez-vous que le chemin d'importation est correct

export default {
    name: 'AppCdDisplay',
    props: {
        cd: Object,
    },
    created(){
        try {
            this.imageSrc = new URL("../../../assets/albums/"+this.cd.albumName.replaceAll(" ","_") + ".jpg", import.meta.url).href
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
        playThisAlbum(){        // C'est lede la fonction
            console.log("play this : ", this.cd)
        }
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-cd-wall{
    background-color: #181818;
    border-radius: 5px;
    height: 100%;
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
/* Fleche play */
.div-btn-play{
    transform: rotateY(0deg);
}

/* Effet rotation d'un cube */
.cube-container {
  perspective: 1000px;
}

.cube {
  position: relative;
  width: 100px; /* Ajustez la taille du cube en fonction de vos besoins */
  height: 100px;
  transform-style: preserve-3d;
  transition: transform 0.5s;
}

.div-cd-wall:hover .cube {
  transform: rotateY(180deg);
}

.cube div {
  position: absolute;
  width: 80%;
  height: 80%;
  backface-visibility: hidden;
}

.display-cd-img {
  transform: translateZ(100px);
}

.div-btn-play {
  transform: rotateY(180deg) translateZ(100px);
}

</style>