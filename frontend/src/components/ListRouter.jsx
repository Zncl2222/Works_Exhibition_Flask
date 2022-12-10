import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import { Link } from "react-router-dom";

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

export default ListItemLink;
