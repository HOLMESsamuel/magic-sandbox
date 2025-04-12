<template>
    <div :style="nameStyle" class="name">
      <div class="player-name">{{ playerName }}</div>
    </div>
</template>
  
  <script>
  
    export default {
      props: {
        playerName: String,
        pIndex: Number,
        userIndex: Number
      },
      computed: {
        nameStyle() {
          let style = {};
          switch (this.pIndex) {
            case 0:
                style.left = "150px";
                style.top = "200px";
                break;
            case 1:
                style.left = "150px";
                style.top = "-250px";
                break;
            case 2:
                style.left = "-250px";
                style.top = "-250px";
                break;
            case 3:
                style.left = "-250px";
                style.top = "200px";
                break;
          } 

          if (this.userIndex === 1 || this.userIndex === 2) {
                style.transform = 'rotate(180deg)';
          }

          //invert everything if rotate is true
          if (this.$store.state.rotate) {
            if (style.transform) {
              style.transform = '';
            } else {
              style.transform = 'rotate(180deg)';
            }
          }

          return style;

        }
      },
    };
  </script>
  
  <style>
.name {
  position: fixed;
}

.player-name {
  font-weight: bold;
  font-size: 3em;
}
  </style>
  