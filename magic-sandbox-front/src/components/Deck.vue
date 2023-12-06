<template>
<div class="deck-container">
    <div class="add-deck-container">
    <input type="text" v-model="deckLink" placeholder="Enter link here">
    <button @click="addDeck">Add Deck</button>
  </div>
</div>
  
</template>

<script>
export default {
  data() {
    return {
      deckLink: ''
    };
  },
  methods: {
    addDeck() {
      this.$emit('add-deck', this.deckLink);
    }
  }
};
</script>

<style>
.deck-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
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
</style>
