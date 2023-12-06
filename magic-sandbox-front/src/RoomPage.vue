<template>
    <div>
      <p>Room ID: {{ roomId }}</p>
      <p>User Name: {{ userName }}</p>
      <img 
        id="card" 
        class="card" 
        src="./assets/card_back.webp" 
        :style="{ left: cardPosition.x + 'px', top: cardPosition.y + 'px' }"
        @mousedown="startDrag">
      />
      <deck @add-deck="handleAddDeck"></deck>
    </div>
  </template>
  
  <script>
  import Deck from './components/Deck.vue';

  export default {
    props: {
      roomId: String
    },
    data() {
      return {
        ws: null,
        cardPosition: { x: 100, y: 100 },
        isDragging: false
      };
    },
    computed: {
      userName() {
        return sessionStorage.getItem('userName');
      }
    },
    mounted() {
      this.connectWebSocket();
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.endDrag);
    },
    components: {
      Deck
    },
    methods: {
      connectWebSocket() {
        const wsBackendUrl = import.meta.env.VITE_WS_BACKEND_URL;
        this.ws = new WebSocket(`${wsBackendUrl}${this.roomId}`);
  
        this.ws.onopen = () => {
          console.log("WebSocket connected");
        };
  
        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          console.log("Received:", data);
          this.cardPosition = { x: data.x, y: data.y };
        };
  
        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
        };
  
        this.ws.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      startDrag(event) {
        event.preventDefault();
        this.isDragging = true;
    },
    drag(event) {
      if (this.isDragging) {
        this.cardPosition.x = event.clientX - 100;
        this.cardPosition.y = event.clientY - 140; 
        this.sendPosition();
      }
    },
    endDrag() {
      this.isDragging = false;
    },
    sendPosition() {
      if (this.ws) {
        this.ws.send(JSON.stringify({ x: this.cardPosition.x, y: this.cardPosition.y }));
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
  position: absolute;
  cursor: pointer;
}
  </style>
  