<template>
    <div class="token" :style="[tokenStyle, tokenShape, tokenColor]" @click.stop="toogleTap" @mousedown.stop="startDrag" @mouseover="hover = true" @mouseleave="hover = false" @mouseup.stop="endDrag">
      <p>{{ text }}</p>  
      <div v-if="hover" class="hover-buttons">
        <button class="token-button" @click.stop="modifyToken">✏️</button>
        <button class="token-button" @click.stop="deleteToken">X</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { eventBus } from '../eventBus';

  export default {
    emits: ['update-token-position', 'open-edit-token-modal'],
    props: {
      initialPosition: {
        type: Object,
        default: () => ({ x: 100, y: 100 })
      },
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      pIndex: Number,
      userIndex: Number,
      reverseMovement: {
        type: Boolean,
        default: false
      },
      player: String,
      tapped: Boolean,
      id: String,
      roomId: String,
      name: String,
      zIndex: Number,
      maxZIndex: Number,
      text: String,
      type: String
    },
    data() {
      return {
        position: this.initialPosition,
        correctedX: null,
        correctedY: null,
        hover: false
      };
    },
    mounted() {
      document.addEventListener('mousemove', this.drag);
      eventBus.on('moveCard', this.onMoveCard);
    },
    beforeUnmount() {
      eventBus.off('moveCard', this.onMoveCard);
    },
    computed: {
      isSelected() {
        return this.$store.state.selectedTokenIds.includes(this.id);
      },
      isTokenDragging() {
        return this.$store.state.currentlyDraggingId === this.id;
      },
      startDragTokenPosition() {
        return this.$store.state.startDragPosition;
      },
      tokenOffset() {
        return this.$store.state.offset;
      },
      tokenStyle() {
        let transformStyles = '';
        let zIndex = 2;
        let border = "black solid 2px";

        if(this.zIndex) {
          zIndex = this.zIndex;
        }
        
        if(this.isTokenDragging) {
          zIndex = this.maxZIndex + 1;
        }

        // Add 90 degrees rotation if the card is tapped
        if (this.tapped) {
          transformStyles += 'rotate(90deg) ';
        }

        if(this.isSelected) {
          border = "solid red 6px";
        }

        // Add 180 degrees rotation based on player index
        if (this.pIndex === 1 || this.pIndex === 2) {
          transformStyles += 'rotate(180deg) ';
        }

        return {
          left: this.position.x + 'px',
          top: this.position.y + 'px',
          position: 'fixed',
          cursor: 'pointer',
          transform: transformStyles,
          'z-index': zIndex,
          'border': border
        };
      },
      tokenShape() {
        if(this.type === "token") {
          return {
            width: "200px",
            height: "280px",
            "border-radius": "10px"
          };
        } else if (this.type === "counter") {
          return {
            width: "100px",
            height: "100px",
            "border-radius": "50px"
          };
        }
      },
      tokenColor() {
        switch (this.pIndex) {
            case 0:
                return {background : "rgb(196, 211, 202)"} //green
            case 1:
                return {background : "rgb(179, 206, 234)"} //blue
            case 2:
                return {background : "rgb(235, 159, 130)"} //red
            case 3:
                return {background : "rgb(248, 231, 185)"} //yellow
          } 
      }
    },
    methods: {
      startDrag(event) {
        event.preventDefault();

        // Calculate the initial position based on the cursor position
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        
        let tokenOffsetX = mouseX - this.position.x;
        let tokenOffsetY = mouseY - this.position.y;

        this.$store.commit('startDragging', {
          id : this.id, 
          startClientX: event.clientX,
          startClientY: event.clientY,
          startDragPosition : { x: this.position.x, y: this.position.y }, 
          offset : {x: tokenOffsetX, y : tokenOffsetY}
        });
      },
      drag(event) {
        if (this.$store.state.currentlyDraggingId !== this.id) return;
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        // Calculate the new position
        let newPositionX = mouseX - this.tokenOffset.x;
        let newPositionY = mouseY - this.tokenOffset.y;

        if (this.reverseMovement) {
          // For reversed movement, invert the direction
          newPositionX = - newPositionX + 2 * this.startDragTokenPosition.x;
          newPositionY = - newPositionY + 2 * this.startDragTokenPosition.y;
        }

        let deltax = this.position.x - newPositionX;
        let deltay = this.position.y - newPositionY;

        if(this.$store.state.selectedTokenIds.includes(this.id)) {
            eventBus.emit('moveCard', {
              id: this.id,
              deltax: deltax,
              deltay: deltay,
            });
        } else {
          // Update the card's position
          this.position.x = newPositionX;
          this.position.y = newPositionY;
        }
      },
      endDrag() {
        this.$store.commit('endDragging');
        this.$emit('update-token-position', { x: this.position.x, y: this.position.y });
        return;
      },
      async toogleTap() {
        if(this.type === "token") {
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
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/token/' + this.id + '/tap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async untap() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/token/' + this.id + '/untap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async deleteToken() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.delete(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/token/' + this.id, {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      modifyToken() {
        this.$emit('open-edit-token-modal', { text: this.text, type: this.type, id: this.id });
        return;
      },
      onMoveCard(payload) {
        if (this.$store.state.selectedTokenIds.includes(this.id)) {
          this.position.x -= payload.deltax;
          this.position.y -= payload.deltay;
        }
      }
    }
  };
  </script>
  
  <style>

.token {
  position: fixed;
  cursor: pointer;
  font-size: 2em;
  text-align: center;
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

.token-button {
  background: #FFF;
  border: none;
  cursor: pointer;
  padding: 5px;
  height: 60px;
  width: 60px;
  font-size: 1.2em;
  border-radius: 50%;
}

.token-button:hover {
  background: #a99d9d;
}

.token-button {
  margin: 0 auto;
}
</style>

  