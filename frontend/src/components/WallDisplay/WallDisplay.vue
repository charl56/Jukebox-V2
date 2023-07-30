<template>
    <div class="div-wall-display d-flex flex-column pa-3 ma-1">
        <!-- Afficha grille avec CDs et lecteur -->
        <v-row v-for="n in 3">
            <v-col>
                <CdDisplay :cd="list.find(cd => cd.position == (3*n - 2))"/>
            </v-col>
            <v-col>
                <PlayerDisplay v-if="(3*n - 1 == 5)" />
                <CdDisplay v-else :cd="list.find(cd => cd.position == (3*n - 1))"/>
            </v-col>
            <v-col>
                <CdDisplay :cd="list.find(cd => cd.position == (3*n))"/>
            </v-col>
        </v-row>
    </div>
</template>
  
<script>
import CdDisplay from './CdDisplay/CdDisplay.vue';
import PlayerDisplay from './PlayerDisplay/PlayerDisplay.vue'

export default {
    name: 'AppWallDisplay',
    components: {
        CdDisplay,
        PlayerDisplay,
    },
    props: {
        list: Array,
    },
    created(){
    },
    data () {
        return {
        
        }
    },
    methods:{
        
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/* Div component */
.div-wall-display{
    height: 96vh;
    background-color: var(--background-color-black-2);
    border-radius: 5px;
}
</style>