const initialState = {
  sgsimList: null,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case "FETCH_SGSIM_RESULT":
      return {
        ...state,
        sgsimList: action?.data ?? null,
      };
    default:
      return state;
  }
};

export default reducer;
