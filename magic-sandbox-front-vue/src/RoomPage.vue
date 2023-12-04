<template>
    <div>
      <p>Room ID: {{ roomId }}</p>
      <p>User Name: {{ userName }}</p>
      <div 
      id="disk" 
      class="disk" 
      :style="{ left: diskPosition.x + 'px', top: diskPosition.y + 'px' }"
      @mousedown="startDrag">
    </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      roomId: String
    },
    data() {
      return {
        ws: null,
        diskPosition: { x: 100, y: 100 },
        isDragging: false,
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
          this.diskPosition = { x: data.x, y: data.y };
        };
  
        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
        };
  
        this.ws.onclose = () => {
          console.log("WebSocket connection closed");
        };
      },
      startDrag(event) {
      this.isDragging = true;
    },
    drag(event) {
      if (this.isDragging) {
        this.diskPosition.x = event.clientX - 25; // 25 is half the disk's width
        this.diskPosition.y = event.clientY - 25; // 25 is half the disk's height
        this.sendPosition();
      }
    },
    endDrag() {
      this.isDragging = false;
    },
    sendPosition() {
      if (this.ws) {
        this.ws.send(JSON.stringify({ x: this.diskPosition.x, y: this.diskPosition.y }));
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
  .disk {
  width: 50px;
  height: 50px;
  background-color: blue;
  position: absolute;
  border-radius: 50%;
  cursor: pointer;
}
  </style>
  