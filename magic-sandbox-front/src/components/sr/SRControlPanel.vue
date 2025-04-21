<template>
    <div :style="deckButtonStyle" class="control-panel"> <!-- if the player is the player using this frontend -->
        <button @click="shuffleDeck(); if (this.$store.state.soundOn === true) {play()};" class="deck-button">Shuffle</button>
        <button @click="resetDeck" class="deck-button">Reset</button>
        <button @click="detapAll" class="deck-button">Detap</button>
        <button @click="openDiceModal" class="deck-button">Dice</button>
        <button @click="discardAll" class="deck-button">Discard all</button>
        <button @click="mix" class="deck-button">Mix discard pile to deck</button>
        <button @click="draw5" class="deck-button">Draw 5</button>
        <button @click="playAllCards" class="deck-button">Play All</button>
    </div>
</template>
  
  <script>
    import axios from 'axios';
    import { useSound } from '@vueuse/sound';
    import shuffleSound from '../../assets/shuffle.mp3'
  
    export default {
      setup() {
        const { play } = useSound(shuffleSound)

        return {
          play,
        }
      },
      emits: ["open-dice-modal"],
      props: {
        playerName: String,
        roomId: String,
        userIndex: Number,
        isDeckLoaded: Boolean
      },
      methods: {
        openDiceModal() {
          this.$emit('open-dice-modal');
        },
        async resetDeck() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/reset', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
          
        },
        async shuffleDeck() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/shuffle', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async detapAll() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/board/detap', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async discardAll() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/board/discard', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async mix() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/graveyard', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async draw5() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/hand/draw5', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async playAllCards() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/hand/playall', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
      },
    };
  </script>
  
  <style>

.button-group {
  display: flex;
  justify-content: space-between;
}

.control-panel {
    position: fixed;
    left: 1%;
    bottom: 2%;
    padding: 10px;
    border-radius: 10px;
    width: 400px;
    background-color: rgba(0, 0, 0, 0.5);
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 10px;
    font-size: 0.6em;
    z-index: 10000;
  }

.deck-button {
  border-radius: 8px;
  border: solid black;
  background-color: inherit;
  color: white;
  padding: 5px 5px;
  font-size: 2em;
  cursor: pointer;
}

.deck-button:hover {
  background-color: rgba(0, 0, 0, 0.2);
}
  </style>
  