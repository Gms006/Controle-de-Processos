# Fluxo CORRETO de conexão WhatsApp - Baseado na análise técnica
Write-Host "`n🔍 DIAGNÓSTICO E CONEXÃO WHATSAPP`n" -ForegroundColor Cyan

$apikey = "acessorias_evolution_key_2025"
$baseUrl = "http://localhost:8081"
$instanceName = "acessorias"

# ==========================================
# PASSO 1: Diagnóstico completo do estado
# ==========================================
Write-Host "📊 Verificando estado real da instância..." -ForegroundColor Yellow

try {
    $instances = Invoke-RestMethod -Uri "$baseUrl/instance/fetchInstances?instanceName=$instanceName" -Method GET -Headers @{"apikey"=$apikey}
    
    if ($instances.Count -eq 0) {
        Write-Host "   ℹ️  Instância não existe`n" -ForegroundColor Gray
        $needsCreate = $true
    } else {
        $instance = $instances[0]
        
        Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host "📋 ESTADO ATUAL DA INSTÂNCIA" -ForegroundColor White
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host "   Nome: $($instance.name)" -ForegroundColor Gray
        Write-Host "   Status: $($instance.connectionStatus)" -ForegroundColor $(if ($instance.connectionStatus -eq "open") { "Green" } else { "Yellow" })
        Write-Host "   Owner: $($instance.ownerJid)" -ForegroundColor Gray
        Write-Host "   Profile: $($instance.profileName)" -ForegroundColor Gray
        
        if ($instance.disconnectionReasonCode) {
            Write-Host "   ⚠️  Código desconexão: $($instance.disconnectionReasonCode)" -ForegroundColor Red
            
            # Parse do disconnectionObject
            if ($instance.disconnectionObject) {
                try {
                    $disconnObj = $instance.disconnectionObject | ConvertFrom-Json
                    if ($disconnObj.error.data.content) {
                        $conflict = $disconnObj.error.data.content | Where-Object { $_.tag -eq "conflict" }
                        if ($conflict) {
                            Write-Host "   ⚠️  Tipo: $($conflict.attrs.type)" -ForegroundColor Red
                        }
                    }
                } catch {
                    # Ignora se não conseguir parsear
                }
            }
        }
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
        
        # Decisão baseada no estado REAL
        if ($instance.connectionStatus -eq "open") {
            Write-Host "✅ INSTÂNCIA JÁ CONECTADA!" -ForegroundColor Green
            Write-Host "   Número: $($instance.ownerJid)`n" -ForegroundColor White
            exit 0
        }
        
        # Se tem device_removed (401) ou outros erros críticos
        if ($instance.disconnectionReasonCode -eq 401) {
            Write-Host "🔴 DEVICE_REMOVED detectado!" -ForegroundColor Red
            Write-Host "   O WhatsApp revogou esta sessão." -ForegroundColor Yellow
            Write-Host "`n📋 Causas possíveis:" -ForegroundColor Gray
            Write-Host "   • Logout manual no app" -ForegroundColor Gray
            Write-Host "   • Reinstalação do WhatsApp" -ForegroundColor Gray
            Write-Host "   • Bug conhecido Evolution/Baileys" -ForegroundColor Gray
            Write-Host "   • Mudanças no protocolo WhatsApp`n" -ForegroundColor Gray
            
            $action = Read-Host "Deletar instância e criar nova? (S/N)"
            if ($action -ne "S" -and $action -ne "s") {
                Write-Host "❌ Cancelado pelo usuário" -ForegroundColor Red
                exit 0
            }
            
            # Deletar instância comprometida
            Write-Host "`n🗑️  Deletando instância comprometida..." -ForegroundColor Yellow
            Invoke-RestMethod -Uri "$baseUrl/instance/delete/$instanceName" -Method DELETE -Headers @{"apikey"=$apikey} | Out-Null
            Write-Host "   ✓ Instância deletada`n" -ForegroundColor Green
            Start-Sleep -Seconds 3
            $needsCreate = $true
            
        } elseif ($instance.connectionStatus -eq "close") {
            Write-Host "🔄 Instância fechada (sem erros críticos)" -ForegroundColor Yellow
            Write-Host "   Tentando logout primeiro...`n" -ForegroundColor Gray
            
            try {
                Invoke-RestMethod -Uri "$baseUrl/instance/logout/$instanceName" -Method DELETE -Headers @{"apikey"=$apikey} | Out-Null
                Write-Host "   ✓ Logout executado`n" -ForegroundColor Green
                Start-Sleep -Seconds 2
            } catch {
                Write-Host "   ℹ️  Logout falhou, seguindo para connect`n" -ForegroundColor Gray
            }
            
            $needsCreate = $false
        } else {
            Write-Host "⚠️ Estado inesperado: $($instance.connectionStatus)" -ForegroundColor Yellow
            $needsCreate = $false
        }
    }
    
} catch {
    Write-Host "   ⚠️ Erro ao consultar: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Assumindo que precisa criar instância`n" -ForegroundColor Gray
    $needsCreate = $true
}

