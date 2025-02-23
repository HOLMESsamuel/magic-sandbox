<template>
    <div class="river-container">
      <div class="river">
        <div v-for="(card, index) in cards" :key="index" class="river-card">
          <img :src="getCardImage(card.name)" :alt="card.name" />
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
      }
    },
    methods: {
      getCardImage(cardName) {
        return getLocalCardImageUrl('../assets/sr/cards/', cardName, 'webp');
      }
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
    width:140%;
    height: auto;
    display: block;
  }

.card {
    width: 400px;
    height: 560px;
    border: 1px solid #333;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  </style>
  
