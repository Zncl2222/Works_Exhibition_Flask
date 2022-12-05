import { Box, IconButton, useTheme } from "@mui/material";
import { useContext, useState } from "react";
import { ColorModeContext, colorSettings } from "../theme";
import InputBase from "@mui/material/InputBase";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import SearchIcon from "@mui/icons-material/Search";
import ColorLensIcon from "@mui/icons-material/ColorLens";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import LabelTwoToneIcon from "@mui/icons-material/LabelTwoTone";
import HexagonTwoToneIcon from "@mui/icons-material/HexagonTwoTone";
import MenuButton from "./Menu";

const Topbar = () => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const [barMode, setBarMode] = useState("yellow");
  const lightColors = ["yellow", "cyan", "default"];
  const BarColor = (barMode) => {
    return barMode === "yellow"
      ? colors.topbar["yellow"]
      : barMode === "cyan"
      ? colors.topbar["cyan"]
      : barMode === "purple"
      ? colors.topbar["purple"]
      : barMode === "red"
      ? colors.topbar["red"]
      : barMode === "blue"
      ? colors.topbar["blue"]
      : colors.topbar["default"];
  };
  const setBarOptions = (barMode) => {
    return barMode === "yellow"
      ? "cyan"
      : barMode === "cyan"
      ? "purple"
      : barMode === "purple"
      ? "red"
      : barMode === "red"
      ? "blue"
      : barMode === "blue"
      ? "default"
      : "yellow";
  };
  const iconColors = () => {
    if (barMode === "default" && theme.palette.mode === "dark") {
      return "#ffffff";
    }
    return lightColors.includes(barMode) ? "#000000" : "#ffffff";
  };

  return (
    <Box
      display="flex"
      justifyContent="space-between"
      p={2}
      bgcolor={BarColor(barMode)}
    >
      {/* SEARCH BAR */}
      <Box
        display="flex"
        backgroudcolor={colors.primary[400]}
        borderRadius="3px"
      >
        <InputBase
          sx={{ ml: 2, flex: 1, color: iconColors() }}
          placeholder="search"
        />
        <IconButton type="button" sx={{ p: 1 }}>
          <SearchIcon sx={{ color: iconColors() }} />
        </IconButton>
      </Box>

      {/* ICONS */}
      <Box display="flex">
        <IconButton onClick={() => setBarMode(setBarOptions(barMode))}>
          <ColorLensIcon sx={{ color: iconColors() }} />
        </IconButton>
        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? (
            <DarkModeOutlinedIcon sx={{ color: iconColors() }} />
          ) : (
            <LightModeOutlinedIcon sx={{ color: iconColors() }} />
          )}
        </IconButton>
        <MenuButton
          icon={<NotificationsOutlinedIcon sx={{ color: iconColors() }} />}
          attr={{
            color: colors.greenAccent[400],
            detail: ["comming soon"],
            subicons: [
              <LabelTwoToneIcon sx={{ mr: 1 }} />,
              <HexagonTwoToneIcon sx={{ mr: 1 }} />,
            ],
          }}
        />
        <MenuButton
          icon={<SettingsOutlinedIcon sx={{ color: iconColors() }} />}
          attr={{
            color: colors.greenAccent[400],
            detail: ["comming soon"],
            subicons: [
              <LabelTwoToneIcon sx={{ mr: 1 }} />,
              <HexagonTwoToneIcon sx={{ mr: 1 }} />,
            ],
          }}
        />
        <MenuButton
          icon={<PersonOutlinedIcon sx={{ color: iconColors() }} />}
          attr={{
            color: colors.greenAccent[400],
            detail: ["comming soon", "comming soon"],
            subicons: [
              <LabelTwoToneIcon sx={{ mr: 1 }} />,
              <HexagonTwoToneIcon sx={{ mr: 1 }} />,
            ],
          }}
        />
      </Box>
    </Box>
  );
};

export default Topbar;
