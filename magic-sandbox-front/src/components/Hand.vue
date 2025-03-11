<template>
    <div class="hand-container" :style="handStyle">
      <div v-if="pIndex == userIndex" v-for="(card, index) in cards" :key="index" class="hand-card" @mouseover="hoverCard(index)"
      @mouseleave="unhoverCard(index)" @click.stop="showCard(card.image)" :style="conditionalCardStyle(index, card)">
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
          :userIndex="userIndex"
          :tapped="card.tapped"
          :inHand="true"
          :maxZIndex="maxZIndex"
          :flipped="card.flipped"
          :flipImage="card.flip_image"
          :reverseMovement="reverseMovement"
          @play-card="handleCardDrop($event, card.id)"
          @move-from-hand-to-hand="moveFromHandToHand($event)"
          @show-card="showCard($event)"
          @open-move-to-deck-modal="emitMoveToDeckModalEvent($event)"
          @move-to-graveyard="moveToGraveyard($event)"
        ></Card>
      </div>
      <div v-if="pIndex != userIndex" v-for="(card, index) in cards" :key="index" class="hand-card">
        <img src="/magic/card_back.webp" :style="hiddenCardStyle" class="Card Image">
      </div>
    </div>
  </template>
  
  <script>
  import Card from './Card.vue'
  import axios from 'axios';

  export default {
    emits: ['open-move-to-deck-modal', 'show-card', 'move-from-hand-to-hand', 'move-to-graveyard'],
    components: {
      Card
    },
    data() {
      return {
        hoveredCardIndex: null
      };
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
      isCardFromHandMoving() {
        return this.cards.some(card => card.id === this.$store.state.currentlyDraggingCardId);
      },
      hiddenCardStyle() {
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
      handStyle() {
        const zIndex = this.isCardFromHandMoving ? this.maxZIndex - 1 : this.maxZIndex;
        switch (this.pIndex) {
          case 0:
            return {
              left: "800px",
              top: "1600px",
              'z-index': zIndex
            };
          case 1:
            return {
              left: "350px",
              top: "-1900px",
              'z-index': zIndex
            };
          case 2:
            return {
              left: "-2100px",
              top: "-1900px",
              'z-index': zIndex
            };
          case 3:
            return {
              left: "-1850px",
              top: "1600px",
              'z-index': zIndex
            };
        }  
      },
    },
    methods: {
      hoverCard(index) {
        this.hoveredCardIndex = index;
      },
      unhoverCard(index) {
        if (this.hoveredCardIndex === index) {
          this.hoveredCardIndex = null;
        }
      },
      getCardStyle(index, card) {
        let expandOrigin = this.reverseMovement ? "top" : "bottom";
        const isHorizontal = card.horizontal || false;
        if (this.hoveredCardIndex === index) {
          return {
            width: isHorizontal ? '280px' : '200px',
            height: isHorizontal ? '200px' : '280px',
            transform: 'scale(2.5)',
            'z-index': 100,
            transition: 'transform 0.2s ease-in-out',
            'transform-origin': expandOrigin + ' center'
          };
        }
        return {
            width: isHorizontal ? '280px' : '200px',
            height: isHorizontal ? '200px' : '280px', 
          };
      },
      conditionalCardStyle(index, card) {
        if (this.$store.state.currentlyDraggingId !== card.id) {
          return this.getCardStyle(index, card);
        }
        return;
      },
      async handleCardDrop(position, cardId) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + cardId + '/play', position);
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      emitMoveToDeckModalEvent(event) {
        this.$emit('open-move-to-deck-modal', event);
      },
      showCard(imageSrc) {
        console.log(imageSrc);
        this.$emit('show-card', imageSrc);
      },
      moveFromHandToHand(event) {
            this.$emit('move-from-hand-to-hand', event);
      },
      moveToGraveyard(event) {
          this.$emit('move-to-graveyard', event);
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
    cursor: pointer;
  }

  .hand-card img {
  width: 100%;
  height: auto;
  display: block;
}
  </style>
  