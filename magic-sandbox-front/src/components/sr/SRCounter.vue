<template>
    <div :style="counterStyle" class="sr-counter">
      <div class="sr-player-name">{{ playerName }}</div>
      <div class="sr-score">{{ score }}</div>
      <div class="sr-button-group">
        <button @click="decrementScore" class="sr-minus-button">-</button>
        <button @click="incrementScore" class="sr-plus-button">+</button>
      </div>
    </div>
</template>
  
  <script>
    import axios from 'axios';
  
    export default {
      props: {
        playerName: String,
        roomId: String,
        initialScore: {
            type: Number,
            default: 20
        },
      },
      data() {
        return {
          score: this.initialScore
        };
      },
      computed: {
        
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
              const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/score/' + this.score, {});
              console.log(response.data);
            } catch (error) {
              console.log(error);
            }
        }
      },
    };
  </script>
  
  <style>
.sr-counter {
  position: fixed;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 8px;
  height: 135px;
  width: 150px;
  flex-direction: column;
  border: solid black 1px;
}

.sr-player-name {
  font-weight: bold;
  font-size: 1em;
  margin-bottom: 10px;
}

.sr-score {
  font-size: 2em;
  margin-bottom: 5px;
}

.sr-button-group {
  display: flex;
  justify-content: space-between;
}

.sr-minus-button, .sr-plus-button {
  border-radius: 50%;
  margin: 5px;
  width: 30px;
  height: 30px;
  line-height: 40px; /* Align text vertically */
  text-align: center;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  padding: 0;
  font-size: 1em;
  cursor: pointer;
}

.sr-minus-button:hover, .sr-plus-button:hover {
  background-color: #e0e0e0;
}
  </style>
  