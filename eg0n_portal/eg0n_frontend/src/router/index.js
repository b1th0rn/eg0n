import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/vulns",
      name: "vulns",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/VulnsView.vue"),
    },
    {
      path: "/hash",
      name: "hahs",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/HashView.vue"),
    },
    {
      path: "/ipadd",
      name: "ipadd",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/IpAddressView.vue"),
    },
    {
      path: "/scoreboard",
      name: "scoreboard",
      component: () => import("../views/ScoreboardView.vue"),
    }
  ],
});

export default router;
