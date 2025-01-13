<template>
  <div class="counter-circle">
    {{ count >= 0 ? ('+' + count) : ('-' + Math.abs(count)) }}/{{ count >= 0 ? ('+' + count) : ('-' + Math.abs(count)) }}
  </div>
</template>

<script>
export default {
  name: "CardCounter",
  props: {
    count: {
      type: Number,
      default: 0
    }
  }
};
</script>

<style scoped>
.counter-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  background-color: red;
  color: white;
  font-weight: bold;
  font-size: 16px;
}
</style>
