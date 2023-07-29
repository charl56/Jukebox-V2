<script setup>
    const iconStop = new URL('../../../assets/icons/stop_white.png', import.meta.url).href
    const iconPlay = new URL('../../../assets/icons/play_white.png', import.meta.url).href
    const iconPause = new URL('../../../assets/icons/pause_white.png', import.meta.url).href
</script>
<template>
    <div class="div-player-display d-flex flex-column justify-space-between">
        <v-row class="display-cd">
        </v-row>
        <v-row class="display-btns d-flex align-end pb-2 px-5">
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconStop" class="display-icon" @click="closeModal()"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPlay" class="display-icon" @click="closeModal()"></v-img>
            </v-col>
            <v-col cols="4" class="d-flex align-center justify-center pa-0 col-display-btns">
                <v-img :src="iconPause" class="display-icon" @click="closeModal()"></v-img>
            </v-col>
        </v-row>
    </div>
</template>
  
<script>
export default {
    name: 'AppPlayerDisplay',
    components: {
    },
    props: {
        id: Number,
    },
    created(){
    //   this.iconDl = new URL('../../assets/Icons/download.png', import.meta.url).href
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
.div-player-display{
    width: 100%;
    height: 100%;
    background-color: #121212;
}
/* Icons play/pause/stop */
.display-btns{
    height: min-content;
}
.col-display-btns{
    height: min-content;
}
.display-icon{
    width: 40px;
    height: 40px;
}.display-icon:hover{
    cursor: pointer;
    background-color: rgba(107, 107, 107, 0.4);
    border-radius: 5px;
    margin-bottom: 3px;
}
</style>