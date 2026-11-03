# Passo 2 — New Relic, PagerDuty e Slack

**TL;DR**

- **O que sai deste passo:** três segredos guardados no seu gerenciador de senhas. Nenhum deles vai para o repositório.
  - `NEW_RELIC_LICENSE_KEY`: chave do tipo Ingest - License, dedicada ao Collector.
  - `PAGERDUTY_INTEGRATION_KEY`: Integration Key da integração Events API V2 do serviço "ToggleMaster Fase 4".
  - `SLACK_WEBHOOK_URL`: URL do Incoming Webhook do canal `#incidentes-tech-challenge`.
  - Os nomes acima são sugestões de rótulo. Os nomes finais das variáveis serão definidos no B1 e no B4.
- **Testes que provam que tudo funciona:**
  1. Um log de teste aparece na tela Logs do New Relic.
  2. Um incidente abre no PagerDuty (com push e e-mail) e depois é resolvido.
  3. Uma mensagem chega ao canal do Slack pelo webhook.
  4. O mesmo incidente do PagerDuty aparece como cartão no canal do Slack.
- **Tempo estimado:** de 1h30 a 2h. É uma estimativa, não uma medição.
- **Data de consulta das fontes:** 2026-11-01.

---

## Antes de começar: regras

### 1. Segredos não saem do gerenciador de senhas

- Nunca cole uma chave ou URL secreta no chat, em print, em vídeo, em issue ou no Git.
- Guarde cada segredo **só no gerenciador de senhas**, logo depois de copiar.
- Hoje você **não** cria nem edita arquivos do repositório. O `.env` fica para o B1.
- Depois de colar um segredo no gerenciador, apague o conteúdo da área de transferência. Se o histórico do Windows estiver ligado (`Win+V`), apague o item de lá também.
- As telas de chaves (API keys do New Relic, aba Integrations do PagerDuty, página do app no Slack) mostram os segredos. Não grave essas telas e não tire print delas.

### 2. Abrir o programa certo

1. Menu Iniciar > digite `Windows PowerShell` > abra **Windows PowerShell** (ícone azul).
2. Não use o **Windows PowerShell ISE**: nele, o `Read-Host -AsSecureString` abre uma caixa de diálogo.
3. Não use o **PowerShell 7** (`pwsh`).
4. Cole cada bloco de comando **inteiro** no console (`Ctrl+V` ou botão direito do mouse) e tecle Enter.
5. Não salve os comandos num arquivo `.ps1`. A política de execução padrão pode bloquear scripts, e o PowerShell 5.1 pode corromper acentos.
6. Quando o comando pedir uma chave, cole com `Ctrl+V` ou com o botão direito. Na tela aparecem só asteriscos. Depois tecle Enter.

Confira a versão e o protocolo TLS:

```powershell
$PSVersionTable.PSVersion.ToString()
[Net.ServicePointManager]::SecurityProtocol
```

Resposta esperada:

```
5.1.26100.xxxx
SystemDefault
```

- A primeira linha deve começar com `5.1`.
- `SystemDefault` significa que o Windows 11 escolhe entre TLS 1.2 e TLS 1.3. Por isso, os comandos deste guia só forçam TLS 1.2 se a sessão **não** estiver em `SystemDefault`. A Microsoft recomenda não fixar a versão do TLS.
- Fonte: https://learn.microsoft.com/en-us/dotnet/framework/network-programming/tls

### 3. Trial do PagerDuty

- O trial dura 14 dias. Pelos Termos, no fim do trial o serviço para, a menos que você assine, escolha o plano Free ou o PagerDuty estenda o trial.
- A conta foi criada em 2026-10-28, então o fim estimado é por volta de **2026-11-11**. A data exata precisa ser conferida na conta (Parte 2, passo 1).
- O vídeo da demonstração deve ser gravado antes dessa data.
- Fonte: https://www.pagerduty.com/terms-of-service/

---

## Parte 1 — New Relic: license key

### 1.1 Confirmar a região US

1. Faça login e olhe a barra de endereço.
2. Você deve ver um endereço começando com `https://one.newrelic.com/`. Isso indica conta US.
   - Se aparecer `one.eu.newrelic.com`, a conta é da região EU. Nesse caso, pare e me avise: os endpoints mudam e os comandos deste guia não servem.
3. A região é definida na criação da organização, e o New Relic não transfere dados entre regiões.

Fonte: https://docs.newrelic.com/docs/accounts/accounts-billing/account-setup/choose-your-data-center/

### 1.2 Anotar o Account ID

1. Caminho: menu do usuário (nome ou avatar) > **Administration** > **Access management** > **Accounts**. Se você tiver mais de uma conta, o ID também aparece no seletor de contas, no topo da tela.
2. Você deve ver um número inteiro.
3. Anote esse número no gerenciador de senhas, junto com a chave que você vai criar.
4. O Account ID não autentica nada. Mesmo assim, por decisão do projeto, ele fica fora de código público.
5. Confira que a conta selecionada é a mesma em que você vai criar a chave e procurar os logs.

