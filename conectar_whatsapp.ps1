# Script completo: Deleta instância antiga + Cria nova + Gera QR Code + Abre HTML
Write-Host "`n🔄 Iniciando processo de conexão WhatsApp...`n" -ForegroundColor Cyan

# PASSO 1: Deletar instância antiga
Write-Host "🗑️  Deletando instância antiga..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "http://localhost:8081/instance/delete/acessorias" -Method DELETE -Headers @{"apikey"="acessorias_evolution_key_2025"} | Out-Null
    Write-Host "   ✓ Instância deletada" -ForegroundColor Green
} catch {
    Write-Host "   ℹ️  Nenhuma instância anterior" -ForegroundColor Gray
}

# Aguardar 2 segundos
Start-Sleep -Seconds 2

# PASSO 2: Criar nova instância e gerar QR Code
Write-Host "`n📱 Gerando novo QR Code..." -ForegroundColor Yellow
try {
    $body = @{
        instanceName="acessorias"
        qrcode=$true
        integration="WHATSAPP-BAILEYS"
        webhook=@{
            enabled=$true
            url="http://localhost:8000/whatsapp/evolution/webhook"
            webhookByEvents=$false
            webhookBase64=$false
            events=@("QRCODE_UPDATED","MESSAGES_UPSERT","MESSAGES_UPDATE","MESSAGES_DELETE","SEND_MESSAGE","CONNECTION_UPDATE")
        }
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "http://localhost:8081/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $body
    
    # Salvar JSON
    $response.qrcode | ConvertTo-Json -Depth 10 | Out-File -FilePath "qr code.json" -Encoding UTF8
    Write-Host "   ✓ QR Code salvo em JSON" -ForegroundColor Green
    
    # PASSO 3: Criar HTML com QR Code embutido
    Write-Host "`n🌐 Criando página HTML..." -ForegroundColor Yellow
    
    $base64 = $response.qrcode.base64
    
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
            font-size: 32px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 18px;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        img {
            width: 300px;
            height: 300px;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .warning {
            background: rgba(255, 152, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 16px;
            font-weight: bold;
        }
        .info {
            margin-top: 20px;
            font-size: 16px;
            opacity: 0.9;
            line-height: 1.6;
        }
        .steps {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: left;
        }
        .step {
            margin: 10px 0;
            padding-left: 25px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 QR Code WhatsApp</h1>
        <p class="subtitle">WhatsApp Business 62 99997-6999</p>
        
        <img src="$base64" alt="QR Code do WhatsApp">
        
        <div class="warning">
            ⏰ VÁLIDO POR 40 SEGUNDOS!<br>
            Escaneie IMEDIATAMENTE!
        </div>
        
        <div class="steps">
            <strong>📱 Como conectar:</strong>
            <div class="step">1️⃣ Abra WhatsApp Business no celular</div>
            <div class="step">2️⃣ Toque em ⋮ (três pontos) → Aparelhos conectados</div>
            <div class="step">3️⃣ Toque em "Conectar aparelho"</div>
            <div class="step">4️⃣ Escaneie este QR Code AGORA!</div>
        </div>
        
        <div class="info">
            ⚠️ Certifique-se que o celular está com INTERNET ativa!
        </div>
    </div>
</body>
</html>
"@
    
    # Salvar HTML
    $html | Out-File -FilePath "qr_code_view.html" -Encoding UTF8
    Write-Host "   ✓ Página HTML criada" -ForegroundColor Green
    
    # PASSO 4: Abrir no navegador
    Write-Host "`n✅ TUDO PRONTO!`n" -ForegroundColor Green
    Write-Host "⏰ ATENÇÃO: Você tem 40 SEGUNDOS para escanear!`n" -ForegroundColor Yellow
    Write-Host "📱 Abrindo navegador com QR Code..." -ForegroundColor Cyan
    
    Start-Process "qr_code_view.html"
    
    Write-Host "`n✨ Página aberta! Escaneie o QR Code AGORA!" -ForegroundColor Green
    Write-Host "   Se não conectar, execute este script novamente.`n" -ForegroundColor Gray
    
} catch {
    Write-Host "`n❌ Erro:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`n🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
