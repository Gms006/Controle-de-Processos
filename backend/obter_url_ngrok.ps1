# Script para obter URL do ngrok
Write-Host "`n🔍 Procurando URL do ngrok..." -ForegroundColor Cyan

$maxTentativas = 15
$tentativa = 0
$encontrado = $false

while ($tentativa -lt $maxTentativas -and -not $encontrado) {
    $tentativa++
    Write-Host "   Tentativa $tentativa de $maxTentativas..." -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
        
        if ($response.tunnels -and $response.tunnels.Count -gt 0) {
            $httpsUrl = $response.tunnels | Where-Object { $_.proto -eq 'https' } | Select-Object -First 1
            
            if ($httpsUrl) {
                $url = $httpsUrl.public_url
                $encontrado = $true
                
                Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor Green
                Write-Host "  ✅ WEBHOOK PÚBLICO DISPONÍVEL!" -ForegroundColor Green  
                Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
                Write-Host ""
                Write-Host "📋 CALLBACK URL (copie exatamente):" -ForegroundColor Yellow
                Write-Host "$url/whatsapp/webhook/whatsapp" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "🔑 VERIFY TOKEN:" -ForegroundColor Yellow
                Write-Host "acessorias_gestor_2025_token_secreto" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
                Write-Host "  ⚙️  PRÓXIMO PASSO:" -ForegroundColor Yellow
                Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
                Write-Host ""
                Write-Host "1. Acesse: https://developers.facebook.com/apps/" -ForegroundColor White
                Write-Host "2. Clique no seu app WhatsApp" -ForegroundColor White
                Write-Host "3. WhatsApp → Configuration" -ForegroundColor White
                Write-Host "4. Webhook → Edit" -ForegroundColor White
                Write-Host "5. Cole a URL acima em 'Callback URL'" -ForegroundColor White
                Write-Host "6. Cole o token em 'Verify Token'" -ForegroundColor White
                Write-Host "7. Marque ✅ 'messages'" -ForegroundColor White
                Write-Host "8. Clique em 'Verify and Save'" -ForegroundColor White
                Write-Host ""
                Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
                Write-Host ""
                
                # Salvar em arquivo também
                $config = @"
WEBHOOK DO WHATSAPP - CONFIGURAÇÃO
==================================

Callback URL:
$url/whatsapp/webhook/whatsapp

Verify Token:
acessorias_gestor_2025_token_secreto

==================================
"@
                $config | Out-File -FilePath "webhook_config.txt" -Encoding UTF8
                Write-Host "💾 Configuração salva em: webhook_config.txt" -ForegroundColor Green
                Write-Host ""
            }
        }
    }
    catch {
        # Aguardar e tentar novamente
        Start-Sleep -Seconds 2
    }
}

if (-not $encontrado) {
    Write-Host "`n❌ Não foi possível conectar ao ngrok!" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Verifique se:" -ForegroundColor Yellow
    Write-Host "   1. A janela do ngrok está aberta" -ForegroundColor White
    Write-Host "   2. Você vê 'Session Status: online' no ngrok" -ForegroundColor White
    Write-Host "   3. Execute este script novamente" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Ou abra manualmente: http://localhost:4040" -ForegroundColor Cyan
    Write-Host ""
}
