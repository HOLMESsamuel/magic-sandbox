<template>
    <div :style="scrapStyle" class="scrap-container" @mouseover="hover = true" @mouseleave="hover = false">
        <div v-if="hover" class="hover-buttons">
            <button @click="openScrapModal" class="button-center">👁️</button>
        </div>
        <div class="scrap-image-container">
            <img v-if="cards && cards.length >0" :src="getCardImageSource(cards[cards.length-1])" draggable="false" class="last-scrap-card">
        </div>
    </div>
</template>
  
  <script>
    import axios from 'axios';
    import { getLocalCardImageUrl } from '../utils/utils';
  
    export default {
      props: {
        userIndex: Number,
        cards: Array
      },
      emits: ["open-scrap-modal"],
      data() {
        return {
            hover: false
        };
      },
      computed: {
        scrapStyle() {
            let transformStyles = '';

            // Add 180 degrees rotation based on player index
            if (this.userIndex === 1 || this.userIndex === 2) {
            transformStyles += 'rotate(180deg) ';
            }
            return {
            transform: transformStyles,
            left: "1000px",
            top: "-140px"
            };
        }  
      },
      methods: {
        openScrapModal() {
            this.$emit('open-scrap-modal');
        },
        getCardImageSource(card) {
        if (card.image === "local") {
          return getLocalCardImageUrl('/sr/cards/', card.name, 'webp')
        } else {
          return card.image
        }
      },
      },
    };
  </script>
  
  <style>
  .scrap-container {
    position: fixed;
    height: 300px;
    background-color: rgba(0, 0, 0, 0.5);
    border: 2px solid #333;
    border-radius: 12px;
    padding: 10px;
    width: 220px;
    margin: 0;
    box-sizing: border-box; 
  }

  .scrap-image-container img {
    width: 100%; 
    height: 100%; 
    object-fit:scale-down; 
    object-position: center; 

  }

  .last-scrap-card {
    position: relative; /* Allows the element to be positioned below the second image */
    z-index: 1;
  }

  .hover-buttons {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: start;
  z-index: 10; /* Ensure it's above the card image */
}

.button-center {
  background: #FFF;
  border: none;
  cursor: pointer;
  padding: 5px;
  height: 60px;
  width: 60px;
  font-size: 2em;
  border-radius: 50%;
}

.button-center:hover {
  background: #a99d9d;
}

.button-center {
  margin: 0 auto;
}
  
  </style>
  