<script setup>// Quand je l'enlève j'ai une erreur : la fonction drag ne fonctionne plus, elle n'est plus trouvée
</script>
<template>
    <div v-if="cd != undefined" class="div-cd-wall" draggable="true" @dragstart="drag(cd)" @dragend="dragEnd()"
        @drop="onDrop(position, $event)" @dragover="onAllowDrop($event)" @dragleave="dragLeaveMe()"
        :class="{ 'drag-over': isDraggingOver, 'drag-over-me': isDraggingOverMine }" @click.stop="playThisAlbum()">
        <!-- Img album -->
        <img :src="imageSrc" class="album-class" @error="imgSrcNotFound()">
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
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        } catch (error) {
        }

        eventBus.on('updateDropPlaces', (bool) => {
            this.isDraggingOver = bool
        })
    },
    data() {
        return {
            imageSrc: '',
            isDraggingOver: false,
            isDraggingOverMine: false,
            cdPlaying: 0
        }
    },
    methods: {
        imgSrcNotFound() {
            this.imageSrc = new URL('@/assets/albums/default.webp', import.meta.url).href
        },
        playThisAlbum() {
            eventBus.emit("waitingScreen", { "bool": true })      // Active animation du chargemeent de la pause

            api.postApiJukebox(`play/${this.cd.position}`)
                .then((res) => {
                    localStorage.cdPlaying = this.cd.position
                    eventBus.emit("waitingScreen", { "bool": false })     // Arrête animation de la pause
                })
                .catch((err) => console.log(err))
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

    .album-class {
        /* Disable event press from smarpthone, for pictures */
        user-select: none !important;
        pointer-events: none;
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
    -webkit-user-drag: none;
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