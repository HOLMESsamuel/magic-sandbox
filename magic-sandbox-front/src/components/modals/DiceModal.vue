<template>
    <div v-if="isDiceModalVisible" class="dice-modal" @click="closeModal">
      <div class="modal-content" @click.stop> <!--allow to click anywhere to close the modal except on the card-->
        <p>Dice value</p>
        <div class="radio-container">
          <label>
            <input name="dice value" type="radio" v-model="diceValue" value="20">
            20
          </label>
          <label>
            <input name="dice value" type="radio" v-model="diceValue" value="6">
            6
          </label>
        </div>
        
        
        <div class="throw-button-container">
          <button class="throw-button" @click="confirm">Throw</button>
        </div>
        <button class="close-button" @click.stop="closeModal"></button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    emits: ["close-dice-modal", "throw-dice"],
    props: {
      isDiceModalVisible: Boolean
    },
    data () {
        return {
            diceValue: 20
        }
    },
    methods: {
      closeModal() {
        this.$emit('close-dice-modal');
      },
      confirm() {
        console.log(this.diceValue);
        this.$emit('throw-dice', this.diceValue);
        this.closeModal();
      }
    }
  };
  </script>
  
  <style>
  .dice-modal {
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

.dice-modal input[type="text"] {
  width: 80%;
  padding: 8px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.dice-modal input[type="checkbox"] {
  margin-right: 5px;
}

.dice-modal label {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.dice-modal .radio-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.throw-button-container {
  display: flex;
  justify-content: center;
}

.dice-modal .throw-button {
  background-color: #4CAF50; /* Green */
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.dice-modal .throw-button:hover {
  background-color: #45a049;
}
  </style>
  