# ==========================================
# PASSO 2: Criar instância (se necessário)
# ==========================================
if ($needsCreate) {
    Write-Host "📝 Criando nova instância..." -ForegroundColor Yellow
    
    try {
        $createBody = @{
            instanceName = $instanceName
            token = $apikey
            qrcode = $false
            integration = "WHATSAPP-BAILEYS"
        } | ConvertTo-Json
        
        $created = Invoke-RestMethod -Uri "$baseUrl/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"=$apikey} -Body $createBody
        
        if ($created.instance.status -eq "created") {
            Write-Host "   ✓ Instância criada: $($created.instance.instanceName)" -ForegroundColor Green
            Write-Host "   ✓ Status: $($created.instance.status)`n" -ForegroundColor Green
            Start-Sleep -Seconds 3
        }
    } catch {
        Write-Host "   ❌ Erro ao criar instância:" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)`n" -ForegroundColor Red
        exit 1
    }
}

# ==========================================
# PASSO 3: Verificar connectionState antes de connect
# ==========================================
Write-Host "🔍 Verificando connectionState..." -ForegroundColor Yellow

try {
    $connState = Invoke-RestMethod -Uri "$baseUrl/instance/connectionState/$instanceName" -Method GET -Headers @{"apikey"=$apikey}
    Write-Host "   Estado: $($connState.state)" -ForegroundColor $(if ($connState.state -eq "open") { "Green" } else { "Yellow" })
    
    if ($connState.state -eq "open") {
        Write-Host "`n✅ JÁ CONECTADO (connectionState confirma)!" -ForegroundColor Green
        exit 0
    }
    
    if ($connState.statusCode -eq 401) {
        Write-Host "   ⚠️ StatusCode 401 detectado no connectionState" -ForegroundColor Red
        Write-Host "   Isso indica bug conhecido Evolution/Baileys" -ForegroundColor Yellow
        Write-Host "   Vamos tentar conectar mesmo assim...`n" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "   ℹ️  ConnectionState indisponível, seguindo...`n" -ForegroundColor Gray
}

# ==========================================
# PASSO 4: Gerar QR Code via /connect
# ==========================================
Write-Host "📱 Gerando QR Code..." -ForegroundColor Yellow

