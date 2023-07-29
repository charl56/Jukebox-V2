<script setup>
    const iconClose = new URL('../../assets/icons/close.png', import.meta.url).href
</script>
<!-- Popup de création/modification de cd, avec les fonction qui permettent la gestion -->
<template>
    <v-dialog v-model="open" v-if="open" transition="dialog-bottom-transition" class="div-item-cu mt-0 d-flex justify-center align-item-center">
        <v-row class="item-cu mx-1 my-2 pb-4 d-flex justify-center align-item-center">
            <!-- Header subSection Create/Update -->
            <v-row class="mx-2 my-2 header-row justify-center d-flex">  
                <v-col cols="1"></v-col>     
                <v-col cols="10">
                    <p class="text-h5 text-center" v-if="this.function == 'Edit'">{{ cd.albumName }}</p>
                    <p class="text-h5 text-center" v-if="this.function == 'Add'">Ajouter un nouveau cd</p>
                </v-col>     
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
                            <v-row class="d-flex justify-space-between mx-6">
                                <v-text-field class="item-name" v-model="cd.albumName" :value="cd.albumName" label="Nom de l'album" variant="outlined"></v-text-field>
                            </v-row>
                            <!-- Nom de l'artiste -->
                            <v-row class="d-flex justify-space-between mx-6">
                                <v-text-field class="item-name" v-model="cd.artiste" :value="cd.artiste" label="Nom de l'artiste" variant="outlined"></v-text-field>
                            </v-row>
                            <!-- Nombre de tracks -->
                            <v-row class="d-flex justify-space-between mx-6">
                                <v-text-field class="item-name" v-model="cd.trackNb" :value="cd.trackNb" label="Nombre de tracks" variant="outlined"></v-text-field>
                            </v-row>
                            <!-- Date de sortie -->
                            <v-row class="d-flex justify-space-between mx-6 mb-4">
                                <label for="releaseDate">Date de sortie:</label>
                                <input type="date" name="releaseDate" v-model="cd.releaseDate">
                            </v-row>
                            <!-- Position -->
                            <v-row v-if="this.function == 'Edit'" class="d-flex justify-space-between mx-6">
                                <v-text-field class="item-name" v-model="cd.position" :value="cd.position" label="Position du cd" variant="outlined"></v-text-field>
                            </v-row>
                        </v-col>
                        <v-col cols="5" class="d-flex align-center justify-center px-0">
                            <div class="display-cd-img-popup d-flex align-center justify-center mb-5">
                                <v-img :src="imageSrc" id="album-img-popup" @error="imgSrcNotFound()" @load="setBackgroundColor()"></v-img>
                            </div>
                        </v-col>
                    </v-row>
                    <!-- Boutons de validation et annulation -->
                    <v-row class="mt-0 mb-1 my-0 px-5 d-flex align-center">
                        <v-col cols="6">           
                            <v-btn type="submit" block class="mt-1 edit-btn" variant="outlined"><p class="font-weight-bold">Enregistrer</p></v-btn>
                        </v-col>
                        <v-col v-if="this.function == 'Edit'" cols="6">
                            <v-btn block class="mt-1 exit-btn" @click="delet()" variant="outlined"><p class="font-weight-bold">Supprimer</p></v-btn>
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

export default {
    created(){
        eventBus.on('openCdCu', (data) => {
            this.closeModal()
            this.open = true
            this.cd = data.data
            this.cdName = this.cd.albumName
            this.function = data.function       // Type de fonction
            this.cdList = JSON.parse(localStorage.dataList)  // On recupère la liste des cds
            this.imageSrc = new URL("../../assets/albums/"+this.cd.albumName.replaceAll(" ","_") + ".jpg", import.meta.url).href      // Source img album 
        });
    },
    data() {
        return {
            cd: {
                'albumName': '', 
                'artiste': '', 
                'trackNb': 0, 
                'releaseDate': '0000-00-00', 
                'position': 0
            },
            cdName: '',
            function: '',
            imageSrc: '', 
            open: false,
            cdList: [],
        }
    },
    beforeMount() {                 // Lance la fonction au chargement de la page
    
    },
    methods: {  
        closeModal(){
            this.cd = {
                'albumName': '', 
                'artiste': '', 
                'trackNb': 0, 
                'releaseDate': '0000-00-00', 
                'position': 0
            }
            this.function = ''
            this.cdName = ''
            this.open = false
        },
        valideCd(){
            if(this.function == 'Edit'){
                this.edit()
            } else if(this.function == 'Add'){
                this.create()
            }
        },
        edit(){    
            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList[indexCd] = this.cd                         // On modifie l'emplacement du cd avec les nouvelles données
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        create(){
            this.cdList.push(this.cd)                            // On ajoute cd à la list
            localStorage.dataList = JSON.stringify(this.cdList, null, 2) // On met a jour la liste
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        delet(){
            let indexCd = this.cdList.findIndex((cd) => cd.albumName == this.cdName) // On recupère la position dans la liste, du cd actuel
            this.cdList.splice(indexCd, 1)                          // On supprimer avec l'index
            localStorage.dataList = JSON.stringify(this.cdList, null, 2)  // On met a jour la liste
            this.closeModal()                               // On ferme le popup
            eventBus.emit('updateLists')                    // On actualise l'app
        },
        imgSrcNotFound(){
            this.imageSrc = new URL('../../assets/albums/default.jpg', import.meta.url).href
        },
        setBackgroundColor(){
            // Récupérer l'image dont vous voulez extraire les couleurs
            let image = document.getElementById('album-img-popup').children[1];
            // Créer une nouvelle instance de ColorThief
            let colorThief = new ColorThief();
            // Extraire la couleur dominante de l'image
            let dominantColor = colorThief.getColor(image, 10);
            // Maintenant, vous avez les valeurs RGB des couleurs dominantes dans dominantColor ou dominantColors.
            let background = document.getElementsByClassName("item-cu")
            background[0].style.background = "linear-gradient(0deg, rgba(72,72,72,1) 87.5%, rgba("+dominantColor[0]+","+dominantColor[1]+","+dominantColor[2]+",1) 100%)"
        }
    }
}
</script>

<style scoped>
/* Dimensions du popup responsive */
@media only screen and (max-width: 900px) {
    .div-item-cu{
        width: 80vw !important;
    }
}@media only screen and (max-width: 500px) {
    .div-item-cu{
        width: 95vw !important;
    }
}
.div-item-cu{
    width: 60vw;
    height: 70vh;
    border-radius: 5px;
    z-index: 999;
}
.item-cu{
    background-color: #484848;
    color: whitesmoke;
    height: 100%;
    width: 100%;
    border-radius: 10px;
}
.item-name{
    width: 40vw !important;
}
/* Image */
.display-cd-img-popup{
    width: 80%;
    height: 100%;
}#album-img-popup{
    border-radius: 5px;
}
/* Icon */
.icon-close{
    height: 30px;
    width: 30px;
}.icon-close:hover{
    cursor: pointer;
}
.header-row{
    width: 100%;
}.form-row{
    width: 100%;
}
/* Formulaire */
.s-s-form{
    width: 100% !important;
}
input{
    color: white;
}
/* Couleur des boutons */
.edit-btn{
    color: #639755;
}.edit-btn:hover{
    background-color: #639755;
    border: 1px solid #639755;
    color: white;
}.exit-btn{
    color: #de8f35;
}.exit-btn:hover{
    background-color: #de8f35;
    border: 1px solid #de8f35;
    color: white;
}
</style>
