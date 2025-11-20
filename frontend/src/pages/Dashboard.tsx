import { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Assessment as AssessmentIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import axios from 'axios';

interface DashboardMetrics {
  total_processos: number;
  processos_concluidos: number;
  processos_em_andamento: number;
  processos_pendentes: number;
  total_empresas: number;
  porcentagem_conclusao: number;
  por_regime: Array<{
    regime: string;
    total: number;
    concluidos: number;
    porcentagem: number;
  }>;
}

export default function Dashboard() {
  console.log('🚀 Dashboard component mounted');
  
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = async () => {
    console.log('📊 Fetching metrics from backend...');
    setLoading(true);
    setError(null);
    
    try {
      const url = '/api/v1/dashboard/metricas';
      console.log('🌐 Request URL:', url);
      
      const response = await axios.get(url);
      console.log('✅ Response received:', response.data);
      
      setMetrics(response.data);
      console.log('💾 Metrics saved to state');
    } catch (err: any) {
      console.error('❌ Error fetching metrics:', err);
      console.error('❌ Error message:', err.message);
      console.error('❌ Error response:', err.response);
      
      const errorMsg = err.response?.data?.detail || err.message || 'Erro desconhecido';
      setError(`Erro ao conectar: ${errorMsg}`);
    } finally {
      setLoading(false);
      console.log('🏁 Fetch complete, loading:', false);
    }
  };

  useEffect(() => {
    console.log('🔄 useEffect triggered - fetching metrics');
    fetchMetrics();
  }, []);

  console.log('📝 Render state:', { loading, error: !!error, hasMetrics: !!metrics });

  if (loading) {
    console.log('⏳ Rendering loading state');
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography ml={2}>Carregando métricas...</Typography>
      </Box>
    );
  }

  if (error) {
    console.log('⚠️ Rendering error state:', error);
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={fetchMetrics} startIcon={<RefreshIcon />}>
          Tentar Novamente
        </Button>
      </Box>
    );
  }

  if (!metrics) {
    console.log('⚠️ Rendering no metrics state');
    return (
      <Box>
        <Alert severity="warning">Nenhum dado disponível</Alert>
        <Button variant="contained" onClick={fetchMetrics} startIcon={<RefreshIcon />} sx={{ mt: 2 }}>
          Carregar Dados
        </Button>
      </Box>
    );
  }

  console.log('✅ Rendering dashboard with metrics');

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchMetrics}
        >
          Atualizar
        </Button>
      </Box>

      {/* Cards de Métricas Principais */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <AssessmentIcon color="primary" sx={{ mr: 1 }} />
                <Typography color="textSecondary" variant="h6">
                  Total
                </Typography>
              </Box>
              <Typography variant="h3">
                {metrics.total_processos}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                processos
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                <Typography color="textSecondary" variant="h6">
                  Concluídos
                </Typography>
              </Box>
              <Typography variant="h3">
                {metrics.processos_concluidos || 0}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {(metrics.porcentagem_conclusao || 0).toFixed(1)}% completo
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <ScheduleIcon color="warning" sx={{ mr: 1 }} />
                <Typography color="textSecondary" variant="h6">
                  Em Andamento
                </Typography>
              </Box>
              <Typography variant="h3">
                {metrics.processos_em_andamento}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                processos ativos
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <BusinessIcon color="info" sx={{ mr: 1 }} />
                <Typography color="textSecondary" variant="h6">
                  Empresas
                </Typography>
              </Box>
              <Typography variant="h3">
                {metrics.total_empresas}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                cadastradas
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Progresso por Regime */}
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Processos por Regime Tributário
          </Typography>
          <Box mt={3}>
            {metrics.por_regime && metrics.por_regime.length > 0 ? (
              metrics.por_regime.map((regime) => (
                <Box key={regime.regime} mb={3}>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body1" fontWeight="bold">
                      {regime.regime}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {regime.concluidos || 0}/{regime.total || 0} ({(regime.porcentagem || 0).toFixed(1)}%)
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      width: '100%',
                      height: 12,
                      backgroundColor: '#e0e0e0',
                      borderRadius: 6,
                      overflow: 'hidden',
                    }}
                  >
                    <Box
                      sx={{
                        width: `${regime.porcentagem || 0}%`,
                        height: '100%',
                        backgroundColor: (regime.porcentagem || 0) === 100 ? '#4caf50' : '#2196f3',
                        transition: 'width 0.3s ease',
                      }}
                    />
                  </Box>
                </Box>
              ))
            ) : (
              <Typography color="textSecondary">Nenhum regime disponível</Typography>
            )}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
