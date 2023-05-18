import { useState } from "react";
import { Box } from "@mui/material";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import PropTypes from "prop-types";

const SelectInputs = (props) => {
  const { label, menu = [] } = props;

  const [core, setCore] = useState("");

  const handleChange = (event) => {
    setCore(event.target.value);
  };

  return (
    <Box sx={{ minWidth: 120, mt: 2 }}>
      <FormControl fullWidth size="small">
        <InputLabel id="demo-simple-select-label">{label}</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={core}
          label={core}
          onChange={handleChange}
        >
          {menu.map((item) => (
            <MenuItem key={item} value={item}>
              {item}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
};

SelectInputs.propTypes = {
  label: PropTypes.string.isRequired,
  menu: PropTypes.arrayOf(PropTypes.string),
};

export default SelectInputs;
