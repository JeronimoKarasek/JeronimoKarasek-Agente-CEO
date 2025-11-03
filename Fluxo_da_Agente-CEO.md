# 🤖 Fluxo Completo da Agente-CEO
## Sistema Autônomo de Marketing e Vendas

---

## 📋 Visão Geral

A **Agente-CEO** é um sistema autônomo que gerencia todo o ciclo de marketing digital, desde a descoberta de produtos até o escalonamento de campanhas lucrativas. Opera 24/7 sem intervenção humana.

---

## 🔄 Fluxo Principal

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIALIZAÇÃO DO SISTEMA                      │
│  - Carrega configurações do banco de dados                       │
│  - Valida credenciais (Meta, TikTok, Supabase)                  │
│  - Inicializa Workers em background                              │
│  - Configura scheduler para tarefas automáticas                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 1: SCOUT DE PRODUTOS                     │
│                                                                   │
│  1. Pesquisa automática em:                                      │
│     • Google Shopping API                                        │
│     • AliExpress Dropshipping Center                            │
│     • TikTok Trending Products                                   │
│     • Amazon Best Sellers                                        │
│                                                                   │
│  2. Critérios de seleção:                                        │
│     ✓ Alta demanda (volume de busca)                            │
│     ✓ Baixa concorrência                                         │
│     ✓ Margem de lucro > 40%                                      │
│     ✓ Tendência crescente                                        │
│     ✓ Adequado para dropshipping                                 │
│                                                                   │
│  3. Extração de dados:                                           │
│     • Título e descrição                                         │
│     • Preço fornecedor vs. mercado                              │
│     • Imagens do produto                                         │
│     • Reviews e avaliações                                       │
│     • Palavras-chave relevantes                                  │
│                                                                   │
│  4. Salva no banco: tabela `products`                            │
│     Status: 'scouted'                                            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASE 2: ANÁLISE E QUALIFICAÇÃO                      │
│                                                                   │
│  1. Guardrails - Validações de segurança:                       │
│     ✓ Produto não está em lista negra                           │
│     ✓ Categoria permitida                                        │
│     ✓ Margens realistas                                          │
│     ✓ Sem violação de direitos autorais                         │
│     ✓ Cumpre políticas Meta/TikTok                              │
│                                                                   │
│  2. Cálculo de score de viabilidade:                             │
│     • Potencial de conversão: 0-100                              │
│     • Competitividade: 0-100                                     │
│     • Margem esperada: %                                         │
│     • Score final: média ponderada                               │
│                                                                   │
│  3. Decisão:                                                     │
│     Se score >= 70 → Aprovado para criativos                    │
│     Se score < 70 → Descartado                                   │
│                                                                   │
│  4. Atualiza status: 'qualified' ou 'rejected'                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│            FASE 3: GERAÇÃO DE CRIATIVOS                          │
│                                                                   │
│  1. Para cada produto qualificado:                               │
│     • Gera 5-10 variações de anúncio                            │
│                                                                   │
│  2. Elementos dos criativos:                                     │
│     A) Copywriting (IA generativa):                              │
│        • Headlines (5 variações)                                 │
│        • Body text (3 estilos: informativo, urgência, social)   │
│        • Call-to-action (10 opções)                              │
│        • Pain points + soluções                                  │
│                                                                   │
│     B) Visuais:                                                  │
│        • Recorte de imagens do produto                           │
│        • Background removido (API)                               │
│        • Overlays de texto                                       │
│        • Badges (desconto, frete grátis, etc.)                  │
│                                                                   │
│     C) Vídeos (TikTok/Reels):                                    │
│        • Templates pré-definidos                                 │
│        • Transições automáticas                                  │
│        • Música trending                                         │
│        • Legendas geradas por IA                                 │
│                                                                   │
│  3. Upload para Supabase Storage:                                │
│     • Bucket: 'media'                                            │
│     • URLs públicas geradas                                      │
│                                                                   │
│  4. Salva metadados: tabela `creatives`                          │
│     • Vincula ao produto                                         │
│     • Armazena copy e URLs                                       │
│     Status: 'ready'                                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          FASE 4: CONFIGURAÇÃO DE CAMPANHAS                       │
│                                                                   │
│  1. Estrutura de campanha (Meta Ads):                            │
│     • Campanha → Ad Set → Ads                                    │
│                                                                   │
│  2. Configurações automáticas:                                   │
│     Nível Campanha:                                              │
│     • Objetivo: CONVERSÕES                                       │
│     • Otimização: COMPRAS                                        │
│     • Budget: $50/dia (inicial)                                  │
│                                                                   │
│     Nível Ad Set:                                                │
│     • Público: Broad (18-65, todos os gêneros)                  │
│     • Países: BR, US (configurável)                              │
│     • Placements: Advantage+ (automático)                        │
│     • Pixel: Rastreamento instalado                              │
│                                                                   │
│     Nível Ad:                                                    │
│     • Criativo gerado na Fase 3                                  │
│     • Página de destino: Loja Shopify/WooCommerce              │
│     • UTM params para tracking                                   │
│                                                                   │
│  3. Configuração TikTok Ads (paralelo):                          │
│     • Mesma estrutura adaptada                                   │
│     • Foco em vídeos UGC-style                                   │
│     • Budget menor: $20/dia inicial                              │
│                                                                   │
│  4. Modo de operação:                                            │
│     • DRY_RUN = true: Apenas simula                             │
│     • AUTO_MODE = true: Publica automaticamente                  │
│     • APPROVAL_MODE = true: Aguarda aprovação                    │
│                                                                   │
│  5. Salva no banco: tabelas `campaigns`, `ad_sets`, `ads`        │
│     Status: 'draft' ou 'active'                                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│            FASE 5: PUBLICAÇÃO E ATIVAÇÃO                         │
│                                                                   │
│  1. Fila de publicação (Redis):                                  │
│     • Enfileira todas as campanhas aprovadas                     │
│     • Worker processa em background                              │
│                                                                   │
│  2. Chamadas API:                                                │
│     Meta Ads:                                                    │
│     POST /v18.0/act_{ad_account}/campaigns                       │
│     POST /v18.0/act_{ad_account}/adsets                          │
│     POST /v18.0/act_{ad_account}/ads                             │
│                                                                   │
│     TikTok Ads:                                                  │
│     POST /v1.3/campaign/create/                                  │
│     POST /v1.3/adgroup/create/                                   │
│     POST /v1.3/ad/create/                                        │
│                                                                   │
│  3. Tratamento de erros:                                         │
│     • Retry automático (3 tentativas)                            │
│     • Exponential backoff                                        │
│     • Log em audit_log                                           │
│     • Alert se falha crítica                                     │
│                                                                   │
│  4. Confirmação:                                                 │
│     • Captura campaign_id, ad_set_id, ad_id                     │
│     • Atualiza banco com IDs externos                            │
│     Status: 'active' ou 'error'                                  │
│                                                                   │
│  5. Notificação:                                                 │
│     • Webhook para CRM                                           │
│     • Log de auditoria                                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          FASE 6: MONITORAMENTO E COLETA DE DADOS                 │
│                                                                   │
│  Executa a cada 1 hora (scheduler):                              │
│                                                                   │
│  1. Coleta métricas das plataformas:                             │
│     Meta Ads:                                                    │
│     GET /v18.0/{campaign_id}/insights                            │
│     • Impressões                                                 │
│     • Cliques (CTR)                                              │
│     • CPC (custo por clique)                                     │
│     • Conversões                                                 │
│     • Custo total                                                │
│     • ROAS (Return on Ad Spend)                                  │
│                                                                   │
│     TikTok Ads:                                                  │
│     GET /v1.3/reports/integrated/get/                            │
│     • Mesmas métricas                                            │
│                                                                   │
│  2. Salva em: tabela `analytics`                                 │
│     • Timestamp                                                  │
│     • Métricas por campanha/ad_set/ad                           │
│     • Agregações diárias                                         │
│                                                                   │
│  3. Cálculos automáticos:                                        │
│     • ROAS = (Receita / Custo)                                   │
│     • CTR = (Cliques / Impressões) * 100                        │
│     • CVR = (Conversões / Cliques) * 100                        │
│     • CPA = Custo / Conversões                                   │
│     • AOV = Receita / Conversões                                 │
│                                                                   │
│  4. Views materializadas:                                        │
│     • mv_campaign_performance                                    │
│     • mv_daily_metrics                                           │
│     Refresh automático a cada hora                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│       FASE 7: ANÁLISE E TOMADA DE DECISÃO (IA)                   │
│                                                                   │
│  Executa a cada 6 horas:                                         │
│                                                                   │
│  1. Para cada campanha ativa:                                    │
│                                                                   │
│     A) Análise de performance:                                   │
│        Período de teste: 24-48h                                  │
│        Mínimo de dados: 1000 impressões                          │
│                                                                   │
│        Critérios de sucesso:                                     │
│        ✓ ROAS >= TARGET_ROAS (1.5)                              │
│        ✓ CTR >= 1.5%                                             │
│        ✓ CVR >= 2%                                               │
│        ✓ CPA <= AOV * 0.4                                        │
│                                                                   │
│     B) Classificação:                                            │
│        🟢 Winner: Todas métricas OK                              │
│        🟡 Potential: Algumas métricas OK                         │
│        🔴 Loser: Nenhuma métrica OK                              │
│                                                                   │
│  2. Ações automáticas:                                           │
│                                                                   │
│     Para Winners (🟢):                                            │
│     • Aumenta budget em 20-30%                                   │
│     • Expande públicos (lookalike)                               │
│     • Testa novos placements                                     │
│     • Duplica ad sets vencedores                                 │
│     Status: 'scaling'                                            │
│                                                                   │
│     Para Potentials (🟡):                                         │
│     • Mantém budget atual                                        │
│     • Ajusta targeting (reduz ou expande)                        │
│     • Testa novos criativos                                      │
│     • Aguarda mais dados (24h)                                   │
│     Status: 'testing'                                            │
│                                                                   │
│     Para Losers (🔴):                                             │
│     • Pausa campanha imediatamente                               │
│     • Marca criativo como 'failed'                               │
│     • Atualiza blacklist (evita repetir erro)                   │
│     Status: 'paused'                                             │
│                                                                   │
│  3. Guardrails de segurança:                                     │
│     • Limite diário: SAFE_BUDGET_CAP_DAILY ($300)               │
│     • Limite semanal: SAFE_BUDGET_CAP_WEEKLY ($1500)            │
│     • Se ultrapassar: pausa todas campanhas                      │
│     • Alert crítico enviado                                      │
│                                                                   │
│  4. Registro de decisões:                                        │
│     Tabela: `audit_log`                                          │
│     • Timestamp                                                  │
│     • Ação tomada                                                │
│     • Justificativa (métricas)                                   │
│     • Resultado esperado                                         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          FASE 8: ESCALONAMENTO INTELIGENTE                       │
│                                                                   │
│  Aplica-se apenas a campanhas 'scaling':                         │
│                                                                   │
│  1. Estratégias de escalonamento:                                │
│                                                                   │
│     A) Vertical Scaling (aumento gradual):                       │
│        • +20% budget a cada 48h                                  │
│        • Máximo: 3x o budget inicial                             │
│        • Monitoramento constante do ROAS                         │
│        • Se ROAS cair >20%: volta ao budget anterior            │
│                                                                   │
│     B) Horizontal Scaling (duplicação):                          │
│        • Cria cópias do ad set vencedor                         │
│        • Testa novos públicos:                                   │
│          - Lookalike 1% (baseado em compradores)                │
│          - Lookalike 2-3%                                        │
│          - Interesse relacionados                                │
│        • Budget inicial: 50% do original                         │
│                                                                   │
│     C) Creative Testing Contínuo:                                │
│        • Introduz novo criativo a cada 72h                       │
│        • Mantém top 3 performers ativos                          │
│        • Desativa bottom 50% após 48h                            │
│                                                                   │
│  2. Otimização de bid:                                           │
│     • Inicia com Lowest Cost                                     │
│     • Após estabilizar: Cost Cap                                 │
│     • Target: CPA = AOV * 0.3                                    │
│                                                                   │
│  3. Expansão geográfica:                                         │
│     • Testa novos países/estados                                 │
│     • Critérios: idioma, poder aquisitivo, logística            │
│                                                                   │
│  4. Multi-plataforma:                                            │
│     • Se Meta ROAS > 2.0: expande para TikTok                   │
│     • Se TikTok ROAS > 2.0: expande para Google                 │
│     • Alocação de budget proporcional ao ROAS                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│        FASE 9: INTEGRAÇÃO COM CRM E FULFILLMENT                  │
│                                                                   │
│  1. Webhook de conversões:                                       │
│     • Pixel envia evento de compra                               │
│     • Sistema recebe via /api/webhooks/meta                      │
│     • Valida assinatura HMAC                                     │
│                                                                   │
│  2. Criação de pedido:                                           │
│     Tabela: `orders`                                             │
│     • Dados do cliente                                           │
│     • Produto(s) comprado(s)                                     │
│     • Valor total                                                │
│     • UTM params (campanha origem)                               │
│     Status: 'pending'                                            │
│                                                                   │
│  3. Integração com fornecedor:                                   │
│     • API do AliExpress/CJ Dropshipping                         │
│     • Cria pedido automaticamente                                │
│     • Tracking code gerado                                       │
│                                                                   │
│  4. Notificação ao cliente:                                      │
│     • Email de confirmação                                       │
│     • SMS com tracking (opcional)                                │
│     • WhatsApp via API                                           │
│                                                                   │
│  5. Atualização de métricas:                                     │
│     • Vincula receita à campanha                                 │
│     • Recalcula ROAS em tempo real                               │
│     • Atualiza LTV do cliente                                    │
│                                                                   │
│  6. CRM automation:                                              │
│     • Adiciona lead ao funil                                     │
│     • Marca tags baseado em produto                              │
│     • Inicia sequência de emails                                 │
│     • Upsell/cross-sell automático                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│            FASE 10: RELATÓRIOS E INSIGHTS                        │
│                                                                   │
│  Gerado diariamente às 00:00 UTC:                                │
│                                                                   │
│  1. Consolidação de dados:                                       │
│     View: mv_daily_metrics                                       │
│     • Total de impressões                                        │
│     • Total de cliques                                           │
│     • Total gasto                                                │
│     • Total de receita                                           │
│     • ROAS geral                                                 │
│     • Novos produtos testados                                    │
│     • Campanhas ativas                                           │
│                                                                   │
│  2. Análise por produto:                                         │
│     • Top 10 produtos por receita                                │
│     • Bottom 5 produtos (candidatos a descarte)                  │
│     • Produtos em fase de teste                                  │
│     • Margem de lucro por produto                                │
│                                                                   │
│  3. Análise por campanha:                                        │
│     • Top performers                                             │
│     • Campanhas em scaling                                       │
│     • Campanhas pausadas                                         │
│     • Budget utilizado vs. alocado                               │
│                                                                   │
│  4. Alertas automáticos:                                         │
│     Tabela: `alerts`                                             │
│     • Orçamento > 80% do limite                                  │
│     • ROAS geral < TARGET                                        │
│     • Nenhuma conversão em 24h                                   │
│     • Falha em API externa                                       │
│     • Produto fora de estoque                                    │
│                                                                   │
│  5. Dashboard em tempo real:                                     │
│     • WebSocket para updates live                                │
│     • Gráficos de performance                                    │
│     • Fila de tarefas                                            │
│     • Status do sistema                                          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              CICLO CONTÍNUO - LOOP INFINITO                      │
│                                                                   │
│  O sistema opera em loop contínuo:                               │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  A cada 24h: SCOUT → Novos produtos                  │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Imediatamente: QUALIFICA → Análise                  │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Em 2h: CRIATIVOS → Geração                          │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Em 30min: PUBLICA → Campanhas live                  │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  A cada 1h: MONITORA → Coleta dados                  │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  A cada 6h: DECIDE → Pausa/Escala/Mantém            │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Contínuo: ESCALA → Winners aumentam                 │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Quando ocorre: FULFILLMENT → Processa pedidos      │       │
│  └──────────────────────────────────────────────────────┘       │
│                           ↓                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Diário 00:00: RELATA → Dashboard atualizado         │       │
│  └──────────────────────────────────────────────────────┘       │
│                           │                                       │
│                           └───────► VOLTA AO INÍCIO               │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