try {
    $connectResponse = Invoke-RestMethod -Uri "$baseUrl/instance/connect/$instanceName" -Method GET -Headers @{"apikey"=$apikey}
    
    # Salvar resposta completa para debug
    $connectResponse | ConvertTo-Json -Depth 10 | Out-File "debug_connect_response.json" -Encoding UTF8
    
    # Detectar onde está o QR Code
    $qrBase64 = $null
    if ($connectResponse.base64) {
        $qrBase64 = $connectResponse.base64
        Write-Host "   ✓ QR encontrado em 'base64'" -ForegroundColor Green
    } elseif ($connectResponse.code) {
        $qrBase64 = $connectResponse.code
        Write-Host "   ✓ QR encontrado em 'code'" -ForegroundColor Green
    } elseif ($connectResponse.instance.state -eq "open") {
        Write-Host "`n⚠️ /connect retornou state: open" -ForegroundColor Yellow
        Write-Host "   Mas fetchInstances mostrou 'close' antes." -ForegroundColor Yellow
        Write-Host "   Estado inconsistente - possível bug Evolution.`n" -ForegroundColor Red
        Write-Host "📋 Resposta salva em: debug_connect_response.json" -ForegroundColor Gray
        Write-Host "`n💡 SUGESTÃO:" -ForegroundColor Cyan
        Write-Host "   1. Abra issue no GitHub Evolution API" -ForegroundColor White
        Write-Host "   2. Anexe o arquivo debug_connect_response.json" -ForegroundColor White
        Write-Host "   3. Mencione: 'state inconsistente + device_removed'`n" -ForegroundColor White
        exit 1
    }
    
    if (-not $qrBase64) {
        Write-Host "`n❌ QR Code não encontrado na resposta!" -ForegroundColor Red
        Write-Host "   Resposta salva em: debug_connect_response.json`n" -ForegroundColor Gray
        exit 1
    }
    
    # Garantir prefixo data:image
    if (-not $qrBase64.StartsWith("data:image")) {
        $qrBase64 = "data:image/png;base64,$qrBase64"
    }
    
    # ==========================================
    # PASSO 5: Criar HTML e monitorar conexão
    # ==========================================
    Write-Host "   ✓ Criando interface HTML...`n" -ForegroundColor Green
    
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>QR Code WhatsApp - $instanceName</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #25D366, #128C7E);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #128C7E;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .instance {
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        img {
            width: 300px;
            height: 300px;
            border: 3px solid #25D366;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .status {
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px;
            margin-top: 20px;
        }
        .status.wait {
            background: #FFF3CD;
            color: #856404;
        }
        .status.ok {
            background: #D4EDDA;
            color: #155724;
        }
        .status.error {
            background: #F8D7DA;
            color: #721C24;
        }
        .logs {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            max-height: 200px;
            overflow-y: auto;
            text-align: left;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        .log-entry {
            padding: 5px;
            border-bottom: 1px solid #dee2e6;
        }
        .log-entry:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 QR Code WhatsApp</h1>
        <div class="instance">Instância: $instanceName</div>
        
        <img src="$qrBase64" alt="QR Code WhatsApp">
        
        <div class="status wait" id="status">
            ⏳ Aguardando escaneamento...
        </div>
        
        <div class="logs" id="logs"></div>
    </div>
    
    <script>
        let checkCount = 0;
        const maxChecks = 90; // 90 segundos
        const logs = [];
        
        function addLog(msg, type = 'info') {
            const now = new Date().toLocaleTimeString();
            logs.push({ time: now, msg, type });
            
            const logsDiv = document.getElementById('logs');
            logsDiv.innerHTML = logs.slice(-10).map(l => 
                '<div class="log-entry">[' + l.time + '] ' + l.msg + '</div>'
            ).join('');
            logsDiv.scrollTop = logsDiv.scrollHeight;
        }
        
        async function checkConnection() {
            checkCount++;
            
            try {
                // Usar connectionState (mais confiável que fetchInstances)
                const res = await fetch('$baseUrl/instance/connectionState/$instanceName', {
                    headers: { 'apikey': '$apikey' }
                });
                const data = await res.json();
                
                const statusEl = document.getElementById('status');
                
                addLog('State: ' + data.state + (data.statusCode ? ' (code: ' + data.statusCode + ')' : ''));
                
                if (data.state === 'open') {
                    statusEl.className = 'status ok';
                    statusEl.innerHTML = '✅ CONECTADO COM SUCESSO!';
                    addLog('✅ Conexão estabelecida!', 'success');
                    clearInterval(intervalId);
                    
                    setTimeout(() => {
                        addLog('Fechando janela em 3s...');
                        setTimeout(() => window.close(), 3000);
                    }, 2000);
                    
                } else if (data.statusCode === 401) {
                    statusEl.className = 'status error';
                    statusEl.innerHTML = '❌ ERRO 401: Device Removed<br>Feche e execute o script novamente';
                    addLog('❌ ERRO 401: WhatsApp revogou a sessão', 'error');
                    clearInterval(intervalId);
                    
                } else {
                    statusEl.className = 'status wait';
                    statusEl.innerHTML = '⏳ Estado: ' + data.state + ' (' + checkCount + 's)';
                }
                
                if (checkCount >= maxChecks) {
                    clearInterval(intervalId);
                    statusEl.className = 'status error';
                    statusEl.innerHTML = '⏰ Tempo esgotado (90s)';
                    addLog('⏰ Timeout atingido', 'error');
                }
                
            } catch (err) {
                addLog('Erro: ' + err.message, 'error');
            }
        }
        
        addLog('Iniciando monitoramento...');
        const intervalId = setInterval(checkConnection, 1000);
        setTimeout(checkConnection, 100);
    </script>
</body>
</html>
"@
    
    $html | Out-File "qr_whatsapp_final.html" -Encoding UTF8
    Write-Host "✅ HTML criado: qr_whatsapp_final.html" -ForegroundColor Green
    Write-Host "🌐 Abrindo navegador...`n" -ForegroundColor Cyan
    
    Start-Process "qr_whatsapp_final.html"
    
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "📱 ESCANEIE O QR CODE AGORA!" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "⏰ Tempo máximo: 90 segundos" -ForegroundColor Gray
    Write-Host "🔄 A página monitora automaticamente" -ForegroundColor Gray
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
    
    Write-Host "💡 OBSERVAÇÕES IMPORTANTES:" -ForegroundColor Cyan
    Write-Host "   • Se aparecer erro 401 novamente = bug conhecido" -ForegroundColor White
    Write-Host "   • Nesse caso, reporte no GitHub Evolution API" -ForegroundColor White
    Write-Host "   • Anexe: debug_connect_response.json + logs`n" -ForegroundColor White
    
} catch {
    Write-Host "`n❌ Erro ao conectar:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host "`n📄 Detalhes:" -ForegroundColor Yellow
        $_.ErrorDetails.Message
    }
}

Write-Host "`n🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
