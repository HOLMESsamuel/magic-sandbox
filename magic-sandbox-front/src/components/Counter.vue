<template>
    <div :style="counterStyle" class="counter">
      <div class="player-name">{{ playerName }}</div>
      <div class="score">{{ score }}</div>
      <div class="button-group">
        <button @click="decrementScore" class="minus-button">-</button>
        <button @click="incrementScore" class="plus-button">+</button>
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
        userIndex: Number
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
                style.background = "rgb(235, 159, 130)" //ref
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
            try{
            const response = await axios.post('http://localhost:8000/room/' + this.roomId +'/player/'+ this.playerName + '/score/' + this.score, {});
            console.log(response.data);
            } catch (error) {
            console.log(error);
            }
        
      },
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
  </style>
  