<template>
  <div v-if="isDeckModalVisible" class="modal" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="card-grid">
        <div v-for="(card, index) in sortedCards" :key="index" class="deck-view-card" @mouseover="hover = true" @mouseleave="hover = false">
          <img :src="card.image" alt="Card Image" draggable="false">
          <button v-if="hover" class="add-to-hand-button" @click.stop="addToHand(card.id)">Add to Hand</button>
        </div>
      </div>
      <button class="close-button" @click.stop="closeModal"></button>
    </div>
  </div>
</template>

<script>
export default {
  emits: ["close-deck-modal", "add-card-to-hand"],
  props: {
    isDeckModalVisible: Boolean,
    cards: Array
  },
  data() {
    return {
      hover: false
    };
  },
  computed: {
    sortedCards() {
      return [...this.cards].sort((a, b) => {
        const nameA = a.name.toLowerCase();
        const nameB = b.name.toLowerCase();
        if (nameA < nameB) return -1;
        if (nameA > nameB) return 1;
        return 0;
      });
    }
  },
  methods: {
    closeModal() {
      this.$emit('close-deck-modal');
    },
    addToHand(cardId) {
      this.$emit('add-card-to-hand', cardId);
    }
  }
};
</script>


<style>
.modal {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.5);
display: flex;
justify-content: center;
align-items: center;
}

.modal-content {
background-color: white;
padding: 30px;
border-radius: 10px;
position: relative; /* Needed for absolute positioning of the button */
overflow-y: auto; /* Enables vertical scrolling */
max-height: 90vh;
}

.card-grid {
display: grid;
grid-template-columns: repeat(4, 200px); /* 4 columns, each 200px wide */
gap: 10px; /* Spacing between cards */
}

.deck-view-card{
width: 200px;
height: 280px;
position: relative;
}

.deck-view-card img {
width: 100%;
height: 100%;
object-fit: cover;
}

.close-button {
position: absolute;
top: 10px;
right: 10px;
width: 30px;
height: 30px;
background: transparent;
border: none;
cursor: pointer;
}

.close-button::before, .close-button::after {
content: '';
position: absolute;
height: 100%;
width: 2px;
background-color: black;
top: 0;
left: 50%;
}

.close-button::before {
transform: rotate(45deg);
}

.close-button::after {
transform: rotate(-45deg);
}

.add-to-hand-button {
  position: absolute;
  bottom: 10px; 
  left: 50%;
  transform: translateX(-50%);
  padding: 5px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s;
}

.deck-view-card:hover .add-to-hand-button {
  opacity: 1;
}
</style>
