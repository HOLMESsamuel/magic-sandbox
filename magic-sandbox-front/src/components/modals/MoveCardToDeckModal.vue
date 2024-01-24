<template>
    <div v-if="isMoveToDeckModalVisible" class="add-to-deck-modal" @click="closeModal">
      <div class="modal-content" @click.stop> <!--allow to click anywhere to close the modal except on the card-->
        <p>Move card to the deck</p>
        <input 
          type="number" 
          v-model="cardPosition" 
          :disabled="lastPositionChecked" 
          :max="deckLength - 1" 
          min="0" 
          placeholder="Enter position"
        >
        <label>
          <input 
            type="checkbox" 
            v-model="lastPositionChecked"
            @change="handleCheckboxChange"
          >
          Last Position
        </label>
      <button class="confirm-button" @click="confirmMove">OK</button>
      <button class="close-button" @click.stop="closeModal"></button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    emits: ["close-move-to-deck-modal", "confirm-move"],
    props: {
      isMoveToDeckModalVisible: Boolean,
      deckLength: Number,
      cardId: String
    },
    data() {
      return {
        cardPosition: 0,
        lastPositionChecked: false
      };
    },
    methods: {
      closeModal() {
        this.$emit('close-move-to-deck-modal');
      },
      async confirmMove() {
        this.$emit('confirm-move', {cardId:this.cardId, cardPosition:this.cardPosition});
        this.closeModal();
      },
      handleCheckboxChange() {
        if (this.lastPositionChecked) {
          this.cardPosition = this.deckLength;
        }
      }
    }
  };
  </script>
  
  <style>
  .add-to-deck-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .add-to-deck-modal .modal-content {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    position: relative; /* Needed for absolute positioning of the button */
  }

  .close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
}

.close-button::before, .close-button::after {
  content: '';
  position: absolute;
  height: 100%;
  width: 2px;
  background-color: black;
  top: 0;
  left: 50%;
}

.close-button::before {
  transform: rotate(45deg);
}

.close-button::after {
  transform: rotate(-45deg);
}

.add-to-deck-modal input[type="number"] {
  width: 80%;
  padding: 8px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.add-to-deck-modal input[type="checkbox"] {
  margin-right: 5px;
}

.add-to-deck-modal label {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.add-to-deck-modal .confirm-button {
  background-color: #4CAF50; /* Green */
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.add-to-deck-modal .confirm-button:hover {
  background-color: #45a049;
}
  </style>
  