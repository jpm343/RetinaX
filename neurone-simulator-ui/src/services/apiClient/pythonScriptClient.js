import axios from "axios";
import Nprogress from "nprogress";
import store from "@/store/index";

export const pythonScriptClient = axios.create({
  baseURL: process.env.VUE_APP_PY_SCRIPT_URL,
  withCredentials: false,
});

pythonScriptClient.interceptors.request.use(
  (config) => {
    Nprogress.start();
    return config;
  },
  (error) => Promise.reject(error)
);

pythonScriptClient.interceptors.response.use((response) => {
  Nprogress.done();
  return response;
});

pythonScriptClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    Nprogress.done();
    if (error.response.status === 500) {
      let snackbar = {
        message: "There was an error processing your petition",
        color: "error",
      };
      store.dispatch("displaySnackbar", snackbar, { root: true });
    }
  }
);
