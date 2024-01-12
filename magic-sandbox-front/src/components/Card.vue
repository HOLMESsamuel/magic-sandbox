<template>
    <div class="card" :style="cardStyle" @click="toogleTap" @mousedown.stop="startDrag" @mouseover="hover = true" @mouseleave="hover = false" @mouseup="endDrag">
      <img :src="imageSrc" :alt="name">
      <!-- Hover Buttons -->
      <div v-if="hover" class="hover-buttons">
        <button class="button-center" @click.stop="showCardDetail">👁️</button>
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
      inHand: Boolean,
      name: String,
      zIndex: Number,
      maxZIndex: Number
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
        let zIndex = 2;

        if(this.zIndex) {
          zIndex = this.zIndex;
        }
        
        if(this.isDragging) {
          zIndex = this.maxZIndex + 1;
        }

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
            transform: transformStyles
          }
        }

        return {
          left: this.position.x + 'px',
          top: this.position.y + 'px',
          position: 'fixed',
          cursor: 'pointer',
          transform: transformStyles,
          'z-index': zIndex
        };
      }
    },
    methods: {
      startDrag(event) {
        event.preventDefault();
        this.isDragging = true;

        // Calculate the initial position based on the cursor position
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        if (this.inHand) {
          // If in hand, set the initial position under the cursor
          this.position.x = mouseX;
          this.position.y = mouseY;
          this.cardOffsetX = mouseX - this.position.x + 100;
          this.cardOffsetY = mouseY - this.position.y + 140;
          
          if(this.reverseMovement) {
            this.position.x = -mouseX + 1300;
            this.position.y = -mouseY - 200;
            this.cardOffsetX = mouseX - this.position.x + 100;
            this.cardOffsetY = mouseY - this.position.y + 140;
          }
          
        } else {
          this.cardOffsetX = mouseX - this.position.x;
          this.cardOffsetY = mouseY - this.position.y;
        }

        this.startDragPosition = { x: this.position.x, y: this.position.y };
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
          this.$emit('play-card', { x: this.position.x, y: this.position.y });
        } else {
          this.$emit('update-position', { x: this.position.x, y: this.position.y });
        }
        
      },
      showCardDetail() {
        this.$emit('show-card', this.imageSrc);
      },
      async toogleTap() {
        if(!this.inHand) {
          if(this.tapped) {
            this.untap();
          } else {
            this.tap();
          }
        } 
      },
      async tap() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/tap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async untap() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/untap', {});
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

.button-center {
  background: #FFF;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
}

.button-center:hover {
  background: #a99d9d;
}

.button-center {
  margin: 0 auto;
}
</style>

  