import PropTypes from "prop-types"; // Import prop-types

import { Box, Typography, useTheme } from "@mui/material";
import { colorSettings } from "../theme";

const StatBox = ({ title, subtitle, icon, increase }) => {
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
        </Box>
      </Box>
      <Box></Box>
      <Box display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ color: colors.greenAccent[100] }}>
          {subtitle}
        </Typography>
        <Typography
          variant="h4"
          fontStyle="italic"
          sx={{ color: colors.greenAccent[600] }}
        >
          {increase}
        </Typography>
      </Box>
    </Box>
  );
};

// Add prop validation using PropTypes
StatBox.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
  icon: PropTypes.element.isRequired,
  progress: PropTypes.number, // Change the type according to your needs
  increase: PropTypes.number, // Change the type according to your needs
};

export default StatBox;