Fonte: https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/

### 1.3 Criar uma license key dedicada

O New Relic tem vários tipos de chave. Para enviar dados, use **Ingest - License**. A **User key** serve para consulta e configuração, não para envio de dados. Não crie User key agora.

Fonte: https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/

1. Abra `https://one.newrelic.com/api-keys`. Também dá para chegar pelo menu do usuário > **API keys**.
2. Clique em **Create a key**.
3. Preencha:
   - Key type: **Ingest - License**
   - Nome: `tc04-otel-collector-local`
   - Descrição (opcional): `Tech Challenge Fase 4 - Collector local - criada 2026-11-01`. [INCERTO] O rótulo exato desse campo na tela não foi confirmado.
4. Clique em **Save**.
5. **Cuidado:** a chave inteira aparece só por um tempo. Copie nessa hora (ou use o menu `...` > **Copy key** na linha da chave) e cole direto no gerenciador de senhas com o rótulo `NEW_RELIC_LICENSE_KEY`.

**O que você deve ver:** uma nova linha do tipo Ingest - License com o nome `tc04-otel-collector-local`. A chave tem 40 caracteres.

- [INCERTO] O formato da chave não é consistente na documentação: uma página diz "40-character hexadecimal" e outra diz que a chave termina em `NRAL`. O que vale é o resultado do teste.

**Cuidados:**

- Depois da criação, a tela mostra só os 8 primeiros caracteres. Se você não guardou a chave a tempo, apague essa chave (`...` > **Delete**) e crie outra. É mais simples do que recuperar a chave pela NerdGraph.
- Use a chave dedicada, não a "original" da conta. A original não pode ser apagada pela interface; trocá-la exige o suporte.
- Se a chave vazar: crie uma nova, atualize o gerenciador e apague a antiga com `...` > **Delete**. Para bloquear sem apagar, use `...` > **Deactivate key**.

Fonte: https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/

### 1.4 Testar a chave (Log API US)

O comando envia um log de teste. A chave é lida sem aparecer na tela e é apagada da memória no final.

```powershell
if ([Net.ServicePointManager]::SecurityProtocol -ne [Net.SecurityProtocolType]::SystemDefault) { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 }
$sec = Read-Host -AsSecureString "Cole a New Relic INGEST - LICENSE key (nao aparece na tela)"
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try { $nrKey = ([Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)).Trim() } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
"Chave lida ($($nrKey.Length) caracteres)."
$body = @{ timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds(); message = "tc04 teste da license key 2026-11-01"; logtype = "tc04-teste"; service = "tc04-setup"; hostname = "tc04-local" } | ConvertTo-Json -Compress
try {
  $r = Invoke-WebRequest -UseBasicParsing -Method Post -Uri "https://log-api.newrelic.com/log/v1" -Headers @{ "Api-Key" = $nrKey } -ContentType "application/json" -Body $body
  "HTTP $($r.StatusCode)"; $r.Content
} catch {
  if ($_.Exception.Response) { "Falhou: HTTP $([int]$_.Exception.Response.StatusCode)" } else { "Falhou sem resposta HTTP (rede/DNS/proxy/TLS): $($_.Exception.Message)" }
  if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message }
} finally {
  Remove-Variable nrKey, sec, bstr, body, r -ErrorAction SilentlyContinue
}
```

Resposta esperada:

```
Chave lida (40 caracteres).
HTTP 202
{"requestId":"..."}
```

Como ler o resultado:

- **Sucesso:** qualquer código 2xx.
  - [INCERTO] A página oficial da Log API não documenta o código nem o corpo de sucesso. O `202` com `requestId` está documentado só para a Metric API. A prova real é o log aparecer na tela (passo 1.5).
- **`Falhou: HTTP 403`:** chave errada ou de tipo errado.
  - [INCERTO] O 403 está documentado para a Event API, não para a Log API.
- **`Falhou: HTTP 429`:** limite de taxa. Espere os segundos indicados no header `Retry-After` e tente de novo.
- **`Falhou sem resposta HTTP`:** problema de rede, DNS, proxy ou TLS. Não é problema da chave.
- [INCERTO] Este comando não foi executado com chave real. A sintaxe foi conferida no PowerShell 5.1.

Fontes: https://docs.newrelic.com/docs/logs/log-api/introduction-log-api/ e https://docs.newrelic.com/docs/data-apis/ingest-apis/metric-api/report-metrics-metric-api/

### 1.5 Ver o log chegando

1. Vá em one.newrelic.com > **All capabilities** > **Logs**. Se a navegação estiver personalizada, use **Browse data** > **Logs**.
2. Na busca, digite `logtype:"tc04-teste"`. Outra opção: clique no botão **NRQL**, ao lado da busca, e cole a consulta abaixo.

