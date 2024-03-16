<template>
    <div v-if="isSettingsModalVisible" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="sound-switch-container">
          <label>Sound</label>
          <button @click="toggleSound" class="sound-button">
            <!--<img v-if="this.$store.state.soundOn === true" src="./assets/sound-on.svg">
            <img v-if="this.$store.state.soundOn === false" src="./assets/sound-off.svg">-->
            <p v-if="this.$store.state.soundOn === true">ON</p>
            <p v-if="this.$store.state.soundOn === false">OFF</p>
          </button>
        </div>
        <button :onClick="disconnect" class="disconnect-button">disconnect</button>
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
  
  .modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  position: relative; /* Needed for absolute positioning of the button */
  overflow-y: auto; /* Enables vertical scrolling */
  max-height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
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

  .sound-button:hover{
    cursor: pointer;
  }
  </style>
  