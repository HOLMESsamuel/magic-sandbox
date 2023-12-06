<template>
  <div>
    <h1>Connection</h1>
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
/* Add styles for your connection page here */
</style>
