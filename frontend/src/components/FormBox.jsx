import { Box, Typography, useTheme } from "@mui/material";
import { colorSettings } from "../theme";
import PropTypes from "prop-types";

const FormBox = (props) => {
  const { icon, title, customComponents } = props;
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
          <Box>{customComponents}</Box>
        </Box>
      </Box>
    </Box>
  );
};

FormBox.propTypes = {
  icon: PropTypes.element.isRequired,
  title: PropTypes.string.isRequired,
  customComponents: PropTypes.element,
};

export default FormBox;
