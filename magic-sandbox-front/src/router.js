import { createRouter, createWebHistory } from 'vue-router';
import ConnectionPage from './ConnectionPage.vue';
import RoomPage from './RoomPage.vue';

const routes = [
  { path: '/', component: ConnectionPage },
  { path: '/room/:roomId', component: RoomPage, name: 'Room', props: true }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
