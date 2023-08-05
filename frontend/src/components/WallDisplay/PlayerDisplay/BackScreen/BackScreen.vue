<!-- Popup -->
<template>
    <div v-if="open" class="div-back-screen d-flex justify-center align-item-center" @keyup="keyup" tabindex="0" v-focus>
        <div class="div-image-back">
            <v-img :src="imageBackSrc" cover class="image-back"></v-img>
        </div>
        <div class="back-filter">
        </div>
        <div class="back-display d-flex justify-start align-center">
            <v-col class="col-image-back pa-0 ml-10 mr-5">
                <v-img :src="imageAlbumSrc" cover class="album-back"></v-img>
            </v-col>
            <v-col class="pa-0">
                <div class="max-content">
                    <p class="text-album">{{ album }}</p>
                </div>
                <div class="max-content">
                    <p class="text-artist">{{ artist }}</p>
                </div>
            </v-col>
        </div>
    </div>
</template>

<script>
import { eventBus } from '../../../../plugins/eventBus';

export default {
    directives: {
        focus: {
            inserted: function (el) {
                el.focus()
            }
        }
    },
    created(){
        eventBus.on('backScreen', (data) => {
            this.open = true
            this.artist = data.artist
            this.album = data.albumName
            this.imageAlbumSrc = new URL("../../../../assets/albums/"+data.albumName.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e") + ".jpg", import.meta.url).href
            this.imageBackSrc = new URL("../../../../assets/artists/"+data.artist.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e") + ".jpg", import.meta.url).href
        });
    },
    data() {
        return {
            open: false,
            artist: '',
            album: '',
            imageAlbumSrc: '',
            imageBackSrc: '',
        }
    },
    beforeMount() {                 // Lance la fonction au chargement de la page
    
    },
    methods: {  
        closeModal(){
            this.open = false
            this.imageBackSrc = this.imageAlbumSrc = this.album = this.artist = ''
        },
        keyup(e){
            if(e.key === 'Escape'){
                this.closeModal()
            }
        },
    }
}
</script>

<style scoped>
/* Popup de fond */
.div-back-screen{
    z-index: 99;
    top: 0;
    left: 0;
    position: absolute;
    width: 100vw;
    height: 100vh;
}
/* Image de fond */
.div-image-back{
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
}.image-back{
    width: 100%;
    height: 100%;
}.album-back{
    width: 100px;
    height: 100px;
    border-radius: 5px;
}.album-back:hover{
    transform: scale(1.1);
    cursor: none;
}
/* Filtre de 'gris' */
.back-filter{
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    animation: clignotte 5s infinite;

}@keyframes clignotte {
    0%{
        background-color: rgba(0, 0, 0, 0.3);
    }
    50%{
        background-color: rgba(0, 0, 0, 0.3);
    }
    75%{
        background-color: rgba(0, 0, 0, 0.5);
    }
    100%{
        background-color: rgba(0, 0, 0, 0.3);
    }
}
/* Image album */
.col-image-back{
    width: 10vw;
    height: 17vh;
}
/* Affichage des données */
.back-display{
    position: absolute;
    width: auto;
    height: auto;
    bottom: -3vh;
    left: 20vw;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
}.col-display-data{
    width: 100%;
}.max-content{
    width: max-content;
}
/* Texts */
.text-album{
    font-size: 5vh;
    font-weight: 600;
}.text-album:hover{
    transform: scale(1.1);
    cursor: none;
}.text-artist{
    font-size: 4vh;
    font-weight: 600;
}.text-artist:hover{
    transform: scale(1.1);
    cursor: none;
}
</style>
