<template>
  <div :style="deckStyle" class="deck-container">
    <div v-if="!isDeckLoaded" class="add-deck-container">
      <div v-if="pIndex==userIndex">
        <input type="text" v-model="deckLink" placeholder="Enter link">
        <button  @click="addDeck" :disabled="isLoading">Add Deck</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
    <div class="deck-loaded" v-if="isDeckLoaded" @click="if (this.$store.state.soundOn === true) {play()}; drawCard();">
    </div>
</div>
  
</template>

<script>
  import axios from 'axios';
  import { useSound } from '@vueuse/sound';
  import drawSound from '../assets/draw.mp3'

  export default {
    setup() {
        const { play } = useSound(drawSound)

        return {
          play,
        }
      },
    props: {
      playerName: String,
      roomId: String,
      pIndex: Number, //index of the player
      userIndex: Number, //index of this frontend user
      cards: Array
    },
    data() {
      return {
        deckLink: '',
        isLoading: false,
        errorMessage: ''
      };
    },
    computed: {
      isDeckLoaded() {
        return this.cards && this.cards.length > 0;
      },
      deckStyle() {
        switch (this.pIndex) {
          case 0:
            return {
              left: "2400px",
              top: "900px"
            };
          case 1:
            return {
              left: "50px",
              top: "-1180px",
              transform: "rotate(180deg)"
            };
          case 2:
            return {
              left: "-2400px",
              top: "-1180px",
              transform: "rotate(180deg)"
            };
          case 3:
            return {
              left: "-250px",
              top: "900px"
            };
        }  
      }
    },
    methods: {
      async addDeck() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        if (!this.deckLink) {
          this.errorMessage = "The URL cannot be empty.";
          return;
        }

        this.isLoading = true;
        this.errorMessage = ''; // Reset the error message
        try {
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck', { url: this.deckLink });
          console.log(response.data);
        } catch (error) {
          if (error.response && error.response.data && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          } else {
            this.errorMessage = "An error occurred while processing the request.";
          }
        } finally {
          this.isLoading = false;
        }
      },
      async drawCard() {
        if(this.pIndex == this.userIndex) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.playerName + '/deck/draw', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        }
      }
    },
  };
</script>

<style>
.deck-container {
  position: fixed;
  height: 280px;
  width: 200px;
  padding: 0;
  margin: 0;
}

.add-deck-container {
  background-color: grey;
  padding: 10px;
  border-radius: 5px;
  height: 100%; 
  width: 100%; 
  box-sizing: border-box; 
}

.add-deck-container input {
  width: calc(100% - 20px); /* Full width minus padding and button width */
  margin-right: 10px;
  font-size: 2em;
}

.add-deck-container button {
  background-color: #f0f0f0;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 2em;
  margin-top: 50px;
}

.add-deck-container button[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.deck-loaded {
  background: url(../assets/card_back.webp);
  background-size: contain;
  padding: 10px;
  border-radius: 5px;
  height: 100%; 
  width: 100%; 
  box-sizing: border-box; 
}

.deck-loaded button {
  background-color: #4CAF50; /* Example color */
  color: white;
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.deck-loaded button:hover {
  background-color: #45a049;
}

</style>