```text
SELECT timestamp, message, service, hostname FROM Log WHERE logtype = 'tc04-teste' SINCE 30 minutes ago
```

**O que você deve ver:** em 1 a 2 minutos, pelo menos uma linha com a mensagem `tc04 teste da license key 2026-11-01`. Isso prova que a chave, a conta e a região estão certas.

Se o comando deu 2xx mas nada aparece em 5 minutos, rode esta consulta de diagnóstico:

```text
SELECT * FROM NrIntegrationError WHERE newRelicFeature = 'Logs' SINCE 1 hour ago
```

O ideal é nenhum resultado. Se aparecerem linhas, o campo `message` explica o motivo do erro.

Fontes: https://docs.newrelic.com/docs/logs/ui-data/use-logs-ui/, https://docs.newrelic.com/docs/logs/ui-data/query-syntax-logs/ e https://docs.newrelic.com/docs/data-apis/manage-data/nrintegrationerror/

---

## Parte 2 — PagerDuty: serviço, integração, notificações e teste

### 2.1 Conferir papel, plano e trial

1. Caminho: ícone do usuário (canto superior direito) > **Subscriptions** > aba **Your Subscription** > cartão **Subscription Details**.
2. Você deve ver Current Plan, Plan Period e Renewal date.
3. Confirme que você é o Account Owner. Só ele vê o faturamento.
4. Anote a data de fim do trial, se ela aparecer na tela, e me diga.
   - [INCERTO] A documentação não diz onde aparece a data exata de fim do trial.
5. **Não clique em Upgrade Plan.** Esse botão abre o fluxo de compra.

Fonte: https://docs.pagerduty.com/account-admin/billing

### 2.2 Escolher a política de escalonamento

1. Caminho: **People** > **Escalation Policies**.
2. Se existir a política **Default**, criada no onboarding do trial, com você no nível 1, use essa.
3. Ignore a **Default Mobilization EP**. Ela é vazia e interna, então não aciona ninguém.
4. Se nenhuma política tiver você no nível 1, crie uma no passo 2.3 com **Generate a new escalation policy**.
5. Não crie políticas extras: o plano Free permite só 1 escalation policy.
   - [INCERTO] A documentação não diz se a Default Mobilization EP conta nesse limite.

Fontes: https://docs.pagerduty.com/get-started/trial-account-onboarding e https://docs.pagerduty.com/incident-management/schedules/escalation-policies

### 2.3 Criar o serviço "ToggleMaster Fase 4"

1. Caminho: **Services** > **Service Directory** > **New Service**.
2. Name: `ToggleMaster Fase 4`. Description: `Alertas do Grafana do Tech Challenge Fase 4`. Clique em **Next**.
3. Escolha **Select an existing escalation policy** e selecione a política do passo 2.2. Se não houver uma adequada, escolha **Generate a new escalation policy**. Clique em **Next**.
4. Se aparecer a etapa de agrupamento de alertas (Alert Grouping), escolha **Turn Off Alert Grouping** e clique em **Next**. Sem o AIOps, essa etapa nem aparece.
5. Em Integrations, clique em **Create service without an integration**. É o caminho sugerido pela documentação do Grafana. A integração entra no passo 2.5.
6. Clique em **Create Service**.

**O que você deve ver:** o serviço listado em Service Directory.

Fontes: https://docs.pagerduty.com/incident-management/services/services-and-integrations e https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/pager-duty/

### 2.4 Conferir a urgência

1. Caminho: serviço **ToggleMaster Fase 4** > aba **Settings** > **Edit** ao lado de **Assign and Notify**.
2. Deixe **High-urgency notifications, escalate as needed**, que é o padrão.
3. Deixe desmarcadas as opções de auto-resolução e de re-trigger. As duas já vêm desligadas.
4. Salve só se tiver mudado algo.

A resolução do incidente deve vir do evento `resolve` (enviado pelo Grafana ou pelo self-healing), não da auto-resolução do PagerDuty.

Fonte: https://docs.pagerduty.com/incident-management/services/configurable-service-settings

### 2.5 Adicionar a integração Events API V2 e copiar a chave

1. Caminho: serviço > aba **Integrations** > **Add another integration** > selecione **Events API V2** > **Add**.
2. Clique à direita da linha da integração para ver a **Integration Key**, que tem 32 caracteres.
3. Copie a chave e cole direto no gerenciador de senhas com o rótulo `PAGERDUTY_INTEGRATION_KEY`.
4. Confira que a integração listada é **Events API V2**.

**Cuidados:**

- Quem tiver essa chave consegue abrir incidentes no seu serviço.
- A aba Integrations exibe a chave: não grave essa tela e não tire print dela.
- [INCERTO] A documentação não descreve como trocar a chave. Se ela vazar, o caminho provável é apagar a integração e criar outra, mas isso não está documentado.