---

## 🏗️ Arquitetura Técnica

### Componentes Principais:

```
┌─────────────────────────────────────────────────────────┐
│                   DASHBOARD WEB                          │
│  • Interface de monitoramento                            │
│  • Configuração de credenciais                           │
│  • Visualização de métricas                              │
│  • Controle manual (opcional)                            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/WebSocket
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   API FastAPI                            │
│  Endpoints:                                              │
│  • /api/run/scout - Inicia scout                         │
│  • /api/run/creatives/{id} - Gera criativos             │
│  • /api/admin/config - Configurações                     │
│  • /api/metrics/summary - Métricas                       │
│  • /api/webhooks/meta - Recebe conversões               │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌──────────┐
    │  REDIS  │ │SUPABASE │ │ WORKERS  │
    │  Queue  │ │PostgreSQL│ │Background│
    └─────────┘ └─────────┘ └──────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌──────────┐
    │ META    │ │ TIKTOK  │ │ STORAGE  │
    │ ADS API │ │ ADS API │ │ Supabase │
    └─────────┘ └─────────┘ └──────────┘
```

### Tecnologias:

- **Backend**: Python 3.12, FastAPI, asyncio
- **Banco de Dados**: PostgreSQL (Supabase) com Row Level Security
- **Cache/Queue**: Redis para filas de tarefas
- **Storage**: Supabase Storage para mídia
- **Orquestração**: Docker Compose
- **Monitoramento**: Prometheus + logs estruturados
- **Frontend**: HTML5, Tailwind CSS, Vanilla JS

