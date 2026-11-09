# Primeiro deploy da Fase 4: ordem e critérios de aceite

TL;DR: a infraestrutura ainda não foi implantada. No primeiro ciclo, preparar a base e o cluster, instalar **somente o ArgoCD**, promover a aplicação e aguardar as cinco imagens no ECR. Só então criar as Applications. Antes de testar a aplicação, inicializar os dois RDS e trocar a chave provisória do evaluation por uma emitida pelo auth. Um pod saudável sozinho não prova que a aplicação funciona.

Última atualização: 2026-11-05, Codex. Este roteiro substitui a seção 6 da [preparação de 2026-11-04](PREPARACAO_B3_2026-11-04_v01.md), que preserva a memória de cálculo, as evidências dos testes, os tokens e o orçamento. As instruções de implantação e encerramento abaixo são para execução pelo usuário ou sob autorização específica. Não foram executadas nesta revisão.

*Atualização de 2026-11-09:* use o [guia de deploy e gravação](GUIA_DEPLOY_E_GRAVACAO_2026-11-09_v01.md), em Git Bash, que segue esta ordem. Duas mudanças valem sobre o texto abaixo: com o repositório público, o `TF_VAR_github_token` não é mais exportado; e o ArgoCD já está no chart 7.7.23 com a imagem v2.13.9 (D-023).

## Onde estamos e quanto custa

- Consulta em 2026-11-05: plano AWS FREE ativo, **US$ 120,00** disponíveis, nenhum cluster EKS em `us-east-2`. O orçamento acumulado `togglemaster-creditos` é de US$ 80 e tem cinco notificações. Orçamento é aviso de consumo, não um desligamento automático.
- A estimativa da AWS Price List de 2026-11-04, para EKS 1.34 em suporte padrão, dois nós `m7i-flex.large`, dois RDS, Redis, um NAT, IPv4, armazenamento e Secrets Manager, é **US$ 9,82 por 24 h**. Com 110 h e 8 GB processados pelo NAT: **US$ 45,35**; sobra estimada **US$ 74,65**. ECR, tráfego, logs e consumo por requisição podem variar. Não contar créditos de atividades ainda não concluídas. O orçamento não substitui o inventário após o encerramento.
- Evidência da base em 2026-11-04: **8 importações, 29 criações, 7 alterações, 0 destruições**. É uma referência para comparação; gerar plano novo no dia. O arquivo parcial de plano do cluster tem erro e não pode ser aplicado. Os planos completos de cluster e k8s dependem das saídas reais da camada anterior.
- PagerDuty Events API V2 e webhook do Slack foram validados isoladamente; há evidência de recebimento e resolução. A instrumentação local gerou 19 spans cobrindo cinco serviços. O teste da falha controlada teve 11 etapas aprovadas. Esses testes não constituem evidência da cadeia no EKS.

## 1. Base e cluster

1. Confirmar branch, conta e região; conferir os três backends em S3, nas chaves distintas sob `phase4/prod/`. Validar cotas, saldo e capacidade. O perfil local pede dois nós (4 vCPU), máximo dois, diante da cota de 5 vCPU. Não depender de um terceiro nó para concluir um upgrade.
2. Para **cada** etapa Terraform: executar `plan -input=false -out=<arquivo>`, conferir com `show <arquivo>`, depois aplicar **esse mesmo arquivo** apenas se a mudança for aceita. Usar caminhos absolutos em pasta local ignorada `validacao-local-*`. Planos e state podem conter segredos. Não usar `apply` interativo, plano antigo, saída JSON agregada ou arquivo parcial. Para uma nova máquina, inicializar cada diretório com seu próprio `backend.hcl`.
3. Primeiro `terraform/`, com importação declarativa dos cinco ECR, role, policy e attachment **já existentes**. Comparar com o plano acima em especial as condições da trust OIDC; parar se houver exclusão, substituição ou difusão das permissões sem explicação. A primeira importação só ocorre no apply.
4. Em `terraform/cluster/`, gerar outro plano **depois** da base e revisar EKS, nós, RDS, Redis, IRSA, volumes e conectividade. Após o apply aprovado, conferir `cluster_name` e atualizar o contexto do kubectl para `togglemaster` em `us-east-2`. Verificar o contexto antes de cada operação. Definir as **Variables** do GitHub `AWS_SELF_HEALING_ROLE_ARN` (output `self_healing_role_arn` da base) e `EKS_CLUSTER_NAME` (output `cluster_name`). Os tokens não são Variables.

## 2. Preparar o Git e instalar só o controlador

Antes do PR, atualizar na `dev` os **cinco campos** abaixo, usando apenas outputs nomeados, não sensíveis e da nova conta. As [URLs do overlay](../../gitops/overlays/prod/patches/endpoints.yaml) e as [roles IRSA](../../gitops/overlays/prod/patches/irsa.yaml) têm sentinelas intencionais.

