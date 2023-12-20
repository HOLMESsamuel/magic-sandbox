<template>
    <div class="card" :style="cardStyle" @mousedown.stop="startDrag" @mouseover="hover = true" @mouseleave="hover = false" @mouseup="endDrag">
      <img :src="imageSrc" alt="Card Image">
      <!-- Hover Buttons -->
      <div v-if="hover" class="hover-buttons">
        <button v-if="tapped && !inHand" @click="untap" class="button-left">⟲</button>
        <button class="button-center" @click.stop="showCardDetail">👁️</button>
        <button v-if="!tapped && !inHand" @click="tap" class="button-right">⟳</button>
      </div>
    </div>
    <CardModal :imageSrc="imageSrc" ref="cardModal"></CardModal>
  </template>
  
  <script>
  import CardModal from './CardModal.vue';
  import axios from 'axios';

  export default {
    emits: ['update-position', 'show-card', 'play-card'],
    components: {
      CardModal
    },
    props: {
      imageSrc: String,
      initialPosition: {
        type: Object,
        default: () => ({ x: 100, y: 100 })
      },
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      pIndex: Number,
      reverseMovement: {
        type: Boolean,
        default: false
      },
      player: String,
      tapped: Boolean,
      id: String,
      roomId: String,
      inHand: Boolean
    },
    data() {
      return {
        position: this.initialPosition,
        isDragging: false,
        cardOffsetX: 0,
        cardOffsetY: 0,
        correctedX: null,
        correctedY: null,
        startDragPosition: null,
        hover: false
      };
    },
    mounted() {
      document.addEventListener('mousemove', this.drag);
    },
    computed: {
      cardStyle() {
        let transformStyles = '';

        // Add 90 degrees rotation if the card is tapped
        if (this.tapped) {
          transformStyles += 'rotate(90deg) ';
        }

        // Add 180 degrees rotation based on player index
        if (this.pIndex === 1 || this.pIndex === 2) {
          transformStyles += 'rotate(180deg) ';
        }

        if(this.inHand && !this.isDragging) {
          return {
          }
        }

        return {
          left: this.position.x + 'px',
          top: this.position.y + 'px',
          position: 'fixed',
          cursor: 'pointer',
          transform: transformStyles
        };
      }
    },
    methods: {
      startDrag(event) {
        event.preventDefault();
        this.isDragging = true;
        const correctedX = (event.clientX - this.offsetX) / this.scale;
        const correctedY = (event.clientY - this.offsetY) / this.scale;
        if (this.inHand) {
          this.position.x = correctedX;
          this.position.y = correctedY;
          this.cardOffsetX = 100;
          this.cardOffsetY = 140;
          this.startDragPosition = { x: this.position.x, y: this.position.y };
        } else {
          this.startDragPosition = { x: this.position.x, y: this.position.y };
          this.cardOffsetX = correctedX - this.position.x;
          this.cardOffsetY = correctedY - this.position.y;
        }
        console.log(this.startDragPosition);
        
        
      },
      drag(event) {
        if (!this.isDragging) return;
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        // Calculate the new position
        let newPositionX = mouseX - this.cardOffsetX;
        let newPositionY = mouseY - this.cardOffsetY;

        if (this.reverseMovement) {
          // For reversed movement, invert the direction
          newPositionX = - newPositionX + 2 * this.startDragPosition.x;
          newPositionY = - newPositionY + 2 * this.startDragPosition.y;
        }

        // Update the card's position
        this.position.x = newPositionX;
        this.position.y = newPositionY;
      },
      endDrag() {
        this.isDragging = false;
        if(this.inHand) {
          console.log("play card");
          this.$emit('play-card', { x: this.position.x, y: this.position.y });
        } else {
          this.$emit('update-position', { x: this.position.x, y: this.position.y });
        }
        
      },
      showCardDetail() {
        this.$emit('show-card', this.imageSrc);
      },
      async tap() {
        try{
          const response = await axios.post('http://localhost:8000/room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/tap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async untap() {
        try{
          const response = await axios.post('http://localhost:8000/room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/untap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      }
    }
  };
  </script>
  
  <style>
.card img {
  width: 100%;
  height: auto;
  display: block;
}

.card {
  position: relative; /* Needed to position child elements absolutely */
}

.hover-buttons {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: start;
}

.button-left, .button-center, .button-right {
  background: #FFF;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
}

.button-left:hover, .button-center:hover, .button-right:hover{
  background: #a99d9d;
}

.button-center {
  margin: 0 auto;
}
</style>

  