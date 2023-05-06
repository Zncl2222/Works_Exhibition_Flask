import { useState, Fragment } from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { IconButton, Typography } from "@mui/material";
import PropTypes from "prop-types";

const MenuButton = (props) => {
  const { icon, attr } = props;
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const textColor = attr.color;
  const detail = attr.detail;
  const subicons = attr.subicons;
  const listItems = detail.map((val, idx) => (
    <MenuItem onClick={handleClose} key={idx}>
      {subicons[idx]}
      <Typography color={textColor}>{val}</Typography>
    </MenuItem>
  ));
  return (
    <Fragment>
      <IconButton onClick={handleClick}>{icon}</IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        {listItems}
      </Menu>
    </Fragment>
  );
};

MenuButton.propTypes = {
  icon: PropTypes.element.isRequired,
  attr: PropTypes.shape({
    color: PropTypes.string.isRequired,
    detail: PropTypes.arrayOf(PropTypes.string.isRequired).isRequired,
    subicons: PropTypes.arrayOf(PropTypes.element.isRequired).isRequired,
  }).isRequired,
};

export default MenuButton;
