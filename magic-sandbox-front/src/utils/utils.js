import * as Constants from '../constants'

//returns the player index if the card was dropped on his hand
export const checkIfCardInPlayerHand = (x, y) => {
    const playersHandAreas = getPlayersHandAreas();
    const cardCenter = {
      x: x,
      y: y
    };

    for (let i = 0; i < playersHandAreas.length; i++) {
      if (isPointInsideRect(cardCenter, playersHandAreas[i])) {
        return i;
      }
    }
    return null;
  }

//returns the player index if the card was dropped on his deck
export const checkIfCardInPlayerDeck = (x, y) => {
    const playersDeckAreas = getPlayersDeckAreas();
    const cardCenter = {
      x: x,
      y: y
    };

    for (let i = 0; i < playersDeckAreas.length; i++) {
      if (isPointInsideRect(cardCenter, playersDeckAreas[i])) {
        return i;
      }
    }
    return null;
}

export const checkIfCardInPlayerGraveyard = (x, y) => {
  const playersGraveyardAreas = getPlayersGraveyardAreas();
  return checkIfCardInArea(x, y, playersGraveyardAreas);
}

export const checkIfCardInPlayerExile = (x, y) => {
  const playersExileAreas = getPlayersExileAreas();
  return checkIfCardInArea(x, y, playersExileAreas);
}

export const checkIfCardInArea = (x, y, areas) => {
  const cardCenter = {
    x: x,
    y: y
  };

  for (let i = 0; i < areas.length; i++) {
    if (isPointInsideRect(cardCenter, areas[i])) {
      return i;
    }
  }
  return null;
}

export const getPlayersGraveyardAreas = () => {
  return [
    { x1: Constants.PLAYER_0_GRAVEYARD_X1, y1: Constants.PLAYER_0_GRAVEYARD_Y1, x2: Constants.PLAYER_0_GRAVEYARD_X2, y2: Constants.PLAYER_0_GRAVEYARD_Y2 },
    { x1: Constants.PLAYER_1_GRAVEYARD_X1, y1: Constants.PLAYER_1_GRAVEYARD_Y1, x2: Constants.PLAYER_1_GRAVEYARD_X2, y2: Constants.PLAYER_1_GRAVEYARD_Y2 },
    { x1: Constants.PLAYER_2_GRAVEYARD_X1, y1: Constants.PLAYER_2_GRAVEYARD_Y1, x2: Constants.PLAYER_2_GRAVEYARD_X2, y2: Constants.PLAYER_2_GRAVEYARD_Y2 },
    { x1: Constants.PLAYER_3_GRAVEYARD_X1, y1: Constants.PLAYER_3_GRAVEYARD_Y1, x2: Constants.PLAYER_3_GRAVEYARD_X2, y2: Constants.PLAYER_3_GRAVEYARD_Y2 },
];
}

export const getPlayersExileAreas = () => {
  return [
    { x1: Constants.PLAYER_0_EXILE_X1, y1: Constants.PLAYER_0_EXILE_Y1, x2: Constants.PLAYER_0_EXILE_X2, y2: Constants.PLAYER_0_EXILE_Y2 },
    { x1: Constants.PLAYER_1_EXILE_X1, y1: Constants.PLAYER_1_EXILE_Y1, x2: Constants.PLAYER_1_EXILE_X2, y2: Constants.PLAYER_1_EXILE_Y2 },
    { x1: Constants.PLAYER_2_EXILE_X1, y1: Constants.PLAYER_2_EXILE_Y1, x2: Constants.PLAYER_2_EXILE_X2, y2: Constants.PLAYER_2_EXILE_Y2 },
    { x1: Constants.PLAYER_3_EXILE_X1, y1: Constants.PLAYER_3_EXILE_Y1, x2: Constants.PLAYER_3_EXILE_X2, y2: Constants.PLAYER_3_EXILE_Y2 },
];
}

export const getPlayersHandAreas = () => {
    // Returns an array of rectangular areas for each player's hand
    // Each area can be an object like { x1: left, y1: top, x2: right, y2: bottom }
    return [
      { x1: Constants.PLAYER_0_HAND_X1, y1: Constants.PLAYER_0_HAND_Y1, x2: Constants.PLAYER_0_HAND_X2, y2: Constants.PLAYER_0_HAND_Y2 },
      { x1: Constants.PLAYER_1_HAND_X1, y1: Constants.PLAYER_1_HAND_Y1, x2: Constants.PLAYER_1_HAND_X2, y2: Constants.PLAYER_1_HAND_Y2 },
      { x1: Constants.PLAYER_2_HAND_X1, y1: Constants.PLAYER_2_HAND_Y1, x2: Constants.PLAYER_2_HAND_X2, y2: Constants.PLAYER_2_HAND_Y2 },
      { x1: Constants.PLAYER_3_HAND_X1, y1: Constants.PLAYER_3_HAND_Y1, x2: Constants.PLAYER_3_HAND_X2, y2: Constants.PLAYER_3_HAND_Y2 }
    ];
}

export const getPlayersDeckAreas = () => {
    // Returns an array of rectangular areas for each player's deck
    // Each area can be an object like { x1: left, y1: top, x2: right, y2: bottom }
    return [
        { x1: Constants.PLAYER_0_DECK_X1, y1: Constants.PLAYER_0_DECK_Y1, x2: Constants.PLAYER_0_DECK_X2, y2: Constants.PLAYER_0_DECK_Y2 },
        { x1: Constants.PLAYER_1_DECK_X1, y1: Constants.PLAYER_1_DECK_Y1, x2: Constants.PLAYER_1_DECK_X2, y2: Constants.PLAYER_1_DECK_Y2 },
        { x1: Constants.PLAYER_2_DECK_X1, y1: Constants.PLAYER_2_DECK_Y1, x2: Constants.PLAYER_2_DECK_X2, y2: Constants.PLAYER_2_DECK_Y2 },
        { x1: Constants.PLAYER_3_DECK_X1, y1: Constants.PLAYER_3_DECK_Y1, x2: Constants.PLAYER_3_DECK_X2, y2: Constants.PLAYER_3_DECK_Y2 },
    ];
}

export const isPointInsideRect = (point, rect) => {
    return (
      point.x >= rect.x1 && point.x <= rect.x2 &&
      point.y >= rect.y1 && point.y <= rect.y2
    );
}