Fonte: https://docs.pagerduty.com/incident-management/services/services-and-integrations

### 2.6 Cadastrar e-mail e app no celular

1. Caminho: ícone do usuário > **My Profile** > aba **Contact Information**.
2. Confira o e-mail. Se precisar de outro, use **Add Email Address**, escolha Work ou Home e clique em **Save**.
3. Instale o app PagerDuty no celular e faça login. O aparelho é registrado para receber push no login.
4. Volte à aba **Contact Information** e confira que o aparelho aparece **sem** a marcação `Expired`.

**Cuidados:**

- Se aparecer `Expired`, remova o aparelho e faça login de novo no app.
- O app exige iOS 17+ ou Android 12+ hoje. A partir de **2026-11-16**, as novas versões exigem iOS 18+ ou Android 13+.
- SMS e voz são opcionais. No Free, são 100 por mês.

Fontes: https://docs.pagerduty.com/account-admin/user-profile/contact-information, https://docs.pagerduty.com/get-started/mobile-app e https://docs.pagerduty.com/account-admin/billing

### 2.7 Regras de notificação (o PagerDuty "aciona o time")

1. Caminho: **My Profile** > aba **Notification Rules**.
2. Em **High urgency incident notifications**, clique em `+` e crie:
   - uma regra com **0 minutos** para o push do app;
   - uma regra com **1 minuto** para o e-mail.
3. Clique em **Save** em cada regra.
4. Em **Low urgency incident notifications**, crie uma regra com **0 minutos** para e-mail ou push.

**O que você deve ver:** num incidente, o push chega na hora. O e-mail chega cerca de 1 minuto depois, se ninguém tiver dado ack.

**Cuidado:** o push de baixa urgência é silencioso por padrão no app.

Fontes: https://docs.pagerduty.com/account-admin/user-profile/notification-rules e https://support.pagerduty.com/docs/mobile-app-settings

### 2.8 Teste manual: trigger, acknowledge e resolve

Use **a mesma janela** do PowerShell do começo ao fim desta seção. Se você fechar a janela, perde a chave e o `dedup_key`, e o resolve deixa de funcionar.

**Comando 1: ler a chave**

```powershell
if ([Net.ServicePointManager]::SecurityProtocol -ne [Net.SecurityProtocolType]::SystemDefault) { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 }
$pdUrl = "https://events.pagerduty.com/v2/enqueue"
$sec = Read-Host -AsSecureString -Prompt "Cole a Integration Key do servico ToggleMaster Fase 4 (nao aparece na tela)"
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try { $pdKey = ([Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)).Trim() } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
if ($pdKey.Length -ne 32) { Write-Warning "A chave tem $($pdKey.Length) caracteres; o esperado sao 32. Confira se copiou a Integration Key inteira." } else { "Chave lida (32 caracteres)." }
```

Resposta esperada:

```
Chave lida (32 caracteres).
```

**Comando 2: trigger (abre o incidente)**

```powershell
$dedup = "togglemaster-teste-" + (Get-Date -Format "yyyyMMdd-HHmmss")
$evento = @{
  routing_key  = $pdKey
  event_action = "trigger"
  dedup_key    = $dedup
  payload      = @{
    summary        = "[TESTE] ToggleMaster Fase 4 - alerta manual via Events API v2"
    source         = "togglemaster-local"
    severity       = "critical"
    component      = "flag-service"
    group          = "togglemaster"
    class          = "teste-manual"
    custom_details = @{ origem = "PowerShell 5.1"; objetivo = "validar PagerDuty e Slack" }
  }
}
$json = $evento | ConvertTo-Json -Depth 5
try {
  $resp = Invoke-WebRequest -Uri $pdUrl -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  "HTTP $($resp.StatusCode)"; $resp.Content; "dedup_key usado: $dedup"
} catch {
  if ($_.Exception.Response) { "HTTP $([int]$_.Exception.Response.StatusCode)" }
  if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
}
```

Resposta esperada:

```
HTTP 202
{"status":"success","message":"Event processed","dedup_key":"togglemaster-teste-AAAAMMDD-HHMMSS"}
dedup_key usado: togglemaster-teste-AAAAMMDD-HHMMSS
```

Onde conferir:

- No PagerDuty web, menu **Incidents**: um incidente com status **Triggered** no serviço ToggleMaster Fase 4.
- O push no celular e, cerca de 1 minuto depois, o e-mail. Olhe também a pasta de spam.
- Anote o horário de cada um.

**Comando 3 (opcional): acknowledge, com o mesmo dedup_key**

```powershell
$evento = @{ routing_key = $pdKey; event_action = "acknowledge"; dedup_key = $dedup }
$json = $evento | ConvertTo-Json -Depth 3
try {
  $resp = Invoke-WebRequest -Uri $pdUrl -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  "HTTP $($resp.StatusCode)"; $resp.Content
} catch {
  if ($_.Exception.Response) { "HTTP $([int]$_.Exception.Response.StatusCode)" }
  if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
}
```

