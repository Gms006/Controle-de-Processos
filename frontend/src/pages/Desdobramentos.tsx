import { Typography, Box } from '@mui/material';

export default function Desdobramentos() {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Desdobramentos Pendentes
      </Typography>
      <Typography variant="body1" color="textSecondary">
        Perguntas e decisões aguardando resposta
      </Typography>
      <Typography variant="body2" color="textSecondary" mt={2}>
        Em desenvolvimento...
      </Typography>
    </Box>
  );
}
