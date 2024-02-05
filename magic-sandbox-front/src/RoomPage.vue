<template>
  <div class="zoom-pan-container" ref="zoomPanContainer" @wheel="handleZoom" @mousedown.stop="startPan" @mouseup="endPan" @mousemove="pan" @mouseleave="endPan">
    <div :style="zoomPanStyles">
      <div :style="containerStyle">
        <div class="axis-horizontal"></div>
        <div class="axis-vertical"></div>
        <div>
          <div v-for="(player, pIndex) in state.players">
            <div v-if="player && player.board && player.board.cards">
              <Card
                v-for="(card, cIndex) in player.board.cards"
                :key="`${card.id}-${card.position.x}-${card.position.y}`"
                :name="card.name"
                :imageSrc="card.image"
                :tapped="card.tapped"
                :roomId="roomId"
                :id="card.id"
                :initialPosition="card.position"
                :player="player.name"
                :userIndex="userIndex"
                :pIndex="pIndex"
                :scale="scale"
                :offsetX="offsetX"
                :offsetY="offsetY"
                :inHand="false"
                :zIndex="card.z_index"
                :maxZIndex="state.max_z_index"
                :reverseMovement="userIndex === 1 || userIndex === 2"
                @open-move-to-deck-modal="openMoveToDeckModal($event)"
                @update-position="updateObjectPosition(player.name, cIndex, $event, 'card')"
                @show-card="showCard($event)"
                @move-from-hand-to-hand="moveFromHandToHand($event)"
                @move-from-board-to-hand="moveFromBoardToHand($event)"
              ></Card>
              <Token
                v-for="(token, tIndex) in player.board.tokens"
                :key="`${token.id}-${token.position.x}-${token.position.y}`"
                :tapped="token.tapped"
                :roomId="roomId"
                :id="token.id"
                :text="token.text"
                :type="token.type"
                :initialPosition="token.position"
                :player="player.name"
                :userIndex="userIndex"
                :pIndex="pIndex"
                :scale="scale"
                :offsetX="offsetX"
                :offsetY="offsetY"
                :zIndex="token.z_index"
                :maxZIndex="state.max_z_index"
                :reverseMovement="userIndex === 1 || userIndex === 2"
                @update-token-position="updateObjectPosition(player.name, tIndex, $event, 'token')"
                @open-edit-token-modal="openEditTokenModal($event)"
              ></Token>
            </div>
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
              :cards="player.hand"
              :roomId="roomId"
              :userIndex="userIndex"
              :player="player.name"
              :scale="scale"
              :offsetX="offsetX"
              :offsetY="offsetY"
              :maxZIndex="state.max_z_index"
              :reverseMovement="userIndex === 1 || userIndex === 2"
              @open-move-to-deck-modal="openMoveToDeckModal($event)"
              @show-card="showCard($event)"
            ></hand>
          </div>
        </div>
      </div>
    </div>
  </div>
  <card-modal
    :modalImageSrc="modalImageSrc"
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
</template>
  
  <script>
  import Deck from './components/Deck.vue';
  import Card from './components/Card.vue';
  import Counter from './components/Counter.vue'
  import Hand from './components/Hand.vue'
  import Token from './components/Token.vue'
  import CardModal from './components/modals/CardModal.vue';
  import DeckModal from './components/modals/DeckModal.vue';
  import MoveCardToDeckModal from './components/modals/MoveCardToDeckModal.vue';
  import TokenModal from './components/modals/TokenModal.vue';
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
        isCardModalVisible: false,
        isDeckModalVisible: false,
        isMoveToDeckModalVisible: false,
        cardIdMovingToDeck: "",
        isTokenModalVisible: false,
        editTokenMode: false,
        currentToken: null,
        isDiceModalVisible: false,
        alertMessage: ""
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
      }
    },
    mounted() {
      this.connectWebSocket();
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.endDrag);
    },
    components: {
      Deck, Card, CardModal, Counter, Hand, DeckModal, MoveCardToDeckModal, TokenModal, Token, DiceModal
    },
    methods: {
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
          this.state = data;
          if(this.state.alertMessage && this.state.alertMessage !== this.alertMessage) {
            this.alertMessage = this.state.alertMessage;
            alert(this.alertMessage);
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
      updateObjectPosition(playerName, index, newPosition, object) {
        const player = this.state.players.find(p => p.name === playerName);
        this.state.max_z_index += 1;
        const maxZIndex = this.state.max_z_index
        if(object === "card") {
          player.board.cards[index].position = newPosition;
          player.board.cards[index].z_index = maxZIndex;
        } else if (object === "token") {
          player.board.tokens[index].position = newPosition;
          player.board.tokens[index].z_index = maxZIndex;
        }
        this.sendPosition();
      },
      sendPosition() {
        if (this.ws) {
          this.ws.send(JSON.stringify(this.state));
        }
      },
      showCard(imageSrc) {
        this.modalImageSrc = imageSrc;
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
      closeCardModal() {
        this.isCardModalVisible = false;
      },
      closeDeckModal() {
        this.isDeckModalVisible = false;
      },
      closeMoveToDeckModal() {
        this.isMoveToDeckModalVisible = false;
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
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/hand/card/' + event.cardId + '/deck/' + event.cardPosition, {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async addToHand(cardId) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/deck/card/' + cardId + '/hand', {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async moveFromBoardToHand(event) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/board/card/' + event.cardId + '/hand/' + targetPlayerName, {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      },
      async moveFromHandToHand(event) {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
        try{
          const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/hand/card/' + event.cardId + '/hand/' + targetPlayerName, {});
          console.log(response.data);
        } catch (error) {
          console.log(error);
        }
      }
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

.zoom-pan-container {
  overflow: hidden;
  position: relative;
  width: 100%;
  height: 100vh;
  cursor: grab;
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
  