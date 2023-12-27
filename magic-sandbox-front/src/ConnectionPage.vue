<template>
  <div class="connection-div">
    <h1>Magic sandbox</h1>
    <input v-model="name" placeholder="Enter your name" />
    <input v-model="roomId" placeholder="Enter Room ID" />
    <button @click="joinRoom">Join</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      roomId: ''
    };
  },
  methods: {
    joinRoom() {
      sessionStorage.setItem('userName', this.name);
      this.$router.push({ name: 'Room', params: { roomId: this.roomId, name: this.name }});
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
  background-color: #48494b; /* Dark background */
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

.connection-div button {
  background-color: #4c5058;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  margin: 10px;
  padding: 12px 20px;
  transition: background-color 0.3s, transform 0.3s;
}

.connection-div button:hover {
  background-color: #62666d;
}

.connection-div button:active {
  transform: scale(0.98);
}

</style>
