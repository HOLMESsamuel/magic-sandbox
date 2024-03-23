<template>
    <div :style="graveyardStyle" class="graveyard-container" @mouseover="hover = true" @mouseleave="hover = false">
        <div v-if="hover" class="hover-buttons">
            <button @click="openGraveyardModal" class="button-center">👁️</button>
        </div>
        <div class="graveyard-image-container">
            <img v-if="cards && cards.length >0" :src="cards[cards.length-1].image" draggable="false">
        </div>
    </div>
</template>
  
  <script>
    import axios from 'axios';
  
    export default {
      props: {
        playerName: String,
        roomId: String,
        pIndex: Number, //index of the player
        userIndex: Number, //index of this frontend user
        cards: Array
      },
      emits: ["open-graveyard-modal"],
      data() {
        return {
            hover: false
        };
      },
      computed: {
        graveyardStyle() {
          switch (this.pIndex) {
            case 0:
              return {
                left: "2400px",
                top: "600px"
              };
            case 1:
              return {
                left: "50px",
                top: "-880px",
                transform: "rotate(180deg)"
              };
            case 2:
              return {
                left: "-2400px",
                top: "-880px",
                transform: "rotate(180deg)"
              };
            case 3:
              return {
                left: "-250px",
                top: "600px"
              };
          }  
        }
      },
      methods: {
        openGraveyardModal() {
            this.$emit('open-graveyard-modal', this.pIndex);
        }
      },
    };
  </script>
  
  <style>
  .graveyard-container {
    position: fixed;
    height: 280px;
    width: 200px;
    margin: 0;
    padding: 6px;
    border-radius: 5px;
    border: solid gray 4px;
    box-sizing: border-box; 
  }

  .graveyard-image-container img {
    width: 100%; 
    height: 100%; 
    object-fit: cover; 
    object-position: center; 

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
  