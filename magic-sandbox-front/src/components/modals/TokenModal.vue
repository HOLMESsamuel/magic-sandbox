<template>
    <div v-if="isTokenModalVisible" class="token-modal" @click="closeModal">
      <div class="modal-content" @click.stop> <!--allow to click anywhere to close the modal except on the card-->
        <input 
          type="text"
          placeholder="Token text"
          v-model="tokenText"
        >
        <div class="radio-container">
          <label>
            <input name="tokenTypeInput" type="radio" v-model="tokenType" value="token">
            Token
          </label>
          <label>
            <input name="tokenTypeInput" type="radio" v-model="tokenType" value="counter">
            Counter
          </label>
        </div>
        
        
        <div class="confirm-button-container">
          <button class="confirm-button" @click="confirm">Create</button>
        </div>
        <button class="close-button" @click.stop="closeModal"></button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    emits: ["close-token-modal", "create-token"],
    props: {
      isTokenModalVisible: Boolean
    },
    data () {
      return {
        tokenText: '',
        tokenType: "token"
      };
    },
    methods: {
      closeModal() {
        this.$emit('close-token-modal');
      },
      confirm() {
        this.$emit('create-token', {text: this.tokenText, type: this.tokenType});
        this.closeModal();
      }
    }
  };
  </script>
  
  <style>
  .token-modal {
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
  
  .modal-content {
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

.token-modal input[type="text"] {
  width: 80%;
  padding: 8px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.token-modal input[type="checkbox"] {
  margin-right: 5px;
}

.token-modal label {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.token-modal .radio-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.confirm-button-container {
  display: flex;
  justify-content: center;
}

.token-modal .confirm-button {
  background-color: #4CAF50; /* Green */
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.token-modal .confirm-button:hover {
  background-color: #45a049;
}
  </style>
  