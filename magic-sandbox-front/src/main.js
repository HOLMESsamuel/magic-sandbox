import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state () {
    return {
        currentlyDraggingId : null,
        startDragPosition : null,
        startClientX: 0,
        startClientY: 0,
        offset : {x : 0, y : 0},
        soundOn : true,
        luminosity : 50,
        rotate : false
    }
  },
  mutations: {
    startDragging (state, {id, startClientX, startClientY, startDragPosition, offset}) {
      state.currentlyDraggingId = id;
      state.startClientX = startClientX;
      state.startClientY = startClientY;
      state.startDragPosition = startDragPosition;
      state.offset = offset;
    },
    endDragging (state) {
        state.currentlyDraggingId = null;
    },
    toggleSound (state) {
      state.soundOn = !state.soundOn;
    },
    updateLuminosity(state, luminosity) {
      state.luminosity = luminosity;
    },
    toggleRotate(state) {
      state.rotate = !state.rotate;
    }
  }
})

createApp(App).use(router).use(store).mount('#app');

