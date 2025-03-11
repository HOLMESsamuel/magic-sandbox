<template>
    <button @click="openSettingsModal" class="settings-button setting-button">
      <img src="./assets/gear.svg">
    </button>
    <button @click="rotate" @keyup.{keyAlias}="" class="rotate-button setting-button">
      <img src="./assets/rotate.svg">
    </button>
    <button @click="moveMode" class="move-button setting-button" :class="{ bordered: isMoveMode }">
      <img src="./assets/move.svg">
    </button>
    <button @click="selectMode" class="select-button setting-button" :class="{ bordered: !isMoveMode }">
      <img src="./assets/select.svg">
    </button>
    <div class="zoom-pan-container" :style="brightnessStyle" ref="zoomPanContainer" @keydown.esc="toggleSettingsModal" @wheel="handleZoom" @mousedown.stop="handleMouseDown" @mouseup="handleMouseUp" @mousemove="handleMouseMove" @mouseleave="endPan" @keydown.alt="handleKeyPress" tabindex="0">
      <div :style="zoomPanStyles">
        <div :style="containerStyle">
          <div v-if="!isMoveMode && selecting" class="selection-box" :style="selectionBoxStyle"></div>
          <div class="axis-horizontal"></div>
          <div class="axis-vertical"></div>
          <river
            :scale="scale"
            :offsetX="offsetX"
            :offsetY="offsetY"
            :userIndex="userIndex"
            :maxZIndex="state.max_z_index"
            :cards="state.river_cards"
            @take-card="takeCardFromRiver($event)"
            @scrap-card="scrapCard($event)"
          ></river>
          <div>
            <div v-for="(player, pIndex) in state.players">
              <background
                :player="player"
                :pIndex="pIndex"
              ></background>
              <Board
              :roomId="roomId"
              :player="player"
              :userIndex="userIndex"
              :game="state.type"
              :pIndex="pIndex"
              :scale="scale"
              :offsetX="offsetX"
              :offsetY="offsetY"
              :maxZIndex="state.max_z_index"
              :reverseMovement="isReverseMovement"
              @open-move-to-deck-modal="openMoveToDeckModal($event)"
              @update-position="updateObjectPosition($event)"
              @show-card="showCard($event)"
              @move-from-board-to-hand="moveFromBoardToHand($event)"
              @move-to-graveyard="moveToGraveyard($event)"
            ></Board>
            <hand
              :pIndex="pIndex"
              :cards="player.hand.cards"
              :roomId="roomId"
              :userIndex="userIndex"
              :player="player.name"
              :scale="scale"
              :offsetX="offsetX"
              :offsetY="offsetY"
              :maxZIndex="state.max_z_index"
              :reverseMovement="userIndex === 1 || userIndex === 2"
              @open-move-to-deck-modal="openMoveToDeckModal($event)"
              @move-from-hand-to-hand="moveFromHandToHand($event)"
              @show-card="showCard($event)"
              @move-to-graveyard="moveToGraveyard($event)"
            ></hand>
            <graveyard
              :playerName="player.name" 
              :roomId="roomId"
              :pIndex="pIndex"
              :userIndex="userIndex"
              :cards="player.graveyard.cards"
              @open-graveyard-modal="openGraveyardModal($event)"
            ></graveyard>
            <deck 
              :playerName="player.name" 
              :roomId="roomId"
              :pIndex="pIndex"
              :userIndex="userIndex"
              :cards="player.deck ? player.deck.cards : []"
              :firstCardRevealed="player.deck.first_card_revealed === true"
              :scale="scale"
              :offsetX="offsetX"
              :offsetY="offsetY"
              :reverseMovement="isReverseMovement"
              :backgroundImage="'/sr/cardback.png'"
            ></deck>
            </div>
          </div>
        </div>
      </div>
    </div>
    <card-modal
      :modalImageSrc="modalImageSrc"
      :modalFlipImageSrc="modalFlipImageSrc"
      :modalImageName="modalImageName"
      :isCardModalVisible="isCardModalVisible"
      :isMoveToDeckModalVisible="isMoveToDeckModalVisible"
      @close-card-modal="closeCardModal"
    ></card-modal>
    <dice-modal
      :isDiceModalVisible="isDiceModalVisible"
      @close-dice-modal="closeDiceModal"
      @throw-dice="throwDice($event)"
    ></dice-modal>
    <settings-modal
      :roomId="roomId"
      :player="userPlayer"
      :isSettingsModalVisible="isSettingsModalVisible"
      @close-settings-modal="closeSettingsModal()"
      @disconnect="disconnect"
    ></settings-modal>
    <graveyard-modal
      :isGraveyardModalVisible="isGraveyardModalVisible"
      :cards="graveyardModalCards()"
      @close-graveyard-modal="closeGraveyardModal()"
      @add-card-to-hand="moveFromGraveyardToHand($event)"
    ></graveyard-modal>
    <SRControlPanel
      :roomId="roomId"
      :userIndex="userIndex"
      :playerName=this.userName
      @show-deck="showDeck($event)"
      @open-token-modal="openTokenModal($event)"
      @open-dice-modal="openDiceModal">
    </SRControlPanel>
  </template>
    
    <script>
    import Deck from './components/Deck.vue';
    import Card from './components/Card.vue';
    import Counter from './components/Counter.vue'
    import Board from './components/Board.vue';
    import Hand from './components/Hand.vue'
    import Graveyard from './components/Graveyard.vue';
    import Background from './components/Background.vue';
    import SRControlPanel from './components/sr/SRControlPanel.vue';
    import CardModal from './components/modals/CardModal.vue';
    import GraveyardModal from './components/modals/GraveyardModal.vue';
    import SettingsModal from './components/modals/SettingsModal.vue';
    import DiceModal from './components/modals/DiceModal.vue';
    import River from './components/sr/River.vue'
    import axios from 'axios';
  
    export default {
      props: {
        roomId: String
      },
      data() {
        return {
          state : {
            players: []
          },
          ws: null,
          scale: 0.25, // Initial zoom level
          panning: false,
          panStartX: 0,
          panStartY: 0,
          offsetX: 0,
          offsetY: 0,
          modalImageSrc: '',
          modalFlipImageSrc: '',
          modalImageName: '',
          isCardModalVisible: false,
          isDeckModalVisible: false,
          isMoveToDeckModalVisible: false,
          isSettingsModalVisible: false,
          cardIdMovingToDeck: "",
          isDiceModalVisible: false,
          alertMessage: "",
          firstMessageReceived: false,
          isGraveyardModalVisible: false,
          graveyardModalPlayerIndex: null,
          isMoveMode: true,
          selectCurrentX: 0,
          selectCurrentY: 0
        };
      },
      computed: {
        userName() {
          return sessionStorage.getItem('userName');
        },
        selecting() {
          return this.$store.state.selecting;
        },
        zoomPanStyles() {
          return {
            transform: `translate(${this.offsetX}px, ${this.offsetY}px) scale(${this.scale})`,
            transformOrigin: '0 0'
          };
        },
        userPlayer() {
          return this.state.players.find(player => player.name === this.userName);
        },
        userIndex() {
          return this.state.players.findIndex(player => player.name === this.userName);
        },
        isReverseMovement() {
          if(this.$store.state.rotate === false) {
            return this.userIndex === 1 || this.userIndex === 2;
          } else {
            return this.userIndex === 0 || this.userIndex === 3;
          }
        },
        userCards() {
          if (this.state.players.length > this.userIndex && this.state.players[this.userIndex] && this.state.players[this.userIndex].deck.cards) {
            return this.state.players[this.userIndex].deck.cards;
          }
          return []; // Return an empty array if the user or cards are not available
        },
        containerStyle() {
          let transformStyle = {};
          switch (this.userIndex) {
            case 0:
            case 3: // First player, normal view
              break;
            case 1:
            case 2: // Second player, rotated 180 degrees
              transformStyle = {
                transform: 'rotate(180deg)'
              };
              break;
            default: // Default case if player index is not found
              break;
          }
  
          //invert everything if rotate is true
          if (this.$store.state.rotate) {
            if (transformStyle.transform) {
              transformStyle.transform = '';
            } else {
              transformStyle = {
                transform: 'rotate(180deg)'
              };
            }
          }
  
          return transformStyle;
        },
        brightnessStyle() {
          const luminosity = this.$store.state.luminosity;
          const baseLuminosity = 50; // The luminosity value at which the brightness is "normal"
          // Convert the luminosity range from [0, 100] to a brightness percentage.
          // Assuming luminosity 50 does not change the brightness, adjust the scale accordingly.
          const brightness = (luminosity / baseLuminosity) * 100;
          return { filter: `brightness(${brightness}%)` };
        },
        selectionBoxStyle() {
          const left = Math.min(this.$store.state.selectStartX, this.selectCurrentX) + 'px';
          const right = left;
          const top = Math.min(this.$store.state.selectStartY, this.selectCurrentY) + 'px';
          const width = Math.abs(this.$store.state.selectStartX - this.selectCurrentX) + 'px';
          const height = Math.abs(this.$store.state.selectStartY - this.selectCurrentY) + 'px';
          if(this.isReverseMovement) {
            return {
              right,
              top,
              width,
              height,
            };
          }
          return {
            left,
            top,
            width,
            height,
          };
        },
      },
      mounted() {
        this.connectWebSocket();
      },
      components: {
        Deck, Card, CardModal, Counter, Hand, DiceModal, Board, SettingsModal, Graveyard, GraveyardModal, Background, SRControlPanel, River
      },
      methods: {
        handleKeyPress(event) {
          if (event.key === 'r') {
            this.rotate();
          } else if (event.key === 'm') {
            this.moveMode();
          } else if (event.key === 's') {
            this.selectMode();
          }
        },
        moveMode() {
          this.isMoveMode = true;
        },
        selectMode() {
          this.isMoveMode = false;
        },
        computeBoardInitialPosition() { //set the initial offset to place the player's board roughly at the center of the screen
          switch (this.userIndex) {
            case 0:
              this.offsetX = window.innerWidth/4;
              this.offsetY = window.innerHeight/4;
              return ;
            case 1: 
              this.offsetX = window.innerWidth/3;
              this.offsetY = window.innerHeight/3;
              return;
            case 2:
              this.offsetX = window.innerWidth/8;
              this.offsetY = window.innerHeight/4;
              return;
            case 3:
              this.offsetX = window.innerWidth/1.5;
              this.offsetY = window.innerHeight/4;
              return;
            default:
              this.offsetX = 0;
              this.offsetY = 0;
              return;
          }
        },
        handleMouseDown(event) {
          if(this.isMoveMode) {
            if(event.button === 2) {
              return;
            }
            this.panning = true;
            this.panStartX = event.clientX - this.offsetX;
            this.panStartY = event.clientY - this.offsetY;
          } else {
            if(event.button === 2) {
              return;
            }
            if(this.isReverseMovement) {
              this.$store.commit('startSelecting', {
                selecting : true, 
                selectStartX: (event.clientX - this.offsetX) / this.scale,
                selectStartY: -(event.clientY - this.offsetY) / this.scale
              });
            } else {
              this.$store.commit('startSelecting', {
                selecting : true, 
                selectStartX: (event.clientX - this.offsetX) / this.scale,
                selectStartY: (event.clientY - this.offsetY) / this.scale
              });
            }
          }
        },
        handleMouseUp(event) {
          if(event.button === 2) {
            return;
          }
          if(this.isMoveMode) {
            this.panning = false;
          } else {
            if(Math.abs(this.selectCurrentX - this.$store.state.selectStartX) > 0 && Math.abs(this.selectCurrentY - this.$store.state.selectStartY) > 0 ) {
              const playerCards = this.userPlayer.board.cards;
              let selectedCardIds = [];
              let selectedTokenIds = [];
              let top = Math.max(this.selectCurrentY, this.$store.state.selectStartY);
              let bottom = Math.min(this.selectCurrentY, this.$store.state.selectStartY);
              let right = Math.max(this.selectCurrentX, this.$store.state.selectStartX);
              let left = Math.min(this.selectCurrentX, this.$store.state.selectStartX);
              if(this.isReverseMovement) {
                top = Math.max(this.selectCurrentY, this.$store.state.selectStartY);
                bottom = Math.min(this.selectCurrentY, this.$store.state.selectStartY);
                right = -(Math.min(this.selectCurrentX, this.$store.state.selectStartX) - window.innerWidth);
                left = -(Math.max(this.selectCurrentX, this.$store.state.selectStartX) - window.innerWidth);
                console.log(top, right, bottom, left, window.innerWidth);
              }
              
              for(let i=0; i<playerCards.length; i++) {
                let card = playerCards[i];
                if(card.position.x > left && card.position.x < right && card.position.y > bottom && card.position.y < top) {
                  selectedCardIds.push(card.id);
                }
              }
              this.$store.commit('stopSelecting', {
                  selectedCardIds: selectedCardIds,
                  selectedTokenIds: selectedTokenIds
              });
            } else {
              this.$store.commit('stopSelecting', {
                  selectedCardIds: this.$store.state.selectedCardIds,
                  selectedTokenIds: this.$store.state.selectedTokenIds
              });
            }
          }
        },
        handleMouseMove(event) {
          if(this.isMoveMode) {
            if (!this.panning) return;
            this.offsetX = event.clientX - this.panStartX;
            this.offsetY = event.clientY - this.panStartY;
          } else {
            if(this.isReverseMovement === true) {
              this.selectCurrentX =  (event.clientX - this.offsetX) / this.scale;
              this.selectCurrentY =  -(event.clientY - this.offsetY) / this.scale;
            } else {
              this.selectCurrentX = (event.clientX - this.offsetX) / this.scale;
              this.selectCurrentY = (event.clientY - this.offsetY) / this.scale;
            }
          }
        },
        handleZoom(event) {
          const rect = this.$refs.zoomPanContainer.getBoundingClientRect();
          const x = event.clientX - rect.left; // Mouse x coordinate relative to the container
          const y = event.clientY - rect.top; // Mouse y coordinate relative to the container
  
          // Calculate the position before zoom
          const beforeZoomX = (x - this.offsetX) / this.scale;
          const beforeZoomY = (y - this.offsetY) / this.scale;
  
          // Update the scale
          if (event.deltaY > 0) {
            this.scale *= 0.9; // Zoom out
          } else {
            this.scale *= 1.1; // Zoom in
          }
  
          // Calculate the position after zoom and adjust the offsets
          const afterZoomX = (x - this.offsetX) / this.scale;
          const afterZoomY = (y - this.offsetY) / this.scale;
          this.offsetX += (afterZoomX - beforeZoomX) * this.scale;
          this.offsetY += (afterZoomY - beforeZoomY) * this.scale;
        },
        connectWebSocket() {
          const wsBackendUrl = import.meta.env.VITE_WS_BACKEND_URL;
          this.ws = new WebSocket(`${wsBackendUrl}sr/${this.roomId}/${this.userName}`);
    
          this.ws.onopen = () => {
            console.log("WebSocket connected");
          };
    
          this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.state = JSON.parse(data);
            if(this.state.alert_message && this.state.alert_message !== this.alertMessage) {
              this.alertMessage = this.state.alert_message;
              alert(this.alertMessage);
            }
            if(this.firstMessageReceived === false) { //this part will trigger only when the first message is received it allows to call compute position method only after the players list is received
              this.computeBoardInitialPosition();
              this.firstMessageReceived = true;
            }
            console.log(this.state);
          };
  
          this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
          };
    
          this.ws.onclose = () => {
            console.log("WebSocket connection closed");
          };
        },
        async disconnect() {
          this.ws.close();
  
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.delete(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName);
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
  
          this.$router.push({ name: 'ConnectionPage'});
  
        },
        updateObjectPosition(event) {
          //recuperer les cartes et token selectionnés et update toutes les positions avec la différence entre position de départ et d'arrivée
          const player = this.state.players.find(p => p.name === event.playerName);
          this.state.max_z_index += 1;
          const maxZIndex = this.state.max_z_index
          let deltax = 0;
          let deltay = 0;
          if(event.type === "card") {
            const card = player.board.cards.find(c => c.id === event.id);
            deltax = card.position.x - event.position.x;
            deltay = card.position.y - event.position.y;
            console.log(deltax);
            card.position = event.position;
            card.z_index = maxZIndex;
          } else if (event.type === "token") {
            const token = player.board.tokens.find(t => t.id === event.id);
            deltax = token.position.x - event.position.x;
            deltay = token.position.y - event.position.y;
            token.position = event.position;
            token.z_index = maxZIndex;
          }
          for(let i=0; i<this.$store.state.selectedCardIds.length; i++) {
            let card = player.board.cards.find(c => c.id === this.$store.state.selectedCardIds[i] && c.id !== event.id);
            if(card) {
              card.position.x -= deltax;
              card.position.y -= deltay;
              card.z_index = maxZIndex;
            }
          }
          for(let i=0; i<this.$store.state.selectedTokenIds.length; i++) {
            let token = player.board.tokens.find(t => t.id === this.$store.state.selectedTokenIds[i] && t.id !== event.id);
            if(token) {
              token.position.x -= deltax;
              token.position.y -= deltay;
              token.z_index = maxZIndex;
            }
          }
          this.sendPosition();
        },
        sendPosition() {
          if (this.ws) {
            this.ws.send(JSON.stringify(this.state));
          }
        },
        graveyardModalCards() {
          if (this.graveyardModalPlayerIndex !== null) {
            return this.state.players[this.graveyardModalPlayerIndex].graveyard.cards;
          }
          return [];
        },
        showCard(event) {
          this.modalImageSrc = event.image;
          this.modalFlipImageSrc = event.flipImage;
          this.modalImageName = event.name;
          this.isCardModalVisible = true;
        },
        showDeck() {
          this.isDeckModalVisible = true;
        },
        openDiceModal() {
          this.isDiceModalVisible = true;
        },
        closeDiceModal() {
          this.isDiceModalVisible = false;
        },
        openMoveToDeckModal(cardId) {
          this.cardIdMovingToDeck = cardId;
          this.isMoveToDeckModalVisible = true;
        },
        openGraveyardModal(pIndex) {
          this.isGraveyardModalVisible= true;
          this.graveyardModalPlayerIndex = pIndex;
        },
        closeGraveyardModal() {
          this.isGraveyardModalVisible = false;
          this.graveyardModalPlayerIndex = null;
        },
        closeCardModal() {
          this.isCardModalVisible = false;
        },
        closeDeckModal() {
          this.isDeckModalVisible = false;
        },
        closeMoveToDeckModal() {
          this.isMoveToDeckModalVisible = false;
          this.isCardModalVisible = false;
        },
        openSettingsModal() {
          this.isSettingsModalVisible = true;
        },
        closeSettingsModal() {
          this.isSettingsModalVisible = false;
        },
        toggleSettingsModal() {
          this.isSettingsModalVisible = !this.isSettingsModalVisible;
        },
        rotate() {
          this.$store.commit('toggleRotate');
        },
        async throwDice(diceValue) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.get(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/dice/' + diceValue);
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async moveCardToDeck(event) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          let cardIds = [event.cardId]
          if(this.$store.state.selectedCardIds && this.$store.state.selectedCardIds.includes(event.cardId)) {
            cardIds = this.$store.state.selectedCardIds
          }
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/deck/' + event.cardPosition, { cardIds : cardIds });
            console.log(response.data);
            this.$store.state.selectedCardIds = [];
          } catch (error) {
            console.log(error);
          }
        },
        async addToHand(cardId) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/deck/card/' + cardId + '/hand', {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async moveFromGraveyardToHand(cardId) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          const targetPlayerName = this.state.players[this.graveyardModalPlayerIndex].name;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ targetPlayerName + '/graveyard/card/' + cardId + '/hand/' + this.userName, {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async moveFromBoardToHand(event) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
          let cardIds = [event.cardId]
          if(this.$store.state.selectedCardIds && this.$store.state.selectedCardIds.includes(event.cardId)) {
            cardIds = this.$store.state.selectedCardIds
          }
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/board/card/hand/' + targetPlayerName, {cardIds : cardIds});
            console.log(response.data);
            this.$store.commit('resetSelectedCards', {});
          } catch (error) {
            console.log(error);
          }
        },
        async takeCardFromRiver(cardId) {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            try{
                const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/river/card/'+  cardId + '/player/' + this.userName, {});
                console.log(response.data);
            } catch (error) {
                console.log(error);
            }
        },
        async scrapCard(cardId) {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            try{
                const response = await axios.delete(`${backendUrl}` + 'room/' + this.roomId +'/river/card/'+  cardId, {});
                console.log(response.data);
            } catch (error) {
                console.log(error);
            }
        },
        async moveFromHandToHand(event) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/hand/card/' + event.cardId + '/hand/' + targetPlayerName, {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        async moveToGraveyard(event) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
          let cardIds = [event.cardId]
          if(this.$store.state.selectedCardIds && this.$store.state.selectedCardIds.includes(event.cardId)) {
            cardIds = this.$store.state.selectedCardIds
          }
  
          let tokenIds = []
          if(this.$store.state.selectedCardIds && this.$store.state.selectedTokenIds && this.$store.state.selectedCardIds.length > 0) {
            tokenIds = this.$store.state.selectedTokenIds;
          }
          
          try{
            const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/graveyard/' + targetPlayerName, {cardIds : cardIds, tokenIds : tokenIds});
            console.log(response.data);
            this.$store.state.selectedCardIds = [];
          } catch (error) {
            console.log(error);
          }
        },
        },
        beforeDestroy() {
          if (this.ws) {
            this.ws.close();
          }
       }
    };
  </script>
    
  <style>
  .card {
    position: fixed;
    cursor: pointer;
  }
  
  .settings-button {
    bottom: 25px;
    right: 25px;
  }
  
  .rotate-button {
    bottom: 25px;
    right: 60px;
  }
  
  .move-button {
    bottom: 25px;
    right: 95px;
  }
  
  .select-button {
    bottom: 25px;
    right: 130px;
  }
  
  .setting-button :hover {
    cursor: pointer;
  }
  
  .setting-button {
    position: fixed;
    background: none;
    border: none;
    z-index: 10000;
  }
  
  .bordered {
    border: solid black 1px;
    border-radius: 3px;
  }
  
  .zoom-pan-container {
    overflow: hidden;
    position: relative;
    width: 100%;
    height: 100vh;
    cursor: grab;
    background-color: #b7aeaf;
  }
  
  .zoom-pan-container:active {
    cursor: grabbing;
  }
  
  .axis-horizontal {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 20000px; /* 20000px long */
    height: 1px;
    background-color: black;
    top: 50%; /* Centered vertically */
  }
  
  .axis-vertical {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    height: 20000px; /* 20000px long */
    width: 1px;
    background-color: black;
    left: 0px; /* Centered horizontally */
  }
  
  .selection-box {
    position: absolute;
    border: 2px dashed #007bff;
    background-color: rgba(0, 123, 255, 0.2);
    pointer-events: none;
    z-index: 9999999999;
  }
  
  /* make everything not selectionable */
  * {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
  
    </style>
    