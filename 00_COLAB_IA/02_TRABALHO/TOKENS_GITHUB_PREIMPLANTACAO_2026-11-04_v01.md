# Tokens GitHub para ArgoCD e Grafana

TL;DR: criar dois tokens fine-grained restritos ao repositório 04 e salvar somente no .env local ignorado. O token de leitura alimenta ArgoCD; o de escrita permite ao Grafana solicitar o workflow de recuperação.

Última atualização: 2026-11-04, Codex.

## Criar os tokens

No GitHub: foto do perfil → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.

Nos dois cadastros, selecionar Resource owner `fiap-devops-arqcloud-2026` e Repository access → Only select repositories → `tech-challenge-04`. Usar expiração suficiente para o ensaio e entrega, por exemplo 2026-11-18. Se a organização exigir aprovação, o token precisa sair de Pending antes de funcionar.

| Nome sugerido | Repository permissions | Variável no .env |
|---|---|---|
| tc04-argocd-read | Contents: Read-only; Metadata de leitura automático | GITHUB_ARGOCD_TOKEN |
| tc04-grafana-dispatch | Contents: Read and write; Metadata de leitura automático | GITHUB_DISPATCH_TOKEN |

Não habilitar permissões de conta/organização adicionais para estes usos. A API repository_dispatch exige Contents: write; não é necessário conceder Actions: write para esse endpoint. [Cadastro de tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), [permissão de dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event), consultados em 2026-11-04.

## Disponibilizar localmente

Editar o arquivo `.env` na raiz do projeto e acrescentar duas linhas com os nomes acima e os valores reais após `=`. Não colar os valores no chat, em comandos de terminal, em prints nem em arquivos versionados. Guardar também no gerenciador de senhas; o GitHub só mostra o valor do token na criação.

Não substituir PAGERDUTY_INTEGRATION_KEY nem NEW_RELIC_LICENSE_KEY. Os tokens têm destinos diferentes.

Após salvar, informar apenas: **“Tokens salvos no .env”**. O agente verificará acesso sem imprimir valores. Para o Terraform, GITHUB_ARGOCD_TOKEN será mapeado para TF_VAR_github_token e GITHUB_DISPATCH_TOKEN para TF_VAR_github_dispatch_token no processo de execução; nomes do .env não são carregados automaticamente pelo Terraform.

## Limites desta preparação

O workflow de recuperação precisa existir na branch padrão para responder ao repository_dispatch. Validar permissão não exige executar a recuperação na AWS. PR/main, implantação e ensaio final continuam nas etapas posteriores reservadas pelo usuário. [Evento repository_dispatch](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#repository_dispatch).
