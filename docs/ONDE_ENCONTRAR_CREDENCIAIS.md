# 🔑 GUIA: ONDE ENCONTRAR AS CREDENCIAIS DO WHATSAPP
## Meta for Developers - Passo a Passo

---

## 📍 INFORMAÇÕES NECESSÁRIAS

Precisamos de **4 credenciais** do Meta for Developers:

1. ✅ **WHATSAPP_VERIFY_TOKEN** - Você escolhe (qualquer texto)
2. 🔍 **WHATSAPP_APP_SECRET** - App Dashboard
3. 🔍 **WHATSAPP_ACCESS_TOKEN** - WhatsApp > API Setup
4. 🔍 **WHATSAPP_PHONE_NUMBER_ID** - WhatsApp > API Setup

---

## 🔍 ONDE ENCONTRAR CADA UM

### 1️⃣ WHATSAPP_VERIFY_TOKEN
**Você escolhe!** Pode ser qualquer texto, exemplo:
```
acessorias_gestor_2025_token_secreto
```

✅ **Já está configurado no .env**

---

### 2️⃣ WHATSAPP_APP_SECRET

**Caminho:**
```
Meta for Developers
└── Meus Apps (My Apps)
    └── [Seu App de WhatsApp]
        └── Settings (⚙️ Configurações)
            └── Basic (Básico)
                └── App Secret [Mostrar]
```

**Passo a passo:**
1. Acesse: https://developers.facebook.com/apps/
2. Clique no seu app
3. Menu lateral esquerdo → **⚙️ Settings** → **Basic**
4. Role a página até encontrar **App Secret**
5. Clique em **[Show]** (Mostrar)
6. Digite sua senha do Facebook
7. **Copie o código** (exemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Cole no .env:**
```env
WHATSAPP_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

### 3️⃣ WHATSAPP_ACCESS_TOKEN

**Caminho:**
```
Meta for Developers
└── Meus Apps
    └── [Seu App]
        └── WhatsApp
            └── API Setup (Configuração da API)
                └── Temporary access token [Copiar]
```

**Passo a passo:**

**Opção A: Token Temporário (24 horas) - Para Teste**
1. Acesse: https://developers.facebook.com/apps/
2. Clique no seu app
3. Menu lateral → **WhatsApp** → **API Setup**
4. Veja a seção **"Temporary access token"**
5. Clique em **[Copy]** (Copiar)
6. Cole no `.env`

**⚠️ Expira em 24 horas!**

**Opção B: Token Permanente (Recomendado para Produção)**
1. No mesmo app, vá em **⚙️ Settings** → **Business Settings**
2. No menu, clique em **System Users** (Usuários do Sistema)
3. Clique em **[Add]** → Crie um system user
   - Nome: "WhatsApp Gestor API"
   - Role: Admin
4. Clique no system user criado
5. Clique em **[Generate New Token]**
6. Selecione seu app
7. Marque as permissões:
   - ✅ `whatsapp_business_messaging`
   - ✅ `whatsapp_business_management`
8. Clique em **[Generate Token]**
9. **COPIE E SALVE** (só mostra uma vez!)

**Cole no .env:**
```env
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 4️⃣ WHATSAPP_PHONE_NUMBER_ID

**Caminho:**
```
Meta for Developers
└── Meus Apps
    └── [Seu App]
        └── WhatsApp
            └── API Setup
                └── From: Phone number ID [ao lado do número]
```

**Passo a passo:**
1. Mesmo caminho do Access Token
2. Menu lateral → **WhatsApp** → **API Setup**
3. Na seção **"From"**, você verá seu número de telefone
4. Logo abaixo ou ao lado está o **Phone number ID**
   - Exemplo: `123456789012345`
5. **Copie o número**

**Cole no .env:**
```env
WHATSAPP_PHONE_NUMBER_ID=123456789012345
```

---

### 5️⃣ SEU NÚMERO DE TELEFONE (Gestor Autorizado)

**O número que VAI USAR o sistema** (seu celular)

**Formato:** Internacional com + e código do país
- ✅ Correto: `+5511999999999`
- ❌ Errado: `11999999999` ou `(11) 99999-9999`

**Cole no .env:**
```env
GESTORES_AUTORIZADOS=+5511999999999
```

Se tiver mais de um gestor:
```env
GESTORES_AUTORIZADOS=+5511999999999,+5511888888888
```

---

## 📝 CHECKLIST - O QUE VOCÊ PRECISA ME FORNECER

```
[ ] 1. App Secret (32 caracteres)
[ ] 2. Access Token (começa com EAA...)
[ ] 3. Phone Number ID (15 dígitos)
[ ] 4. Seu número de telefone (+55...)
```

---

## 🎯 RESUMO: O QUE FAZER AGORA

### **Você precisa:**

1. **Abrir** https://developers.facebook.com/apps/
2. **Clicar** no seu app de WhatsApp
3. **Copiar 3 informações:**
   - App Secret (Settings > Basic)
   - Access Token (WhatsApp > API Setup)
   - Phone Number ID (WhatsApp > API Setup)
4. **Me informar:**
   - Essas 3 credenciais
   - Seu número de telefone

### **Eu vou:**
1. Atualizar o `.env` com suas credenciais
2. Integrar o webhook ao backend
3. Testar a conexão
4. Te ensinar a enviar o primeiro comando!

---

## 🖼️ REFERÊNCIA VISUAL

### Screenshot 1: App Secret
```
┌─────────────────────────────────────────────┐
│ Settings > Basic                            │
├─────────────────────────────────────────────┤
│ App ID: 1234567890                          │
│ Display Name: Meu App WhatsApp              │
│                                             │
│ App Secret: ••••••••••••••••• [Show]  ←──┐ │
│                                           │ │
└───────────────────────────────────────────┼─┘
                                            │
                                    Clique aqui!
```

### Screenshot 2: Access Token
```
┌─────────────────────────────────────────────┐
│ WhatsApp > API Setup                        │
├─────────────────────────────────────────────┤
│ Temporary access token                      │
│ ┌─────────────────────────────────────┐    │
│ │ EAAxxxxxxxxxxxxxxxxx... [Copy]  ←───┼────┤
│ └─────────────────────────────────────┘    │ Copie isso!
│                                             │
│ From:                                       │
│ ┌─────────────────────────────────────┐    │
│ │ +15550123456                        │    │
│ │ Phone number ID: 123456789012345 ←──┼────┤
│ └─────────────────────────────────────┘    │ E isso!
└─────────────────────────────────────────────┘
```

---

## 💬 ME ENVIE ASSIM:

```
App Secret: a1b2c3d4e5f6g7h8i9j0
Access Token: EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Phone Number ID: 123456789012345
Meu Telefone: +5511999999999
```

**Assim que você me passar, continuo a configuração!** 🚀

---

## 🔒 SEGURANÇA

⚠️ **NUNCA compartilhe essas credenciais publicamente!**
- App Secret e Access Token são como senhas
- Mantenha o `.env` privado
- Não commite no Git (já está no .gitignore)

---

## ❓ DÚVIDAS COMUNS

**P: Não encontro "WhatsApp" no menu lateral**
R: Certifique-se que adicionou o produto WhatsApp ao app

**P: Phone Number ID não aparece**
R: Verifique se o número está verificado e conectado ao app

**P: Access Token expirou**
R: Gere um token permanente (System Users)

**P: Posso usar número de teste?**
R: Sim! Meta fornece um número de teste gratuito

---

**Aguardando suas credenciais para continuar! 😊**
