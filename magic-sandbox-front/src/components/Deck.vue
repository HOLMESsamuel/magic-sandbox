<template>
<div class="deck-container">
    <div class="add-deck-container">
    <input type="text" v-model="deckLink" placeholder="Enter link here">
    <button @click="addDeck" :disabled="isLoading">Add Deck</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</div>
  
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        deckLink: '',
        isLoading: false,
        errorMessage: ''
      };
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
          // Handle the response as needed
        } catch (error) {
          if (error.response && error.response.data && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          } else {
            this.errorMessage = "An error occurred while processing the request.";
          }
        } finally {
          this.isLoading = false;
        }
      }
    }
  };
</script>

<style>
.deck-container {
  position: relative;
  top: 52vh;
  left: 83vw;
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

</style>
