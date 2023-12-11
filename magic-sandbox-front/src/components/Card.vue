<template>
    <div class="card" :style="cardStyle" @mousedown.stop="startDrag">
      <img :src="imageSrc" alt="Card Image">
    </div>
  </template>
  
  <script>
 import throttle from 'lodash/throttle';

  export default {
    props: {
      imageSrc: String,
      initialPosition: {
        type: Object,
        default: () => ({ x: 100, y: 100 })
      },
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      reverseMovement: {
      type: Boolean,
      default: false
    }
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
        console.log("correctedX");
        console.log(correctedX);
        console.log("cardOffset");
        console.log(this.cardOffsetX);
      },
      drag: throttle(function(event) {
        if (!this.isDragging) return;
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;
        console.log("mouse");
        console.log(mouseX);

        if (this.reverseMovement) {
          this.position.x = this.initialPosition.x - (mouseX - this.cardOffsetX);
          this.position.y = this.initialPosition.y - (mouseY - this.cardOffsetY);
        } else {
          this.position.x = mouseX - this.cardOffsetX;
          this.position.y = mouseY - this.cardOffsetY;
        }
        console.log("position");
        console.log(this.position.x);
      }, 10),
      endDrag() {
        this.isDragging = false;
        this.$emit('update-position', { x: this.position.x, y: this.position.y });
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
  