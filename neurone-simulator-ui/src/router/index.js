import Vue from "vue";
import VueRouter from "vue-router";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import Home from "../views/Home.vue";
import Simulate from "../views/Simulate.vue";
import ResultsHistory from "../views/ResultsHistory.vue";
import DisplayResults from "@/views/DisplayResults.vue";
//import ResultsHeatMaps from "@/views/ResultsHeatMaps";
import BaseHeatMap from "@/components/charts/BaseHeatMap.vue";

//loading stuff
import NProgress from "nprogress";
import "nprogress/nprogress.css";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "main",
    component: DefaultLayout,
    meta: { title: "Main", group: "apps", icon: "" },
    children: [
      {
        path: "/home",
        name: "home",
        meta: { title: "Home", group: "apps", icon: "" },
        component: Home,
      },
      {
        path: "/simulate",
        name: "simulate",
        meta: { title: "Start simulation", gruop: "apps", icon: "" },
        component: Simulate,
      },
      {
        path: "/results-history",
        name: "results-history",
        meta: { title: "Results history", group: "apps", icon: "" },
        component: ResultsHistory,
      },
      {
        path: "/show-results",
        name: "show-results",
        meta: { title: "Show results", group: "apps", icon: "" },
        component: DisplayResults,
      },
      {
        path: "/results-heatmap",
        name: "results-heatmap",
        meta: { title: "Results heatmap", group: "apps", icon: "" },
        component: BaseHeatMap,
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// router gards
router.beforeEach((to, from, next) => {
  NProgress.start();
  next();
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
