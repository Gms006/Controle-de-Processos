# Script de conexão WhatsApp usando CÓDIGO DE PAREAMENTO
Write-Host "`n🔄 Conexão via CÓDIGO DE PAREAMENTO`n" -ForegroundColor Cyan

# PASSO 1: Deletar instância antiga
Write-Host "🗑️  Deletando instância antiga..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "http://localhost:8081/instance/delete/acessorias" -Method DELETE -Headers @{"apikey"="acessorias_evolution_key_2025"} | Out-Null
    Write-Host "   ✓ Instância deletada" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "   ℹ️  Nenhuma instância anterior" -ForegroundColor Gray
}

# PASSO 2: Criar instância com pairing code
Write-Host "`n📱 Gerando código de pareamento..." -ForegroundColor Yellow
try {
    $body = @{
        instanceName = "acessorias"
        number = "5562999976999"  # Número com DDI (sem espaços, hífens ou parênteses)
        integration = "WHATSAPP-BAILEYS"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8081/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $body
    
    if ($response.pairingCode) {
        Write-Host "`n✅ CÓDIGO DE PAREAMENTO GERADO!`n" -ForegroundColor Green
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
        Write-Host "   CÓDIGO: $($response.pairingCode)" -ForegroundColor Yellow -BackgroundColor Black
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
        
        Write-Host "📱 COMO CONECTAR:" -ForegroundColor White
        Write-Host ""
        Write-Host "1️⃣  Abra o WhatsApp Business no celular" -ForegroundColor Gray
        Write-Host "2️⃣  Toque em ⋮ (três pontos) → Aparelhos conectados" -ForegroundColor Gray
        Write-Host "3️⃣  Toque em 'Conectar aparelho'" -ForegroundColor Gray
        Write-Host "4️⃣  Escolha 'Conectar com número de telefone'" -ForegroundColor Gray
        Write-Host "5️⃣  Digite o código: $($response.pairingCode)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "⏰ Você tem 3 MINUTOS para usar este código!" -ForegroundColor Red
        Write-Host ""
    } else {
        Write-Host "`n❌ Erro: Não foi possível gerar o código" -ForegroundColor Red
        $response | ConvertTo-Json -Depth 10
    }
    
} catch {
    Write-Host "`n❌ Erro ao criar instância:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`n🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