| Onde | Campo | Origem |
|---|---|---|
| ConfigMap do evaluation | `REDIS_URL` | `terraform -chdir=terraform/cluster output -raw redis_url` |
| ConfigMaps do evaluation **e** do analytics | `AWS_SQS_URL` em ambos | `terraform -chdir=terraform output -raw sqs_queue_url` |
| ServiceAccounts do evaluation **e** do analytics | `eks.amazonaws.com/role-arn` de cada uma | `terraform -chdir=terraform/cluster output -json irsa_role_arns` |

As **cinco imagens** são responsabilidade do CI após o merge. Não inventar tags para passar no teste. Executar o [verificador manual do overlay](preflight-b3-2026-11-05/checar_overlay.py) no modo `pre-pr` para conferir os cinco campos mesmo que as imagens ainda tenham sentinelas. Exemplo (PowerShell, na raiz da `dev` inicializada):

```powershell
py -3.14 00_COLAB_IA/02_TRABALHO/preflight-b3-2026-11-05/checar_overlay.py pre-pr
```

Carregar no processo do Terraform **somente** as cinco correspondências abaixo a partir do `.env` local ignorado. Não imprimir valores, não usar listagem de todas as variáveis nem transferir segredos para o Git. O backend da camada k8s conterá os Secrets; `sensitive` oculta valores no terminal, não os remove do state.

| Local | Variável do Terraform |
|---|---|
| `NEW_RELIC_LICENSE_KEY` | `TF_VAR_new_relic_license_key` |
| `PAGERDUTY_INTEGRATION_KEY` | `TF_VAR_pagerduty_integration_key` |
| `SLACK_WEBHOOK_URL` | `TF_VAR_slack_webhook_url` |
| `GITHUB_DISPATCH_TOKEN` | `TF_VAR_github_dispatch_token` |
| `GITHUB_ARGOCD_TOKEN` | `TF_VAR_github_token` |

No PowerShell, na raiz da dev, este bloco lê valores simples do arquivo local sem interpretá-lo como código. Ele rejeita campos vazios ou duplicados, valida os cinco antes de exportar e não imprime seus valores. Usar um terminal da sessão de implantação e fechá-lo ao terminar.

```powershell
$nomes = @{
    NEW_RELIC_LICENSE_KEY = 'TF_VAR_new_relic_license_key'
    PAGERDUTY_INTEGRATION_KEY = 'TF_VAR_pagerduty_integration_key'
    SLACK_WEBHOOK_URL = 'TF_VAR_slack_webhook_url'
    GITHUB_DISPATCH_TOKEN = 'TF_VAR_github_dispatch_token'
    GITHUB_ARGOCD_TOKEN = 'TF_VAR_github_token'
}
$localizados = @{}
foreach ($linha in (Get-Content -LiteralPath '.env' -Encoding utf8)) {
    if ($linha -notmatch '^\s*([A-Z_]+)\s*=(.*)$') { continue }
    $nome = $Matches[1]
    if (-not $nomes.ContainsKey($nome)) { continue }
    if ($localizados.ContainsKey($nome)) { throw "Entrada duplicada: $nome" }
    $valor = $Matches[2].Trim()
    if ($valor.Length -ge 2 -and ($valor[0] -eq '"' -or $valor[0] -eq "'") -and $valor[-1] -eq $valor[0]) {
        $valor = $valor.Substring(1, $valor.Length - 2)
    }
    if ([string]::IsNullOrWhiteSpace($valor)) { throw "Entrada vazia: $nome" }
    $localizados[$nome] = $valor
}
foreach ($nome in $nomes.Keys) {
    if (-not $localizados.ContainsKey($nome)) { throw "Entrada ausente: $nome" }
}
foreach ($nome in $nomes.Keys) {
    [Environment]::SetEnvironmentVariable($nomes[$nome], $localizados[$nome], 'Process')
}
Remove-Variable linha,valor,localizados,Matches
```

Na primeira instalação em `terraform/k8s`, gerar um **plano direcionado** com `-target=helm_release.argocd` e `-out=<arquivo>`. Conferir e aplicar esse plano. Aguardar `kubectl wait --for=condition=Established crd/applications.argoproj.io --timeout=180s`. O chart instala o tipo Application; `depends_on` não faz o tipo existir na hora do primeiro plano. **Não criar as Applications ainda:** ambas rastreiam a `main` e sincronizam automaticamente.

## 3. Primeira publicação e sincronização

