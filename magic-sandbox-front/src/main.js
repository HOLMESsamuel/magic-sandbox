import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state () {
    return {
        currentlyDraggingCardId : null,
        startDragPosition : null,
        cardOffset : {x : 0, y : 0},
        soundOn : true
    }
  },
  mutations: {
    startDragging (state, {cardId, startDragPosition, cardOffset}) {
      state.currentlyDraggingCardId = cardId;
      state.startDragPosition = startDragPosition;
      state.cardOffset = cardOffset;
    },
    endDragging (state) {
        state.currentlyDraggingCardId = null;
        state.startDragPosition = null;
        state.cardOffset = {x : 0, y : 0};
    },
    toggleSound (state) {
      state.soundOn = !state.soundOn;
    }
  }
})

createApp(App).use(router).use(store).mount('#app');

