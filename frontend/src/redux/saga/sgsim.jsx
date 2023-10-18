import { takeLatest } from "redux-saga/effects";
import { API_METHOD } from "../api/apiServices";
import { SGSIM } from "../api/API";
import { fetchApi } from ".";

function* fetchSgsim(action) {
  yield fetchApi({
    ...action,
    method: API_METHOD.GET,
    path: SGSIM,
    reducer: "FETCH_SGSIM_RESULT",
  });
}

function* mySaga() {
  yield takeLatest("FETCH_SGSIM", fetchSgsim);
}

export default mySaga;
