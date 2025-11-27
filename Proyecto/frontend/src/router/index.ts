
import { createRouter, createWebHistory } from "vue-router";

import LandingView from "../views/LandingView.vue";
import LoginView from "../views/LoginView.vue";

import CitizenDashboardView from "../views/CitizenDashboardView.vue";
import ResearcherDashboardView from "../views/ResearcherDashboardView.vue";
import AdminDashboardView from "../views/AdminDashboardView.vue";

const routes = [
  { path: "/", component: LandingView },
  { path: "/login", component: LoginView },

  { path: "/dashboard/citizen", component: CitizenDashboardView },
  { path: "/dashboard/researcher", component: ResearcherDashboardView },
  { path: "/dashboard/admin", component: AdminDashboardView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
