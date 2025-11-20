import { Typography, Box } from '@mui/material';

export default function Declaracoes() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Declarações do Mês
      </Typography>
      <Typography variant="body1" color="textSecondary">
        DAS, EFD REINF, DIFAL, ICMS, ISS, DIRB...
      </Typography>
      <Typography variant="body2" color="textSecondary" mt={2}>
        Em desenvolvimento...
      </Typography>
    </Box>
  );
}
