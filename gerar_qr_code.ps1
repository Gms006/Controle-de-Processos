# Script para gerar QR Code e salvar em JSON automaticamente
Write-Host "🔐 Gerando QR Code WhatsApp para instância 'acessorias'..." -ForegroundColor Cyan

# Deletar instância antiga se existir
Write-Host "`n🗑️ Deletando instância antiga..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "http://localhost:8081/instance/delete/acessorias" -Method DELETE -Headers @{"apikey"="acessorias_evolution_key_2025"} | Out-Null
    Write-Host "✅ Instância antiga deletada" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ Nenhuma instância anterior encontrada" -ForegroundColor Gray
}

# Criar nova instância com QR Code
Write-Host "`n📱 Criando nova instância..." -ForegroundColor Yellow
$body = @{
  instanceName="acessorias"
  qrcode=$true
  integration="WHATSAPP-BAILEYS"
  webhook=@{
    url="http://localhost:8000/whatsapp/evolution/webhook"
    enabled=$true
    webhookByEvents=$false
    webhookBase64=$true
    events=@("QRCODE_UPDATED","CONNECTION_UPDATE","MESSAGES_UPSERT")
  }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8081/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $body
    
    # Verificar se tem QR Code
    if ($response.qrcode -and $response.qrcode.base64) {
        # Salvar apenas o objeto qrcode em JSON
        $response.qrcode | ConvertTo-Json -Depth 10 | Out-File -FilePath "qr code.json" -Encoding UTF8
        
        Write-Host "`n✅ QR Code gerado com sucesso!" -ForegroundColor Green
        Write-Host "📁 Arquivo salvo: qr code.json" -ForegroundColor Cyan
        Write-Host "`n🌐 Abra o arquivo 'qr code.html' no navegador para visualizar!" -ForegroundColor Yellow
        Write-Host "   O QR Code será carregado automaticamente." -ForegroundColor Gray
        
        # Abrir HTML automaticamente no navegador padrão
        Start-Process "qr code.html"
        
    } else {
        Write-Host "`n❌ Erro: QR Code não foi gerado na resposta" -ForegroundColor Red
        Write-Host "Resposta completa:" -ForegroundColor Gray
        $response | ConvertTo-Json -Depth 10
    }
    
} catch {
    Write-Host "`n❌ Erro ao criar instância:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`n✨ Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
