<template>
  <button @click="openSettingsModal" class="settings-button">
    <img src="./assets/gear.svg">
  </button>
  <div class="zoom-pan-container" :style="brightnessStyle" ref="zoomPanContainer" @keydown.esc="toggleSettingsModal" @wheel="handleZoom" @mousedown.stop="startPan" @mouseup="endPan" @mousemove="pan" @mouseleave="endPan" tabindex="0">
    <div :style="zoomPanStyles">
      <div :style="containerStyle">
        <div class="axis-horizontal"></div>
        <div class="axis-vertical"></div>
        <div>
          <div v-for="(player, pIndex) in state.players">
            <Board
              :roomId="roomId"
              :player="player"
              :userIndex="userIndex"
              :pIndex="pIndex"
              :scale="scale"
              :offsetX="offsetX"
              :offsetY="offsetY"
              :maxZIndex="state.max_z_index"
              :reverseMovement="userIndex === 1 || userIndex === 2"
              @open-move-to-deck-modal="openMoveToDeckModal($event)"
              @update-position="updateObjectPosition($event)"
              @show-card="showCard($event)"
              @move-from-board-to-hand="moveFromBoardToHand($event)"
              @open-edit-token-modal="openEditTokenModal($event)"
              @move-to-graveyard="moveToGraveyard($event)"
            ></Board>
            <deck 
              :playerName="player.name" 
              :roomId="roomId"
              :pIndex="pIndex"
              :userIndex="userIndex"
              :cards="player.deck.cards">
            </deck>
            <counter
              :key="`${player.name}-${player.score}`"
              :playerName="player.name"
              :isDeckLoaded="player.deck.cards && player.deck.cards.length > 0"
              :roomId="roomId"
              :pIndex="pIndex"
              :initialScore="player.score"
              :userIndex="userIndex"
              @show-deck="showDeck($event)"
              @open-token-modal="openTokenModal($event)"
              @open-dice-modal="openDiceModal">
            </counter>
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
              @open-graveyard-modal="openGraveyardModal()"
            ></graveyard>
          </div>
        </div>
      </div>
    </div>
  </div>
  <card-modal
    :modalImageSrc="modalImageSrc"
    :modalFlipImageSrc="modalFlipImageSrc"
    :isCardModalVisible="isCardModalVisible"
    @close-card-modal="closeCardModal"
  ></card-modal>
  <deck-modal
    :isDeckModalVisible="isDeckModalVisible"
    :cards="userCards"
    @close-deck-modal="closeDeckModal"
    @add-card-to-hand="addToHand($event)"
  ></deck-modal>
  <move-card-to-deck-modal
    :isMoveToDeckModalVisible="isMoveToDeckModalVisible"
    :deckLength="userCards.length"
    :cardId="cardIdMovingToDeck"
    @close-move-to-deck-modal="closeMoveToDeckModal"
    @confirm-move="moveCardToDeck($event)"
  ></move-card-to-deck-modal>
  <token-modal
    :key="isTokenModalVisible"
    :isTokenModalVisible="isTokenModalVisible"
    :currentToken="currentToken"
    :editTokenMode="editTokenMode"
    @close-token-modal="closeTokenModal"
    @create-token="createToken($event)"
    @modify-token="modifyToken($event)"
  ></token-modal>
  <dice-modal
    :isDiceModalVisible="isDiceModalVisible"
    @close-dice-modal="closeDiceModal"
    @throw-dice="throwDice($event)"
  ></dice-modal>
  <settings-modal
    :isSettingsModalVisible="isSettingsModalVisible"
    @close-settings-modal="closeSettingsModal"
    @disconnect="disconnect"
  ></settings-modal>
  <graveyard-modal
    :isGraveyardModalVisible="isGraveyardModalVisible"
    :cards="userGraveyard"
    @close-graveyard-modal="closeGraveyardModal()"
    @add-card-to-hand="moveFromGraveyardToHand($event)"
  ></graveyard-modal>
