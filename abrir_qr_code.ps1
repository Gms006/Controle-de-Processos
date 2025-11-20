# Script para abrir QR Code com servidor HTTP local
Write-Host "🌐 Iniciando servidor HTTP local..." -ForegroundColor Cyan

# Verificar se Python está disponível
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    
    # Iniciar servidor HTTP na porta 8888
    Write-Host "✅ Servidor iniciado em: http://localhost:8888/qr%20code.html" -ForegroundColor Green
    Write-Host "📱 O QR Code será carregado automaticamente!" -ForegroundColor Yellow
    Write-Host "`n🔴 Pressione Ctrl+C para parar o servidor`n" -ForegroundColor Red
    
    # Abrir navegador
    Start-Sleep -Seconds 1
    Start-Process "http://localhost:8888/qr%20code.html"
    
    # Iniciar servidor
    python -m http.server 8888
    
} catch {
    Write-Host "❌ Python não encontrado. Abrindo arquivo diretamente..." -ForegroundColor Yellow
    Start-Process "qr code.html"
    Write-Host "`n💡 INSTRUÇÕES:" -ForegroundColor Cyan
    Write-Host "1. Abra o arquivo 'qr code.json'" -ForegroundColor White
    Write-Host "2. Selecione todo o conteúdo (Ctrl+A)" -ForegroundColor White
    Write-Host "3. Copie (Ctrl+C)" -ForegroundColor White
    Write-Host "4. Cole no campo do HTML e clique em 'Mostrar QR Code'" -ForegroundColor White
}
