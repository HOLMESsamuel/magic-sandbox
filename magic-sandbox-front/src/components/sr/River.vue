<template>
    <div class="river-container">
      <div class="river" :style="rotation">
        <div v-for="(card, index) in cards" :key="index" class="river-card" :style="getCardStyle(card)">
          <img :src="getCardImage(card.name)" :alt="card.name" draggable="false">
          <div class="card-button-container">
            <button class="take-card-button" @click="takeCard(card)">Take</button>
            <button class="scrap-card-button" @click="scrapCard(card)">Scrap</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { getLocalCardImageUrl } from '../../utils/utils';
  export default {
    name: 'River',
    props: {
      cards: {
        type: Array,
        required: true
      },
      userIndex: Number
    },
    emits: ['take-card', 'scrap-card'],
    methods: {
      getCardImage(cardName) {
        return getLocalCardImageUrl('/sr/cards/', cardName, 'webp');
      },
      takeCard(card) {
        this.$emit('take-card', card.id);
      },
      scrapCard(card) {
        this.$emit('scrap-card', card.id);
      },
      getCardStyle(card) {
        const isHorizontal = card.horizontal || false;
        return {
            width: isHorizontal ? '280px' : '200px',
            height: isHorizontal ? '200px' : '280px',
        };
    }
    },
    computed: {
        rotation() {
            let transformStyle = {};
            if(this.userIndex === 1 || this.userIndex ===2) {
            transformStyle.transform = 'rotate(180deg)';
            }

            if(this.$store.state.rotate === true) {
            if(transformStyle.transform) {
                transformStyle.transform = '';
            } else {
                transformStyle.transform = "rotate(180deg)";
            }
            }

            return transformStyle;
        },
    }
  };
  </script>
  
  <style>
  .river-container {
    position: fixed;
    top: 0;
    left: 0;
    transform: translate(-50%, -50%);
    background-color: rgba(0, 0, 0, 0.5);
    border: 2px solid #333;
    border-radius: 12px;
    padding: 10px;
    width: fit-content;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .river {
    display: flex;
    gap: 15px;
    justify-content: center;
    align-items: center;
  }
  
  .river-card {
    position: relative;
    margin: 5px;
    width: 200px;
    height: 280px;
    border: 1px solid #333;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .river-card img {
    width: 100%;
    height: auto;
    display: block;
  }
  
  /* Button container that keeps the buttons centered */
  .card-button-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
  
  /* Take button - Green */
  .take-card-button {
    background-color: #4CAF50; /* Green */
    color: white;
    font-size: 30px;
    padding: 10px 18px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }
  
  /* Scrap button - Red */
  .scrap-card-button {
    background-color: #F44336; /* Red */
    color: white;
    font-size: 20px;
    padding: 10px 18px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }
  
  /* Show buttons on hover */
  .river-card:hover .take-card-button,
  .river-card:hover .scrap-card-button {
    opacity: 1;
  }
  </style>
  
  