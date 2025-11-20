# Script para criar HTML com QR Code embutido
Write-Host "📱 Criando página HTML com QR Code..." -ForegroundColor Cyan

# Ler o JSON
$json = Get-Content "qr code.json" -Raw | ConvertFrom-Json

if ($json.base64) {
    $base64 = $json.base64
    
    # Criar HTML simples com QR Code embutido
    $html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code WhatsApp - Acessorias</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        h1 {
            font-size: 28px;
            margin-bottom: 20px;
        }
        img {
            width: 300px;
            height: 300px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .info {
            margin-top: 20px;
            font-size: 16px;
            opacity: 0.9;
        }
        .warning {
            background: rgba(255, 152, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 QR Code WhatsApp</h1>
        <p>Escaneie com WhatsApp Business 62 99997-6999</p>
        <img src="$base64" alt="QR Code do WhatsApp">
        <div class="warning">
            <strong>⏰ VÁLIDO POR 40 SEGUNDOS!</strong><br>
            Escaneie imediatamente!
        </div>
        <div class="info">
            📱 WhatsApp Business → ⋮ → Aparelhos conectados → Conectar aparelho
        </div>
    </div>
</body>
</html>
"@

    # Salvar HTML
    $html | Out-File -FilePath "qr_code_view.html" -Encoding UTF8
    
    Write-Host "✅ Página criada: qr_code_view.html" -ForegroundColor Green
    Write-Host "⏰ ESCANEIE EM 40 SEGUNDOS!" -ForegroundColor Yellow
    
    # Abrir no navegador
    Start-Process "qr_code_view.html"
    
} else {
    Write-Host "❌ Erro: QR Code não encontrado no JSON!" -ForegroundColor Red
}
