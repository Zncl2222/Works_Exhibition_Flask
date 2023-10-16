import { all, put } from "redux-saga/effects";
import { API_METHOD, APIKit } from "../api/apiServices";
import _ from "lodash";
import Swal from "sweetalert2";
import Cookies from "js-cookie";
import FileDownload from "js-file-download";

export function* setLoading(loading, path, method) {
  yield put({ type: "SET_LOADING", data: { loading, path, method } });
}

export function* fetchApi({
  method,
  path,
  reducer = null,
  data = null,
  successMessage = null,
  successAction,
  errorAction,
  failValue = null,
  params = {},
  json = false,
  isDownload = false,
}) {
  yield setLoading(true, path, method);
  let result = failValue;
  let success = false;

  const requestData = json ? data : new FormData();
  if (!json) {
    for (const key in data) {
      if (Array.isArray(data[key])) {
        for (let i = 0; i < data[key].length; i++) {
          requestData.append(key + "[" + i + "]", data[key][i]);
        }
      } else requestData.append(key, data[key]);
    }
  }

  params = {
    params: { ...params },
    headers: {
      "X-CSRFToken": Cookies.get(import.meta.env.VITE_CSRF_COOKIE_NAME) ?? "",
    },
  };
  if (isDownload) {
    params.responseType = "blob";
  }

  try {
    const {
      data: response,
      status: statusCode,
      headers,
    } = method === API_METHOD.GET || method === API_METHOD.DELETE
      ? yield APIKit[method](path, params)
      : yield APIKit[method](path, requestData, params);
    result = response;
    success = true;
    if (statusCode === 200 && isDownload) {
      const fileName = headers["content-disposition"].split("=")[1];
      FileDownload(response, fileName);
    }
  } catch (error) {
    let isAlert = true;
    if (error.code === "ECONNABORTED") {
      Swal.fire({
        icon: "error",
        title: "Server busy, try again after 30 seconds.",
        text: error?.message,
      }).then(() => {
        errorAction();
      });
    }

    const errorKey = Object.entries(error.response.data).map(function (item) {
      return `${item[0]}`;
    });
    const errorList = Object.entries(error.response.data).map(function (item) {
      return `${item[1]}`;
    });
    const statusCode = error?.response?.status;
    let errorTitle = error?.response?.data?.title ?? errorKey ?? "Oops";
    let errorMsg = error?.response?.data?.detail ?? errorList[0];

    if (statusCode === 403) {
      if (
        error.response.data.detail ===
          "Authentication credentials were not provided." ||
        error.response.data.detail ===
          "CSRF Failed: CSRF token missing or incorrect."
      ) {
        Cookies.remove(import.meta.env.VITE_CSRF_COOKIE_NAME);
        Cookies.remove(import.meta.env.VITE_SESSION_COOKIE_NAME);

        Swal.fire({
          icon: "error",
          title: "Please login again",
          text: error.response.data.detail,
        }).then(() => {
          window.location.href = import.meta.env.VITE_CAS_LOGOUT_URL;
        });
        return;
      }
      if (error.response.data.type === "application/json") {
        isAlert = false;
        const reader = new FileReader();
        reader.onload = function () {
          Swal.fire({
            icon: "error",
            title: JSON.parse(reader.result).title,
            text: JSON.parse(reader.result).detail,
          });
        };
        // return
        reader.readAsText(error.response.data);
      }
    } else if (statusCode === 404) {
      if (error.response.headers["content-type"] === "text/html")
        errorTitle = "Oops 404!";
      errorMsg = "No api url";
    } else if (statusCode === 400) {
      if (error.response.headers["content-type"] === "text/html")
        errorTitle = "Oops 400!";
      errorMsg = error.response.data.detail;
      if (error.response.data.type === "application/json") {
        isAlert = false;
        const reader = new FileReader();
        reader.onload = function () {
          Swal.fire({
            icon: "error",
            title: JSON.parse(reader.result).title,
            text: JSON.parse(reader.result).detail,
          });
        };
        // return
        reader.readAsText(error.response.data);
      }
    } else if (statusCode === 500) {
      if (error.response.headers["content-type"] === "text/html")
        errorTitle = "Oops! Server has trouble.";

      errorMsg = "500 Internal Server Error";
    } else if (statusCode === 503) {
      errorMsg = `${error.response.data?.detail}<br>Please note this error message and contact developers.`;
    }

    if (isAlert && errorAction) {
      errorAction(error);
      return yield put({
        type: "SET_API_ERROR",
        data: {
          title: errorTitle,
          message: errorMsg,
          action: errorAction,
        },
      });
    }
  }

  if (reducer) yield put({ type: reducer, data: result });

  if (success && successMessage) {
    yield put({
      type: "SET_API_SUCCESS",
      data: {
        title: successMessage,
        action: successAction,
      },
    });
  } else if (successAction) {
    successAction(result);
  }

  yield setLoading(false, path, method);

  return result;
}

function* rootSaga() {
  const sagas = _.map(_.values(import.meta.globEagerDefault("./*.jsx")), (o) =>
    o()
  );
  yield all(sagas);
}

export default rootSaga;
