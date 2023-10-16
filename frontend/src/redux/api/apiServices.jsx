import axios from "axios";

export const APIKit = axios.create({
  baseURL: import.meta.env.VITE_API_HOST,
  timeout: 1200000,
});

export const API_METHOD = {
  GET: "get",
  POST: "post",
  PUT: "put",
  PATCH: "patch",
  DELETE: "delete",
};