</template>
  
  <script>
  import Deck from './components/Deck.vue';
  import Card from './components/Card.vue';
  import Counter from './components/Counter.vue'
  import Board from './components/Board.vue';
  import Hand from './components/Hand.vue'
  import Token from './components/Token.vue'
  import Graveyard from './components/Graveyard.vue';
  import CardModal from './components/modals/CardModal.vue';
  import DeckModal from './components/modals/DeckModal.vue';
  import MoveCardToDeckModal from './components/modals/MoveCardToDeckModal.vue';
  import GraveyardModal from './components/modals/GraveyardModal.vue';
  import TokenModal from './components/modals/TokenModal.vue';
  import SettingsModal from './components/modals/SettingsModal.vue';
  import DiceModal from './components/modals/DiceModal.vue';
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
        isCardModalVisible: false,
        isDeckModalVisible: false,
        isMoveToDeckModalVisible: false,
        isSettingsModalVisible: false,
        cardIdMovingToDeck: "",
        isTokenModalVisible: false,
        editTokenMode: false,
        currentToken: null,
        isDiceModalVisible: false,
        alertMessage: "",
        firstMessageReceived: false,
        isGraveyardModalVisible: false
      };
    },
    computed: {
      userName() {
        return sessionStorage.getItem('userName');
      },
      zoomPanStyles() {
        return {
          transform: `translate(${this.offsetX}px, ${this.offsetY}px) scale(${this.scale})`,
          transformOrigin: '0 0'
        };
      },
      userIndex() {
        return this.state.players.findIndex(player => player.name === this.userName);
      },
      userCards() {
        if (this.state.players.length > this.userIndex && this.state.players[this.userIndex] && this.state.players[this.userIndex].deck.cards) {
          return this.state.players[this.userIndex].deck.cards;
        }
        return []; // Return an empty array if the user or cards are not available
      },
      userGraveyard() {
        if (this.state.players.length > this.userIndex && this.state.players[this.userIndex] && this.state.players[this.userIndex].graveyard.cards) {
          return this.state.players[this.userIndex].graveyard.cards;
        }
        return [];
      },
      containerStyle() {
        switch (this.userIndex) {
          case 0: // First player, normal view
            return {};
          case 1: // Second player, rotated 180 degrees
            return {
              transform: 'rotate(180deg)'
            };
          case 2: // Third player, rotated 180 degrees and translated
            return {
              transform: 'rotate(180deg)'
            };
          case 3: // Fourth player, normal view
            return {};
          default: // Default case if player index is not found
            return {};
        }
      },
      brightnessStyle() {
        const luminosity = this.$store.state.luminosity;
        const baseLuminosity = 50; // The luminosity value at which the brightness is "normal"
        // Convert the luminosity range from [0, 100] to a brightness percentage.
        // Assuming luminosity 50 does not change the brightness, adjust the scale accordingly.
        const brightness = (luminosity / baseLuminosity) * 100;
        return { filter: `brightness(${brightness}%)` };
      }
    },
    mounted() {
      this.connectWebSocket();
    },
    components: {
      Deck, Card, CardModal, Counter, Hand, DeckModal, MoveCardToDeckModal, TokenModal, Token, DiceModal, Board, SettingsModal, Graveyard, GraveyardModal
    },
    methods: {
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
      startPan(event) {
        this.panning = true;
        this.panStartX = event.clientX - this.offsetX;
        this.panStartY = event.clientY - this.offsetY;
      },
      endPan() {
        this.panning = false;
      },
      pan(event) {
        if (!this.panning) return;
        this.offsetX = event.clientX - this.panStartX;
        this.offsetY = event.clientY - this.panStartY;
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
        this.ws = new WebSocket(`${wsBackendUrl}${this.roomId}/${this.userName}`);
  
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
        const player = this.state.players.find(p => p.name === event.playerName);
        this.state.max_z_index += 1;
        const maxZIndex = this.state.max_z_index
        if(event.type === "card") {
          player.board.cards[event.index].position = event.position;
          player.board.cards[event.index].z_index = maxZIndex;
        } else if (event.type === "token") {
          player.board.tokens[event.index].position = event.position;
          player.board.tokens[event.index].z_index = maxZIndex;
        }
        this.sendPosition();
      },
      sendPosition() {
        if (this.ws) {
          this.ws.send(JSON.stringify(this.state));
        }
      },
      showCard(event) {
        this.modalImageSrc = event.image;
        this.modalFlipImageSrc = event.flipImage;
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
      openTokenModal() {
        this.editTokenMode = false;
        this.isTokenModalVisible = true;
      },
      closeTokenModal() {
        this.isTokenModalVisible = false;
      },
      openEditTokenModal(token) {
        this.isTokenModalVisible = true;
        this.editTokenMode = true;
        this.currentToken = token;
      },
      openMoveToDeckModal(cardId) {
        this.cardIdMovingToDeck = cardId;
        this.isMoveToDeckModalVisible = true;
      },
      openGraveyardModal() {
        this.isGraveyardModalVisible = true;
      },
      closeGraveyardModal() {
        this.isGraveyardModalVisible = false;
      },
      closeCardModal() {
        this.isCardModalVisible = false;
      },
      closeDeckModal() {
        this.isDeckModalVisible = false;
      },
      closeMoveToDeckModal() {
        this.isMoveToDeckModalVisible = false;
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
      async throwDice(diceValue) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.get(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/dice/' + diceValue);
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async createToken(token) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/token', token);
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async modifyToken(token) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/token/' + token.id, token);
          this.editTokenMode = false;
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async moveCardToDeck(event) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/card/' + event.cardId + '/deck/' + event.cardPosition, {});
          console.log(response.data);
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
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/graveyard/card/' + cardId + '/hand/' + this.userName, {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async moveFromBoardToHand(event) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/board/card/' + event.cardId + '/hand/' + targetPlayerName, {});
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
        try{
          const response = await axios.put(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/card/' + event.cardId + '/graveyard/' + targetPlayerName, {});
          console.log(response.data);
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
  width: 200px;
  height: 280px; 
  position: fixed;
  cursor: pointer;
}

.settings-button {
  position: fixed;
  bottom: 25px;
  right: 25px;
  z-index: 10000;
  background: none;
  border: none;
}

.settings-button :hover{
  cursor: pointer;
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

/* make everything not selectionable */
* {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

  </style>
  