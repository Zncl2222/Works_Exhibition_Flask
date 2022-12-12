import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import { useTheme } from "@mui/material";
import { colorSettings } from "../theme";

const Footer = () => {
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);
  return (
    <Box sx={{ mt: 30, py: 3 }}>
      <Container maxWidth="90%">
        <Stack spacing={4}>
          <Box>
            <Grid container spacing={2}>
              <Grid item xs={6} md={3}>
                <Stack spacing={2}>
                  <Typography sx={{ mt: 1 }} color={colors.grey[100]}>
                    © 2022 Zncl2222, Inc.
                  </Typography>
                </Stack>
              </Grid>
              <Grid item xs={6} md={3}>
                <Stack spacing={2}></Stack>
              </Grid>
              <Grid item xs={6} md={3}>
                <Stack spacing={2}></Stack>
              </Grid>
              <Grid item xs={6} md={3}>
                <Stack spacing={2}></Stack>
              </Grid>
            </Grid>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
};

export default Footer;
