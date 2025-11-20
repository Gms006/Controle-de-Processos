# Configurar webhook - versão simplificada
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

Write-Host "Configurando webhook..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8081/webhook/set/acessorias" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $webhookBody
    Write-Host "✅ Sucesso!" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "❌ Erro:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Yellow
    $_.ErrorDetails.Message
}
