<template>
    <div v-if="isSettingsModalVisible" class="modal" @click="closeModal">
      <div class="settings-modal-content" @click.stop>
        <div class="sound-switch-container">
          <label>Sound : </label>
          <button v-if="this.$store.state.soundOn === true" @click="toggleSound" class="sound-button sound-button-on">
            <p>ON</p>
          </button>
          <button v-if="this.$store.state.soundOn === false" @click="toggleSound" class="sound-button sound-button-off">
            <p>OFF</p>
          </button>
        </div>
        <div class="disconnect-button-container">
          <button :onClick="disconnect" class="disconnect-button">disconnect</button>
        </div>
        <button class="close-button" @click.stop="closeModal"></button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    emits: ["close-settings-modal", "disconnect"],
    props: {
      isSettingsModalVisible: Boolean
    },
    data() {
      return {
        hover: false
      };
    },
    methods: {
      closeModal() {
        this.$emit('close-settings-modal');
      },
      disconnect() {
        this.$emit('disconnect');
        this.closeModal();
      },
      toggleSound() {
        this.$store.commit('toggleSound');
      }
    }
  };
  </script>
  
  
  <style>
  .modal {
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
  
  .settings-modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  position: relative; /* Needed for absolute positioning of the button */
  max-height: 90vh;
  display: flex;
  flex-direction: column;
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

  .disconnect-button {
    background-color: #c51e1e;
    color: white;
    padding: 10px 20px;
    margin-top: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }

  .settings-button {
    background: none;
    border: none;
  }

  .disconnect-button-container {
    align-self: center;
    margin: 0 auto;
  }

  .sound-switch-container {
    display: flex;
    align-self: center;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    gap: 5px;
  }

  .sound-switch-container > label {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .sound-button {
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    height: 30px;
    width: 50px;
    text-align: center;
  }

  .sound-button-on {
    background-color: #4CAF50;
  }

  .sound-button-on:hover {
    background-color: #45a049;
  }

  .sound-button-off {
    background-color: #c51e1e;
  }

  .sound-button-off:hover {
    background-color: #a51717;
  }
  </style>
  