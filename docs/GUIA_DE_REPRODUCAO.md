# 🧭 Guia de reprodução — ToggleMaster Fase 4

**Resumo:** valide localmente, prepare a conta e o backend, publique imagens, provisione as camadas Terraform e confira o GitOps antes de demonstrar observabilidade e self-healing. **Atualizado em 2026-11-10.** Este guia descreve a Fase 4; valores da conta da Fase 3 não devem ser reutilizados. Fontes: código deste repositório e [ensaio de 2026-11-09](evidencias/README.md).

## 1. Para gravar no ambiente já criado

O ensaio integrado funcionou em 2026-11-09; não é necessário reprovisionar a infraestrutura para gravar. A preparação abaixo deve ser repetida no dia do vídeo porque login, túneis e estado do cluster podem mudar.

1. Abra o [roteiro com falas e tempos](gravacao/README.md) e o [arquivo de comandos](gravacao/COMANDOS.md). Use **Git Bash** nos blocos operacionais.
2. Faça login no GitHub, New Relic, PagerDuty e Slack; confirme o acesso à conta AWS e ao cluster corretos sem exibir credenciais.
3. Confira nós/pods/Applications pelos comandos abaixo. Espere o ArgoCD ficar Synced/Healthy e as aplicações Ready.
4. Abra os túneis de Grafana, ArgoCD e evaluation conforme COMANDOS.md. Se já houver túnel, confira-o; não mate todos os processos kubectl.
5. Verifique dados recentes no Grafana e Loki, disponibilidade do Service Map e um trace completo no New Relic. O cache de 30 s é por flag; siga a criação de uma flag exclusiva do roteiro.
6. Confirme tráfego HTTP 200, regra Normal, ausência de cooldown e dashboards/interfaces abertos antes de iniciar a falha. Faça um teste de áudio e texto legível.
7. Grave a sequência planejada de cerca de 21 min; o limite do enunciado é 25 min (p. 5). Siga a recuperação até HTTP 200 e resolução do alerta.

```bash
# Identifica o contexto Kubernetes selecionado, sem imprimir credenciais.
kubectl config current-context
# Confere os nós de trabalho.
kubectl get nodes
# Confere os cinco serviços e dependências no namespace da aplicação.
kubectl get pods -n togglemaster
# Confere a stack de observabilidade.
kubectl get pods -n observability
# Confere sincronização e saúde das Applications.
kubectl get applications -n argocd
```

Não ler Secrets em tela. Não mostrar `kubectl describe pod trafego`: a variável do pod pode conter uma chave. As interfaces devem estar autenticadas antes da captura.

## 2. Reprodução local, sem recursos AWS

Pré-requisitos: Docker Desktop com engine Linux, Compose, Bash e Python 3. Ferramentas adicionais são necessárias para o conjunto completo de validações; o script informa quando uma está ausente.

```bash
# Testa os cinco serviços, bancos, Redis, fila e armazenamento em Moto local.
bash scripts/test-compose.sh
# Testa telemetria, propagação de contexto, persistência e sanitização local.
bash scripts/test-observability.sh
# Valida configuração, segurança e testes disponíveis no ambiente.
bash scripts/validate-all.sh
```

Os testes usam valores fictícios de `.env.example`. `test-compose.sh` e `test-observability.sh` compartilham o projeto Compose `tc04-integration`; execute sequencialmente. O laboratório não é removido automaticamente. Consulte [observability/README.md](../observability/README.md) para evidências locais, exportação opcional ao New Relic e encerramento do laboratório. CI local aprovado não comprova execução no EKS.

## 3. Reproduzir na sua própria conta

Esta seção é uma ordem de execução, não um conjunto de valores para copiar sem conferência. Para a implantação atual, use a seção 1; em conta nova, substitua identidade, bucket, região, endpoints e roles pelos seus próprios outputs. Não migrar state da Fase 3.

