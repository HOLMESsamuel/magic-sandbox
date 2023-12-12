<template>
  <div class="zoom-pan-container" @wheel="handleZoom" @mousedown="startPan" @mouseup="endPan" @mousemove="pan" @mouseleave="endPan">
    <div :style="zoomPanStyles">
      <div :style="containerStyle">
        <div class="axis-horizontal"></div>
        <div class="axis-vertical"></div>
        <div>
          <div v-for="(player, pIndex) in state.players">
            <div v-if="player && player.board">
              <Card
                v-for="(card, cIndex) in player.board"
                :key="`${card.position.x}-${card.position.y}`"
                :imageSrc="card.image"
                :initialPosition="card.position"
                :player="player.name"
                :pIndex="pIndex"
                :scale="scale"
                :offsetX="offsetX"
                :offsetY="offsetY"
                :reverseMovement="userIndex === 1 || userIndex === 2"
                @update-position="updateCardPosition(player.name, cIndex, $event)"
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import Deck from './components/Deck.vue';
  import Card from './components/Card.vue';
  

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
        scale: 1, // Initial zoom level
        panning: false,
        panStartX: 0,
        panStartY: 0,
        offsetX: 0,
        offsetY: 0
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
      Deck, Card
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
        const rect = this.$el.getBoundingClientRect();
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
        player.board[index].position = newPosition;
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


  </style>
  