Resposta esperada: `HTTP 202` com `"status":"success"`. No PagerDuty, o incidente passa para **Acknowledged**.

**Comando 4: resolve, com o mesmo dedup_key**

```powershell
$evento = @{ routing_key = $pdKey; event_action = "resolve"; dedup_key = $dedup }
$json = $evento | ConvertTo-Json -Depth 3
try {
  $resp = Invoke-WebRequest -Uri $pdUrl -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($json)) -UseBasicParsing
  "HTTP $($resp.StatusCode)"; $resp.Content
} catch {
  if ($_.Exception.Response) { "HTTP $([int]$_.Exception.Response.StatusCode)" }
  if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
}
```

Resposta esperada: `HTTP 202` com `"status":"success"` e o mesmo `dedup_key`. No PagerDuty, o incidente passa para **Resolved** (veja em Incidents com o filtro Resolved).

**Comando 5: limpeza**

Se você vai fazer a Parte 4 agora, pule este comando e rode no final.

```powershell
Remove-Variable -Name pdKey, pdUrl, sec, bstr, evento, json, resp, dedup -ErrorAction SilentlyContinue
"Variaveis removidas. Feche esta janela do PowerShell."
```

Resposta esperada:

```
Variaveis removidas. Feche esta janela do PowerShell.
```

**Como ler os códigos de erro:**

- **HTTP 400:** JSON ou campos inválidos. Não repita o comando; corrija primeiro.
- **HTTP 429 ou 5xx:** espere alguns minutos e repita.
- **Mensagem sem HTTP:** erro de rede ou de TLS.

**Cuidados:**

- Nunca deixe incidente de teste aberto: sempre feche com o resolve.
- Os comandos foram testados contra um servidor local simulado, não contra o PagerDuty. [INCERTO] O corpo exato de um HTTP 400 do PagerDuty não foi confirmado.
- [INCERTO] A leitura com `Read-Host -AsSecureString` foi validada só pelo analisador de sintaxe. A primeira execução confirma que funciona.

Fontes: https://docs.pagerduty.com/developer/send-alert-event, https://docs.pagerduty.com/developer/api/reference/events-v2/send-event/create-v2-event, https://docs.pagerduty.com/developer/events-api-v2-overview e https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-5.1

---

## Parte 3 — Slack: canal, Incoming Webhook e teste

### 3.1 Criar o canal

1. Na barra lateral do Slack, clique em `+` > **Channel**.
2. Nome: `incidentes-tech-challenge`. Deixe como **Public** e clique em **Create**.
3. Não use o `#general`: o webhook pode falhar com o erro `posting_to_general_channel_denied`.

Fontes: https://slack.com/help/articles/201402297-Create-a-channel e https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/

### 3.2 Criar o app em branco

1. Abra https://api.slack.com/apps, com a mesma conta do workspace.
2. Clique em **Create an app** ou **Create New App**.
3. Escolha a opção em branco: **From scratch** ou **Blank app** (nesse caso, clique em **Continue**).
   - [INCERTO] Os rótulos variam entre as versões da documentação.
4. App Name: `grafana-alertas-tc4`. Selecione o workspace do projeto e clique em **Create** ou **Create App**.
5. Não use "From a manifest" nem a Slack CLI.

**O que você deve ver:** a página do app aberta em **Basic Information**.

Fonte: https://docs.slack.dev/app-management/quickstart-app-settings/

### 3.3 Ativar o webhook e gerar a URL

1. No menu do app: **Features** > **Incoming Webhooks** > ligue **Activate Incoming Webhooks** (On).
2. Clique em **Add New Webhook to Workspace**.
3. Escolha `#incidentes-tech-challenge` e clique em **Allow** ou **Authorize**. Essa autorização é sua, feita conscientemente.
4. Na seção **Webhook URLs for Your Workspace**, aparece uma linha nova com o botão **Copy**. A URL tem o formato `https://hooks.slack.com/services/...`.
5. Clique em **Copy** e cole direto no gerenciador de senhas com o rótulo `SLACK_WEBHOOK_URL`.

**Cuidados:**

- A URL é o próprio segredo: quem tiver a URL consegue postar no canal.
- O Slack procura segredos vazados e revoga os que encontra.
- A página do app continua mostrando a URL. Não grave essa tela.
- Se o botão virar um pedido de aprovação, a aprovação de apps foi ligada no workspace (o padrão é desligado). Como Owner, você aprova o pedido.
  - [INCERTO] A documentação não detalha a tela de aprovação.

Fontes: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/ e https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace

### 3.4 Testar o webhook

