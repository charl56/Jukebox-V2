<script setup>
const iconSave = new URL('../../assets/icons/save_white.png', import.meta.url).href
const iconClose = new URL('../../assets/icons/close_white.png', import.meta.url).href
const iconDelete = new URL('../../assets/icons/delete_white.png', import.meta.url).href
</script>
<!-- Popup de création/modification de cd, avec les fonction qui permettent la gestion -->
<template>
    <div v-if="open" class="dialog-overlay" @click.self="closeModal()">
        <div class="dialog-content">
            <!-- Header -->
            <div class="dialog-header">
                <input v-if="functionType == 'Edit'" type="text" name="albumName" placeholder="Nom de l'album"
                    class="input-cd-popup-title" v-model="cd.albumName" @input="edit">
                <h2 v-if="functionType == 'Add'" class="text-h5">Ajout d'un nouveau cd</h2>
                <img :src="iconClose" class="icon-close" @click="closeModal()">
            </div>

            <!-- Form -->
            <form @submit.prevent="create" class="dialog-form">
                <div class="form-content">
                    <div class="form-left">
                        <!-- Nom de l'album (seulement si Add) -->
                        <div v-if="functionType == 'Add'" class="form-group">
                            <input type="text" name="albumName" placeholder="Nom de l'album" class="input-cd-popup"
                                v-model="cd.albumName">
                        </div>

                        <!-- Nom de l'artiste -->
                        <div class="form-group">
                            <input type="text" name="artisteName" placeholder="Nom de l'artiste" class="input-cd-popup"
                                v-model="cd.artiste" @input="edit">
                        </div>

                        <!-- Nombre de tracks -->
                        <div class="form-group">
                            <input type="text" name="trackNb" placeholder="Nombre de tracks" class="input-cd-popup"
                                v-model="cd.trackNb" @input="edit">
                        </div>

                        <!-- Date de sortie -->
                        <div class="form-group">
                            <input type="date" name="releaseDate" class="input-cd-popup" v-model="cd.releaseDate"
                                @input="edit">
                        </div>
                    </div>

                    <div class="form-right">
                        <div v-if="functionType == 'Add'" class="display-cd-img-popup">
                            <input type="file" accept="image/jpeg" @change="handleFileUpload" />
                        </div>
                        <div v-else class="display-cd-img-popup">
                            <img :src="imageSrc" class="album-img" id="album-img-popup" @error="imgSrcNotFound()"
                                @load="setBackgroundColor()">
                        </div>
                    </div>
                </div>

                <!-- Boutons -->
                <div class="dialog-actions">
                    <div>
                        <img v-if="functionType == 'Add'" :src="iconSave" class="icon-action" @click="create()">
                    </div>
                    <div v-if="functionType == 'Edit'">
                        <img :src="iconDelete" class="icon-action" @click="deleteCd()">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { eventBus } from '../../plugins/eventBus';
import ColorThief from 'colorthief';
import axios from 'axios';
import { SyncronizeCdWithBack } from '../../plugins/syncronization';
import api from '../../plugins/api.js';

