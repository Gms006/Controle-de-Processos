# Script para atualizar Evolution API com as correções
Write-Host "`n🔧 ATUALIZANDO EVOLUTION API`n" -ForegroundColor Cyan

Write-Host "📋 Alterações que serão aplicadas:" -ForegroundColor Yellow
Write-Host "   • Versão: v2.0.10 → v2.2.0 (Baileys mais novo)" -ForegroundColor White
Write-Host "   • Redis: Ativado completamente (TTL, save instances)" -ForegroundColor White
Write-Host "   • Cache: Otimizado para sessões WhatsApp`n" -ForegroundColor White

$confirm = Read-Host "Deseja continuar? (S/N)"
if ($confirm -ne "S" -and $confirm -ne "s") {
    Write-Host "❌ Cancelado pelo usuário" -ForegroundColor Red
    exit 0
}

Write-Host "`n🛑 Parando containers..." -ForegroundColor Yellow
cd 'C:\acessorias processos\evolution-api'
docker-compose down

Write-Host "`n🗑️  Limpando imagem antiga..." -ForegroundColor Yellow
docker rmi atendai/evolution-api:v2.0.10 -f 2>$null

Write-Host "`n⬇️  Baixando nova versão..." -ForegroundColor Yellow
docker pull atendai/evolution-api:v2.2.0

Write-Host "`n🚀 Iniciando containers atualizados..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "`n⏳ Aguardando inicialização" -NoNewline
Start-Sleep -Seconds 5
Write-Host "." -NoNewline
Start-Sleep -Seconds 5
Write-Host "." -NoNewline
Start-Sleep -Seconds 5
Write-Host ".`n" -NoNewline

Write-Host "`n✅ ATUALIZAÇÃO CONCLUÍDA!`n" -ForegroundColor Green

Write-Host "📊 Status dos containers:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎯 PRÓXIMO PASSO:" -ForegroundColor Yellow
Write-Host "   Execute: .\conectar_whatsapp_correto.ps1" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "🔹 Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
