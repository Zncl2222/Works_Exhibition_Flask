import { Box } from "@mui/material";
import TextField from "@mui/material/TextField";
import PropTypes from "prop-types";

const BasicInputs = (props) => {
  const { items = [] } = props;
  return (
    <div>
      {items.map((chunk, index) => (
        <Box display="flex" flexWrap="wrap" key={index}>
          {chunk.map((key) => (
            <TextField
              key={key}
              label={key}
              id="outlined-basic"
              variant="outlined"
              size="small"
              sx={{
                mt: 2,
                marginRight: "10px",
              }}
            />
          ))}
        </Box>
      ))}
    </div>
  );
};

BasicInputs.propTypes = {
  items: PropTypes.arrayOf(PropTypes.string),
};

export default BasicInputs;
