import { Box, Typography, useTheme } from "@mui/material";
// import TextField from "@mui/material/TextField";
import SelectInputs from "./SelectInputs";
import { colorSettings } from "../theme";
import PropTypes from "prop-types";
import BasicInputs from "./BasicInputs";

const FormBox = (props) => {
  const { icon, title, inputItems = [], selectMenus = [] } = props;
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);

  return (
    <Box width="100%" m="0 30px">
      <Box display="flex" justifyContent="space-between">
        <Box>
          {icon}
          <Typography
            variant="h4"
            fontWeight="bold"
            sx={{ color: colors.grey[100] }}
          >
            {title}
          </Typography>
          <SelectInputs
            label="Core"
            menu={selectMenus}
            box_display="inline-block"
          />
        </Box>
      </Box>
      <BasicInputs items={inputItems} />
    </Box>
  );
};

FormBox.propTypes = {
  icon: PropTypes.element.isRequired,
  title: PropTypes.string.isRequired,
  inputItems: PropTypes.arrayOf(PropTypes.string),
  selectMenus: PropTypes.arrayOf(PropTypes.string),
};

export default FormBox;
