<template>
  <div :style="deckStyle" class="deck-container">
    <div v-if="!isDeckLoaded" class="add-deck-container">
      <p>{{ playerName }}</p>
      <input type="text" v-model="deckLink" placeholder="Enter link here">
      <button  @click="addDeck" :disabled="isLoading">Add Deck</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
    <div class="deck-actions" v-if="isDeckLoaded">
      <p>{{ playerName }}</p>
      <button @click="drawCard">Draw</button>
      <button @click="millCard">Mill</button>
      <button @click="scryCard">Scry</button>
      <button @click="lookCard">Look</button>
      <button @click="shuffleDeck">Shuffle</button>
      <button @click="resetDeck">Reset</button>
    </div>
</div>
  
</template>

<script>
  import axios from 'axios';

  export default {
    props: {
      playerName: String,
      roomId: String,
      pIndex: Number
    },
    data() {
      return {
        deckLink: '',
        isLoading: false,
        errorMessage: '',
        isDeckLoaded: false
      };
    },
    computed: {
      deckStyle() {
        switch (this.pIndex) {
          case 0:
            return {
              left: "50px",
              top: "0px"
            };
          case 1:
            return {
              left: "0px",
              top: "-280px"
            };
          case 2:
            return {
              left: "-200px",
              top: "-280px"
            };
          case 3:
            return {
              left: "-200px",
              top: "0px"
            };
        }  
      }
    },
    methods: {
      async addDeck() {
        if (!this.deckLink) {
          this.errorMessage = "The URL cannot be empty.";
          return;
        }

        this.isLoading = true;
        this.errorMessage = ''; // Reset the error message
        try {
          const response = await axios.post('http://localhost:8000/deck', { url: this.deckLink });
          console.log(response.data);
          this.$emit('add-deck', response.data);
          this.isDeckLoaded = true;

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
      async resetDeck() {
        try{
          const response = await axios.post('http://localhost:8000/room/' + this.roomId +'/player/'+ this.playerName + '/deck/reset', {});
          console.log(response.data);
          this.isDeckLoaded = false;
        } catch (error) {
          console.log(error);
        }
        
      },
      async millCard() {
        try{
          const response = await axios.post('http://localhost:8000/room/' + this.roomId +'/player/'+ this.playerName + '/deck/mill', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
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
}

.add-deck-container button {
  background-color: #f0f0f0;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.add-deck-container button[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.deck-actions {
  background: url(../assets/card_back.webp);
  background-size: contain;
  padding: 10px;
  border-radius: 5px;
  height: 100%; 
  width: 100%; 
  box-sizing: border-box; 
}

.deck-actions button {
  background-color: #4CAF50; /* Example color */
  color: white;
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.deck-actions button:hover {
  background-color: #45a049;
}

</style>