---

## 🔒 Segurança e Governança

### Guardrails Implementados:

1. **Financeiro**:
   - Budget cap diário e semanal
   - Pausa automática se exceder
   - Aprovação para gastos > threshold

2. **Compliance**:
   - Validação de políticas de anúncios
   - Blacklist de produtos proibidos
   - Verificação de direitos autorais

3. **Qualidade**:
   - Mínimo de dados antes de decisão
   - Período de teste obrigatório
   - Rollback automático se performance cair

4. **Operacional**:
   - Rate limiting em APIs externas
   - Retry com exponential backoff
   - Circuit breaker para falhas
   - Idempotência em operações críticas

---

## 📊 KPIs Monitorados

### Principais Métricas:

| Métrica | Target | Ação se Below Target |
|---------|--------|---------------------|
| ROAS    | ≥ 1.5  | Pausa campanha |
| CTR     | ≥ 1.5% | Testa novo criativo |
| CVR     | ≥ 2%   | Otimiza landing page |
| CPA     | ≤ $30  | Ajusta público |
| AOV     | ≥ $50  | Upsell/bundling |

### Frequência de Análise:

- **Tempo Real**: Conversões, custos acumulados
- **Horária**: Métricas de campanha
- **6 em 6 horas**: Decisões de scaling/pausa
- **Diária**: Relatórios consolidados
- **Semanal**: Análise estratégica

