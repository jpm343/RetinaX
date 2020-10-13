import { pythonScriptClient } from "@/services/apiClient/pythonScriptClient.js";
import { simulationMiddlewareClient } from "@/services/apiClient/simulationMiddlewareClient.js";

export default {
  startSimulation() {
    return pythonScriptClient.get("/api/v1/runsimulation");
  },
  /*
  setParams(params) {
    return pythonScriptClient.post("/api/v1/resources/setparams", params);
  },
  */
  setParams(params) {
    return simulationMiddlewareClient.post(
      "/v1/simulations/runAndSave",
      params
    );
  },
  fetchSimulations() {
    return simulationMiddlewareClient.get("/v1/simulations");
  },
  deleteSimulationResult(simulationResult) {
    return simulationMiddlewareClient.delete(
      "/v1/simulations/" + simulationResult.id
    );
  },
  fetchSingleResultDetails(result) {
    return simulationMiddlewareClient.get("/v1/simulations/" + result.id);
  },
  fetchHeatMapData(heatMapDataCommand) {
    return simulationMiddlewareClient.post(
      "/v1/simulations/getHeatMapData",
      heatMapDataCommand
    );
  }
};