```powershell
if ([Net.ServicePointManager]::SecurityProtocol -ne [Net.SecurityProtocolType]::SystemDefault) { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 }
$sec = Read-Host -AsSecureString 'Cole a URL do Incoming Webhook do Slack (nao aparece na tela)'
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try { $url = ([Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)).Trim() } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
if ($url -notlike 'https://hooks.slack.com/services/*') { Write-Warning 'A URL nao comeca com https://hooks.slack.com/services/ - confira se copiou inteira.' }
$payload = @{ text = ('Teste manual do webhook - Tech Challenge Fase 4 - ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')) } | ConvertTo-Json -Compress
$bytes = [Text.Encoding]::UTF8.GetBytes($payload)
try {
  $r = Invoke-RestMethod -Uri $url -Method Post -ContentType 'application/json; charset=utf-8' -Body $bytes -TimeoutSec 30
  Write-Host ('Resposta: ' + $r)
} catch {
  if ($_.Exception.Response) { Write-Host ('HTTP: ' + [int]$_.Exception.Response.StatusCode) }
  Write-Host ('Erro: ' + $_.ErrorDetails.Message)
  Write-Host ('Detalhe: ' + $_.Exception.Message)
} finally {
  Remove-Variable url, sec, bstr, payload, bytes, r -ErrorAction SilentlyContinue
}
```

Resposta esperada:

```
Resposta: ok
```

**Onde conferir:** no canal `#incidentes-tech-challenge` aparece a mensagem `Teste manual do webhook - Tech Challenge Fase 4 - <data e hora>`, com o nome do app.

**Erros mais comuns:**

| Erro | HTTP | O que fazer |
|---|---|---|
| `invalid_payload` | 400 | JSON malformado. Corrija antes de repetir. |
| `channel_not_found` | 404 | Canal inválido. Corrija antes de repetir. |
| `action_prohibited` | 403 | Um admin restringiu. Não repita. |
| `channel_is_archived` | 410 | O canal foi arquivado. |
| `no_service` / `no_active_hooks` | [INCERTO] não documentado | Webhook removido, desativado ou URL cortada. |
| (limite de taxa) | 429 | Espere o tempo do header `Retry-After`. |

[INCERTO] A página oficial do `Invoke-RestMethod` não documenta como o PowerShell 5.1 preenche `$_.ErrorDetails.Message`. É a prática comum, e por isso o comando também mostra `$_.Exception.Message`.

Fontes: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/, https://docs.slack.dev/changelog/2016-05-17-changes-to-errors-for-incoming-webhooks, https://docs.slack.dev/apis/web-api/rate-limits/ e https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1

---

## Parte 4 — Ligar o PagerDuty ao Slack e repetir o teste

### 4.1 Instalar o app do PagerDuty no Slack

1. No PagerDuty: **Integrations** > **Extensions** > tile **Slack**. Se aparecer, clique em **Authorize Integration**.
2. Clique em **Add Workspace**.
3. Na tela do Slack, confira que o workspace certo está selecionado e clique em **Allow**. Isso concede permissões OAuth ao PagerDuty; faça você mesmo, conscientemente.
4. De volta ao PagerDuty, se aparecer a faixa **Link Account**, clique nela.

**Requisitos:**

- No PagerDuty: papel Admin, Global Admin ou Account Owner.
- No Slack: ser admin ou owner do workspace. Quem cria o workspace é owner.
- O Slack Free permite até 10 apps. O projeto passa a usar 2: o do webhook e o do PagerDuty.

Fontes: https://docs.pagerduty.com/integrations/slack-integration-guide e https://slack.com/help/articles/115002422943-Message-file-and-app-limits-on-the-free-version-of-Slack

### 4.2 Vincular a conta e conectar o canal

1. No canal `#incidentes-tech-challenge`, digite `/pd link`. Clique no link para vincular as contas e entre no PagerDuty na janela que abrir. Na região US o comando é `/pd`; na região EU seria `/pdeu`.
2. No mesmo canal, digite `/pd connect`.
3. No formulário:
   - escolha sua conta PagerDuty;
   - busque e escolha o serviço **ToggleMaster Fase 4**;
   - escolha **Responder**. Ele mostra o cartão com botões; "Stakeholder" mostra o cartão sem botões.
4. Clique em **Connect**.

**Cuidados:**

- [INCERTO] Os rótulos exatos do formulário não estão na documentação. Me diga o que a tela mostrou.
- Se a conexão ficar pendente, aprove no portal de admin do Slack: app PagerDuty > **Manage app for entire workspace?** > **Approve**.

Fontes: https://docs.pagerduty.com/integrations/slack-integration-guide e https://docs.pagerduty.com/integrations/slack-integration-guide/slack-user-guide

### 4.3 Escolher quais eventos vão para o canal

1. No PagerDuty: **Integrations** > **Extensions** > **Slack** > seu workspace > aba **Notification Channels**.
2. Na conexão do canal, troque o preset padrão **Status Updates Only** por **All Updates**. Outra opção é **Custom**, marcando triggered, acknowledged, escalated e resolved.
3. Os presets existentes são Highlights Only, Status Updates Only, No Updates, All Updates e Custom.