---

## 🎯 Resultados Esperados

### Performance Típica (após otimização):

- **ROAS médio**: 2.5x - 4.0x
- **Taxa de aprovação de produtos**: 30-40%
- **Campanhas ativas simultâneas**: 15-25
- **Conversões diárias**: 10-50 (depende do budget)
- **Tempo de break-even**: 3-7 dias por produto

### Autonomia:

- **100% automático** em modo AUTO_MODE
- **0 intervenção humana** necessária após setup
- **24/7 operação** contínua
- **Auto-scaling** baseado em performance
- **Auto-healing** de erros recuperáveis

---

## 🚨 Alertas e Notificações

Sistema de alertas automáticos para:

- ⚠️ Budget próximo do limite (80%)
- 🔴 ROAS abaixo do target por 24h
- ❌ Falha em API externa (3+ tentativas)
- ⏸️ Campanha pausada automaticamente
- 🎉 Novo winner encontrado
- 💰 Conversão acima da média
- 📦 Produto fora de estoque

Canais de notificação:
- Dashboard em tempo real
- Tabela `alerts` no banco
- (Futuro) Email, Slack, Telegram

---

## 🔄 Manutenção e Evolução

### Tarefas Automáticas:

- **Limpeza de dados antigos**: Purga logs > 90 dias
- **Refresh de views**: Materializa métricas agregadas
- **Backup**: Snapshot diário do banco
- **Health checks**: Valida conexões a cada 5 min

