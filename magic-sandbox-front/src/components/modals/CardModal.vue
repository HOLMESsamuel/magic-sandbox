<template>
    <div v-if="isCardModalVisible && !isMoveToDeckModalVisible" class="cardModal" @click="closeModal">
      <div class="card-modal-content">
        <img :src="getCardImageSource()" alt="Enlarged Card" />
        <img v-if="modalFlipImageSrc && modalFlipImageSrc !== DEFAULT_CARD_BACK_URL" :src="modalFlipImageSrc" alt="Enlarged Card flipped" />
        <button class="close-button" @click.stop="closeModal"></button>
      </div>
    </div>
  </template>
  
  <script>
  import { DEFAULT_CARD_BACK_URL } from '../../constants';
  import { getLocalCardImageUrl } from '../../utils/utils';

  export default {
    emits: ["close-card-modal"],
    data() {
      return {
        DEFAULT_CARD_BACK_URL
      }
    },
    props: {
      modalImageSrc: String,
      modalFlipImageSrc: String,
      modalImageName: String,
      isCardModalVisible: Boolean,
      isMoveToDeckModalVisible: Boolean
    },
    methods: {
      closeModal() {
        this.$emit('close-card-modal');
      },
      getCardImageSource() {
        if (this.modalImageSrc === "local") {
          return getLocalCardImageUrl('/sr/cards/', this.modalImageName, 'webp')
        } else {
          return this.modalImageSrc
        }
      },
    }
  };
  </script>
  
  <style>
  .cardModal {
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
  
  .card-modal-content {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    position: relative; /* Needed for absolute positioning of the button */
    overflow-y: hidden;
    overflow-x: hidden;
  }
  
  .card-modal-content img {
    max-width: 90vw;
    height: 90vh;
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
  </style>
  