[INCERTO] O nome do controle aparece só na legenda de uma imagem da documentação ("Conditions dropdown"). Se a tela tiver outros nomes, me diga.

Fonte: https://docs.pagerduty.com/integrations/slack-integration-guide

### 4.4 Repetir o teste do PagerDuty vendo o canal

1. Se a janela da Parte 2 foi fechada, rode de novo o **Comando 1**.
2. Rode o **Comando 2**. Ele gera um `dedup_key` novo.
3. Segundos depois do `HTTP 202`, deve aparecer no canal o cartão `[TESTE] ToggleMaster Fase 4 ...`, com os botões Acknowledge, Resolve, Run a Workflow e More actions.
4. Rode o **Comando 3** (opcional) e depois o **Comando 4**. Veja as atualizações aparecerem no canal.
5. Rode o **Comando 5** e feche a janela.
6. Tire prints do canal e da lista de incidentes, **sem** nenhuma chave visível.

Não há procedimento oficial de teste para a integração com o Slack. Esta conferência é empírica.

Fonte: https://docs.pagerduty.com/integrations/slack-integration-guide/slack-user-guide

---

## Checklist final e o que me dizer (sem segredos)

- [ ] Parte 1: região US confirmada. Chave `tc04-otel-collector-local` no gerenciador. O teste deu 2xx e o log apareceu em Logs.
- [ ] Parte 2: serviço "ToggleMaster Fase 4" criado com Events API V2. Chave no gerenciador. Push e e-mail chegaram. O incidente abriu e resolveu.
- [ ] Parte 3: canal `#incidentes-tech-challenge` criado. URL do webhook no gerenciador. `Resposta: ok` e a mensagem no canal.
- [ ] Parte 4: app do PagerDuty conectado ao canal. O cartão apareceu e foi atualizado até Resolved.
- [ ] Nenhum incidente de teste ficou aberto.
- [ ] Área de transferência limpa e janelas do PowerShell fechadas.

Me mande frases como estas:

- "Parte 1 ok: HTTP 202, log apareceu em Logs às HH:MM."
- "Parte 2 ok: incidente abriu e resolveu; dedup_key togglemaster-teste-...; push às HH:MM, e-mail às HH:MM."
- "Parte 3 ok: Resposta ok, mensagem no canal às HH:MM."
- "Parte 4 ok: cartão chegou no Slack e mudou para Resolved."
- A data de fim do trial vista em Subscriptions.
- Os rótulos que a tela mostrou nos pontos marcados como [INCERTO].
- Qualquer erro, com o código HTTP e o texto do erro. Nunca a chave ou a URL.

O `dedup_key` e o Account ID não são segredos. Mesmo assim, o Account ID fica fora de código público.

---

## Onde cada segredo será usado depois

| Segredo | Bloco | Uso |
|---|---|---|
| `NEW_RELIC_LICENSE_KEY` | B1: Collector → New Relic | Exporter `otlp_http/newrelic` com endpoint `https://otlp.nr-data.net` e header `api-key: ${env:NEW_RELIC_LICENSE_KEY}`, lido de um `.env` local criado no B1. O `.gitignore` ignora o `.env` (linha 28, conferido em 2026-11-01). |
| `PAGERDUTY_INTEGRATION_KEY` | B4: Grafana → PagerDuty | Campo **Integration Key** do contact point PagerDuty no Grafana. Se o self-healing for resolver o incidente, entra como Actions secret no GitHub e é usada para enviar `resolve` com o `dedup_key` do alerta. |
| `SLACK_WEBHOOK_URL` | B4: Grafana → Slack | Campo **Webhook URL** do contact point Slack no Grafana. Talvez também seja usada para avisar o resultado do self-healing. |

Notas para o B1 e o B4:

1. Desde o Collector v0.144.0, o nome do exporter é `otlp_http`; `otlphttp` virou alias obsoleto. O projeto usa a 0.163.2.
   - Fonte: https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.144.0
2. No Grafana, o botão **Test** do contact point só existe com o Grafana Alertmanager. O teste do PagerDuty cria um incidente na aba Activity do serviço.
3. [INCERTO] A documentação do Grafana não diz se ele envia `resolve` automaticamente ao PagerDuty. Isso será validado no B4.
4. Fixe a imagem `grafana/grafana:13.3.0`, que tem a correção do CVE-2026-100105. Nunca use `latest`.
   - Fonte: https://grafana.com/security/security-advisories/cve-2026-100105/
