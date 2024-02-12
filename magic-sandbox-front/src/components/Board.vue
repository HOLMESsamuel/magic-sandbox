<template>
    <div v-if="player && player.board && player.board.cards">
        <Card
        v-for="(card, cIndex) in player.board.cards"
        :key="`${card.id}-${card.position.x}-${card.position.y}`"
        :name="card.name"
        :imageSrc="card.image"
        :tapped="card.tapped"
        :roomId="roomId"
        :id="card.id"
        :initialPosition="card.position"
        :player="player.name"
        :userIndex="userIndex"
        :pIndex="pIndex"
        :scale="scale"
        :offsetX="offsetX"
        :offsetY="offsetY"
        :inHand="false"
        :zIndex="card.z_index"
        :maxZIndex="maxZIndex"
        :flippable="card.flip_image !== ''"
        :flipped="card.flipped"
        :flipImage="card.flip_image"
        :reverseMovement="userIndex === 1 || userIndex === 2"
        @open-move-to-deck-modal="openMoveToDeckModal($event)"
        @update-position="updateObjectPosition(player.name, cIndex, $event, 'card')"
        @show-card="showCard($event)"
        @move-from-hand-to-hand="moveFromHandToHand($event)"
        @move-from-board-to-hand="moveFromBoardToHand($event)"
        ></Card>
        <Token
        v-for="(token, tIndex) in player.board.tokens"
        :key="`${token.id}-${token.position.x}-${token.position.y}`"
        :tapped="token.tapped"
        :roomId="roomId"
        :id="token.id"
        :text="token.text"
        :type="token.type"
        :initialPosition="token.position"
        :player="player.name"
        :userIndex="userIndex"
        :pIndex="pIndex"
        :scale="scale"
        :offsetX="offsetX"
        :offsetY="offsetY"
        :zIndex="token.z_index"
        :maxZIndex="maxZIndex"
        :reverseMovement="userIndex === 1 || userIndex === 2"
        @update-token-position="updateObjectPosition(player.name, tIndex, $event, 'token')"
        @open-edit-token-modal="openEditTokenModal($event)"
        ></Token>
    </div>
</template>

<script>
  import Card from './Card.vue';
  import Token from './Token.vue';
  import axios from 'axios';

  export default {
    emits: ['update-position', 'show-card', 'play-card', 'move-from-hand-to-hand', 'move-from-board-to-hand', 'open-move-to-deck-modal'],
    components: {
        Card, Token
    },
    props: {
      scale: Number,
      offsetX: Number,
      offsetY: Number,
      pIndex: Number,
      userIndex: Number,
      roomId: String,
      reverseMovement: {
        type: Boolean,
        default: false
      },
      player: Object,
      maxZIndex: Number
    },
    data() {
      return {
        position: this.initialPosition,
        isDragging: false,
        cardOffsetX: 0,
        cardOffsetY: 0,
        correctedX: null,
        correctedY: null,
        startDragPosition: null,
        hover: false
      };
    },
    mounted() {
    },
    computed: {
    },
    methods: {
        openMoveToDeckModal(cardId) {
            this.$emit('open-move-to-deck-modal', cardId);
        },
        moveFromHandToHand(event) {
            this.$emit('move-from-hand-to-hand', event);
        },
        moveFromHandToBoard(event) {
          this.$emit('play-card', event);
        },
        updateObjectPosition(playerName, cIndex, position, type) {
          this.$emit('update-position', {playerName: playerName, index: cIndex, position: position, type: type});
        },
        showCard(event) {
          this.$emit('show-card', event);
        },
        moveFromBoardToHand(event) {
          this.$emit('move-from-board-to-hand', event);
        },
        async moveFromHandToHand(event) {
          const backendUrl = import.meta.env.VITE_BACKEND_URL;
          const targetPlayerName = this.state.players[event.targetPlayerIndex].name;
          try{
            const response = await axios.post(`${backendUrl}` + 'room/' + this.roomId +'/player/'+ this.userName + '/hand/card/' + event.cardId + '/hand/' + targetPlayerName, {});
            console.log(response.data);
          } catch (error) {
            console.log(error);
          }
        },
        openEditTokenModal(event) {
          this.$emit('open-edit-token-modal', event);
        }
    }
}
  </script>
  
<style>

</style>