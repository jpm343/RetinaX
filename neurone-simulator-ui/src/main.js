import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import heatmap from "vue-heatmapjs";

Vue.config.productionTip = false;

Vue.use(heatmap);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");

router.replace({
  name: "simulate"
});
