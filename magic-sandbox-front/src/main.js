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
        offset : {x : 0, y : 0},
        soundOn : true,
        luminosity : 50
    }
  },
  mutations: {
    startDragging (state, {id, startDragPosition, offset}) {
      state.currentlyDraggingId = id;
      state.startDragPosition = startDragPosition;
      state.offset = offset;
    },
    endDragging (state) {
        state.currentlyDraggingId = null;
        state.startDragPosition = null;
        state.offset = {x : 0, y : 0};
    },
    toggleSound (state) {
      state.soundOn = !state.soundOn;
    },
    updateLuminosity(state, luminosity) {
      state.luminosity = luminosity;
    }
  }
})

createApp(App).use(router).use(store).mount('#app');

