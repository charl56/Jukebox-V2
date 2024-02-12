<script setup>
const iconSave = new URL('../../assets/icons/save_white.png', import.meta.url).href
const iconClose = new URL('../../assets/icons/close_white.png', import.meta.url).href
const iconDelete = new URL('../../assets/icons/delete_white.png', import.meta.url).href
</script>
<!-- Popup de création/modification de cd, avec les fonction qui permettent la gestion -->
<template>
    <v-dialog v-model="open" v-if="open" transition="dialog-bottom-transition"
        class="div-item-cu mt-0 d-flex justify-center align-item-center">
        <v-row class="item-cu mx-1 my-2 pb-4 d-flex justify-center align-item-center">
            <!-- Header subSection Create/Update -->
            <v-row class="mx-2 my-2 header-row d-flex justify-center">
                <v-col cols="6" class="py-0">
                    <!-- <p class="text-h5 text-start font-weight-bold" v-if="this.function == 'Edit'"> </p> -->
                    <input v-if="functionType == 'Edit'" type="text" name="albumName" placeholder="Nom de l'album"
                        class="input-cd-popup-title" v-model="cd.albumName">
                    <p class="text-h5 text-start" v-if="functionType == 'Add'">Ajouter un nouveau cd</p>
                </v-col>
                <v-col cols="5"></v-col>
                <v-col cols="1">
                    <v-img :src="iconClose" class="icon-close" @click="closeModal()"></v-img>
                </v-col>
            </v-row>
            <v-row class="row-log mx-0 form-row" justify="center">
                <!-- Form lié avec la fonction 'valideCd'. Permet d'utiliser un form. Ensuite dans la fonction choix entre edit et add -->
                <v-form v-on:submit.prevent="valideCd" class="s-s-form d-flex flex-column" justify="center">
                    <v-row>
                        <v-col cols="7" class="px-0">
                            <!-- Nom de l'album -->
                            <v-row v-if="functionType == 'Add'" class="d-flex justify-space-between mx-6">
                                <input type="text" name="albumName" placeholder="Nom de l'album" class="input-cd-popup"
                                    v-model="cd.albumName">
                            </v-row>
                            <!-- Nom de l'artiste -->
                            <v-row class="d-flex justify-space-between mx-6">
                                <input type="text" name="artisteName" placeholder="Nom de l'artiste" class="input-cd-popup"
                                    v-model="cd.artiste">
                            </v-row>
                            <!-- Nombre de tracks -->
                            <v-row class="d-flex justify-space-between mx-6">
                                <input type="text" name="trackNb" placeholder="Nombre de tracks" class="input-cd-popup"
                                    v-model="cd.trackNb">
                            </v-row>
                            <!-- Date de sortie -->
                            <v-row class="d-flex justify-start mx-6">
                                <input type="date" name="releaseDate" class="input-cd-popup" v-model="cd.releaseDate">
                            </v-row>
                        </v-col>
                        <v-col cols="5" class="d-flex flex-column align-center justify-center px-0">
                            <div v-if="functionType == 'Add'"
                                class="display-cd-img-popup d-flex align-center justify-center mb-5">
                                <input type="file" accept="image/jpeg" @change="handleFileUpload" />
                            </div>
                            <div v-else class="display-cd-img-popup d-flex align-center justify-center mb-5">
                                <v-img :src="imageSrc" class="elevation-10" id="album-img-popup" @error="imgSrcNotFound()" @load="setBackgroundColor()"></v-img>
                            </div>
                        </v-col>
                    </v-row>
                    <!-- Boutons de validation et annulation -->
                    <v-row class="mt-0 mb-1 my-0 px-5 d-flex align-center justify-space-between">
                        <v-col cols="6">
                            <v-img :src="iconSave" type="submit" class="icon-close" @click="valideCd()"></v-img>
                        </v-col>
                        <v-col v-if="functionType == 'Edit'" cols="1" class="d-flex justify-end">
                            <v-img :src="iconDelete" class="icon-close" @click="deleteCd()"></v-img>
                        </v-col>
                    </v-row>
                </v-form>
            </v-row>
        </v-row>
    </v-dialog>
</template>

<script>
import { eventBus } from '../../plugins/eventBus';
import ColorThief from 'colorthief';
import axios from 'axios';

