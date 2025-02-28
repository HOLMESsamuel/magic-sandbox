<template>
    <div class="river-container">
      <div class="river">
        <div v-for="(card, index) in cards" :key="index" class="river-card">
          <img :src="getCardImage(card.name)" :alt="card.name" />
          <button class="take-card-button" @click="takeCard(card)">Take</button>
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
    emits: ['take-card'],
    methods: {
      getCardImage(cardName) {
        return getLocalCardImageUrl('../assets/sr/cards/', cardName, 'webp');
      },
      takeCard(card) {
        this.$emit('take-card', card.id);
        console.log(card.id)
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
    width: 140%;
    height: auto;
    display: block;
  }
  
  .take-card-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }
  
  .river-card:hover .take-card-button {
    opacity: 1;
  }
  </style>
  