1. Promover a alteração humana por **PR da dev para a main**, somente na janela definida pelo usuário. Revisar os checks correspondentes ao diff completo; no primeiro merge, os filtros incluem os cinco serviços. No PR, o CI constrói e escaneia imagens. **Só o push resultante na main** autentica via OIDC, publica no ECR e atualiza o overlay.
2. Guardar o SHA completo do evento de publicação (o merge da primeira promoção). Aguardar os jobs `image` e `gitops` dos **cinco** serviços. A tag esperada é `v1.0.0-<primeiros sete caracteres do SHA da publicação>`. O HEAD da main poderá ter avançado pelos commits automáticos do GitOps; não usar esse novo SHA para calcular a tag inicial. Conferir o estado final dos cinco Deployments, não contar commits.
3. Em um checkout limpo da **main remota atual** situado nas pastas autorizadas, rodar o verificador `pre-sync` a partir da cópia que possui os backends inicializados. Verifica novamente Redis, SQS e IRSA e compara cada imagem renderizada com o repositório Terraform, a tag esperada e o ECR. Se algum job falhou ou uma imagem segue em `.invalid`, **parar antes de criar as Applications**. Opções exatas do comando: [instruções do verificador](preflight-b3-2026-11-05/README.md).
4. Só depois, gerar um **novo plano completo** em `terraform/k8s` e aplicar o arquivo revisado. Aguardar ArgoCD para aplicação e observabilidade (inclusive Applications filhas), saúde dos pods, PVCs vinculados e datasources. Registrar o primeiro login OIDC real do CI e as revisões sincronizadas. Fontes: [configuração ArgoCD](../../terraform/k8s/argocd.tf), [observabilidade](../../terraform/k8s/observability.tf), [CI Go](../../.github/workflows/_ci-go.yml) e [CI Python](../../.github/workflows/_ci-python.yml).

## 4. Inicializar os dados e comprovar o funcionamento

1. O Terraform cria os dois bancos RDS **sem as tabelas da aplicação**. De dentro da rede privada, executar com `psql -v ON_ERROR_STOP=1` o [SQL do auth](../../services/auth-service/db/init.sql) no banco do auth e o [SQL do flag](../../services/flag-service/db/init.sql) no banco do flag. Preferir pod temporário com `DATABASE_URL` de `secretKeyRef` de cada serviço; não gravar URLs com senha no YAML, argumentos do PodSpec, gravação ou LOG. Conferir a presença de `api_keys` e `flags`. No targeting, o StatefulSet inicializa `targeting_rules` no primeiro PVC vazio; conferir, sem apagar o volume.
2. A chave inicial do [Secret do evaluation](../../terraform/k8s/secrets.tf) é provisória. Emitir uma chave real pelo `POST /admin/keys` autenticado do auth, conferir o HTTP e o campo `key` sem exibi-lo, atualizar apenas `SERVICE_API_KEY` do Secret `evaluation-service-secret` e reiniciar o Deployment do evaluation para reler o ambiente. O `ignore_changes` preserva esse valor nos próximos applies. Não registrar payloads, fragmentos de chaves ou credenciais decodificadas. Os objetos e a sequência estão na [seção 8 do guia de reprodução](../../docs/GUIA_DE_REPRODUCAO.md#8-schemas-chave-de-serviço-e-dados-de-exemplo).
3. **Aceite da implantação:** criar uma flag e uma regra de teste; consultar a avaliação sem cache prévio; comprovar a resposta esperada e o evento correspondente no DynamoDB depois do consumo da SQS. Confirmar métricas no Prometheus/Grafana, logs no Loki e traces do EKS no New Relic. Guardar apenas evidência sem credenciais. O `/health` não substitui essa verificação.
4. **Tópico 6, separado:** na janela de demonstração, produzir tráfego, ativar a falha por `POST /admin/fault`, mostrar o alerta, a abertura do incidente no PagerDuty, Slack, o workflow na main e o restart. Registrar recuperação da aplicação e resolução do mesmo incidente. Até esse ensaio, a cadeia no EKS segue sem comprovação.

## 5. Encerramento: definir o que fica antes de aprovar a remoção

**Não aprovar um destroy integral da base por padrão.** Depois da importação, cinco ECR, role/policy/attachment do CI passam a ser gerenciados por ela. `force_delete=true` permite remover também imagens dos ECR; mudar `import_manual_resources` para `false` não retira objetos já gerenciados do state. O provedor OIDC preexistente é consultado como dado. Fontes: [imports](../../terraform/imports.tf), [ECR](../../terraform/modules/ecr/main.tf), [IAM](../../terraform/modules/iam-ci/main.tf).

Antes de encerrar, o usuário define se preserva registros, imagens e identidade do CI. Gerar e revisar planos de remoção **separados por camada e em ordem reversa**, manter o cluster disponível para o controlador terminar de limpar recursos/volumes, e conferir exclusões, dados e recursos órfãos. Para preservar a base, considerar manter os importados e desligar o NAT por plano normal próprio, revisando custos residuais. Para remover a base mas manter só os importados, preparar antes uma separação explícita de propriedade no código/state, com backup e revisão; não improvisar com `state rm`. O orçamento externo ao Terraform deve continuar disponível. Nenhuma dessas operações é parte da revisão de 2026-11-05.
