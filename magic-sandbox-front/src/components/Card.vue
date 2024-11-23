<template>
  <div @mouseleave="showMenu = false">
    <div class="card" @click.stop="handleCardClick" :style="cardStyle" @dblclick.stop="handleCardDoubleClick()" @mousedown.stop="startDrag" @mouseover="hover = true" @mouseleave="hover = false" @mouseup.stop="endDrag" @contextmenu.prevent="showCustomMenu($event)">
      <div v-if="this.copy" class="text-overlay">Copy</div>
      <img :src="flipped ? flipImage : imageSrc" :alt="name">
      <!-- Hover Buttons -->
      <div v-if="!inHand && hover" class="hover-buttons">
        <button @click.stop="showCardDetail" class="button-center">👁️</button>
      </div>
    </div>
    <div v-if="showMenu" class="menu" :style="customMenuStyle" @contextmenu.prevent="this.showMenu = false">
        <ul>
          <li @click.stop="flipCards">Flip</li>
          <li @click.stop="openMoveToDeckModal">Move to deck</li>
          <li v-if="!this.inHand" @click.stop="copyCard">Copy</li>
          <li v-if="!this.inHand && this.tapped === false" @click.stop="tap">Tap</li>
          <li v-if="!this.inHand && this.tapped === true" @click.stop="untap">Untap</li>
          <li v-if="!this.inHand" @click.stop="moveToHand(this.userIndex)">Move to hand</li>
        </ul>
    </div>
  </div>
    
  </template>
  
  <script>
  import axios from 'axios';
  import * as Constants from '../constants'
  import {checkIfCardInPlayerDeck, checkIfCardInPlayerExile, checkIfCardInPlayerGraveyard, checkIfCardInPlayerHand} from '../utils/utils'
  import { eventBus } from '../eventBus';

  export default {
    emits: ['update-position', 'show-card', 'play-card', 'move-from-hand-to-hand', 'move-from-board-to-hand', 'open-move-to-deck-modal', 'move-to-exile', 'move-to-graveyard', 'copy-card'],
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
      flipImage: String,
      copy: Boolean

    },
    data() {
      return {
        position: this.initialPosition,
        correctedX: null,
        correctedY: null,
        hover: false,
        showMenu: false,
        menuPosition: { x: 0, y: 0 },
        clickTimeout: null,
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
      isDragging() {
        return this.$store.state.currentlyDraggingId === this.id;
      },
      startDragPosition() {
        return this.$store.state.startDragPosition;
      },
      cardOffset() {
        return this.$store.state.offset;
      },
      isSelected() {
        return this.$store.state.selectedCardIds.includes(this.id);
      },
      cardStyle() {
        let transformStyles = '';
        let zIndex = 2;
        let border = 'none'

        if(this.imageSrc === '') {
          border = "solid black 1px";
        }

        if(this.isSelected) {
          border = "solid red 6px";
        }

        if(this.zIndex) {
          zIndex = this.zIndex;
        }
        
        if(this.$store.state.currentlyDraggingId === this.id) {
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
        clearTimeout(this.clickTimeout);
        this.clickTimeout = null;
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
          id : this.id, 
          startClientX: event.clientX,
          startClientY: event.clientY,
          startDragPosition : { x: this.position.x, y: this.position.y }, 
          offset : {x: cardOffsetX, y : cardOffsetY}
        });
      },
      drag(event) {
        if (this.$store.state.currentlyDraggingId === this.id) { //if the card is supposed to be dragging
          clearTimeout(this.clickTimeout);
          this.clickTimeout = null;
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

          if(this.$store.state.selectedCardIds.length == 0) {
            this.$emit('update-position', { x: newPositionX, y: newPositionY });
          }
          
          let deltax = this.position.x - newPositionX;
          let deltay = this.position.y - newPositionY;

          if(this.$store.state.selectedCardIds.includes(this.id)) {
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
          return;
        }
      },
      endDrag(event) {
        clearTimeout(this.clickTimeout);
        this.clickTimeout = null;
        event.preventDefault();
        if(event.button === 2 ) { //right click
          return;
        }
        this.$store.commit('endDragging');
        let handPlayerIndex = checkIfCardInPlayerHand(this.position.x, this.position.y);
        let deckPlayerIndex = checkIfCardInPlayerDeck(this.position.x, this.position.y);
        let graveyardPlayerIndex = checkIfCardInPlayerGraveyard(this.position.x, this.position.y);
        let exilePlayerIndex = checkIfCardInPlayerExile(this.position.x, this.position.y);


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

        if(this.isMovingToExile(exilePlayerIndex)){
          this.moveToExile(exilePlayerIndex);
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
      onMoveCard(payload) {
        if (this.$store.state.selectedCardIds.includes(this.id)) {
          this.position.x -= payload.deltax;
          this.position.y -= payload.deltay;
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
      isMovingToExile(exilePlayerIndex) {
        return exilePlayerIndex !== null
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
      copyCard() {
        this.showMenu = !this.showMenu;
        this.$emit('copy-card', this.id);
      },
      moveToHand(handPlayerIndex) {
        this.$emit('move-from-board-to-hand', { cardId: this.id, targetPlayerIndex: handPlayerIndex });
      },
      moveToGraveyard(graveyardPlayerIndex) {
        this.$emit('move-to-graveyard', { cardId: this.id, targetPlayerIndex: graveyardPlayerIndex });
      },
      moveToExile(exilePlayerIndex) {
        this.$emit('move-to-exile', { cardId: this.id, targetPlayerIndex: exilePlayerIndex });
      },
      showCustomMenu(event) {
        if(this.pIndex === this.userIndex) {// only the card owner can use right click
          this.showMenu = !this.showMenu;
          const mouseX = (event.clientX - this.offsetX) / this.scale;
          const mouseY = (event.clientY - this.offsetY) / this.scale;
          if(this.inHand) {
            if(this.reverseMovement) {
              this.menuPosition = { 
                x: 0.4(-mouseX + window.innerWidth - this.handX - Constants.CARD_HALF_WIDTH), 
                y: 0.4(-mouseY - this.handY - Constants.CARD_HALF_HEIGHT)
              };
            } else {
              this.menuPosition = { 
                x: 0.4(mouseX-this.handX-Constants.CARD_HALF_WIDTH), 
                y: 0.4(mouseY-this.handY-Constants.CARD_HALF_HEIGHT)
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
        if(event.clientX !== this.$store.state.startClientX || event.clientY !== this.$store.state.startClientY) {
          return;
        }
        if(event.button === 2 ) { //right click
          return;
        }
        //if another click action has been triggered, return
        if (this.clickTimeout !== null) {
          clearTimeout(this.clickTimeout);
          this.clickTimeout = null;
          return;
        }
        //else we set a timeout, the action inside is executed within the delay if nothing else removes it
        this.clickTimeout = setTimeout(() => {
          this.showMenu = false;
          if (this.inHand) {
            this.showCardDetail();
          } else {
            this.toogleTap();
          }
          this.clickTimeout = null;
        }, 150); 
      },
      handleCardDoubleClick() {
        //remove the simple click timeout
        clearTimeout(this.clickTimeout);
        this.clickTimeout = null;
        this.showCardDetail();
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
        let cardIds = this.getSelectedCardIds();
        try{
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/tap', { cardIds: cardIds });
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async untap() {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        let cardIds = this.getSelectedCardIds();
        try{
          const response = await axios.patch(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.player + '/card/untap', { cardIds: cardIds });
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async flipCards() {
        this.showMenu = false;
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        let cardIds = this.getSelectedCardIds();
        try {
            const response = await axios.patch(
                `${backendUrl}room/${this.roomId}/player/${this.player}/card/flip`, 
                { cardIds: cardIds }
            );
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
      },
      getSelectedCardIds() {
        let cardIds = [this.id]
        if(this.$store.state.selectedCardIds && this.$store.state.selectedCardIds.includes(this.id)) {
          cardIds = this.$store.state.selectedCardIds
        }
        return cardIds;
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
  z-index: 100000; /* Ensure the menu appears above other content */
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

.text-overlay {
  position: absolute;
  top: 40%;  /* Centré verticalement */
  left: 50%; /* Centré horizontalement */
  transform: translate(-50%, -50%); /* Ajuste le centrage précis */
  color: rgb(190, 0, 0); /* Couleur du texte */
  font-size: 60px; /* Taille du texte */
  z-index: 10; /* S'assure que le texte est au-dessus de l'image */
}
</style>

  