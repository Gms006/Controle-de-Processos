# Script CORRETO de conexão WhatsApp - Seguindo fluxo oficial
Write-Host "`n🔄 CONEXÃO WHATSAPP - FLUXO CORRETO`n" -ForegroundColor Cyan

$apikey = "acessorias_evolution_key_2025"
$baseUrl = "http://localhost:8081"
$instanceName = "acessorias"

# PASSO 1: Verificar se instância já existe
Write-Host "🔍 Verificando instância..." -ForegroundColor Yellow
try {
    $instances = Invoke-RestMethod -Uri "$baseUrl/instance/fetchInstances" -Method GET -Headers @{"apikey"=$apikey}
    $existente = $instances | Where-Object { $_.name -eq $instanceName }
    
    if ($existente) {
        Write-Host "   ℹ️  Instância '$instanceName' já existe" -ForegroundColor Gray
        Write-Host "   Status: $($existente.connectionStatus)" -ForegroundColor Gray
        
        if ($existente.connectionStatus -eq "open") {
            Write-Host "`n✅ JÁ CONECTADO!" -ForegroundColor Green
            Write-Host "   Número: $($existente.number)" -ForegroundColor White
            exit 0
        }
        
        # Se não está conectada, vamos reconectar
        Write-Host "   🔄 Instância existe mas não conectada, gerando novo QR..." -ForegroundColor Yellow
    } else {
        # PASSO 2: Criar instância (apenas se não existir)
        Write-Host "`n📝 Criando nova instância..." -ForegroundColor Yellow
        
        $createBody = @{
            instanceName = $instanceName
            token = $apikey
            qrcode = $false
            integration = "WHATSAPP-BAILEYS"
        } | ConvertTo-Json
        
        $created = Invoke-RestMethod -Uri "$baseUrl/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"=$apikey} -Body $createBody
        
        if ($created.instance.status -eq "created") {
            Write-Host "   ✓ Instância criada com sucesso!" -ForegroundColor Green
        }
        
        Start-Sleep -Seconds 2
    }
} catch {
    Write-Host "   ❌ Erro ao verificar/criar instância" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# PASSO 3: Chamar /instance/connect para gerar QR Code
Write-Host "`n📱 Gerando QR Code..." -ForegroundColor Yellow
try {
    $connectResponse = Invoke-RestMethod -Uri "$baseUrl/instance/connect/$instanceName" -Method GET -Headers @{"apikey"=$apikey}
    
    if ($connectResponse.code) {
        Write-Host "   ✓ QR Code gerado!" -ForegroundColor Green
        
        # Salvar JSON
        $connectResponse | ConvertTo-Json -Depth 10 | Out-File -FilePath "qr code.json" -Encoding UTF8
        
        # Criar HTML com QR Code embutido
        $base64 = $connectResponse.code
        
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
            background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
            color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            max-width: 500px;
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
        .status {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            font-size: 14px;
        }
    </style>
    <script>
        let checkCount = 0;
        const maxChecks = 60; // 60 segundos
        
        async function checkConnection() {
            try {
                const response = await fetch('http://localhost:8081/instance/connectionState/$instanceName', {
                    headers: { 'apikey': '$apikey' }
                });
                const data = await response.json();
                
                document.getElementById('status').innerHTML = 
                    '🔄 Status: <strong>' + data.state + '</strong><br>' +
                    '⏱️ Checando há ' + checkCount + ' segundos...';
                
                if (data.state === 'open') {
                    document.getElementById('status').innerHTML = 
                        '✅ <strong>CONECTADO COM SUCESSO!</strong><br>' +
                        'Você já pode fechar esta página.';
                    clearInterval(intervalId);
                    document.body.style.background = 'linear-gradient(135deg, #00C851 0%, #007E33 100%)';
                }
                
                checkCount++;
                if (checkCount >= maxChecks) {
                    clearInterval(intervalId);
                    document.getElementById('status').innerHTML = 
                        '⚠️ Tempo esgotado. Recarregue a página para novo QR.';
                }
            } catch (err) {
                console.log('Erro ao verificar status:', err);
            }
        }
        
        // Iniciar verificação a cada 1 segundo
        const intervalId = setInterval(checkConnection, 1000);
        setTimeout(checkConnection, 100); // Primeira verificação imediata
    </script>
</head>
<body>
    <div class="container">
        <h1>🔐 QR Code WhatsApp</h1>
        <p class="subtitle">Instância: $instanceName</p>
        
        <img src="$base64" alt="QR Code do WhatsApp">
        
        <div class="warning">
            ⏰ Escaneie com seu WhatsApp!
        </div>
        
        <div class="steps">
            <strong>📱 Como conectar:</strong>
            <div class="step">1️⃣ Abra WhatsApp no celular</div>
            <div class="step">2️⃣ Toque em ⋮ → Aparelhos conectados</div>
            <div class="step">3️⃣ Toque em "Conectar aparelho"</div>
            <div class="step">4️⃣ Escaneie este QR Code</div>
        </div>
        
        <div class="status" id="status">
            🔄 Aguardando conexão...
        </div>
    </div>
</body>
</html>
"@
        
        $html | Out-File -FilePath "qr_code_connect.html" -Encoding UTF8
        Write-Host "   ✓ Página HTML criada" -ForegroundColor Green
        
        Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host "✅ TUDO PRONTO!" -ForegroundColor Green
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
        
        # Abrir navegador
        Start-Process "qr_code_connect.html"
        
        Write-Host "📱 Escaneie o QR Code que abriu no navegador" -ForegroundColor Yellow
        Write-Host "🔄 A página vai detectar automaticamente quando conectar!`n" -ForegroundColor Gray
        
        # Aguardar conexão (monitorar connectionState)
        Write-Host "⏳ Aguardando conexão" -NoNewline
        $timeout = 60
        $elapsed = 0
        
        while ($elapsed -lt $timeout) {
            Start-Sleep -Seconds 2
            $elapsed += 2
            Write-Host "." -NoNewline
            
            try {
                $state = Invoke-RestMethod -Uri "$baseUrl/instance/connectionState/$instanceName" -Method GET -Headers @{"apikey"=$apikey}
                
                if ($state.state -eq "open") {
                    Write-Host "`n`n✅ CONECTADO COM SUCESSO!" -ForegroundColor Green
                    Write-Host "   Instância: $instanceName" -ForegroundColor White
                    Write-Host "   Status: OPEN`n" -ForegroundColor Green
                    exit 0
                }
            } catch {
                # Continua tentando
            }
        }
        
        Write-Host "`n`n⚠️ Timeout atingido" -ForegroundColor Yellow
        Write-Host "   Execute o script novamente se não conectou.`n" -ForegroundColor Gray
        
    } else {
        Write-Host "   ⚠️ Resposta inesperada do /connect" -ForegroundColor Yellow
        $connectResponse | ConvertTo-Json -Depth 5
    }
    
} catch {
    Write-Host "`n❌ Erro ao gerar QR Code:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`n🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
