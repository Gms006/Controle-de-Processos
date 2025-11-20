# Frontend - Sistema de Gestão de Processos Contábeis

Interface React + TypeScript + Material-UI para visualização e gestão de processos contábeis.

## 🚀 Tecnologias

- **React 18** - Framework UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool ultra-rápido
- **Material-UI (MUI)** - Componentes UI profissionais
- **React Router** - Navegação entre páginas
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos e visualizações

## 📦 Instalação

```bash
cd frontend
npm install
```

## 🏃 Executar

```bash
# Desenvolvimento (porta 3000)
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## 📁 Estrutura

```
frontend/
├── src/
│   ├── components/      # Componentes reutilizáveis
│   │   └── Layout.tsx   # Layout principal com sidebar
│   ├── pages/           # Páginas da aplicação
│   │   ├── Dashboard.tsx       # Dashboard principal
│   │   ├── Empresas.tsx        # Análise por empresa
│   │   ├── Declaracoes.tsx     # Declarações do mês
│   │   ├── Faturamento.tsx     # Análise de faturamento
│   │   └── Desdobramentos.tsx  # Desdobramentos pendentes
│   ├── App.tsx          # Componente raiz
│   ├── main.tsx         # Entry point
│   └── index.css        # Estilos globais
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 🌐 Páginas

### 1. Dashboard (`/`)
- **Métricas principais**: Total de processos, concluídos, em andamento, empresas
- **Gráficos por regime**: SimplesNacional, LucroPresumido, LucroReal
- **Porcentagem de conclusão** global e por regime
- **Botão de atualização** manual

### 2. Empresas (`/empresas`)
- Análise individual por empresa
- Histórico de processos
- Detalhes de cada processo

### 3. Declarações (`/declaracoes`)
- Obrigações do mês:
  - DAS (Simples Nacional)
  - EFD REINF
  - DIFAL
  - ICMS
  - ISS
  - DIRB

### 4. Faturamento (`/faturamento`)
- Empresas que faturaram
- Empresas que não faturaram
- Comparativos e análises

### 5. Desdobramentos (`/desdobramentos`)
- Perguntas pendentes
- Decisões aguardando resposta
- Filtros e buscas

## 🔌 API

O frontend se conecta ao backend FastAPI em `http://localhost:8000`

Proxy configurado no `vite.config.ts`:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

## 🎨 Tema

- **Cor primária**: #1976d2 (Azul Material)
- **Cor secundária**: #dc004e (Rosa)
- **Background**: #f5f5f5 (Cinza claro)

## 📱 Responsivo

- Mobile-first design
- Sidebar colapsável em telas pequenas
- Layout adaptativo para tablets e desktops
