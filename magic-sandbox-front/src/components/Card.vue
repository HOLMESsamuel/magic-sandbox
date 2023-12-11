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
      pIndex: Number,
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
        cardOffsetY: 0,
        correctedX: null,
        correctedY: null,
        startDragPosition: null
      };
    },
    mounted() {
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.endDrag);
    },
    computed: {
      cardStyle() {
        let style = {
          left: this.position.x + 'px',
          top: this.position.y + 'px',
          position: 'fixed',
          cursor: 'pointer'
        };

        switch (this.pIndex) {
          case 1:
          case 2:
            style.transform = 'rotate(180deg)';
        }

        return style;
      }
    },
    methods: {
      startDrag(event) {
        event.preventDefault();
        this.isDragging = true;
        this.startDragPosition = { x: this.position.x, y: this.position.y };
        console.log(this.startDragPosition);
        const correctedX = (event.clientX - this.offsetX) / this.scale;
        const correctedY = (event.clientY - this.offsetY) / this.scale;
        this.cardOffsetX = correctedX - this.position.x;
        this.cardOffsetY = correctedY - this.position.y;
      },
      /*drag: throttle(function(event) {
        if (!this.isDragging) return;
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        if (this.reverseMovement) {
          this.position.x = this.correctedX - (mouseX - this.cardOffsetX);
          this.position.y = this.correctedY - (mouseY - this.cardOffsetY);
        } else {
          this.position.x = mouseX - this.cardOffsetX;
          this.position.y = mouseY - this.cardOffsetY;
        }
      }, 10),*/
      drag(event) {
        if (!this.isDragging) return;
        const mouseX = (event.clientX - this.offsetX) / this.scale;
        const mouseY = (event.clientY - this.offsetY) / this.scale;

        // Calculate the new position
        let newPositionX = mouseX - this.cardOffsetX;
        let newPositionY = mouseY - this.cardOffsetY;

        if (this.reverseMovement) {
          // For reversed movement, invert the direction
          newPositionX = - newPositionX + 2 * this.startDragPosition.x;
          newPositionY = - newPositionY + 2 * this.startDragPosition.y;
        }

        // Update the card's position
        this.position.x = newPositionX;
        this.position.y = newPositionY;
      },
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
  