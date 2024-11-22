<template>
    <div :style="exileStyle" class="exile-container" @mouseover="hover = true" @mouseleave="hover = false">
        <div v-if="hover" class="hover-buttons">
            <button @click="openExileModal" class="button-center">👁️</button>
        </div>
        <div class="exile-image-container">
            <img v-if="cards && cards.length >0" :src="cards[cards.length-1].image" draggable="false" class="last-exile-card">
            <img src="../assets/ban.png" draggable="false" class="exile-image">
        </div>
    </div>
</template>
  
  <script>
  
    export default {
      props: {
        playerName: String,
        roomId: String,
        pIndex: Number, //index of the player
        userIndex: Number, //index of this frontend user
        cards: Array
      },
      emits: ["open-exile-modal"],
      data() {
        return {
            hover: false
        };
      },
      computed: {
        exileStyle() {
          switch (this.pIndex) {
            case 0:
              return {
                left: "2630px",
                top: "600px"
              };
            case 1:
              return {
                left: "280px",
                top: "-880px",
                transform: "rotate(180deg)"
              };
            case 2:
              return {
                left: "-2170px",
                top: "-880px",
                transform: "rotate(180deg)"
              };
            case 3:
              return {
                left: "-480px",
                top: "600px"
              };
          }  
        }
      },
      methods: {
        openExileModal() {
            this.$emit('open-exile-modal', this.pIndex);
        }
      },
    };
  </script>
  
  <style>
  .exile-container {
    position: fixed;
    height: 280px;
    width: 200px;
    margin: 0;
    padding: 6px;
    border-radius: 5px;
    border: solid gray 4px;
    box-sizing: border-box; 
  }

  .exile-image-container img {
    width: 100%; 
    height: 100%; 
    object-fit:scale-down; 
    object-position: center; 

  }

  .last-exile-card {
    position: relative; /* Allows the element to be positioned below the second image */
    z-index: 1;
  }

  .exile-image{
      position: absolute;
      top: 0;
      left: 0;
      z-index: 2;
      scale: 0.4;
  }

  .hover-buttons {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: start;
  z-index: 10; /* Ensure it's above the card image */
}

.button-center {
  background: #FFF;
  border: none;
  cursor: pointer;
  padding: 5px;
  height: 60px;
  width: 60px;
  font-size: 2em;
  border-radius: 50%;
}

.button-center:hover {
  background: #a99d9d;
}

.button-center {
  margin: 0 auto;
}
  
  </style>
  