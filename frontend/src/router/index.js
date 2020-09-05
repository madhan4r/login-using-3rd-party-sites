import Vue from "vue";
import VueRouter from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import SignupPage from "../views/SignupPage.vue"
import HomePage from "../views/HomePage.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LoginPage",
    component: LoginPage
  },
  {
    path: "/signup",
    name: "SignupPage",
    component: SignupPage
  },
  {
    path: "/home",
    name: "HomePage",
    component: HomePage
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
