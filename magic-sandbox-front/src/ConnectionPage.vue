<template>
  <div class="connection-div">
    <h1>Magic sandbox</h1>
    <input v-model="name" placeholder="Enter your name" />
    <div class="button-grid">
      <div v-for="(room, index) in mtgRooms" :key="room" class="button-container">
        <button @click="joinRoom(room, 'MTGRoom')">
          <img src="./assets/magic/mtg-logo.png" alt="MTG Room" />
        </button>
        <span>{{ room }}</span>
      </div>
    </div>
    <div class="button-grid">
      <div v-for="(room, index) in starRealmsRooms" :key="room" class="button-container">
        <button @click="joinRoom(room, 'SRRoom')">
          <img src="./assets/sr/sr-logo.png" alt="Star Realms Room" />
        </button>
        <span>{{ room }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      mtgRooms: ['MTG-1', 'MTG-2', 'MTG-3', 'MTG-4'],
      starRealmsRooms: ['Star-Realms-1', 'Star-Realms-2', 'Star-Realms-3', 'Star-Realms-4']
    };
  },
  methods: {
    joinRoom(room, type) {
      if (!this.name.trim()) {
        alert('Please enter your name before selecting a room.');
        return;
      }
      sessionStorage.setItem('userName', this.name);
      this.$router.push({ name: type, params: { roomId: room, name: this.name }});
    }
  }
};
</script>

<style>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.connection-div {
  background-color: #48494b;
  font-family: 'Trebuchet MS', sans-serif;
  color: #f4f4f4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.connection-div input {
  background-color: #1c1e22;
  border: 2px solid #3a3b3e;
  border-radius: 4px;
  color: #fff;
  margin: 10px;
  padding: 12px 20px;
  width: 250px;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  margin-top: 40px;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-grid button {
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s, transform 0.3s;
  width: 140px;
  height: 140px;
  position: relative;
}

.button-grid button img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.button-grid button:hover img {
  filter: brightness(0.8);
}

.button-grid button:active {
  transform: scale(0.95);
}

.button-container span {
  margin-top: 10px;
  font-size: 16px;
  font-weight: bold;
}
</style>
