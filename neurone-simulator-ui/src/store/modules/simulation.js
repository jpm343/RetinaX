import SimulationService from "@/services/SimulationService.js";

export const namespaced = true;

export const state = {
  simulationResponse: {},
  resultsHistory: [],
  currentHeatMapData: {},
  comesFromHistory: true //in order to know if response to display comes from history or directly from new simulation
};

export const mutations = {
  SET_SIMULATION_RESPONSE(state, response) {
    state.simulationResponse = response;
  },
  SET_RESULTS_HISTORY(state, response) {
    state.resultsHistory = response;
  },
  DELETE_RESULT(state, result) {
    state.resultsHistory.splice(state.resultsHistory.indexOf(result), 1);
  },
  //decide if the results comes from history
  //origin -> bool
  SET_ORIGIN(state, origin) {
    state.comesFromHistory = origin;
  },
  SET_HEATMAP_DATA(state, heatmapData) {
    state.currentHeatMapData = heatmapData;
  },
  FLUSH_HEATMAP_DATA(state) {
    state.currentHeatMapData = {};
  }
};

export const actions = {
  startSimulation({ commit, dispatch }, params) {
    //params should be passed by POST
    //console.log(params);
    return SimulationService.startSimulation().then(response => {
      //(params, response);
      commit("SET_SIMULATION_RESPONSE");
      let snackbar = {
        message: "Simulation Succeded",
        color: "success"
      };
      dispatch("displaySnackbar", snackbar, { root: true });
    });
  },

  setParams({ dispatch, commit }, params) {
    //console.log(params);
    return SimulationService.setParams(params)
      .then(response => {
        commit("SET_ORIGIN", false); //doesn't come from history
        commit("SET_SIMULATION_RESPONSE", response.data);
        let snackbar = {
          message: "Simulation Succeded",
          color: "success"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
      })
      .catch(error => {
        let snackbar = {
          message: "Unexpected error.",
          color: "error"
        };
        if (error.response) {
          snackbar.message +=
            " message: " +
            error.response.data.message +
            " status code: " +
            error.response.status;
        }
        dispatch("displaySnackbar", snackbar, { root: true });
        throw error;
      });
  },

  fetchResults({ commit, dispatch }) {
    return SimulationService.fetchSimulations()
      .then(response => {
        commit("SET_RESULTS_HISTORY", response.data);
      })
      .catch(error => {
        let snackbar = {
          message: "There was an error fetching results",
          color: "error"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
        throw error;
      });
  },

  fetchHeatMapData({ commit, dispatch }, heatMapDatacommand) {
    //console.log("FROM STORE", heatMapDatacommand);
    return SimulationService.fetchHeatMapData(heatMapDatacommand)
      .then(response => {
        commit("SET_HEATMAP_DATA", response.data);
      })
      .catch(error => {
        let snackbar = {
          message: "There was an error fetching heatmap data",
          color: "error"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
        throw error;
      });
  },

  fetchSingleResultDetails({ commit, dispatch }, result) {
    return SimulationService.fetchSingleResultDetails(result)
      .then(response => {
        commit("SET_SIMULATION_RESPONSE", response.data);
        //console.log(response.data);
      })
      .catch(error => {
        let snackbar = {
          message: "There was an error fetching result details",
          color: "error"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
        throw error;
      });
  },

  deleteResult({ commit, dispatch }, result) {
    return SimulationService.deleteSimulationResult(result)
      .then(() => {
        commit("DELETE_RESULT", result);
        let snackbar = {
          message: "Simulation result deleted successfuly",
          color: "success"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
      })
      .catch(error => {
        let snackbar = {
          message: "There was an error deleting the simulation result",
          color: "error"
        };
        dispatch("displaySnackbar", snackbar, { root: true });
        throw error;
      });
  },
  loadResults({ commit }, results) {
    commit("SET_ORIGIN", true); //does come from history
    commit("SET_SIMULATION_RESPONSE", results);
  },
  flushHeatmapData({ commit }) {
    commit("FLUSH_HEATMAP_DATA");
  }

  //por mientras
  /*
  setParams({ dispatch }, params) {
    console.log(params);
    let snackbar = {
      message: "Check console",
      color: "warning",
    };
    dispatch("displaySnackbar", snackbar, { root: true });
  },
  */
};
