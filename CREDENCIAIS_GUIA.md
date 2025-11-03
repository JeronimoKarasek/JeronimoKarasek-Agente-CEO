# 🔑 Guia Completo de Credenciais - Agente-CEO

## 📝 Índice
1. [Supabase](#supabase)
2. [Meta/Facebook Ads](#metafacebook-ads)
3. [TikTok Ads](#tiktok-ads)
4. [Instagram Business](#instagram-business)

---

## 🗄️ Supabase

### 1. Supabase URL
**Onde encontrar:**
1. Acesse: https://supabase.com/dashboard
2. Entre no seu projeto
3. Vá em **Settings** → **API**
4. Copie a **Project URL**

**Formato:** `https://xxxxxxxxxx.supabase.co`

### 2. Supabase Anon Key
**Onde encontrar:**
1. Mesma página: **Settings** → **API**
2. Procure por **Project API keys**
3. Copie a chave **anon** / **public**

**Formato:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...`

### 3. Supabase Service Key (Opcional - Cuidado!)
**Onde encontrar:**
1. Mesma página: **Settings** → **API**
2. Clique em **Reveal** ao lado de **service_role key**
3. ⚠️ **ATENÇÃO**: Esta chave tem acesso total ao banco!

**Formato:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...`

---

## 📘 Meta/Facebook Ads

### 1. Meta Access Token
**Onde obter:**

#### Opção A - Graph API Explorer (Desenvolvimento)
1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu **App** no canto superior direito
3. Clique em **Get User Access Token** ou **Get App Token**
4. Selecione as permissões:
   - ✅ `ads_management`
   - ✅ `ads_read`
   - ✅ `business_management`
   - ✅ `pages_read_engagement`
   - ✅ `instagram_basic`
   - ✅ `instagram_content_publish`
5. Clique em **Generate Access Token**
6. Copie o token gerado

#### Opção B - App Dashboard (Produção)
1. Acesse: https://developers.facebook.com/apps/
2. Entre no seu aplicativo
3. Vá em **Tools** → **Access Token Tool**
4. Ou use o Marketing API para gerar um token de longa duração

**Formato:** `EAAx...` (começa com EAA)

**⏱️ Validade:**
- Token de curta duração: 1 hora
- Token de longa duração: 60 dias
- Token de página/sistema: Não expira (recomendado)

#### Como obter Token de Longa Duração:
```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=SEU_TOKEN_CURTO"
```

### 2. Meta Ad Account ID
**Onde encontrar:**
1. Acesse: https://business.facebook.com/settings/ad-accounts
2. Selecione sua conta de anúncios
3. O ID aparece na URL ou na página de configurações

**Formato:** `act_123456789` (começa com "act_")

### 3. Meta Pixel ID
**Onde encontrar:**
1. Acesse: https://business.facebook.com/events_manager2
2. Selecione seu Pixel
3. Clique em **Settings** no menu lateral
4. O **Pixel ID** está no topo

**Formato:** `123456789012345` (número de 15 dígitos)

### 4. Meta App ID (Opcional)
**Onde encontrar:**
1. Acesse: https://developers.facebook.com/apps/
2. Entre no seu aplicativo
3. O **App ID** está no topo da página

**Formato:** `123456789012345`

### 5. Meta App Secret (Opcional)
**Onde encontrar:**
1. No dashboard do app
2. Vá em **Settings** → **Basic**
3. Clique em **Show** ao lado de **App Secret**
4. ⚠️ **Nunca compartilhe este valor!**

**Formato:** Sequência alfanumérica de 32 caracteres

---

## 📸 Instagram Business

### Instagram Business Account ID
**Onde encontrar:**

#### Método 1 - Facebook Business Manager
1. Acesse: https://business.facebook.com/settings/instagram-accounts
2. Selecione sua conta Instagram Business
3. O ID numérico aparece na configuração

#### Método 2 - Graph API
1. Use o Graph API Explorer: https://developers.facebook.com/tools/explorer/
2. Com seu access token, faça a requisição:
```
GET /me/accounts
```
3. Depois, para cada página:
```
GET /{page-id}?fields=instagram_business_account
```
4. Copie o ID retornado

**Formato:** `17841400000000000` (número de 17 dígitos começando com 17841)

---

## 🎵 TikTok Ads

### 1. TikTok Access Token
**Onde obter:**
1. Acesse: https://ads.tiktok.com/marketing_api/
2. Entre em **Tools** → **Authorization**
3. Crie um novo token com permissões:
   - ✅ Campaign Management
   - ✅ Ad Management
   - ✅ Reporting
4. Copie o access token gerado

**Formato:** String longa alfanumérica

**⏱️ Validade:** Tokens TikTok normalmente expiram em 24 horas

### 2. TikTok Advertiser ID
**Onde encontrar:**
1. Acesse: https://ads.tiktok.com/i18n/
2. Entre no seu Ads Manager
3. O Advertiser ID aparece na URL: `...advertiser_id=1234567890`
4. Ou em **Settings** → **Advertiser Account**

**Formato:** `1234567890123456789` (número de 19 dígitos)

### 3. TikTok Pixel ID
**Onde encontrar:**
1. No TikTok Ads Manager
2. Vá em **Assets** → **Events**
3. Selecione seu Pixel
4. O Pixel ID está nas configurações

**Formato:** `C9X...` (começa com C9X)

---

## 🎯 Passo a Passo de Configuração

### 1️⃣ Acesse o Dashboard
```
http://mkt.farolbase.com/index_complete.html
```

### 2️⃣ Vá para Configuração
- Clique na aba **⚙️ Configuração**

### 3️⃣ Preencha as Credenciais
Siga este checklist:

#### ✅ Obrigatório (Mínimo para funcionar)
- [ ] Supabase URL
- [ ] Supabase Anon Key
- [ ] Meta Access Token
- [ ] Meta Ad Account ID

#### 🔶 Recomendado (Para funcionalidades completas)
- [ ] Meta Pixel ID
- [ ] Instagram Business Account ID

#### 🔷 Opcional (Recursos avançados)
- [ ] TikTok Access Token
- [ ] TikTok Advertiser ID
- [ ] Supabase Service Key

### 4️⃣ Configure os Modos
- **Modo Automático**: ✅ Ativado (sistema roda sozinho)
- **Modo Aprovação**: ❌ Desativado (não precisa aprovar cada ação)
- **Dry Run**: ✅ Ativado (recomendado para primeiro teste!)
- **Target ROAS**: `1.5` (retorno de 1.5x sobre investimento)
- **Budget Cap Diário**: `300` USD
- **Budget Cap Semanal**: `1500` USD

### 5️⃣ Salve e Teste
1. Clique em **💾 Salvar Configurações**
2. Clique em **🔌 Testar Conexão**
3. Aguarde confirmação: **✅ Conexão OK!**

---

## 🔐 Segurança

### ⚠️ Importante:
1. **NUNCA** compartilhe seus tokens com ninguém
2. **NUNCA** commite tokens no Git
3. Use **Dry Run Mode** para testar primeiro
4. Monitore seus gastos regularmente
5. Revogue tokens antigos quando não usar mais

### 🛡️ Proteção no Sistema:
- Tokens são armazenados criptografados no banco
- API mascara credenciais sensíveis ao exibir
- Row Level Security habilitado
- Audit log de todas as mudanças

---

## 📞 Suporte e Documentação Oficial

### Meta/Facebook
- Documentação: https://developers.facebook.com/docs/marketing-apis
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Business Manager: https://business.facebook.com/

### TikTok
- Marketing API: https://ads.tiktok.com/marketing_api/docs
- Ads Manager: https://ads.tiktok.com/

### Supabase
- Dashboard: https://supabase.com/dashboard
- Documentação: https://supabase.com/docs

---

## 🎬 Próximos Passos

Após configurar tudo:

1. ✅ Salve as configurações
2. ✅ Teste a conexão
3. ✅ Vá para **🚀 Operações**
4. ✅ Execute um **Scout de Produtos** com termo de busca
5. ✅ Monitore os resultados em **📈 Monitoramento**
6. ✅ Verifique logs em **📋 Logs**

**Pronto! Seu Agente-CEO está configurado! 🎉**
