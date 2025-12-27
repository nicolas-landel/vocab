
export default [
  {
    path: "",
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: 'session/:id',
    name: 'sessionActive',
    component: () => import('@/views/SessionView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/summary/:id',
    name: 'Summary',
    component: () => import('@/views/SummaryView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
];
