/* eslint-disable react/prop-types */
import { Typography, Box, useTheme } from "@mui/material";
import { colorSettings } from "../theme";
import PropTypes from "prop-types";

const Header = ({ title, subtitle }) => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);
  return (
    <Box mb="40px">
      <Typography
        variant="h3"
        color={colors.grey[100]}
        fontWeight="bold"
        sx={{ mb: "10px" }}
      >
        {title}
      </Typography>
      <Typography variant="h5" color={colors.header["cyan"]}>
        {subtitle}
      </Typography>
    </Box>
  );
};

Header.propTypes = {
  title: PropTypes.string.isRequired,
  subtitle: PropTypes.string.isRequired,
};

export default Header;
