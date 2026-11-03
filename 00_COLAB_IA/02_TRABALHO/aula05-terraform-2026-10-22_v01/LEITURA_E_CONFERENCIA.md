# Aula 05 — IaC em Pipelines com Terraform: leitura e limites

TL;DR: PDF da Fase 3 lido integralmente, com figuras/tabelas relevantes inspecionadas. Ambientes, módulos e estados são conceitos distintos. O exemplo específico de branch para módulos/testes não consta no PDF; a aula remete a prática às videoaulas. Explicações adicionais devem ser rotuladas como Complemento.

Última atualização: 2026-10-22, Codex; revisão independente pelos agentes audit_requirements e estado_fase4.

## Checklist

- [x] Localizar fonte e confirmar instruções de somente leitura da Fase 3.
- [x] Extrair e ler as 16 páginas; remover a marca pessoal dos extratos auxiliares.
- [x] Renderizar/inspecionar p. 5, 6, 8, 9, 10 e 11, incluindo todas as figuras.
- [x] Conferir documentação primária atual e código/workflow da Fase 3.
- [x] Separar conteúdo do PDF, Complemento técnico e incertezas; verificar preservação da fonte.

## Fonte e mapa de páginas

Arquivo somente leitura: `C:/Users/Gabriel/Documents/GitHub/tech-challenge-03/docs/aulas-fiap/02_CI-CD/POSTECH - CI-CD - Aula 5.pdf`. Hash original e extração em `extracao.json`; texto em `extracao.txt`. Imagens de QA, ignoradas no Git, em `../qa-aula05-terraform-2026-10-22/`.

| Páginas | Evidência conferida |
|---|---|
| 3–4 | Objetivo e prática remetida às videoaulas/códigos; init, plan, apply |
| 5–6 | Write/Plan/Apply, plano salvo com `-out=FILE`, execução `terraform apply FILENAME`; figuras CI/CD, Actions, AWS/Okta |
| 7–8 | Estado remoto, bloqueio, versionamento/backups e estados menores |
| 9–10 | Módulos reutilizáveis e variáveis; workspaces CLI e recomendação de diretórios por ambiente |
| 10–11 | Gráfico de dependências e `terraform graph` |
| 12–16 | Mercado/licença/OpenTofu, revisão, referências e encerramento; fora do foco da pergunta |

## Limitações e inconsistências

- **[INCERTO] Exemplo da branch:** não há branch `modules`, `?ref=`, feature branch ou YAML de teste no PDF. A figura p. 5 mostra `Push (main)`/`Pull request`; `MODULES` na figura p. 9 é um rótulo conceitual. Nenhum vídeo/transcrição foi localizado no repositório. A existência/formato do exemplo na videoaula não foi conferida.
- **[INCERTO] Tabela p. 10:** linha de reutilização atribui “Baixa” a módulos, em aparente inconsistência com o texto p. 9 e a documentação HashiCorp. Não reproduzir como regra técnica; módulos servem à reutilização.
- Figuras p. 8–9 apresentam dev/test/prod por workspaces, enquanto o texto p. 9–10 recomenda diretórios separados para ambientes duradouros. Explicar que workspaces CLI são tecnicamente capazes de separar estados, mas não constituem isolamento forte de contas/credenciais/permissões. Não generalizar isso para workspaces HCP Terraform.
- O plano salvo pode passar entre executores mantendo o mesmo destino; não deve ser reinterpretado como plano dev aplicável à prod.

## Complemento técnico a explicar

Módulo raiz compõe recursos/módulos filhos; filhos expõem inputs/outputs e têm recursos registrados no estado da configuração chamadora. Diretórios/arquivos tfvars não escolhem, sozinhos, um estado/conta isolados. Ambientes precisam combinar configuração, backend/chave de estado, identidade e recursos/nomes adequados. Branch Git é versão do código e só aciona Actions quando os eventos/filtros do workflow correspondem.

Branch temporária para desenvolver módulo e referência Git `?ref=...` para consumi-lo são situações diferentes. Uma branch móvel pode mudar; tags/commits permitem selecionar uma revisão mais controlada. Exemplos ilustrativos não são código da FIAP.

Pipeline didática: mudança → PR → fmt/init/validate → testes/plan quando configurados → revisão → aplicação controlada no ambiente correspondente. `terraform test` pode criar recursos reais por padrão; testes com plan/mocks têm outro alcance. Não executar nada na nuvem nesta consulta.

## Relação com nossa Fase 3

`terraform/README.md`, linhas 3–11 e 19–42: três raízes, `terraform/` (base), `terraform/cluster/` e `terraform/k8s/`, com chaves `prod/base.tfstate`, `prod/cluster.tfstate`, `prod/k8s.tfstate`. São camadas por ciclo de vida, não três ambientes. Módulos filhos locais em `terraform/modules/`; VPC usa módulo de Registry.

`.github/workflows/terraform-check.yml`, linhas 30–44 e 73–97: PR com caminhos pertinentes, push na main ou execução manual; fmt e init sem backend/validate nas três raízes. Não contém plan, apply ou terraform test. Portanto, simples push de uma branch chamada modules não garante disparo desse workflow.

## Referências complementares consultadas em 2026-10-22

- https://developer.hashicorp.com/terraform/language/modules
- https://developer.hashicorp.com/terraform/language/modules/configuration
- https://developer.hashicorp.com/terraform/language/state/workspaces
- https://developer.hashicorp.com/terraform/cli/workspaces
- https://developer.hashicorp.com/terraform/language/tests
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow

Sem alterações na Fase 3, código, workflows, ambientes, decisões de arquitetura ou memória global. Somente estudo e registros auxiliares na pasta autorizada do 04; nada executado em Terraform/AWS/Git remoto.
