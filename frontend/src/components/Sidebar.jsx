import { useState } from "react";
import { Box, IconButton, Typography, useTheme, styled } from "@mui/material";
import { colorSettings } from "../theme";
import ListItemLink from "./ListRouter";
import MuiDrawer from "@mui/material/Drawer";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import MenuIcon from "@mui/icons-material/Menu";
import List from "@mui/material/List";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import Collapse from "@mui/material/Collapse";
import FunctionsIcon from "@mui/icons-material/Functions";
import PublicIcon from "@mui/icons-material/Public";
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined";
import QuizOutlinedIcon from "@mui/icons-material/QuizOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import DashboardIcon from "@mui/icons-material/Dashboard";

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(7)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": closedMixin(theme),
  }),
}));

const Sidebar = () => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);
  const [open, setOpen] = useState(true);
  const [openResource, setOpenResource] = useState(false);
  const [openStatistic, setOpenStatistic] = useState(false);

  const handleResourceClick = () => {
    if (open) {
      setOpenResource(!openResource);
    } else if (!open) {
      handleDrawerOpen();
      setOpenResource(true);
    }
  };

  const handleStatisticClick = () => {
    if (open) {
      setOpenStatistic(!openStatistic);
    } else if (!open) {
      handleDrawerOpen();
      setOpenStatistic(true);
    }
  };

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpenResource(false);
    setOpenStatistic(false);
    setOpen(false);
  };

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <Drawer
        variant="permanent"
        open={open}
        PaperProps={{
          sx: {
            backgroundColor: colors.grey[900],
          },
        }}
      >
        <DrawerHeader>
          {open && (
            <Box display="flex" ml={`${drawerWidth / 3}px`}>
              <Typography variant="h3" color={colors.grey[100]}>
                ZWeb
              </Typography>
            </Box>
          )}
          <IconButton
            color={colors.grey[900]}
            aria-label="open drawer"
            onClick={open === false ? handleDrawerOpen : handleDrawerClose}
          >
            <MenuIcon />
          </IconButton>
        </DrawerHeader>

        <Divider />
        {open && (
          <Box mb="25px" mt="10px">
            <Box display="flex" justifyContent="center" alignItems="center">
              <img
                alt="profile-user"
                width="100px"
                height="100px"
                src={`../../logo512.png`}
                style={{ cursor: "pointer", borderRadius: "50%" }}
              />
            </Box>
            <Box textAlign="center">
              <Typography
                variant="h2"
                color={colors.grey[100]}
                fontWeight="bold"
                sx={{ m: "10px 0 0 0" }}
              >
                React
              </Typography>
              <Typography variant="h5" color={colors.greenAccent[500]}>
                ZWeb application
              </Typography>
            </Box>
          </Box>
        )}
        {/* List Item */}
        <List>
          <ListItemLink
            primary="Home"
            to="/"
            icon={<HomeOutlinedIcon sx={{ mr: 4 }} />}
          />

          <ListItemLink
            primary="Dashboard"
            to="/dashboard"
            icon={<DashboardIcon sx={{ mr: 4 }} />}
          />

          {/* Nested List Item */}
          <ListItemButton onClick={handleResourceClick}>
            <PublicIcon sx={{ mr: 4 }} />
            <ListItemText primary="Resource" />
            {openResource ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={openResource} timeout="auto" unmountOnExit>
            <List>
              <ListItemLink
                primary="sgsim"
                to="/sgsim"
                icon={<FunctionsIcon sx={{ mr: 4 }} />}
                isSubList={true}
              />
            </List>
          </Collapse>

          {/* Nested List Item */}
          <ListItemButton onClick={handleStatisticClick}>
            <AssessmentOutlinedIcon sx={{ mr: 4 }} />
            <ListItemText primary="Statistic" />
            {openStatistic ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={openStatistic} timeout="auto" unmountOnExit>
            <List>
              <ListItemLink
                primary="BarChart"
                to="/barchart"
                icon={<AssessmentOutlinedIcon sx={{ mr: 4 }} />}
                isSubList={true}
              />
            </List>
          </Collapse>

          <ListItemLink
            primary="Settings"
            to="/settings"
            icon={<SettingsOutlinedIcon sx={{ mr: 4 }} />}
          />

          <ListItemLink
            primary="Help"
            to="/help"
            icon={<QuizOutlinedIcon sx={{ mr: 4 }} />}
          />
        </List>
      </Drawer>
    </Box>
  );
};

export default Sidebar;
