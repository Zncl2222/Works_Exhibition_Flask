import { Box, Typography, useTheme } from "@mui/material";
import TextField from "@mui/material/TextField";
import { colorSettings } from "../theme";

const FormBox = (props) => {
  const { icon, title, forms = [] } = props;
  const theme = useTheme();
  const colors = colorSettings(theme.palette.mode);

  return (
    <Box width="100%" m="0 30px">
      <Box display="flex" justifyContent="space-between">
        <Box>
          {icon}
          <Typography
            variant="h4"
            fontWeight="bold"
            sx={{ color: colors.grey[100] }}
          >
            {title}
          </Typography>
        </Box>
      </Box>

      {forms.map((key, i) => (
        <Box>
          {forms.length % 2 !== 0 && i === forms.length - 1 ? (
            <TextField
              label={key}
              id="outlined-size-small"
              size="small"
              sx={{ mt: "10px" }}
            />
          ) : (
            <TextField
              label={key}
              id="outlined-size-small"
              size="small"
              sx={{ mt: "10px" }}
            />
          )}
        </Box>
      ))}
    </Box>
  );
};

export default FormBox;
