<template>
    <div :style="graveyardStyle" class="graveyard-container">
        <div class="graveyard-image-container">
            <img v-if="cards && cards.length >0" :src="cards[cards.length-1].image">
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
  
  </style>
  