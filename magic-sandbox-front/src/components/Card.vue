<template>
    <div class="card" :style="cardStyle" @mousedown.stop="startDrag" @mouseover="hover = true" @mouseleave="hover = false" @mouseup="endDrag" @contextmenu.prevent="showCustomMenu($event)">
      <img :src="flipped ? flipImage : imageSrc" :alt="name">
      <!-- Hover Buttons -->
      <div v-if="!inHand && hover" class="hover-buttons">
        <button class="button-center">👁️</button>
      </div>
    </div>
    <div v-if="showMenu" class="menu" :style="customMenuStyle" @contextmenu.prevent="this.showMenu = false">
      <!-- Custom menu content here -->
      <ul>
        <li @click="flipCard">Flip</li>
        <li @click="openMoveToDeckModal">Move to deck</li>
        <li v-if="!this.inHand" @click="moveToHand(this.userIndex)">Move to hand</li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import * as Constants from '../constants'
  import {checkIfCardInPlayerDeck, checkIfCardInPlayerGraveyard, checkIfCardInPlayerHand} from '../utils/utils'

  export default {
    emits: ['update-position', 'show-card', 'play-card', 'move-from-hand-to-hand', 'move-from-board-to-hand', 'open-move-to-deck-modal', 'move-to-graveyard'],
    props: {
      imageSrc: String,
      initialPosition: {
        type: Object,
        default: () => ({ x: 100, y: 100 })
      },
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      pIndex: Number, //index of the player owning the card
      userIndex: Number, //index of the player
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
      maxZIndex: Number,
      flipped: Boolean,
      flipImage: String

    },
    data() {
      return {
        position: this.initialPosition,
        correctedX: null,
        correctedY: null,
        hover: false,
        showMenu: false,
        menuPosition: { x: 0, y: 0 }
      };
    },
    mounted() {
    document.addEventListener('mousemove', this.drag);
  },
    computed: {
      isDragging() {
        return this.$store.state.currentlyDraggingCardId === this.id;
      },
      startDragPosition() {
        return this.$store.state.startDragPosition;
      },
      cardOffset() {
        return this.$store.state.cardOffset;
      },
      cardStyle() {
        let transformStyles = '';
        let zIndex = 2;
        let border = 'none'

        if(this.imageSrc === '') {
          border = "solid black 1px";
        }

        if(this.zIndex) {
          zIndex = this.zIndex;
        }
        
        if(this.$store.state.currentlyDraggingCardId === this.id) {
          zIndex = this.maxZIndex + 1000;
        }

        // Add 90 degrees rotation if the card is tapped
        if (this.tapped) {
          transformStyles += 'rotate(90deg) ';
        }

        // Add 180 degrees rotation based on player index
        if (this.pIndex === 1 || this.pIndex === 2) {
          transformStyles += 'rotate(180deg) ';
        }

        if(this.inHand && this.isDragging === false) {
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
          'z-index': zIndex,
          'border': border
        };
      },
      customMenuStyle() {
        let transformStyles = '';

        // Add 180 degrees rotation based on player index
        if (this.pIndex === 1 || this.pIndex === 2) {
          transformStyles += 'rotate(180deg) ';
        }

        return {
          transform: transformStyles,
          top: this.menuPosition.y + 'px',
          left: this.menuPosition.x + 'px'
        };
      },
      handX() {
        switch (this.pIndex) {
          case 0:
            return Constants.PLAYER_0_HAND_X1;
          case 1:
            return Constants.PLAYER_1_HAND_X1;
          case 2:
            return Constants.PLAYER_2_HAND_X1;
          case 3:
            return Constants.PLAYER_3_HAND_X1;
        }
      },
      handY() {
        switch (this.pIndex) {
          case 0:
            return Constants.PLAYER_0_HAND_Y1;
          case 1:
            return Constants.PLAYER_1_HAND_Y1;
          case 2:
            return Constants.PLAYER_2_HAND_Y1;
          case 3:
            return Constants.PLAYER_3_HAND_Y1;
        }
      },
    },
    methods: {
      startDrag(event) {
        if(this.isDragging === true) {
          return;
        }
        if(event.button === 2 ) { //right click
          return;
        }
        event.preventDefault();

        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        let cardOffsetX = mouseX - this.position.x;
        let cardOffsetY = mouseY - this.position.y;

        if (this.inHand) {
          cardOffsetX = Constants.CARD_HALF_WIDTH;
          cardOffsetY = Constants.CARD_HALF_HEIGHT;
          
          if(this.reverseMovement) {
            cardOffsetX = 2 * mouseX - window.innerWidth + Constants.CARD_HALF_WIDTH;
            cardOffsetY = 2 * mouseY + Constants.CARD_HALF_HEIGHT;
          }

          this.position.x = mouseX - cardOffsetX;
          this.position.y = mouseY - cardOffsetY;
          
        }

        this.$store.commit('startDragging', {
          cardId : this.id, 
          startDragPosition : { x: this.position.x, y: this.position.y }, 
          cardOffset : {x: cardOffsetX, y : cardOffsetY}
        });
      },
      drag(event) {
        if (this.$store.state.currentlyDraggingCardId === this.id) { //if the card is supposed to be dragging
          const mouseX = (event.clientX - this.offsetX) / this.scale;
          const mouseY = (event.clientY - this.offsetY) / this.scale;

          // Calculate the new position
          let newPositionX = mouseX - this.cardOffset.x;
          let newPositionY = mouseY - this.cardOffset.y;

          if (this.reverseMovement) {
            // For reversed movement, invert the direction
            newPositionX = - newPositionX + 2 * this.startDragPosition.x;
            newPositionY = - newPositionY + 2 * this.startDragPosition.y;
          }

          // Update the card's position
          this.position.x = newPositionX;
          this.position.y = newPositionY;
          return;
        }
      },
      endDrag(event) {
        const draggedDistance = Math.sqrt(Math.pow(this.position.x - this.startDragPosition.x, 2) + Math.pow(this.position.y - this.startDragPosition.y, 2));
        this.$store.commit('endDragging');
        let handPlayerIndex = checkIfCardInPlayerHand(this.position.x, this.position.y);
        let deckPlayerIndex = checkIfCardInPlayerDeck(this.position.x, this.position.y);
        let graveyardPlayerIndex = checkIfCardInPlayerGraveyard(this.position.x, this.position.y);
        
        //can't use a click because it triggers with mousedown, if the card does not move I consider it a click
        if(draggedDistance < 5) {
          this.handleCardClick(event);
          return;
        }

        if(this.isReturningToSameHand(handPlayerIndex)) {
          return;
        }

        if(this.isMovingHandToHand(handPlayerIndex)) {
          this.$emit('move-from-hand-to-hand', { cardId: this.id, targetPlayerIndex: handPlayerIndex });
          return;
        }

        if(this.isMovingBoardToHand(handPlayerIndex)) {
          this.moveToHand(handPlayerIndex);
          return;
        }

        if(this.isMovingToGraveyard(graveyardPlayerIndex)){
          this.moveToGraveyard(graveyardPlayerIndex);
          return
        }

        if(this.isMovingFromHandToDeck(deckPlayerIndex) || this.isMovingBoardToDeck(deckPlayerIndex)) {
          this.openMoveToDeckModal();
          return;
        }

        if(this.isMovingHandToBoard()) {
          this.$emit('play-card', { x: this.position.x, y: this.position.y });
          return;
        } 

        if(this.isMovingBoardToBoard()) {
          this.$emit('update-position', { x: this.position.x, y: this.position.y });
          return;
        }
      },
      isReturningToSameHand(handPlayerIndex) {
        return this.inHand && handPlayerIndex === this.userIndex;
      },
      isMovingHandToHand(handPlayerIndex) {
        return handPlayerIndex !== null && this.inHand && handPlayerIndex !== this.userIndex;
      },
      isMovingBoardToHand(handPlayerIndex) {
        return handPlayerIndex !== null && !this.inHand;
      },
      isMovingBoardToDeck(deckPlayerIndex) {
        return deckPlayerIndex !== null && !this.inHand;
      },
      isMovingFromHandToDeck(deckPlayerIndex) {
        return deckPlayerIndex !== null && deckPlayerIndex === this.userIndex && this.inHand;
      },
      isMovingToGraveyard(graveyardPlayerIndex) {
        return graveyardPlayerIndex !== null
      },
      isMovingHandToBoard() {
        return this.inHand;
      },
      isMovingBoardToBoard() {
        return !this.inHand;
      },
      showCardDetail() {
        this.$emit('show-card', {image: this.imageSrc, flipImage: this.flipImage});
      },
      openMoveToDeckModal() {
        this.$emit('open-move-to-deck-modal', this.id);
      },
      moveToHand(handPlayerIndex) {
        this.$emit('move-from-board-to-hand', { cardId: this.id, targetPlayerIndex: handPlayerIndex });
      },
      moveToGraveyard(graveyardPlayerIndex) {
        this.$emit('move-to-graveyard', { cardId: this.id, targetPlayerIndex: graveyardPlayerIndex });
      },
      showCustomMenu(event) {
        if(this.pIndex === this.userIndex) {// only the card owner can use right click
          this.showMenu = !this.showMenu;
          const mouseX = (event.clientX - this.offsetX) / this.scale;
          const mouseY = (event.clientY - this.offsetY) / this.scale;
          if(this.inHand) {
            if(this.reverseMovement) {
              this.menuPosition = { 
                x: -mouseX + window.innerWidth - this.handX - Constants.CARD_HALF_WIDTH, 
                y: -mouseY - this.handY - Constants.CARD_HALF_HEIGHT
              };
            } else {
              this.menuPosition = { 
                x: mouseX-this.handX-Constants.CARD_HALF_WIDTH, 
                y: mouseY-this.handY-Constants.CARD_HALF_HEIGHT
              };
            }
          } else {
            if(this.reverseMovement) {
              this.menuPosition = { x: -mouseX + window.innerWidth, y: -mouseY};
            } else {
              this.menuPosition = { x: mouseX, y: mouseY};
            }
          }
          
          event.preventDefault();
        }
      },
      handleCardClick(event) {
        if(event.button === 2 ) { //right click
          return;
        }
        this.showMenu = false;
        if (this.dragging) {
          // If dragging, don't execute any click logic
          return;
        }

        if (event.target.matches('.button-center')) {
          // If the clicked element is the show button
          this.showCardDetail();
          return;
        }

        if (this.inHand) {
          this.showCardDetail();
        } else {
          this.toogleTap();
        }
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
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/tap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async untap() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/untap', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async flipCard() {
        this.showMenu = false;
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/' + this.id + '/flip', {});
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

.menu {
  position: absolute;
  border: 1px solid #ccc;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  z-index: 1000; /* Ensure the menu appears above other content */
}

.menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu li {
  padding: 8px 12px;
  cursor: pointer;
}

.menu li:hover {
  background-color: #f0f0f0;
}

.custom-context-menu {
  padding: 20px;
  background-color: #eee;
  border: 1px solid #ddd;
}
</style>

  