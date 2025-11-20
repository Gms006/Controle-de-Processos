# Guia de Instalação e Uso

## 📦 Instalação Detalhada

### Pré-requisitos
- Python 3.8 ou superior
- Acesso à API Acessórias
- Token de API válido

### Passo a Passo

1. **Verificar Python**
   ```powershell
   python --version
   ```

2. **Criar ambiente virtual**
   ```powershell
   cd "c:\acessorias processos"
   python -m venv venv
   ```

3. **Ativar ambiente virtual**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Instalar dependências**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Configurar credenciais**
   ```powershell
   copy .env.example .env
   notepad .env
   ```
   Adicione seu token da API no arquivo `.env`

## 🎮 Como Executar

### Buscar Processos de Simples Nacional

```powershell
python scripts\buscar_processos_simples_nacional.py
```

### Verificar Logs

```powershell
type logs\app.log
```

### Abrir Planilhas Geradas

```powershell
start output\planilhas\
```

## 🔍 Troubleshooting

### Erro de Autenticação
- Verifique se o token está correto no arquivo `.env`
- Gere um novo token no sistema Acessórias

### Erro de Rate Limit
- O script já respeita o limite de 90 req/min
- Aguarde 1 minuto e tente novamente

### Erro de Dependências
```powershell
pip install --upgrade -r requirements.txt
```

## 📚 Referências

- [GUIA_API_ACESSORIAS.md](../GUIA_API_ACESSORIAS.md) - Documentação completa da API
- [README.md](../README.md) - Visão geral do projeto
