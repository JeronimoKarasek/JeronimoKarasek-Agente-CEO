# 🌐 GUIA DE ACESSO - AGENTE CEO

## 🚀 API REST

### 📍 URLs de Acesso

#### **1. Acesso Público (via Internet)**
```
http://103.199.187.127:8080
```

#### **2. Acesso Local (na própria máquina)**
```
http://localhost:8080
```

---

## 📋 ENDPOINTS DISPONÍVEIS

### ✅ **Health Check**
```bash
# Verificar se está funcionando
curl http://103.199.187.127:8080/health

# Ou no navegador:
http://103.199.187.127:8080/health
```

**Resposta esperada:**
```json
{"ok": true}
```

---

### 📊 **Métricas**

#### **Analytics**
```bash
curl http://103.199.187.127:8080/api/metrics/summary
```
```
http://103.199.187.127:8080/api/metrics/summary
```

#### **Prometheus**
```bash
curl http://103.199.187.127:8080/metrics
```
```
http://103.199.187.127:8080/metrics
```

---

### 🛠️ **Admin**

#### **Configurações**
```
GET http://103.199.187.127:8080/api/admin/config
```

#### **Status da Fila**
```
GET http://103.199.187.127:8080/api/admin/queue
```

#### **Alertas**
```
GET http://103.199.187.127:8080/api/admin/alerts
```

#### **Auditoria**
```
GET http://103.199.187.127:8080/api/admin/audit
```

---

### 🎯 **Operações**

#### **Scout de Produtos**
```bash
curl -X POST http://103.199.187.127:8080/api/run/scout \
  -H "Content-Type: application/json" \
  -d '{"search_term": "trending product"}'
```

#### **Gerar Criativos**
```bash
curl -X POST http://103.199.187.127:8080/api/run/creatives/PRODUCT_ID \
  -H "Content-Type: application/json"
```

#### **Lançar Campanha**
```bash
curl -X POST http://103.199.187.127:8080/api/ads/launch \
  -H "Content-Type: application/json" \
  -d '{"name": "Campanha Teste", "platform": "meta", "daily_budget": 50}'
```

---

## 🖥️ **DASHBOARD (Frontend)**

### **Opção 1: Via Navegador (File Protocol)**

1. **Baixe os arquivos do dashboard:**
   ```bash
   # Se estiver na máquina local, copie a pasta dashboard
   # Ou acesse via SFTP: dashboard/index.html
   ```

2. **Abra no navegador:**
   - Arraste `dashboard/index.html` para o navegador
   - Ou abra: `file:///caminho/para/dashboard/index.html`

### **Opção 2: Servidor HTTP Simples**

**Se tiver Python na sua máquina local:**
```bash
# Baixe a pasta dashboard primeiro
cd dashboard
python -m http.server 3000

# Acesse:
# http://localhost:3000
```

**Se tiver Node.js:**
```bash
cd dashboard
npx serve

# Acesse:
# http://localhost:3000
```

### **Opção 3: Servir via Nginx no servidor**

Posso configurar um servidor web simples se preferir!

---

## 🧪 **TESTANDO NO NAVEGADOR**

### **URLs Para Testar Diretamente:**

1. **Health Check:**
   ```
   http://103.199.187.127:8080/health
   ```

2. **Métricas:**
   ```
   http://103.199.187.127:8080/api/metrics/summary
   ```

3. **Config:**
   ```
   http://103.199.187.127:8080/api/admin/config
   ```

4. **Prometheus:**
   ```
   http://103.199.187.127:8080/metrics
   ```

---

## 🔧 **FERRAMENTAS ÚTEIS**

### **Postman / Insomnia**
Importe esta coleção:

```json
{
  "name": "Agente CEO API",
  "baseUrl": "http://103.199.187.127:8080",
  "endpoints": [
    {
      "name": "Health Check",
      "method": "GET",
      "url": "{{baseUrl}}/health"
    },
    {
      "name": "Metrics Summary",
      "method": "GET",
      "url": "{{baseUrl}}/api/metrics/summary"
    },
    {
      "name": "Scout Products",
      "method": "POST",
      "url": "{{baseUrl}}/api/run/scout",
      "body": {
        "search_term": "trending product"
      }
    }
  ]
}
```

### **cURL (Terminal)**
```bash
# Health Check
curl http://103.199.187.127:8080/health

# Métricas
curl http://103.199.187.127:8080/api/metrics/summary

# Scout
curl -X POST http://103.199.187.127:8080/api/run/scout \
  -H "Content-Type: application/json" \
  -d '{"search_term": "iPhone"}'
```

---

## 🔒 **SEGURANÇA**

### **Importante:**
A API está **ABERTA** na internet (porta 8080). Para produção:

1. **Adicione autenticação**
2. **Use HTTPS/SSL**
3. **Configure firewall**
4. **Use Nginx como reverse proxy**

---

## 📱 **ACESSANDO DE DISPOSITIVOS MÓVEIS**

No seu celular/tablet, acesse:
```
http://103.199.187.127:8080/health
```

---

## 🌐 **CONFIGURAR DOMÍNIO (Opcional)**

Se você tiver um domínio, pode configurar:

1. **DNS Record:**
   ```
   A record: api.seudominio.com -> 103.199.187.127
   ```

2. **Nginx Reverse Proxy:**
   ```bash
   # Posso ajudar a configurar se necessário!
   ```

---

## 📊 **MONITORAMENTO**

### **Ver logs em tempo real:**
```bash
# API
docker compose logs -f api

# Worker
docker compose logs -f worker

# Todos
docker compose logs -f
```

### **Status dos containers:**
```bash
docker compose ps
```

---

## 🎯 **TESTE RÁPIDO**

### **No seu navegador, acesse:**
```
http://103.199.187.127:8080/health
```

**Deve aparecer:**
```json
{"ok": true}
```

### **Teste via terminal:**
```bash
curl http://103.199.187.127:8080/health
```

---

## ✅ **CHECKLIST DE ACESSO**

- [x] API rodando na porta 8080
- [x] Acessível via IP público: `103.199.187.127`
- [x] Health check funcionando
- [x] Endpoints REST disponíveis
- [ ] Dashboard (precisa baixar os arquivos)
- [ ] HTTPS (opcional, para produção)

---

## 📞 **PRECISA DE AJUDA?**

### **Comandos úteis:**

```bash
# Parar a API
docker compose down

# Reiniciar
docker compose restart

# Ver status
docker compose ps

# Ver logs
docker compose logs -f api
```

---

**IP Público:** `103.199.187.127`  
**Porta:** `8080`  
**Status:** 🟢 **ONLINE E ACESSÍVEL!**

---

## 🎉 **RESUMO**

✅ **API está acessível de qualquer lugar:**
```
http://103.199.187.127:8080
```

✅ **Todos os endpoints funcionando**

✅ **Pronto para testes e desenvolvimento**

🚀 **Comece testando:** http://103.199.187.127:8080/health
