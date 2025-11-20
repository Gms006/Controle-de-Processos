# Script para configurar webhook na instância já conectada
Write-Host "`n🔧 Configurando Webhook no WhatsApp conectado...`n" -ForegroundColor Cyan

try {
    # Configurar webhook
    $webhookBody = @{
        enabled = $true
        url = "http://localhost:8000/whatsapp/evolution/webhook"
        webhookByEvents = $false
        webhookBase64 = $false
        events = @(
            "QRCODE_UPDATED",
            "MESSAGES_UPSERT",
            "MESSAGES_UPDATE",
            "MESSAGES_DELETE",
            "SEND_MESSAGE",
            "CONNECTION_UPDATE"
        )
    } | ConvertTo-Json
    
    Write-Host "📡 Configurando webhook..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "http://localhost:8081/webhook/set/acessorias" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $webhookBody
    
    Write-Host "✅ Webhook configurado com sucesso!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 10
    
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "✅ CONFIGURAÇÃO COMPLETA!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
    
    Write-Host "📱 TESTE AGORA:" -ForegroundColor White
    Write-Host "   Envie '0' ou 'menu' para 62 99997-6999" -ForegroundColor Yellow
    Write-Host "   Deve responder com o menu de comandos!`n" -ForegroundColor Gray
    
} catch {
    Write-Host "`n❌ Erro ao configurar webhook:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
