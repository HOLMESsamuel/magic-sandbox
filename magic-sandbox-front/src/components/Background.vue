<template>
    <div class="container">
      <img v-if="player && player.background !== ''" :style="backgroundStyle" class="image">
    </div>
</template>
  
  <script>
  export default {
    props : {
        player: Object,
        pIndex: Number
    },
    computed: {
        backgroundStyle() {
        const background = this.player.background;
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const backgroundUrl = `url("${backendUrl}${background}")`;

        let position = {};
        let transformStyles = '';

        if (this.pIndex === 1 || this.pIndex === 2) {
          transformStyles += 'rotate(180deg) ';
        }

        if (this.pIndex === 3) {
            transformStyles += 'translate(' + -this.player.background_width + 'px) ';
        }

        if (this.pIndex === 2) {
            transformStyles += 'translate(' + this.player.background_width + 'px) ';
        }

        switch (this.pIndex) {
            case 0:
            position = { left: '0', top: '0' };
            break;
            case 1:
            position = { left: '0', bottom: '0' };
            break;
            case 2:
            position = { left: '0', bottom: '0' };
            break;
            case 3:
            position = { left: '0', top: '0' };
            break;
        }

        return {
            backgroundImage: backgroundUrl,
            backgroundSize: 'cover',
            width: this.player.background_width + 'px', 
            height: this.player.background_height + 'px',
            ...position,
            transform: transformStyles
        };
        },
    },
  };
  </script>
  
  <style scoped>
  .container {
    position: relative;
    width: 100%;
    height: 100%; 
  }
  
  .image {
    position: absolute;
  }
  </style>
  