5. [INCERTO] No plano Free, depois do trial, a linha "Events" da tabela de preços aparece como "Not included". O efeito disso na Events API v2 não foi confirmado.
6. [INCERTO] Também no Free, ações de Slack como "Send Message to a Slack channel" aparecem como não incluídas, enquanto "Chat Experience" está incluída. O efeito disso na conexão feita com `/pd connect` não foi confirmado. Por isso, grave o vídeo durante o trial.
7. Existem dois caminhos até o Slack: o cartão do PagerDuty (Parte 4) e o webhook direto do Grafana (Parte 3). A escolha fica para o B4.

---

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| A janela abre como caixa de diálogo ao pedir a chave | Você está no PowerShell ISE | Use o console **Windows PowerShell** |
| "A chave tem N caracteres" | A cópia veio incompleta ou com espaços | Copie de novo do gerenciador |
| New Relic: `Falhou: HTTP 403` | Chave de tipo errado (User ou Browser) [INCERTO para a Log API] | Use uma chave **Ingest - License** |
| New Relic: 2xx, mas nenhum log aparece | Conta diferente ou erro assíncrono | Confira o seletor de contas e rode a consulta `NrIntegrationError` |
| New Relic: a chave sumiu da tela | Ela só aparece inteira uma vez | Apague a chave e crie outra |
| PagerDuty: o resolve não faz nada | `dedup_key` diferente ou janela fechada | Use a mesma janela. O resolve precisa da mesma chave e do mesmo `dedup_key`. |
| PagerDuty: o push não chega | Aparelho `Expired` ou regra de notificação ausente | Remova o aparelho, entre de novo no app e confira as Notification Rules |
| Slack: `posting_to_general_channel_denied` | O webhook aponta para o `#general` | Gere o webhook para `#incidentes-tech-challenge` |
| Slack: `no_service` | URL cortada ou webhook removido | Copie a URL de novo |
| O cartão do PagerDuty não aparece no Slack | Canal sem conexão, conexão pendente, preset ou app removido do canal | Confira em Integrations > Extensions > Slack, aprove a conexão pendente e verifique o preset |
| `Falhou sem resposta HTTP` | Rede, proxy ou TLS | Rode `[Net.ServicePointManager]::SecurityProtocol` e confira a rede |

---

## Fontes (consultadas em 2026-11-01)

**New Relic**

- https://docs.newrelic.com/docs/accounts/accounts-billing/account-setup/choose-your-data-center/
- https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/
- https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/
- https://docs.newrelic.com/docs/infrastructure/infrastructure-agent/new-relic-guided-install-overview/
- https://docs.newrelic.com/docs/logs/log-api/introduction-log-api/
- https://docs.newrelic.com/docs/data-apis/ingest-apis/event-api/introduction-event-api/
- https://docs.newrelic.com/docs/data-apis/ingest-apis/metric-api/report-metrics-metric-api/
- https://docs.newrelic.com/docs/logs/ui-data/use-logs-ui/
- https://docs.newrelic.com/docs/logs/ui-data/query-syntax-logs/
- https://docs.newrelic.com/docs/data-apis/manage-data/nrintegrationerror/
- https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/

**OpenTelemetry Collector**

- https://github.com/open-telemetry/opentelemetry-collector/releases/tag/v0.144.0

**PagerDuty**

- https://docs.pagerduty.com/account-admin/billing
- https://docs.pagerduty.com/get-started/trial-account-onboarding
- https://docs.pagerduty.com/incident-management/schedules/escalation-policies
- https://docs.pagerduty.com/incident-management/services/services-and-integrations
- https://docs.pagerduty.com/incident-management/services/configurable-service-settings
- https://docs.pagerduty.com/account-admin/user-profile/contact-information
- https://docs.pagerduty.com/account-admin/user-profile/notification-rules
- https://support.pagerduty.com/docs/mobile-app-settings
- https://docs.pagerduty.com/get-started/mobile-app
- https://docs.pagerduty.com/developer/send-alert-event
- https://docs.pagerduty.com/developer/api/reference/events-v2/send-event/create-v2-event
- https://docs.pagerduty.com/developer/events-api-v2-overview
- https://docs.pagerduty.com/integrations/slack-integration-guide
- https://docs.pagerduty.com/integrations/slack-integration-guide/slack-user-guide
- https://www.pagerduty.com/pricing/incident-management/
- https://www.pagerduty.com/terms-of-service/

**Slack**

- https://slack.com/help/articles/201402297-Create-a-channel
- https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace
- https://slack.com/help/articles/115002422943-Message-file-and-app-limits-on-the-free-version-of-Slack
- https://docs.slack.dev/app-management/quickstart-app-settings/
- https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/
- https://docs.slack.dev/changelog/2016-05-17-changes-to-errors-for-incoming-webhooks
- https://docs.slack.dev/apis/web-api/rate-limits/

**Grafana**

- https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/pager-duty/
- https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/configure-slack/
- https://grafana.com/security/security-advisories/cve-2026-100105/

**Microsoft (PowerShell)**

- https://learn.microsoft.com/en-us/dotnet/framework/network-programming/tls
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-5.1
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1