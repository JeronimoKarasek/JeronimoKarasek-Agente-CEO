# 🎯 Guia de Configuração - Dashboard Agente-CEO

## 📋 Passo a Passo

### 1️⃣ Acessar o Dashboard

Abra no navegador: **http://mkt.farolbase.com/index_complete.html**

### 2️⃣ Configurar Credenciais

Clique na aba **⚙️ Configuração** e preencha:

#### 🗄️ Supabase
```
Supabase URL: https://seu-projeto.supabase.co
Supabase Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 📘 Meta/Facebook Ads
```
Access Token: Obtido em https://developers.facebook.com/tools/explorer/
Ad Account ID: act_123456789
Pixel ID: 123456789
Instagram Business Account ID: 17841...
```

#### 🎵 TikTok Ads (Opcional)
```
Access Token: Da sua conta TikTok Ads
Advertiser ID: ID do anunciante
Pixel ID: ID do pixel
```

#### 🎛️ Configurações da Aplicação
- **Modo Automático**: Sistema roda sozinho
- **Modo Aprovação**: Requer aprovação manual
- **Dry Run**: Apenas simula (recomendado para testes)
- **Target ROAS**: 1.5 (retorno sobre investimento)
- **Budget Cap Diário**: 300 USD
- **Budget Cap Semanal**: 1500 USD

#### 🔗 API URL
```
URL Base: http://103.199.187.127:8080/api
```

### 3️⃣ Salvar e Testar

1. Clique em **💾 Salvar Configurações**
2. Clique em **🔌 Testar Conexão**
3. Aguarde confirmação: "✅ Conexão OK!"

### 4️⃣ Usar o Dashboard

#### 📊 Dashboard (Painel Principal)
- Visualiza métricas em tempo real
- Receita do dia
- Tarefas na fila
- Status do sistema

#### 🚀 Operações
- **Scout de Produtos**: Busca produtos trending
- **Gerar Criativos**: Cria variações de anúncios

#### 📈 Monitoramento
- Status da fila
- Métricas do sistema
- Alertas recentes

#### 📋 Logs
- Histórico de ações
- Auditoria

## 🔑 Obtendo Credenciais

### Meta/Facebook Access Token
1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu aplicativo
3. Gere um token com permissões:
   - `ads_management`
   - `ads_read`
   - `business_management`
4. Copie o token

### Ad Account ID
1. Acesse: https://business.facebook.com/settings/ad-accounts
2. Copie o ID da conta (formato: act_123456789)

### Instagram Business Account ID
1. Acesse: https://business.facebook.com/settings/instagram-accounts
2. Copie o ID numérico (formato: 17841...)

## ⚠️ Importante

- **Todas as configurações são salvas no navegador (localStorage)**
- **Não compartilhe seus tokens com ninguém**
- **Use Dry Run Mode para testar antes de rodar em produção**
- **Monitore os custos regularmente**

## 🆘 Problemas Comuns

### "Erro na conexão"
- Verifique se a API está rodando: http://103.199.187.127:8080/health
- Confirme que a URL base está correta

### "Token inválido"
- Regenere o token no Facebook Developers
- Verifique as permissões necessárias

### "Página em branco"
- Certifique-se de acessar `/index_complete.html`
- Limpe o cache do navegador (Ctrl+Shift+Del)

## 📞 Suporte

Em caso de dúvidas, verifique:
1. Logs no terminal: `docker-compose logs -f api`
2. Console do navegador (F12)
3. Arquivo GUIA_ACESSO.md

---

✅ **Dashboard pronto para uso!**
