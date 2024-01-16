<template>
  <div class="zoom-pan-container" ref="zoomPanContainer" @wheel="handleZoom" @mousedown.stop="startPan" @mouseup="endPan" @mousemove="pan" @mouseleave="endPan">
    <div :style="zoomPanStyles">
      <div :style="containerStyle">
        <div class="axis-horizontal"></div>
        <div class="axis-vertical"></div>
        <div>
          <div v-for="(player, pIndex) in state.players">
            <div v-if="player && player.board">
              <Card
                v-for="(card, cIndex) in player.board"
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
                @update-position="updateCardPosition(player.name, cIndex, $event)"
                @show-card="showCard($event)"
                @move-from-hand-to-hand="moveFromHandToHand($event)"
                @move-from-board-to-hand="moveFromBoardToHand($event)"
              ></Card>
            </div>
            <deck 
              :playerName="player.name" 
              :roomId="roomId"
              :pIndex="pIndex"
              :userIndex="userIndex"
              :cards="player.deck.cards"
              @add-deck="handleAddDeck($event)">
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
              @open-token-modal="openTokenModal($event)">
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
    @close-token-modal="closeTokenModal"
  ></token-modal>
</template>
  
  <script>
  import Deck from './components/Deck.vue';
  import Card from './components/Card.vue';
  import Counter from './components/Counter.vue'
  import Hand from './components/Hand.vue'
  import CardModal from './components/CardModal.vue';
  import DeckModal from './components/DeckModal.vue';
  import MoveCardToDeckModal from './components/MoveCardToDeckModal.vue';
  import TokenModal from './components/TokenModal.vue';

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
        isTokenModalVisible: false
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
      Deck, Card, CardModal, Counter, Hand, DeckModal, MoveCardToDeckModal, TokenModal
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
          console.log(this.state);
        };
  
        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
        };
  
        this.ws.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      updateCardPosition(playerName, index, newPosition) {
        const player = this.state.players.find(p => p.name === playerName);
        this.state.max_z_index += 1;
        const maxZIndex = this.state.max_z_index
        player.board[index].position = newPosition;
        player.board[index].z_index = maxZIndex;
        this.sendPosition();
      },
      sendPosition() {
        if (this.ws) {
          this.ws.send(JSON.stringify(this.state));
        }
      },
      handleAddDeck(deck) {
        console.log(deck);
        const player = this.state.players.find(p => p.name === this.userName);
        if (player) {
          player.deck = deck;
        } else {
          console.error(`Player with name ${this.userName} not found.`);
        }
        this.sendPosition();
      },
      showCard(imageSrc) {
        this.modalImageSrc = imageSrc;
        this.isCardModalVisible = true;
      },
      showDeck() {
        this.isDeckModalVisible = true;
      },
      openTokenModal() {
        this.isTokenModalVisible = true;
      },
      closeTokenModal() {
        this.isTokenModalVisible = false;
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
  