<template>
  <div class="zoom-pan-container" @wheel="handleZoom" @mousedown="startPan" @mouseup="endPan" @mousemove="pan" @mouseleave="endPan">
    <div :style="zoomPanStyles">
      <div>
        <p>User Name: {{ userName }}</p>
        <Card
          v-for="(card, index) in cards"
          :key="index"
          :imageSrc="card.image"
          :initialPosition="card.position"
          :scale="scale"
          :offsetX="offsetX"
          :offsetY="offsetY"
          @update-position="updateCardPosition(index, $event)"
        ></Card>
        <deck @add-deck="handleAddDeck"></deck>
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
        ws: null,
        isDragging: false,
        scale: 1, // Initial zoom level
        panning: false,
        panStartX: 0,
        panStartY: 0,
        offsetX: 0,
        offsetY: 0,
        cards: [
        { image: 'https://cards.scryfall.io/normal/front/d/f/dfaaa58d-89bb-4cb3-96a6-b480e6f6954e.jpg?1608911671', position: { x: 100, y: 100 } }
      ]
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
      handleAddDeck() {
        
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
        this.ws = new WebSocket(`${wsBackendUrl}${this.roomId}`);
  
        this.ws.onopen = () => {
          console.log("WebSocket connected");
        };
  
        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.cards[0].position.x = data.x;
          this.cards[0].position.y = data.y;
        };
  
        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
        };
  
        this.ws.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      
      updateCardPosition(index, newPosition) {
        this.cards[index].position = newPosition;
        this.sendPosition(index);
      },
      sendPosition(index) {
        if (this.ws) {
          this.ws.send(JSON.stringify({ x: this.cards[index].position.x, y: this.cards[index].position.y }));
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
  </style>
  