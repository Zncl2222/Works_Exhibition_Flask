import { Box } from "@mui/material";
import TextField from "@mui/material/TextField";
import PropTypes from "prop-types";

const BasicInputs = (props) => {
  const { items = [] } = props;

  // Divide the items into chunks of 4
  const chunkedItems = [];
  for (let i = 0; i < items.length; i += 4) {
    chunkedItems.push(items.slice(i, i + 4));
  }

  return (
    <div>
      {chunkedItems.map((chunk, rowIndex) => (
        <Box
          display="flex"
          flexWrap="wrap"
          key={rowIndex}
          sx={{
            marginBottom: "10px", // Add some spacing between rows
          }}
        >
          {chunk.map((label, colIndex) => (
            <TextField
              key={colIndex}
              id={`outlined-basic-${rowIndex}-${colIndex}`}
              label={label}
              variant="outlined"
              size="small"
              sx={{
                mt: 1,
                marginRight: "10px",
                minWidth: "150px", // Adjust the width as needed
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