| Etapa | Preparação/execução | Referência |
|---|---|---|
| Contas | AWS com cotas/orçamento, repositório GitHub, New Relic, PagerDuty e canal Slack disponíveis | [Arquitetura e papéis](ARQUITETURA.md) |
| Backend | Bucket S3 próprio; `backend.hcl` local por raiz com bucket/região. Chaves `phase4/prod/` separadas | [Terraform](../terraform/README.md) |
| Variáveis | Preencher exemplos locais; conferir `expected_aws_account_id`, `state_bucket` e `state_region` | [Exemplos Terraform](../terraform) |
| Base | Inicializar, validar, salvar plano, revisar e aplicar a base: rede, ECR, fila, tabela e IAM/OIDC | [terraform/README.md](../terraform/README.md) |
| GitHub | Configurar as cinco repository variables; revisar trust OIDC para a main do seu repositório | [CI/CD](CI-CD.md) |
| Imagens | Levar mudanças dev → PR → main após checks; aguardar os cinco pipelines e tags no ECR/GitOps | [Workflows](../.github/workflows) |
| Cluster | Planejar/aplicar `terraform/cluster`; atualizar kubeconfig com a mesma identidade autorizada | [Camada cluster](../terraform/cluster) |
| Overlay | Preencher SQS, Redis e IRSA com outputs da conta; confirmar tags publicadas | [GitOps](../gitops/README.md) |
| Kubernetes | Instalar ArgoCD antes das Applications/CRDs; depois aplicar a camada k8s completa, com Secrets locais | [Camada k8s](../terraform/k8s) |
| Dados | Inicializar schemas/chave/flag e tráfego de demonstração antes de gravar | [Schemas dos serviços](../services) e [comandos de demonstração](gravacao/COMANDOS.md) |
| Aceite | Conferir pods, Applications, três sinais, mapa/trace e cadeia automática | [Evidências](evidencias/README.md) |

Cada camada tem um diretório de trabalho próprio e um state próprio. O backend parcial recebe a configuração local por `init -backend-config=backend.hcl`; preencher os exemplos antes de executar. Para operação Terraform, sempre **plan salvo → revisão → apply desse plano**, evitando colagens que respondam involuntariamente a prompts.

A primeira instalação de `terraform/k8s` exige ArgoCD/CRDs antes de planejar `kubernetes_manifest`. O código documenta o bootstrap por `helm_release.argocd` e, depois, o plano completo. Não repetir bootstrap seletivo num ambiente existente sem inspecionar o plano e o estado.

O PostgreSQL targeting é um StatefulSet com volume persistente; os bancos de auth e flag são RDS. Credenciais de serviço e integrações são fornecidas à camada k8s por mecanismo local protegido e seguem o [contrato de Secrets](../gitops/SECRETS-CONTRATO.md). Não imprimir outputs sensíveis nem copiar manifests reais de Secrets para o Git.

## 4. O que provar na demonstração

| Prova | Onde mostrar | Critério de sucesso |
|---|---|---|
| Base/IaC/GitOps | Terraform, Lens/terminal, ArgoCD e Actions | Código da infraestrutura, serviços Ready, sync/health e pipeline de publicação |
| Métricas e logs | Grafana dashboard + Explore/Loki | Dados recentes de recursos, requisições e logs; consulta retornando linhas |
| OTel | Diagrama e values dos Collectors | Explicar recepção, processamento e destinos sem abrir Secrets |
| APM | New Relic | Service Map dos cinco serviços, requisição real e trace detalhado |
| Incidente | Falha controlada, Grafana, PagerDuty e Slack | 503, Firing, incidente automático e mensagem no canal |
| Self-healing | GitHub Actions + pods/tráfego | repository_dispatch, restarted, rollout completo e HTTP 200 |

Fonte: enunciado da Fase 4, p. 5–6. Execute a falha somente com tráfego e integrações prontos; aguarde pelo menos 600 s após qualquer restart anterior. Se houver recuperação manual, declare a intervenção e não a apresente como automação.

## 5. Fechamento da entrega e do ambiente

- Conferir os quatro prints do relatório: dashboard, trace, ChatOps e execução da automação (enunciado p. 6). [Pasta de evidências](evidencias/README.md).
- Publicar o vídeo, testar o link sem depender da sua sessão e incluí-lo no relatório/README. O [relatório PDF](relatorio/README.md) mantém essa pendência explícita enquanto não houver URL.
- Confirmar data, horário, canal e regra de acesso no portal/tutor. O PDF fornecido não informa esses dados; não usar prazo da Fase 3 por herança.
- Encerrar a infraestrutura somente depois de revisar vídeo e arquivos e de autorizar a destruição. Planejar com state vigente e plano salvo, conferir PVC/PV/EBS antes de retirar cluster/CSI e revisar recursos remanescentes, NAT e bancos. O bucket de estado é tratado por último.

Não há estimativa de custo vigente neste guia: valores da conta anterior não representam o ambiente atual. Conferir faturamento/créditos na conta antes de manter o laboratório ligado.
