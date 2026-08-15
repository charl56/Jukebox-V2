<template>
    <div v-if="cd != undefined" class="div-border-display" @click.stop="openPlayer()">
        <p class="text-subtitle-1 font-weight-bold disable-text-selection">{{ cd.albumName }} - {{ cd.artiste }}</p>
        <img :src="imageSrc" class="div-border-display_img" @error="imgSrcNotFound()"
            @click.stop="" draggable="false">
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus'
import api from '@/plugins/api';

export default {
    name: 'AppBorderPlayer',
    props: {
        cd: Object,
    },
    mounted() {
        try {
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".webp"
        } catch (error) {
            // Fermer, et ouvrir le toast avec message erreur
        }
    },
    data() {
        return {
            imageSrc: '',
            cdPlaying: 0,
        }
    },
    methods: {
        openPlayer() {
            localStorage.isPlayerOpen = true
            eventBus.emit('refresh')
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.div-border-display {
    position: absolute;
    height: 5rem;
    width: -webkit-fill-available;
    background-color: var(--background-color-black-2);


    margin: 0 1rem;
    padding: 0 1rem;
    
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-direction: row;
    z-index: 50;
}

.div-border-display:hover{
    background-color: var(--background-color-black-3);
    cursor: pointer;
}

.div-border-display_img {
    height: 4rem;
    width: 4rem;
    border-radius: 5px;
}

</style>