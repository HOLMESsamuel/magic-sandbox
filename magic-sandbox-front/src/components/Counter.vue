<template>
    <div :style="counterStyle" class="counter">
      <div class="player-name">{{ playerName }}</div>
      <div class="score">{{ score }}</div>
      <div class="button-group">
        <button @click="decrementScore" class="minus-button">-</button>
        <button @click="incrementScore" class="plus-button">+</button>
      </div>
    </div>
    <div v-if="pIndex == userIndex">
        <div v-if="isDeckLoaded" :style="deckButtonStyle" class="deck-buttons"> <!-- if the player is the player using this frontend -->
          <button @click="millCard" class="deck-button">Mill</button>
          <button @click="scryCard" class="deck-button">Scry</button>
          <button @click="lookCard" class="deck-button">Look</button>
          <button @click="shuffleDeck" class="deck-button">Shuffle</button>
          <button @click="resetDeck" class="deck-button">Reset</button>
        </div>
      </div>
</template>
  
  <script>
    import axios from 'axios';
  
    export default {
      props: {
        playerName: String,
        roomId: String,
        pIndex: Number,
        initialScore: {
            type: Number,
            default: 20
        },
        userIndex: Number,
        isDeckLoaded: Boolean
      },
      data() {
        return {
          score: this.initialScore
        };
      },
      computed: {
        counterStyle() {
          let style = {};
          switch (this.pIndex) {
            case 0:
                style.left = "0px";
                style.top = "0px";
                style.background = "rgb(196, 211, 202)" //green
                break;
            case 1:
                style.left = "0px";
                style.top = "-300px";
                style.background = "rgb(179, 206, 234)" //blue
                break;
            case 2:
                style.left = "-300px";
                style.top = "-300px";
                style.background = "rgb(235, 159, 130)" //red
                break;
            case 3:
                style.left = "-300px";
                style.top = "0px";
                style.background = "rgb(248, 231, 185)" //yellow
                break;
          } 

          if (this.userIndex === 1 || this.userIndex === 2) {
                style.transform = 'rotate(180deg)';
          }

          return style;

        },
        deckButtonStyle() {
          let style = {};
          switch (this.pIndex) {
            case 0:
              style = { left: "0px", top: "305px", background: "rgb(196, 211, 202)"};
              break;
            case 1:
              style = { left: "0px", top: "-495px", transform: "rotate(180deg)", background: "rgb(179, 206, 234)" };
              break;
            case 2:
              style = { left: "-300px", top: "-495px", transform: "rotate(180deg)", background: "rgb(235, 159, 130)" };
              break;
            case 3:
              style = { left: "-300px", top: "305px", background: "rgb(248, 231, 185)" };
              break;
          }
          return style;
        }
      },
      methods: {
        incrementScore() {
            this.score += 1;
            this.updateScore();
        },
        decrementScore() {
            this.score -= 1;
            this.updateScore();
        },
        async updateScore() {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            try{
              const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/score/' + this.score, {});
              console.log(response.data);
            } catch (error) {
              console.log(error);
            }
        },
        async resetDeck() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/reset', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
          
        },
        async millCard() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/mill', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async shuffleDeck() {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/shuffle', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
          
        }
      },
    };
  </script>
  
  <style>
.counter {
  position: fixed;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 8px;
  height: 300px;
  width: 300px;
  flex-direction: column;
}

.player-name {
  font-weight: bold;
  font-size: 3em;
  margin-bottom: 10px;
}

.score {
  font-size: 4em;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.minus-button, .plus-button {
  border-radius: 50%;
  margin: 10px;
  width: 60px;
  height: 60px;
  line-height: 40px; /* Align text vertically */
  text-align: center;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  padding: 0;
  font-size: 3em;
  cursor: pointer;
}

.minus-button:hover, .plus-button:hover {
  background-color: #e0e0e0;
}

.deck-buttons {
    position: fixed;
    padding: 10px;
    border-radius: 10px;
    width: 280px;
    background-color: rgba(0, 0, 0, 0.5);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    font-size: 0.9em;
    z-index: 1;
  }

.deck-button {
  border-radius: 8px;
  border: solid black;
  background-color: inherit;
  color: black;
  padding: 5px 5px;
  font-size: 2em;
  cursor: pointer;
}

.deck-button:hover {
  background-color: rgba(0, 0, 0, 0.2);
}
  </style>
  