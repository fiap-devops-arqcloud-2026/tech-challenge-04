# PagerDuty: OAuth e integração de alertas

TL;DR: OAuth conecta um aplicativo/assistente à conta; a Integration Key conecta os alertas ao serviço. São cadastros separados. A integração PRTG existente passou no teste registrado pelo Claude; a troca por Events API V2 ainda depende de execução e validação.

Última atualização: 2026-11-03, Codex. Fontes oficiais consultadas nesta data; nenhuma alteração remota executada nesta orientação.

## 1. Entender as credenciais

| Campo | Para que serve |
|---|---|
| OAuth Client ID | Identifica o aplicativo registrado no PagerDuty. |
| OAuth Client Secret | Autentica esse aplicativo quando o fluxo exige segredo. Não é a senha de login. |
| Integration Key / routing_key | Permite enviar eventos à integração de um serviço. É a credencial usada no caminho de alertas do projeto. |

OAuth permite obter tokens para a REST API. O tipo de OAuth, os escopos e a URL de retorno precisam ser compatíveis com o cliente usado. [Fonte: OAuth Functionality](https://docs.pagerduty.com/developer/oauth-functionality).

## 2. Onde obter ID e segredo OAuth

1. No PagerDuty, abrir **Integrations → Developer Tools → App Registration**.
2. Em **My Apps**, abrir o aplicativo existente; se ainda não houver, usar **New App**, informando nome e descrição.
3. Na configuração, **Functionality → OAuth → Add**. Para configuração existente, usar **Manage**.
4. Configurar o tipo de OAuth e o retorno exigidos pelo cliente, salvar e guardar as credenciais emitidas.

App Registration exige papel-base Manager, Global Admin ou Account Owner. [Fonte: Register an App](https://docs.pagerduty.com/developer/register-an-app).

O segredo é apresentado no cadastro. Guardá-lo no gerenciador de senhas e preencher apenas a tela do conector. O `redirect_uri` precisa corresponder ao retorno registrado; não usar uma URL inventada. [Fonte: OAuth Functionality](https://docs.pagerduty.com/developer/oauth-functionality).

**[INCERTO]** O usuário ainda não identificou a tela que solicita as credenciais. Pergunta enviada: Claude/Claude Code, ChatGPT/Codex ou outro aplicativo. Falta esse dado para indicar callback, tipo e escopos concretos. Não é necessário resolver OAuth para preparar a Events API V2.

Caso seja MCP: o servidor hospedado aceita OAuth ou chave de API e não oferece cadastro dinâmico de clientes. Endpoint padrão: `https://mcp.pagerduty.com/mcp`; contas da região EU usam `https://mcp.eu.pagerduty.com/mcp`. O exemplo oficial específico do Claude Code usa callback local com porta fixa; não aplicar esse retorno a outros clientes. [Fonte: PagerDuty MCP Server](https://docs.pagerduty.com/ai-automation/advance/pagerduty-mcp-server).

## 3. Adicionar Events API V2 ao serviço existente

1. Abrir **Services → Service Directory → ToggleMaster Fase 4**.
2. Selecionar **Integrations → Add another integration**.
3. Buscar e selecionar **Events API V2**, depois **Add**.
4. Expandir a integração nova e copiar sua **Integration Key**.

É possível manter várias integrações no mesmo serviço. [Fonte: Services and Integrations](https://docs.pagerduty.com/incident-management/services/services-and-integrations).

Aplicação ao projeto: atualizar somente o valor de `PAGERDUTY_INTEGRATION_KEY` no `.env` local ignorado pelo Git. Não substituir por Client ID/Client Secret e não enviar a chave no chat. Este arquivo não foi aberto nem alterado pelo Codex nesta orientação.

Recomendação operacional: manter PRTG enquanto valida a integração nova; usar a mesma nova chave para trigger e resolve de um incidente de teste, conferir o cartão no Slack e registrar evidências. Só depois considerar retirar a integração antiga. Não excluir o serviço. A recomendação melhora a clareza do projeto; não estabelece exigência nem penalidade da FIAP.

## 4. Ponto de retomada

Fonte interna: [LOG](../LOG_DE_TRABALHO.md), entrada Claude de 2026-11-03 14:50, atualizada após consulta ao Slack; [backlog vigente](../PENDENCIAS_E_PROXIMOS_PASSOS.md).

- B0/B1 concluídos; cinco serviços, Service Map e trace New Relic conferidos pelo usuário.
- Integração atual: PRTG Notification For PagerDuty Events API v2. Trigger 14:40:27, cartão Slack 14:40:35, resolve 14:43:36 e atualização Resolved 14:43:41 (UTC-03:00). Isso confirma o 4.4 anterior, sem comprovar a futura chave genérica.
- B2 parcial. Código da falha proposital e testes preexistentes preservados; TODO(human) reservado ao usuário.
- Incoming Webhook direto do Slack ainda aguarda autorização para teste. O cartão do aplicativo PagerDuty é outro caminho.
- Nesta orientação não houve teste externo, evento, mensagem, configuração SaaS, commit/push ou operação AWS.

Guia anterior de contas: [PASSO2, seção 2.5](PASSO2_CONTAS_SAAS_2026-11-01_v01.md). Seus passos de teste precisam usar a chave da integração que se deseja validar.
