<template>
    <div v-if="player">
      <div v-if="player.board && player.board.cards">
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
        :flipped="card.flipped"
        :flipImage="card.flip_image"
        :reverseMovement="reverseMovement"
        @open-move-to-deck-modal="openMoveToDeckModal($event)"
        @update-position="updateObjectPosition(player.name, cIndex, $event, 'card')"
        @show-card="showCard($event)"
        @move-from-board-to-hand="moveFromBoardToHand($event)"
        @move-to-graveyard="moveToGraveyard($event)"
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
        :reverseMovement="reverseMovement"
        @update-token-position="updateObjectPosition(player.name, tIndex, $event, 'token')"
        @open-edit-token-modal="openEditTokenModal($event)"
        ></Token>
      </div>
    </div>
    
</template>

<script>
  import Card from './Card.vue';
  import Token from './Token.vue';

  export default {
    emits: ['update-position', 'show-card', 'play-card', 'move-from-hand-to-hand', 'move-from-board-to-hand', 'open-move-to-deck-modal', 'move-to-graveyard'],
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
    methods: {
        openMoveToDeckModal(cardId) {
            this.$emit('open-move-to-deck-modal', cardId);
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
        moveToGraveyard(event) {
          this.$emit('move-to-graveyard', event);
        },
        openEditTokenModal(event) {
          this.$emit('open-edit-token-modal', event);
        }
    }
}
  </script>
  
<style>

</style>