<template>
    <div class="div-server-unreachable">
        <p>Connexion au server impossible</p>
        <p>Essayer de recharger la page, ou de relancer le server</p>
    </div>

</template>

<script>

export default {
    name: 'AppServerUnreachable',

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.div-server-unreachable {
    height: 100dvh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.div-server-unreachable p {
    font-size: 1em;
    font-weight: 700;
    animation: breathing-rotation 5s ease-in-out infinite;
}

@keyframes breathing-rotation {
    0% {
        transform: scale(1) rotate(0deg);
    }
    25% {
        transform: scale(1.1) rotate(180deg);
    }
    100% {
        transform: scale(1) rotate(360deg);
    }
}
</style>