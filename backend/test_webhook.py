"""
Script de Teste - WhatsApp Webhook
Testa o webhook localmente sem encerrar o servidor
"""

import requests
import json

BASE_URL = "http://localhost:8000/whatsapp/webhook/whatsapp"

print("=" * 70)
print(" 🧪 TESTE DO WEBHOOK WHATSAPP")
print("=" * 70)

# ============ TESTE 1: Verificação (Meta) ============
print("\n1️⃣ Testando Verificação do Webhook...")
print("-" * 70)

try:
    response = requests.get(
        BASE_URL,
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "acessorias_gestor_2025_token_secreto",
            "hub.challenge": "TESTE_12345"
        }
    )
    
    if response.status_code == 200:
        print(f"✅ Verificação OK!")
        print(f"   Challenge retornado: {response.text}")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na conexão: {e}")

# ============ TESTE 2: Mensagem (Menu) ============
print("\n\n2️⃣ Testando Recebimento de Mensagem (Comando: Menu)...")
print("-" * 70)

payload = {
    "object": "whatsapp_business_account",
    "entry": [{
        "changes": [{
            "value": {
                "messages": [{
                    "from": "5562992731445",
                    "text": {
                        "body": "0"
                    }
                }]
            }
        }]
    }]
}

try:
    response = requests.post(
        BASE_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print(f"✅ Mensagem processada!")
        result = response.json()
        print(f"\n📩 Resposta gerada:")
        print(f"   Status: {result.get('status')}")
        if 'resposta' in result:
            print(f"\n{result['resposta']}")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na conexão: {e}")

# ============ TESTE 3: Resumo Geral ============
print("\n\n3️⃣ Testando Comando: Resumo Geral (KPIs)...")
print("-" * 70)

payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"] = "1"

try:
    response = requests.post(
        BASE_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print(f"✅ Comando executado!")
        result = response.json()
        if 'resposta' in result:
            print(f"\n📊 KPIs:")
            # Mostrar primeiras linhas
            lines = result['resposta'].split('\n')[:15]
            for line in lines:
                print(f"   {line}")
            print(f"\n   ... ({len(result['resposta'])} caracteres total)")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na conexão: {e}")

# ============ TESTE 4: Empresas sem Faturamento ============
print("\n\n4️⃣ Testando Comando: Empresas sem Faturamento...")
print("-" * 70)

payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"] = "4"

try:
    response = requests.post(
        BASE_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print(f"✅ Análise concluída!")
        result = response.json()
        if 'resposta' in result:
            lines = result['resposta'].split('\n')[:10]
            for line in lines:
                print(f"   {line}")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na conexão: {e}")

print("\n" + "=" * 70)
print(" ✅ TESTES CONCLUÍDOS!")
print("=" * 70)
print("\n💡 Próximo passo: Configurar ngrok para webhook público")
print("   ngrok http 8000")
print("=" * 70 + "\n")