export default {
    created() {
        eventBus.on('openCdCu', (data) => {
            this.closeModal()
            this.open = true
            this.cd = data.data
            this.cdName = this.cd.albumName
            this.functionType = data.function       // Type de fonction
            if(this.functionType == 'Add') {
                document.documentElement.style.setProperty('--border-color-cd-popup', 'white');
            }
            this.cdList = JSON.parse(localStorage.dataList)  // On recupère la liste des cds
            this.imageSrc = this.$backendPort + "images/albums/" + this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
        });
    },
    data() {
        return {
            cd: {
                'albumName': '',
                'artiste': '',
                'trackNb': '',
                'releaseDate': '0000-00-00',
                'position': 0
            },
            albumImage: [],
            cdName: '',
            functionType: '',
            imageSrc: '',
            open: false,
            cdList: [],
            selectedFile: null,
        }
    },
    beforeMount() {                 // Lance la fonction au chargement de la page

    },
    methods: {
        closeModal() {
            this.cd = {
                'albumName': '',
                'artiste': '',
                'trackNb': '',
                'releaseDate': '0000-00-00',
                'position': 0
            }
            this.albumImage = []
            this.functionType = this.cdName = ''
            this.open = false
            this.selectedFile = null
        },
        valideCd() {
            if (this.functionType == 'Edit') {
                this.edit()
            } else if (this.functionType == 'Add') {
                this.create()
            }
        },
        edit() {
            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList[indexCd] = this.cd                         // On modifie l'emplacement du cd avec les nouvelles données
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        create() {
            this.cdList.push(this.cd)                            // On ajoute cd à la list
            localStorage.dataList = JSON.stringify(this.cdList, null, 2) // On met a jour la liste
            this.uploadFile()
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        uploadFile() {
            if (!this.selectedFile) {
                alert("Il faut ajouter la pochette de l'album");
                return;
            }

            const formData = new FormData();
            const albumName = this.cd.albumName.replaceAll(" ","_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
            formData.append("fileName", albumName);
            formData.append("file", this.selectedFile);

            
            axios.post(this.$backendPort + "upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
                .then(response => {
                    console.log(response.data);
                    // Handle success
                })
                .catch(error => {
                    console.error(error);
                    // Handle error
                });
        },
        deleteCd() {
            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList.splice(indexCd, 1)                          // On supprimer avec l'index
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        imgSrcNotFound() {
            this.imageSrc = new URL('../../assets/albums/default.jpg', import.meta.url).href
        },
        setBackgroundColor() {
            try {
                // Récupérer l'image dont vous voulez extraire les couleurs
                let image = document.getElementById('album-img-popup').children[1];
                image.crossOrigin = "Anonymous"
                // Créer une nouvelle instance de ColorThief
                let colorThief = new ColorThief();
                // Extraire la couleur dominante de l'image
                let dominantColor = colorThief.getColor(image, 10);
                // Maintenant, vous avez les valeurs RGB des couleurs dominantes dans dominantColor ou dominantColors.
                let background = document.getElementsByClassName("item-cu")
                background[0].style.background = "linear-gradient(90deg, rgba(72,72,72,1) 55%, rgba(" + dominantColor[0] + "," + dominantColor[1] + "," + dominantColor[2] + ",1) 100%)"
                document.documentElement.style.setProperty('--border-color-cd-popup', 'rgba(' + dominantColor[0] + ',' + dominantColor[1] + ',' + dominantColor[2] + ',1)');
            } catch (error) {
                console.log(error)
            }
        },
        handleFileUpload(event) {
            this.selectedFile = event.target.files[0];
        },
    }
}
</script>

<style scoped>
/* Dimensions du popup responsive */
@media only screen and (max-width: 900px) {
    .div-item-cu {
        width: 80vw !important;
    }
}

@media only screen and (max-width: 500px) {
    .div-item-cu {
        width: 95vw !important;
    }
}

.div-item-cu {
    width: 60vw;
    height: 70vh;
    border-radius: 5px;
    z-index: 999;
}

.item-cu {
    background-color: var(--background-color-black-4);
    color: whitesmoke;
    height: 100%;
    width: 100%;
    border-radius: 10px;
}

.item-name {
    width: 40vw !important;
}

/* Image */
.display-cd-img-popup {
    width: 80%;
    height: 100%;
}

#album-img-popup {
    border-radius: 5px;
}

#album-img-popup:hover {
    cursor: pointer;
    transform: scale(1.01);
}

/* Icon */
.icon-close {
    height: 30px;
    width: 30px;
}

.icon-close:hover {
    cursor: pointer;
    background-color: rgba(107, 107, 107, 0.4);
    border-radius: 5px;
    transform: scale(1.06);
}

.header-row {
    width: 100%;
}

.form-row {
    width: 100%;
}

/* Formulaire */
.s-s-form {
    width: 100% !important;
}

.input-cd-popup-title {
    /* color: var(--border-color-cd-popup); */
    color: white;
    margin: 12px 5px 0px 5px;
    padding: 5px 3px;
    width: 100%;
    font-size: larger;
    font-weight: bold;
}

.input-cd-popup-title:focus-within {
    outline: none;
    /* Supprimer le contour par défaut (utile pour certains navigateurs) */

}

.input-cd-popup {
    /* color: var(--border-color-cd-popup); */
    color: white;
    border-bottom: 1px solid var(--border-color-cd-popup);
    margin: 12px 5px;
    padding: 5px 3px;
    width: 80%;
}

.input-cd-popup:focus-within {
    outline: none;
}

/* Cacher l'icon calendrier */
input[type="date"]::-webkit-inner-spin-button,
input[type="date"]::-webkit-calendar-picker-indicator {
    display: none;
    -webkit-appearance: none;
}

/* Ajout image */
.div-input-file {
    width: 20vw;
}


</style>
