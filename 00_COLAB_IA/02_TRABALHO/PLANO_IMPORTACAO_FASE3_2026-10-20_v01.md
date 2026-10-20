# Importação da base da Fase 3 para a Fase 4

TL;DR: recomenda-se integrar o histórico da Fase 3 ao repositório 04 existente, em branch própria, preservando os documentos atuais e a Fase 3. Método ainda não executado. O usuário decidiu continuar na AWS; a criação de outra conta não renova, pelas regras atuais, a elegibilidade de cliente antigo ao Free Tier.

Última atualização: 2026-10-20, Codex. Inspeção Git e fontes oficiais nesta data.

## Estado conferido

- Fase 3: `main` e `dev` no commit `6100879`; checkout limpo. Origem: `fiap-devops-arqcloud-2026/tech-challenge-03`.
- Fase 4: `dev` em `9696185`, `main` em `003a707`; origens no repositório `tech-challenge-04` da mesma organização. Documentação de colaboração, requisitos e cinco guias ainda não rastreados.
- Comparação de árvores Git e arquivos presentes no 04: nenhuma colisão de caminho exato com a base atual da Fase 3. Isso não dispensa a revisão semântica de README, documentação histórica e automações.
- D-009 já registra a preferência por trazer o histórico e preservar o 03 como entregue. O usuário atual perguntou pela melhor opção; nenhuma importação/commit/push foi executada nesta análise.

## Recomendação

Usar uma branch de importação derivada da `dev` do 04, por exemplo `codex/import-fase3`, e fazer merge da base fixada `6100879` com `--allow-unrelated-histories`. Os dois históricos serão ancestrais do resultado; `services/`, `terraform/`, `gitops/` e workflows permanecem nos caminhos esperados.

| Opção | Avaliação para este caso |
|---|---|
| Merge dos históricos | Recomendada: preserva a evolução dos dois projetos e a estrutura de código existente |
| Cópia dos arquivos rastreados | Mais simples, mas perde ancestralidade dos commits dos serviços no 04; não atende tão bem à D-009 |
| Novo fork do 03 | Exigiria reincorporar os materiais e histórico já existentes no 04; repo de destino já existe |
| Subtree em subpasta | Acrescenta um nível e exige alterar caminhos de CI/Docker/Terraform/GitOps sem benefício necessário aqui |

## Sequência proposta

1. Preparar e revisar um checkpoint dos arquivos atuais do 04, distinguindo entregáveis, fontes e auxiliares. Não fazer `git add .` indiscriminado. Commit somente após autorização, como exigido pelo usuário.
2. Preparar a branch no 04, com fonte fixada na base revisada do 03. A operação não modifica o checkout/repositório 03.
3. Integrar o histórico, preservar os materiais do 04 e ajustar README e referências de fase. Manter registros históricos identificados como históricos, sem sobrescrever a colaboração atual.
4. Adaptar CI/GitOps para o repositório 04 e a conta AWS efetivamente disponível: URL do ArgoCD, backend e chaves de estado, referências de imagens/ECR, IAM/OIDC e identidades dos pods.
5. Fazer validação local apropriada e revisar o diff; seguir o fluxo já estabelecido `dev → PR → main` após autorização para publicar.

Não transportar `.git/`, `.terraform/`, `terraform.tfstate*`, `tfvars` reais, kubeconfig, credenciais ou caches da pasta local do 03. O merge traz conteúdo versionado; ainda requer revisão de referências e do histórico antes de publicação. `.terraform.lock.hcl` versionado é lock de dependências, não estado, e pode ser reaproveitado com validação.

## Nova conta AWS

O usuário informou em 2026-10-20 que pretende criar outra conta e manter a AWS. Isso define a preferência de provedor, mas não comprova conta criada, saldo ou elegibilidade.

A documentação atual da AWS diz que clientes que possuem ou já possuíram conta não são elegíveis ao Free plan/Free Tier credits. Os termos também vedam benefícios adicionais pela criação de mais de uma conta. Portanto, não basear o orçamento em renovação automática do crédito por outra conta do mesmo cliente.

Fontes oficiais consultadas em 2026-10-20: [AWS Billing — Free Tier FAQ](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-FAQ.html), [AWS Free Tier Terms](https://aws.amazon.com/free/terms/).

Se for usada outra conta efetivamente disponível, o código pode ser reaproveitado, mas a infraestrutura deve ser provisionada para ela, com backend/estado próprios e identidades novas. Não apontar a conta nova para o estado da conta anterior como se os recursos fossem os mesmos. O estado antigo continua sendo referência do ambiente anterior e só pode ser removido mediante autorização específica.

## Verificação antes de concluir a importação

- Histórico de ambas as bases acessível e origem `6100879` documentada.
- Arquivos da Fase 3 intactos; materiais da Fase 4 preservados.
- README e colaboração atuais coerentes com a Fase 4; histórico de entrega anterior identificado.
- Nenhum estado ou segredo copiado; referências operacionais antigas revisadas.
- Compose/testes e validações de Terraform/Kustomize executadas conforme mudanças e ferramentas disponíveis; código validado não equivale a implantação.
- CI/publicação/deploy apenas no destino correto e dentro da autorização aplicável.

## Estado para retomada

P-003: provedor AWS escolhido pelo usuário, sem migração para Azure. Método Git acima é recomendação, não importação executada. P-002/E0 continua pendente: checkpoint, importação, configuração de conta/identidade e validação local. Não houve alteração do 03, das branches ou dos remotes nesta análise.
