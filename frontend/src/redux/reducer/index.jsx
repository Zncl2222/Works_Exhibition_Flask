import _ from "lodash";

const reducer = (state = {}, action) => {
  const reducers = _.reduce(
    import.meta.globEagerDefault("./*.jsx"),
    (dict, func, path) => {
      const key = path.replace("./", "").replace(".jsx", "");
      dict[key] = func(state[key], action);
      return dict;
    },
    {}
  );

  // always return a new object for the root state
  return reducers;
};

export default reducer;
