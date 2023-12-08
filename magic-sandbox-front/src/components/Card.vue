<template>
    <div class="card" :style="cardStyle" @mousedown.stop="startDrag">
      <img :src="imageSrc" alt="Card Image">
    </div>
  </template>
  
  <script>
  export default {
    props: {
      imageSrc: String,
      initialPosition: {
        type: Object,
        default: () => ({ x: 0, y: 0 })
      },
      scale: Number,
      offsetX: Number,
      offsetY: Number
    },
    data() {
      return {
        position: this.initialPosition,
        isDragging: false,
        cardOffsetX: 0,
        cardOffsetY: 0
      };
    },
    mounted() {
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.endDrag);
    },
    computed: {
      cardStyle() {
        return {
          left: this.position.x + 'px',
          top: this.position.y + 'px',
          position: 'fixed',
          cursor: 'pointer'
        };
      }
    },
    methods: {
      startDrag(event) {
        event.preventDefault();
        this.isDragging = true;
        const correctedX = (event.clientX - this.offsetX) / this.scale;
        const correctedY = (event.clientY - this.offsetY) / this.scale;
        this.cardOffsetX = correctedX - this.position.x;
        this.cardOffsetY = correctedY - this.position.y;
      },
      drag(event) {
        if (!this.isDragging) return;
        this.position.x = (event.clientX - this.offsetX) / this.scale - this.cardOffsetY;
        this.position.y = (event.clientY - this.offsetY) / this.scale - this.cardOffsetX;
        this.$emit('update-position', { x: this.position.x, y: this.position.y });
      },
      endDrag() {
        this.isDragging = false;
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
  </style>
  