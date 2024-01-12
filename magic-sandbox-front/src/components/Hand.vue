<template>
    <div class="hand-container" :style="handStyle">
      <div v-if="pIndex == userIndex" v-for="(card, index) in cards" :key="index" class="hand-card">
        <Card :key="index"
          :imageSrc="card.image"
          :name="card.name"
          :scale="scale"
          :offsetX="offsetX" 
          :offsetY="offsetY"
          :pIndex="pIndex" 
          :player="player" 
          :id="card.id"
          :roomId="roomId" 
          :tapped="card.tapped"
          :inHand="true"
          :maxZIndex="maxZIndex"
          :reverseMovement="reverseMovement"
          @play-card="handleCardDrop($event, card.id)"
        ></Card>
      </div>
      <div v-if="pIndex != userIndex" v-for="(card, index) in cards" :key="index" class="hand-card">
        <img src="../assets/card_back.webp" alt="Card Image">
      </div>
    </div>
  </template>
  
  <script>
  import Card from './Card.vue'
  import axios from 'axios';

  export default {
    components: {
      Card
    },
    props: {
      roomId: String,
      cards: Array,
      pIndex: Number,
      userIndex: Number,
      player: String,
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      reverseMovement: {
        type: Boolean,
        default: false
      }, 
      maxZIndex: Number
    },
    computed: {
      handStyle() {
        switch (this.pIndex) {
          case 0:
            return {
              left: "800px",
              top: "1200px",
              'z-index': this.maxZIndex
            };
          case 1:
            return {
              left: "350px",
              top: "-1500px",
              'z-index': this.maxZIndex
            };
          case 2:
            return {
              left: "-2100px",
              top: "-1500px",
              'z-index': this.maxZIndex
            };
          case 3:
            return {
              left: "-1850px",
              top: "1200px",
              'z-index': this.maxZIndex
            };
        }  
      },
    },
    methods: {
      async handleCardDrop(position, cardId) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + cardId + '/play', position);
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      }
    }
  };
  </script>
  
  <style>
  .hand-container {
    position: fixed;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    padding: 10px;
    width: 1500px;
    height: 300px;
  }

  .hand-container:hover {
    z-index: 0;
  }
  
  .hand-card {
    margin: 5px;
    width: 200px;
    height: 280px;
    cursor: pointer;
  }

  .hand-card img {
  width: 100%;
  height: auto;
  display: block;
}
  </style>
  