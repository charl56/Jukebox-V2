<script setup>
const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
</script>
<template>
    <div v-if="cd != undefined" class="div-cd-wall" draggable="true" @dragstart="drag(cd)" @dragend="dragEnd()"
        @drop="onDrop(position, $event)" @dragover="onAllowDrop($event)" @dragleave="dragLeaveMe()"
        :class="{ 'drag-over': isDraggingOver, 'drag-over-me': isDraggingOverMine }">
        <!-- Img album -->
        <img :src="imageSrc" class="album-class" :id="'album-id_' + cd.position" @error="imgSrcNotFound()"
            @click.stop="playThisAlbum()" @contextmenu.prevent>
    </div>
    <div v-else class="div-cd-wall no-cd" @drop="onDrop(position, $event)" @dragover="onAllowDrop($event)"
        @dragend="dragEnd()" @dragleave="dragLeaveMe()"
        :class="{ 'drag-over': isDraggingOver, 'drag-over-me': isDraggingOverMine }">
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
    created() {
        try {
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
        } catch (error) {
        }
        eventBus.on('updateDropPlaces', (bool) => {
            this.isDraggingOver = bool
        })

        eventBus.on('playThisCd', (data) => {
            if (data.cdPos == this.position && this.cdPlaying == 0) this.startTurningCd()
            else if (data.cdPos == this.position && this.cdPlaying != 0) {
                eventBus.emit("stopThisCd", { "cdPos": this.cdPlaying })
                this.startTurningCd()
            }
            this.cdPlaying = data.cdPos
        })

        eventBus.on('stopThisCd', (data) => {
            if (data.cdPos == this.position) this.stopTurningCd()
            this.cdPlaying = 0
        })
    },
    data() {
        return {
            imageSrc: '',
            isDraggingOver: false,
            isDraggingOverMine: false,
            cdIsPlaying: false,
            cdPlaying: 0
        }
    },
    methods: {
        openCdOnWall() {
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {
                    "data":
                        this.cd,
                    "function": "Edit"
                });
        },
        imgSrcNotFound() {
            this.imageSrc = new URL('../../../assets/albums/default.jpg', import.meta.url).href
        },
        playThisAlbum() {
            if (import.meta.env.VITE_CUSTOM_MODE) {
                // eventBus.emit("waitCdPause", { "bool": true, "name": this.cd.albumName, "movement": "Lancement" })      // Active animation du chargemeent de la pause
                // eventBus.emit("waitCdPause", { "bool": false, "name": '' })     // Arrête animation de la pause
                this.cdIsPlaying ? eventBus.emit("playThisCd", { "cdPos": this.cd.position }) : eventBus.emit("stopThisCd", { "cdPos": this.cd.position })
                // eventBus.emit("displayPlayer", { "bool": true, "name": this.cd.albumName, "artist": this.cd.artiste })     // Affichage du lecteur cd 
                return
            }

            else {
                // eventBus.emit("waitCdPause", { "bool": true, "name": this.cd.albumName, "movement": "Chargement" })      // Active animation du chargemeent de la pause
                axios.post(this.$backendPort + "playThisCd", { "data": this.cd.position })
                    .then(() => {
                        // eventBus.emit("waitCdPause", { "bool": false, "name": '' })     // Arrête animation de la pause
                        this.cdIsPlaying ? eventBus.emit("playThisCd", { "cdPos": this.cd.position }) : eventBus.emit("stopThisCd", { "cdPos": this.cd.position })

                        // eventBus.emit("displayPlayer", { "bool": true, "name": this.cd.albumName, "artist": this.cd.artiste })     // Affichage du lecteur cd 
                    })
                    .catch((err) => console.log(err))
            }
            this.cdIsPlaying = !this.cdIsPlaying
        },
        startTurningCd() {
            document.getElementById('album-id_' + this.position).classList.add('turning-cd')
        },
        stopTurningCd() {
            document.getElementById('album-id_' + this.position).classList.remove('turning-cd')
        },
        onAllowDrop(event) {
            eventBus.emit('updateDropPlaces', true)
            this.isDraggingOverMine = true
            allowDrop(event)
        },
        onDrop(pos, event) {
            eventBus.emit('updateDropPlaces', false)
            this.isDraggingOverMine = false

            // On recupere le cd drag
            let newCd = drop()
            // On recupre la liste de tous les albums
            let listCds = JSON.parse(localStorage.dataList) // On met a jour la liste
            // On check si CD sur cette position
            let index = listCds.findIndex((cd) => cd.position == pos)
            // Si pas de cd à la position, le cd drag prend la position
            if (index == -1) {
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
        },
        dragEnd() {
            eventBus.emit('updateDropPlaces', false)
            this.isDraggingOverMine = false
        },
        dragLeaveMe() {
            this.isDraggingOverMine = false
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-cd-wall {
    display: flex;
    justify-content: center;
    align-items: center;

    width: 30vh;
    height: 30vh;
}

@media (max-width: 800px) {
    .div-cd-wall {
        width: 14vh;
        height: 14vh;
    }
}



/* Affichage album */
.album-class {
    border-radius: 50%;
    width: 100%;
    height: 100%;
    transition: 0.3s;


    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none;   /* Safari */
    -khtml-user-select: none;    /* Konqueror HTML */
    -moz-user-select: none;      /* Firefox */
    -ms-user-select: none;       /* Internet Explorer/Edge */
    user-select: none;           /* Non-prefixed version */
    touch-action: none;          /* Empêche les actions tactiles par défaut */

}

.album-class:hover {
    transform: scale(1.03);
    cursor: pointer;

}

.turning-cd {
    animation: turn 10s infinite linear;
}

@keyframes turn {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


.img-play-btn {
    height: 60px;
    width: 60px;
    pointer-events: none;
    position: absolute;
    visibility: hidden;
    transition: 0.2s;
}

.img-play-btn:hover {
    visibility: visible;
}

.no-cd {
    background-color: var(--background-color-black-1);
    border-radius: 50%;
}



/* Css effect when can drop here */
.drag-over {
    border: 2px dashed #ff9800;
    /* Bordure en pointillé orange */
    box-shadow: 0 4px 20px rgba(255, 152, 0, 0.5);
    /* Ombre portée pour effet de profondeur */
    transition: background-color 0.6s ease, transform 0.2s ease;
    /* Transition douce pour les changements de couleur et d'effet */
    transform: scale(1.02);
    /* Légère mise à l'échelle pour attirer l'attention */
    z-index: 10;
    /* Assurez-vous que l'élément est au-dessus des autres éléments */
}

.drag-over-me {
    background-color: rgba(255, 223, 186, 0.8);
    /* Couleur de fond douce */
}
</style>