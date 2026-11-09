# Criar role IAM do GitHub Actions pela interface
TL;DR: criar provedor OIDC, policy restrita aos cinco ECR e role `togglemaster-github-actions`. Copiar seu ARN para a Repository variable `AWS_ROLE_ARN`. As políticas ao lado são modelos: substituir `SUBSTITUA_ID_AWS` pelo ID de 12 dígitos da conta nova antes de usar.
Última atualização: 2026-10-28, Codex. Orientação a pedido do usuário; nenhum recurso AWS foi criado pelo agente.

## 1. O que estamos criando
- Provedor OIDC: permite à AWS verificar a identidade dos workflows do GitHub.
- Trust policy da role: define quem pode assumir a role; proposta limitada ao repo04 e à main.
- Permissions policy: permite autenticação e publicação/leitura nos cinco ECR do projeto.
Isso é uma role IAM; o perfil da CLI é uma configuração local diferente.

## 2. Preparar os modelos
Abra [trust policy](trust-policy_TEMPLATE.json) e [permissions policy](ecr-permissions_TEMPLATE.json).
Copie o conteúdo para o editor JSON do console e substitua todas as ocorrências de `SUBSTITUA_ID_AWS` pelo ID de 12 dígitos da conta nova. Não usar ID da conta antiga.
As permissões assumem a região configurada no projeto, `us-east-2`. Se os ECR foram criados em outra região, alinhar ARNs e AWS_REGION com ela.
Os IDs numéricos do GitHub já foram confirmados e não precisam ser substituídos.

## 3. Criar o provedor
IAM → Identity providers / Provedores de identidade → Add provider / Adicionar provedor.
Escolher OpenID Connect; Provider URL = `https://token.actions.githubusercontent.com`; Audience = `sts.amazonaws.com`; salvar.
Se esse provedor já existir, verificar a audience e reutilizá-lo; não criar outro com a mesma URL.
Fonte: [AWS — provedor OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).

## 4. Criar a policy de permissões
IAM → Policies / Políticas → Create policy / Criar política → editor JSON.
Colar o conteúdo ajustado de `ecr-permissions_TEMPLATE.json`, avançar e salvar com nome `togglemaster-ci-ecr-push`.
Ela não concede administração da conta nem criação/deleção de infraestrutura. O Resource `*` é necessário apenas no statement de `ecr:GetAuthorizationToken`; as demais ações ficam nos cinco ARNs.
Os repositórios podem ser criados depois, mas precisam existir para o push.
Ações/nomes conferidos com `terraform/modules/iam-ci/main.tf`; fundamentação: [AWS — permissões de push](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html).

## 5. Criar a role
IAM → Roles / Funções → Create role / Criar função.
Em Trusted entity type, escolher Custom trust policy / Política de confiança personalizada e colar o JSON ajustado de `trust-policy_TEMPLATE.json`.
Avançar, selecionar a policy `togglemaster-ci-ecr-push`, avançar e usar o nome `togglemaster-github-actions`. Revisar e criar.
Usar a opção personalizada permite informar o subject real confirmado, sem depender de um assistente que gere o formato antigo.
A condição principal já está pronta:
`repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817:ref:refs/heads/main`
Ela limita a assunção à main. O CI local publica apenas nessa branch; dev continua para desenvolvimento/testes. Não houve autorização ou execução de merge/push/PR.
Se futuramente o job usar um GitHub environment, sua condição de subject precisará ser revista.
Fontes: [AWS — roles OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html), [GitHub — subject imutável](https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims).

## 6. Obter o ARN e configurar GitHub
Abra a role criada e copie ARN em Summary / Resumo. Formato:
`arn:aws:iam::<ID_DA_CONTA>:role/togglemaster-github-actions`
No repo04: Settings → Secrets and variables → Actions → Variables → New repository variable:
- `AWS_ROLE_ARN`: ARN real copiado.
- `AWS_REGION`: região real dos ECR.
- `ECR_REGISTRY`: hostname `<ID_DA_CONTA>.dkr.ecr.<REGIAO>.amazonaws.com`.
Não cadastrar chaves AWS permanentes para esse fluxo OIDC.
Fonte: [GitHub — OIDC AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).

## 7. Verificação sem publicar imagens
Na conta correta, pode consultar:
```powershell
aws iam get-role --role-name togglemaster-github-actions --query "Role.{Arn:Arn,Trust:AssumeRolePolicyDocument}" --output json
aws iam list-attached-role-policies --role-name togglemaster-github-actions
```
A primeira consulta mostra ARN/trust; a segunda deve listar `togglemaster-ci-ecr-push`. Não comprovam a autenticação do pipeline, que requer teste autorizado posterior. AccessDenied não prova ausência da role.
Checklist do usuário: [ ] provedor criado/reutilizado; [ ] policy; [ ] role e trust corretos; [ ] policy anexada; [ ] três Variables; [ ] validação posterior do CI.

## 8. Compatibilidade com Terraform e handoff
F-023: em 2026-10-28 a API do GitHub confirmou `use_immutable_subject=true` e o prefixo com IDs; ver [evidência](verificacao-oidc.json).
O Terraform ainda contém o padrão antigo `repo:fiap-devops-arqcloud-2026/tech-challenge-04:*`, que não corresponde ao subject efetivo. Precisa ser ajustado antes do apply para não restaurar uma trust incompatível.
A limitação à main é uma recomendação para esta configuração manual; o código atual permite todos os contextos do repo no formato antigo. A alteração IaC ainda não foi aplicada.
Criações manuais devem ser reconciliadas com Terraform: role, policy e attachment importados ao estado correto; provedor OIDC importado se for de propriedade do projeto ou explicitamente reutilizado via `create_github_oidc_provider=false`. Inventariar antes, sem apagar/recriar por atalho.
Nenhum state antigo deve ser transportado. P-003/P-010 continuam abertos; a conta existe e CLI foi acessada segundo o usuário, não houve consulta autenticada AWS nesta orientação.

