import axios from "axios";
import Nprogress from "nprogress";
import store from "@/store/index";

export const simulationMiddlewareClient = axios.create({
  baseURL: process.env.VUE_APP_SIM_MIDDLEWARE_URL,
  withCredentials: false
});

simulationMiddlewareClient.interceptors.request.use(
  config => {
    Nprogress.start();
    return config;
  },
  error => Promise.reject(error)
);

simulationMiddlewareClient.interceptors.response.use(response => {
  Nprogress.done();
  return response;
});

simulationMiddlewareClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    Nprogress.done();
    return Promise.reject(error);
  }
);
