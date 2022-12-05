import { useState, Fragment } from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { IconButton, Typography } from "@mui/material";

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
    <MenuItem onClick={handleClose}>
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

export default MenuButton;
