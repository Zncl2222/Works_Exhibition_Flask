/* eslint-disable react/prop-types */
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

const ListItemLink = (props) => {
  const { icon, primary, to, isSubList = false } = props;

  return (
    <ListItemButton
      component={Link}
      to={to}
      sx={{ pl: isSubList ? 4 : undefined }}
    >
      {icon}
      <ListItemText
        primary={primary}
        primaryTypographyProps={{
          fontWeight: "large",
        }}
      />
    </ListItemButton>
  );
};

ListItemLink.propTypes = {
  icon: PropTypes.element.isRequired,
  primary: PropTypes.string.isRequired,
  to: PropTypes.string.isRequired,
  isSubList: PropTypes.bool,
};

export default ListItemLink;