### Ciclo de Melhoria:

1. **Coleta de dados** contínua
2. **Análise mensal** de padrões
3. **Ajuste de parâmetros** (targets, timings)
4. **A/B testing** de estratégias
5. **Machine Learning** (futuro) para predição

---

## 📞 Suporte e Documentação

- **Código fonte**: GitHub - JeronimoKarasek/Agente-CEO
- **API Docs**: http://103.199.187.127:8080/docs
- **Dashboard**: http://mkt.farolbase.com
- **Logs**: `docker compose logs -f`
- **Guias**: Ver repositório /docs

---

## ✅ Checklist de Operação

### Setup Inicial:
- [ ] Configurar credenciais (Supabase, Meta, TikTok)
- [ ] Aplicar migrations SQL
- [ ] Definir budget caps
- [ ] Configurar modo (AUTO/APPROVAL/DRY_RUN)
- [ ] Validar conexões

### Operação Diária:
- [ ] Verificar dashboard ao iniciar o dia
- [ ] Revisar alertas
- [ ] Confirmar budget restante
- [ ] Checar campanhas em scaling
- [ ] Validar novos winners

### Manutenção Semanal:
- [ ] Analisar relatório semanal
- [ ] Ajustar targets se necessário
- [ ] Adicionar produtos à blacklist
- [ ] Revisar margem de lucro real
- [ ] Backup manual (extra segurança)

---

**Versão**: 1.0.0  
**Data**: 03/11/2025  
**Autor**: Sistema Agente-CEO  
**Status**: Produção

---

*Este documento descreve o fluxo completo do sistema autônomo de marketing Agente-CEO. Para detalhes técnicos de implementação, consulte o código fonte no repositório.*
