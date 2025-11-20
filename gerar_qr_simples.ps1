# Script corrigido - QR Code direto do /connect
Write-Host "`n📱 Gerando QR Code WhatsApp`n" -ForegroundColor Cyan

$apikey = "acessorias_evolution_key_2025"
$baseUrl = "http://localhost:8081"
$instanceName = "acessorias"

try {
    Write-Host "🔄 Chamando /instance/connect..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/instance/connect/$instanceName" -Method GET -Headers @{"apikey"=$apikey}
    
    Write-Host "✓ Resposta recebida`n" -ForegroundColor Green
    
    # Salvar resposta completa para debug
    $response | ConvertTo-Json -Depth 10 | Out-File "debug_response.json" -Encoding UTF8
    
    # Verificar se tem base64
    if ($response.base64) {
        Write-Host "✓ QR Code base64 encontrado!" -ForegroundColor Green
        $qrBase64 = $response.base64
    } elseif ($response.code) {
        Write-Host "✓ QR Code em 'code' encontrado!" -ForegroundColor Green
        $qrBase64 = $response.code
    } else {
        Write-Host "❌ QR Code não encontrado na resposta!" -ForegroundColor Red
        Write-Host "`nChaves disponíveis:" -ForegroundColor Yellow
        $response.PSObject.Properties | ForEach-Object { Write-Host "  - $($_.Name)" }
        Write-Host "`nResposta completa salva em: debug_response.json`n" -ForegroundColor Gray
        exit 1
    }
    
    # Verificar se já tem prefixo data:image
    if (-not $qrBase64.StartsWith("data:image")) {
        $qrBase64 = "data:image/png;base64,$qrBase64"
    }
    
    Write-Host "✓ Preparando HTML...`n" -ForegroundColor Green
    
    # HTML simples e direto
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>QR Code - WhatsApp</title>
    <style>
        body {
            font-family: Arial;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #25D366, #128C7E);
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            text-align: center;
        }
        img {
            width: 300px;
            height: 300px;
            border: 3px solid #25D366;
            border-radius: 10px;
        }
        h1 { color: #128C7E; margin-top: 0; }
        .status {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 10px;
            font-weight: bold;
        }
        .ok { color: #00C851; }
        .wait { color: #FF8800; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔐 QR Code WhatsApp</h1>
        <img src="$qrBase64" alt="QR Code">
        <div class="status wait" id="status">⏳ Aguardando escaneamento...</div>
    </div>
    
    <script>
        let checks = 0;
        const interval = setInterval(async () => {
            checks++;
            try {
                const res = await fetch('$baseUrl/instance/connectionState/$instanceName', {
                    headers: { 'apikey': '$apikey' }
                });
                const data = await res.json();
                
                const statusEl = document.getElementById('status');
                
                if (data.state === 'open') {
                    statusEl.className = 'status ok';
                    statusEl.innerHTML = '✅ CONECTADO!';
                    clearInterval(interval);
                    setTimeout(() => window.close(), 3000);
                } else {
                    statusEl.innerHTML = '⏳ Status: ' + data.state + ' (' + checks + 's)';
                }
                
                if (checks > 60) {
                    clearInterval(interval);
                    statusEl.innerHTML = '⚠️ Tempo esgotado';
                }
            } catch(e) {
                console.log('Erro:', e);
            }
        }, 1000);
    </script>
</body>
</html>
"@
    
    $html | Out-File "qr_whatsapp.html" -Encoding UTF8
    Write-Host "✅ HTML criado: qr_whatsapp.html`n" -ForegroundColor Green
    
    Start-Process "qr_whatsapp.html"
    Write-Host "🌐 Abrindo no navegador..." -ForegroundColor Cyan
    Write-Host "📱 Escaneie o QR Code agora!`n" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Erro:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nDetalhes:" -ForegroundColor Yellow
    $_.ErrorDetails.Message
}

Write-Host "`nPressione qualquer tecla..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
