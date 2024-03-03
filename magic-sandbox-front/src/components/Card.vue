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
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import * as Constants from '../constants'

  export default {
    emits: ['update-position', 'show-card', 'play-card', 'move-from-hand-to-hand', 'move-from-board-to-hand', 'open-move-to-deck-modal'],
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
      userIndex: Number,
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
        isDragging: false,
        cardOffsetX: 0,
        cardOffsetY: 0,
        correctedX: null,
        correctedY: null,
        startDragPosition: null,
        hover: false,
        showMenu: false,
        menuPosition: { x: 0, y: 0 }
      };
    },
    mounted() {
      document.addEventListener('mousemove', this.drag);
    },
    computed: {
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
        if(event.button === 2 ) { //right click
          return;
        }
        event.preventDefault();
        this.isDragging = true;

        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        if (this.inHand) {
          this.cardOffsetX = Constants.CARD_HALF_WIDTH;
          this.cardOffsetY = Constants.CARD_HALF_HEIGHT;
          
          if(this.reverseMovement) {
            this.cardOffsetX = 2 * mouseX - window.innerWidth + Constants.CARD_HALF_WIDTH;
            this.cardOffsetY = 2 * mouseY + Constants.CARD_HALF_HEIGHT;
          }

          this.position.x = mouseX - this.cardOffsetX;
          this.position.y = mouseY - this.cardOffsetY;
          
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
      endDrag(event) {
        this.isDragging = false;
        let handPlayerIndex = this.checkIfCardInPlayerHand();
        let deckPlayerIndex = this.checkIfCardInPlayerDeck();
        const draggedDistance = Math.sqrt(Math.pow(this.position.x - this.startDragPosition.x, 2) + Math.pow(this.position.y - this.startDragPosition.y, 2));
        
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
          this.$emit('move-from-board-to-hand', { cardId: this.id, targetPlayerIndex: handPlayerIndex });
          return;
        }

        if(this.isMovingFromHandToDeck(deckPlayerIndex)) {
          this.$emit('open-move-to-deck-modal', this.id);
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
      isMovingFromHandToDeck(deckPlayerIndex) {
        return deckPlayerIndex !== null && deckPlayerIndex != this.userIndex && this.inHand;
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
      showCustomMenu(event) {
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
      },
      //returns the player index if the card was dropped on his hand
      checkIfCardInPlayerHand() {
        const playersHandAreas = this.getPlayersHandAreas();
        const cardCenter = {
          x: this.position.x,
          y: this.position.y
        };

        for (let i = 0; i < playersHandAreas.length; i++) {
          if (this.isPointInsideRect(cardCenter, playersHandAreas[i])) {
            return i;
          }
        }
        return null;
      },
      //returns the player index if the card was dropped on his deck
      checkIfCardInPlayerDeck() {
        const playersDeckAreas = this.getPlayersDeckAreas();
        const cardCenter = {
          x: this.position.x,
          y: this.position.y
        };

        for (let i = 0; i < playersDeckAreas.length; i++) {
          if (this.isPointInsideRect(cardCenter, playersDeckAreas[i])) {
            return i;
          }
        }
        return null;
      },

      getPlayersHandAreas() {
        // Returns an array of rectangular areas for each player's hand
        // Each area can be an object like { x1: left, y1: top, x2: right, y2: bottom }
        return [
          { x1: Constants.PLAYER_0_HAND_X1, y1: Constants.PLAYER_0_HAND_Y1, x2: Constants.PLAYER_0_HAND_X2, y2: Constants.PLAYER_0_HAND_Y2 },
          { x1: Constants.PLAYER_1_HAND_X1, y1: Constants.PLAYER_1_HAND_Y1, x2: Constants.PLAYER_1_HAND_X2, y2: Constants.PLAYER_1_HAND_Y2 },
          { x1: Constants.PLAYER_2_HAND_X1, y1: Constants.PLAYER_2_HAND_Y1, x2: Constants.PLAYER_2_HAND_X2, y2: Constants.PLAYER_2_HAND_Y2 },
          { x1: Constants.PLAYER_3_HAND_X1, y1: Constants.PLAYER_3_HAND_Y1, x2: Constants.PLAYER_3_HAND_X2, y2: Constants.PLAYER_3_HAND_Y2 }
        ];
      },

      getPlayersDeckAreas() {
        // Returns an array of rectangular areas for each player's deck
        // Each area can be an object like { x1: left, y1: top, x2: right, y2: bottom }
        return [
          { x1: 2300, y1: 775, x2: 2500, y2: 1020 }, //player 0
          { x1: -45, y1: -1325, x2: 150, y2: -1035 }, //player 1
          { x1: -2500, y1: -1300, x2: -2300, y2: -1000 }, //player 2
          { x1: -350, y1: 780, x2: -150, y2: 1080 }  //player 3
        ];
      },

      isPointInsideRect(point, rect) {
        return (
          point.x >= rect.x1 && point.x <= rect.x2 &&
          point.y >= rect.y1 && point.y <= rect.y2
        );
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

  