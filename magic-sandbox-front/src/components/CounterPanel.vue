<template>
    <div class="counter-panel">
        <div v-for="player in players" :key="player.score" class="counter-wrapper">
            <SRCounter 
                :playerName="player.name"
                :roomId="roomId"
                :initialScore="player.score"
            />
        </div>
    </div>
</template>

<script>
import SRCounter from './sr/SRCounter.vue';

export default {
    components: {
        SRCounter
    },
    props: {
        players: Array,
        roomId: String
    }
}
</script>

<style>
.counter-panel {
    position: fixed;
    border: solid black 1px;
    bottom: 2%;
    left: 500px;
    width: 600px;
    height: 135px;
    background: rgba(0, 0, 0, 0.5);
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 10px;
    padding: 15px;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
}

.counter-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
