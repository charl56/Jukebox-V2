<template>
    <div class="div-list-display d-flex flex-column pa-3 ma-1">
        <!-- Btn ajout cd -->
        <div class="div-btn-add ma-1 pa-1 justify-center">
            <v-btn class="btn-add" variant="outlined" @click="addCd()">Ajouter</v-btn>
            <v-btn class="btn-add" variant="outlined" @click="Sync()">Sync</v-btn>
        </div>
        <!-- List des CD en rab, v-for -->
        <div v-for="cd in list" class="div-cd-list ma-2" @click="openCd(cd)">
            <div>
                {{ cd.albumName }}
            </div>
        </div>
    </div>
</template>
  
<script>
import { eventBus } from '../../plugins/eventBus';
import axios from 'axios';

export default {
    name: 'AppListDisplay',
    components: {
    },
    props:{
        list: Array,
    },
    created(){
        //   this.iconDl = new URL('../../assets/Icons/download.png', import.meta.url).href
    },
    data () {
        return {
        
        }
    },
    methods:{
        // Ajouter un nv CD
        addCd(){
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {"data":
                    {'albumName': '', 'artiste': '', 'trackNb': 0, 'releaseDate': new Date().toISOString().split('T')[0], position: 0},
                "function": "Add"
            });   
        },
        // Ouvrir un CD
        openCd(cd){
            eventBus.emit('openCdCu',   // On créer un cd, on envoie un modèle vide pour le remplir
                {"data":
                    cd,
                "function": "Edit"
            });  
        },
        Sync(){
            // Creation du json qui sera save dans le fichier
            let data = {
                "cd": JSON.parse(localStorage.dataList)
            }
            // Requete vers le back pour save les données du JSON
            axios.post('http://127.0.0.1:5025/syncData', {data: JSON.stringify(data)})
                .then((resp) => {
                    console.log(resp)
                })
                .catch((err) => {
                    console.log(err)
                })
        }
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div du composant */
.div-list-display{
    width: 100%;
    height: 95vh;
    background-color: #121212;
    border-radius: 5px;
    /* overflow-y: scroll; */
}
/* Row btn add */
.div-btn-add{
    height: fit-content;
}.btn-add:hover{
    color: #121212;
    background-color: white;
}

.div-cd-list{
    height: 10vh;
}.div-cd-list:hover{
    cursor: pointer;
    background-color: #282828;
    border-radius: 5px;
}

</style>