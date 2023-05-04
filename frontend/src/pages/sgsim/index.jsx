import { Box, Button, useTheme } from "@mui/material";
import { colorSettings } from "../../theme";

import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";

import Header from "../../components/Header";
import Footer from "../../components/Footer";

const Dashboard = () => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header
          title="Sequential Gaussian Simulation"
          subtitle="geostatistic algorithm based on kriging"
        />
        <Box>
          <Button
            sx={{
              backgroundColor: colors.primary[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Download
          </Button>
        </Box>
      </Box>
      <Footer />
    </Box>
  );
};

export default Dashboard;
