import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { colorSettings } from "../../theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import InputIcon from "@mui/icons-material/Input";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

import FormBox from "../../components/FormBox";
import BasicInputs from "../../components/BasicInputs";
import SelectInputs from "../../components/SelectInputs";
import HistoryIcon from "@mui/icons-material/History";

const Dashboard = () => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);
  const forms = [
    "Realizations Number",
    "Model Size (X)",
    "Kriging Range",
    "Kriging Sill",
  ];
  const cores = ["Python", "C"];
  const covModel = ["Gaussian", "Exponential", "Spherical"];

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
            Download Reports
          </Button>
        </Box>
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 8"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="top"
          justifyContent="center"
        >
          <FormBox
            title="Parameters"
            customComponents={
              <Box>
                <Box sx={{ mb: 1 }}>
                  <SelectInputs
                    label="Core"
                    menu={cores}
                    box_display="inline-block"
                  />
                  <SelectInputs
                    label="Covariance"
                    menu={covModel}
                    box_display="inline-block"
                  />
                </Box>
                <BasicInputs items={forms} />
              </Box>
            }
            icon={
              <InputIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
          <Box
            mr="10px"
            mt="200px"
            display="flex"
            justifyContent="top"
            alignItems="center"
          >
            <Button
              variant="contained"
              sx={{
                backgroundColor: colors.primary[300],
                color: colors.primary[100],
                fontSize: "10px",
                fontWeight: "bold",
              }}
            >
              Run
            </Button>
          </Box>
        </Box>

        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="top"
          justifyContent="left"
        >
          <FormBox
            title="History"
            icon={
              <HistoryIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>

        {/* ROW 2 */}
        <Box
          gridColumn="span 8"
          gridRow="span 4"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h3"
                fontWeight="600"
                color={colors.grey[100]}
              >
                Results
              </Typography>
            </Box>
            <Box>
              <IconButton>
                <DownloadOutlinedIcon
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
              </IconButton>
            </Box>
          </Box>
          <Box height="300px" m="100px 0 0 0"></Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 4"
          backgroundColor={colors.primary[400]}
          overflow="auto"
        >
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            borderBottom={`4px solid ${colors.primary[500]}`}
            colors={colors.grey[100]}
            p="15px"
          >
            <Typography color={colors.grey[100]} variant="h5" fontWeight="600">
              Statistic Results
            </Typography>
          </Box>
        </Box>
      </Box>
      <Footer />
    </Box>
  );
};

export default Dashboard;
