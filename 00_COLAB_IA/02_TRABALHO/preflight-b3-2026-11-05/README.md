# Conferência do overlay de produção no primeiro deploy

TL;DR: depois dos applies da base e do cluster, confira a fila, o Redis e as identidades IAM antes do PR. Depois da publicação das cinco imagens pelo CI, confira as tags na main e no ECR antes da primeira sincronização. Última atualização: 2026-11-05, Codex.

Abra o PowerShell na raiz da cópia de trabalho da Fase 4, com os backends de `terraform` e `terraform/cluster` já inicializados para a conta de destino. Use Python 3.14 com PyYAML, Terraform e kubectl. A segunda conferência também usa o remoto Git `origin` do repositório 04 e a AWS CLI autenticada com permissão de leitura `ecr:DescribeImages`.

```powershell
$verificador = '00_COLAB_IA/02_TRABALHO/preflight-b3-2026-11-05/checar_overlay.py'
py -3.14 -B $verificador pre-pr
```

O comando renderiza o overlay local com `kubectl kustomize` e consulta somente os outputs nomeados `sqs_queue_url`, `redis_url` e `irsa_role_arns`. Confere os valores que os contêineres evaluation e analytics recebem e a ServiceAccount usada por cada Deployment. Neste ponto, as imagens podem continuar com as sentinelas que o CI substituirá.

Para a segunda conferência, espere os cinco jobs GitOps do primeiro merge em `main` concluírem e abra uma cópia limpa da `main` já atualizada, separada da sua `dev`. No mesmo terminal da etapa anterior, informe o caminho dessa cópia e o **SHA de 40 caracteres do commit de publicação** mostrado nos cinco runs de push. O SHA atual da `main` normalmente já inclui os commits posteriores que o robô fez ao gravar as tags.

```powershell
$copiaMain = Read-Host 'Caminho absoluto da copia limpa da main do repositorio 04'
$shaPublicacao = Read-Host 'SHA de 40 caracteres do merge que publicou os cinco servicos'
py -3.14 -B $verificador pre-sync --checkout $copiaMain --sha-publicacao $shaPublicacao
```

O segundo comando lê também o mapa `ecr_repository_urls` da base. Para cada um dos cinco Deployments, compara a imagem renderizada com o repositório do serviço e com `v1.0.0-<sete primeiros caracteres do SHA>`. Depois consulta a tag exata com `aws ecr describe-images`, na conta e região extraídas da URL do repositório. Ao começar e ao terminar, confere que o diretório `gitops` está limpo e que o checkout corresponde à ponta da `main` remota.

A saída `OK` permite avançar com **essa conferência**. Um código de saída diferente de zero identifica uma divergência ou uma leitura inconclusiva. Corrija a origem indicada e repita antes da sincronização. A saúde dos pods, o acesso da aplicação à AWS e o estado do ArgoCD são verificados após a implantação. Este comando foi desenhado para o primeiro lote de cinco imagens a partir do mesmo merge.

Para repetir o ensaio local sem conta AWS ou estado Terraform, execute:

```powershell
py -3.14 -B 00_COLAB_IA/02_TRABALHO/preflight-b3-2026-11-05/test_checar_overlay.py -v
```

Os testes renderizam o overlay atual e substituem valores apenas em memória. As consultas externas dos cenários de ECR e Git usam respostas simuladas. Fontes do contrato em 2026-11-05: [outputs da base](../../../terraform/outputs.tf), [outputs do cluster](../../../terraform/cluster/outputs.tf), [pipeline Go](../../../.github/workflows/_ci-go.yml), [pipeline Python](../../../.github/workflows/_ci-python.yml) e [overlay prod](../../../gitops/overlays/prod/kustomization.yaml).
