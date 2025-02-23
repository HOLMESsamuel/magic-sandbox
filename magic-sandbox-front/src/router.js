import { createRouter, createWebHistory } from 'vue-router';
import ConnectionPage from './ConnectionPage.vue';
import MTGRoomPage from './MTGRoomPage.vue';
import SRRoomPage from './SRRoomPage.vue';

const routes = [
  { path: '/', component: ConnectionPage, name: 'ConnectionPage' },
  { path: '/mtg-room/:roomId', component: MTGRoomPage, name: 'MTGRoom', props: true },
  { path: '/sr-room/:roomId', component: SRRoomPage, name: 'SRRoom', props: true }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
