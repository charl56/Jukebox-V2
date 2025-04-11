<script setup>
const iconPlay = new URL('@/assets/icons/play_white.png', import.meta.url).href
</script>
<template>
    <div v-if="cd != undefined" class="div-cd-wall" draggable="true" @dragstart="drag(cd)" @dragend="dragEnd()"
        @drop="onDrop(position, $event)" @dragover="onAllowDrop($event)" @dragleave="dragLeaveMe()"
        :class="{ 'drag-over': isDraggingOver, 'drag-over-me': isDraggingOverMine }">
        <!-- Img album -->
        <img :src="imageSrc" class="album-class" :id="'album-id_' + cd.position" @error="imgSrcNotFound()"
            @click.stop="playThisAlbum()" draggable="false">
    </div>
    <div v-else class="div-cd-wall no-cd" @drop="onDrop(position, $event)" @dragover="onAllowDrop($event)"
        @dragend="dragEnd()" @dragleave="dragLeaveMe()"
        :class="{ 'drag-over': isDraggingOver, 'drag-over-me': isDraggingOverMine }">
    </div>

</template>

<script>
import { eventBus } from '@/plugins/eventBus'
import { drag, drop, allowDrop } from '@/plugins/dragNdrop';
import api from '@/plugins/api';

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

        eventBus.on('stopAllCds', () => {
            this.stopTurningCd()
            this.cdPlaying = 0
        })
    },
    mounted() {
        // Permet de garder la rotation du cd en cours, si refresh de la page, dragNdrop...
        if (localStorage.cdPlaying == this.position) this.startTurningCd()
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
            this.imageSrc = new URL('@/assets/albums/default.jpg', import.meta.url).href
        },
        playThisAlbum() {
            eventBus.emit("stopAllCds")
            if (!this.cdIsPlaying || (localStorage.cdPlaying != this.cd.position)) {
                eventBus.emit("waitCdPause", { "bool": true, "name": this.cd.albumName, "movement": "Chargement" })      // Active animation du chargemeent de la pause
                api.postApiJukebox(`play/${this.cd.position}`)
                    .then((res) => {
                        this.cdIsPlaying = !this.cdIsPlaying
                        eventBus.emit("waitCdPause", { "bool": false, "name": '' })     // Arrête animation de la pause
                        eventBus.emit("playThisCd", { "cdPos": this.cd.position })
                        // On sauvegarde l'indice du cd qui tourne, pour quand refresh
                        localStorage.cdPlaying = this.cd.position
                    })
                    .catch((err) => console.log(err))
            } else {
                api.postApiJukebox('pause')
                    .then((res) => {
                        eventBus.emit("stopThisCd", { "cdPos": this.cd.position })
                        this.cdIsPlaying = !this.cdIsPlaying
                        localStorage.cdPlaying = 0
                    })
            }
        },
        startTurningCd() {
            try {
                document.getElementById('album-id_' + this.position).classList.add('turning-cd')
            } catch (error) {

            }
        },
        stopTurningCd() {
            try {
                document.getElementById('album-id_' + this.position).classList.remove('turning-cd')
            } catch (error) {

            }
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
                // On stop la rotation
                if (localStorage.cdPlaying == pos || localStorage.cdPlaying == posCdDrag) localStorage.cdPlaying = 0
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

@media (min-width: 800px) {
    .album-class:hover {
        transform: scale(1.03);
        cursor: pointer;
    }
}


/* Affichage album */
.album-class {
    border-radius: 50%;
    width: 100%;
    height: 100%;
    transition: 0.3s;

    /* disable download option for smartphones */
    user-select: none !important;
    -webkit-user-drag: none;
    -khtml-user-drag: none;
    -moz-user-drag: none;
    -o-user-drag: none;
    -ms-user-drag: none;

}


.turning-cd {
    animation: turn 10s infinite linear forwards;
}

@keyframes turn {
    to {
        rotate: 1turn
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