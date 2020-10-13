import Vue from "vue";
import Vuex from "vuex";
import * as parameters from "@/store/modules/parameters.js";
import * as simulation from "@/store/modules/simulation.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    parameters,
    simulation,
  },
  state: {
    snackbar_show: false,
    snackbar_timeout: 6000,
    snackbar_message: "",
    snackbar_color: "",
  },
  mutations: {
    DISPLAY_SNACKBAR(state, props) {
      state.snackbar_message = props.message;
      state.snackbar_color = props.color;
      state.snackbar_show = true;
    },
    CLOSE_SNACKBAR(state, show) {
      state.snackbar_show = show;
      state.snackbar_message = "";
      state.snackbar_color = "";
      state.snackbar_show = false;
    },
  },
  actions: {
    displaySnackbar({ commit }, snackbar_props) {
      commit("DISPLAY_SNACKBAR", snackbar_props);
    },
    closeSnackbar({ commit }) {
      commit("CLOSE_SNACKBAR");
    },
  },
});