export default {
    created() {
        eventBus.on('openCdCu', (data) => {
            this.closeModal()
            this.open = true
            this.cd = data.data
            this.cdName = this.cd.albumName
            this.functionType = data.function       // Type de fonction
            if (this.functionType == 'Add') {
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
        edit() {
            if (this.functionType == 'Add') return
            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList[indexCd] = this.cd                         // On modifie l'emplacement du cd avec les nouvelles données
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste
            SyncronizeCdWithBack(this.$backendPort)             // Sync des données dans le back
        },
        create() {
            if (!this.selectedFile) {
                alert("Il faut ajouter la pochette de l'album");
                return;
            }
            this.cdList.push(this.cd)                            // On ajoute cd à la list
            localStorage.dataList = JSON.stringify(this.cdList, null, 2) // On met a jour la liste
            this.uploadFile()
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        uploadFile() {
            const formData = new FormData();
            const albumName = this.cd.albumName.replaceAll(" ", "_").replaceAll("é", "e").replaceAll("è", "e").toLowerCase() + ".jpg"
            formData.append("fileName", albumName);
            formData.append("file", this.selectedFile);

            api.postApi('upload', formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
                .then(() => {
                    console.log("Image uploaded successfully");
                })
                .catch((err) => {
                    console.error(err);
                });


            // axios.post(this.$backendPort + "api/upload", formData, {
            //     headers: {
            //         "Content-Type": "multipart/form-data"
            //     }
            // })
            //     .catch(e => console.error(e));
        },
        deleteCd() {
            if (!confirm("Voulez-vous vraiment supprimer cet album ?")) {
                return
            }

            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList.splice(indexCd, 1)                          // On supprimer avec l'index
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste

            // Delete image
            axios.delete(this.$backendPort + 'api/images', { "data": this.cdName })
                .catch(e => console.error(e));


            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        imgSrcNotFound() {
            this.imageSrc = new URL('../../assets/albums/default.jpg', import.meta.url).href
        },
        setBackgroundColor() {
            try {
                // Récupérer l'image dont vous voulez extraire les couleurs
                let image = document.getElementById('album-img-popup');
                image.crossOrigin = "Anonymous"
                // Créer une nouvelle instance de ColorThief
                let colorThief = new ColorThief();
                // Extraire la couleur dominante de l'image
                let dominantColor = colorThief.getColor(image, 10);
                // Appliquer la couleur dominante au background
                const dialogContent = document.querySelector('.dialog-content');
                const angle = window.innerWidth > 800 ? 90 : 225;
                dialogContent.style.background = `linear-gradient(${angle}deg, rgba(72,72,72,1) 55%, rgba(${dominantColor[0]},${dominantColor[1]},${dominantColor[2]},1) 100%)`;
                document.documentElement.style.setProperty('--border-color-cd-popup', `rgba(${dominantColor[0]},${dominantColor[1]},${dominantColor[2]},1)`);
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
/* Dialog styles */
.dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    background-color: rgba(0, 0, 0, 0.5);
}


.dialog-content {
    background-color: var(--background-color-black-4);
    color: whitesmoke;
    width: 80%;
    height: auto;
    border-radius: 10px;
    padding: 20px;
}

/* Header styles */
.dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
        font-weight: bold;
        text-align: left;
    }
}

/* Form styles */
.dialog-form {
    width: 100%;
    height: 90%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}

.form-content {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.form-left {
    flex: 7;
    padding-right: 20px;
}

.form-right {
    flex: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.form-group {
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
}

/* Input styles */
.input-cd-popup-title {
    color: white;
    margin: 0;
    padding: 5px 3px;
    width: 80%;
    font-size: larger;
    font-weight: bold;
    background: transparent;
    border: none;
}

.input-cd-popup-title:focus-within {
    outline: none;
}

.input-cd-popup {
    color: white;
    border: none;
    border-bottom: 1px solid var(--border-color-cd-popup);
    margin: 12px 5px;
    padding: 5px 3px;
    width: 80%;
    background: transparent;
}

.input-cd-popup:focus-within {
    outline: none;
}

/* Hide calendar icon */
input[type="date"]::-webkit-inner-spin-button,
input[type="date"]::-webkit-calendar-picker-indicator {
    display: none;
    -webkit-appearance: none;
}

/* Image container */
.display-cd-img-popup {
    width: 80%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;

    input {
        width: 80%;
    }
}

.album-img {
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    max-width: 100%;
    height: auto;
}

.album-img:hover {
    transform: scale(1.01);
    transition: transform 0.2s ease;
}

/* Icon styles */
.icon-close,
.icon-action {
    height: 30px;
    width: 30px;
    cursor: pointer;
}

.icon-close:hover,
.icon-action:hover {
    cursor: pointer;
    transform: scale(1.06);
    transition: transform 0.2s ease;
}

/* Action buttons */
.dialog-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

/* Responsive design */
@media only screen and (max-width: 900px) {
    .dialog-container {
        width: 85vw;
    }

    .form-content {
        flex-direction: column;
    }

    .form-left,
    .form-right {
        width: 100%;
        padding-right: 0;
    }
}

@media only screen and (max-width: 500px) {
    .dialog-container {
        width: 95vw;
    }

    .dialog-content {
        width: 90%;
    }

    .dialog-header {

        h2 {
            font-size: larger !important;
        }
    }

}
</style>