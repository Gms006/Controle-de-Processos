import { Typography, Box } from '@mui/material';

export default function Faturamento() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Análise de Faturamento
      </Typography>
      <Typography variant="body1" color="textSecondary">
        Empresas que faturaram vs não faturaram
      </Typography>
      <Typography variant="body2" color="textSecondary" mt={2}>
        Em desenvolvimento...
      </Typography>
    </Box>
  );
}
