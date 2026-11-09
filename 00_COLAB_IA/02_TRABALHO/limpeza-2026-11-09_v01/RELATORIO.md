# Limpeza executada após a auditoria do Claude

TL;DR: removidos 121 arquivos versionados comprovadamente dispensáveis e 29.310 arquivos locais de cache/binários, em 22 alvos. Os caches liberaram 1,92 GiB (2.059.708.350 bytes). Código, materiais FIAP, credenciais e evidências úteis foram preservados.
Última atualização: 2026-11-09, Codex.

## O que a análise confirmou

O Claude não havia feito exclusões: o commit eb408a5 registrou a auditoria somente leitura. Reconfirmei os itens contra o disco, as referências, o histórico e o código atual, sem usar apenas idade, nome ou ausência de import como critério.

| Grupo versionado removido | Arquivos | Motivo |
|---|---:|---|
| Cópias no arquivo morto | 99 | Sem consumidor operacional; versões exatas recuperáveis no Git |
| Partes HTML do plano | 9 | Concatenação idêntica, byte a byte, ao HTML completo preservado |
| Harness OIDC e auxiliares | 9 | Substituído pelo teste ativo do módulo iam-ci, integrado ao CI; resumo do ensaio preservado |
| Extração da aula da Fase 3 | 2 | Texto derivado do PDF preservado no repo03; relatório de leitura mantido |
| pyproject.toml | 1 | Ruff não utilizado; flake8/pylint vigentes preservados |
| Apresentação Fase 3 | 1 | SHA-256 idêntico ao arquivo do repo03; não é apresentação da Fase 4 |

As propostas “depois do B5/B6” para cópias redundantes do arquivo morto foram antecipadas porque não há dependência de execução; a autorização de 2026-11-09 cobre a remoção. Permanecem os itens de arquitetura, documentação, materiais de estudo e dependências que têm função e só precisam de atualização ou decisão.

Localmente saíram: cache do harness aposentado, caches Go do ensaio de 2026-10-27, ambiente virtual antigo, seis executáveis Go e caches de bytecode. Foram removidos somente os alvos do manifesto, nunca uma pasta qa-* inteira. Tamanhos são bytes lógicos: o histórico .git não foi reescrito nem reduzido por essa operação.

## Preservação

- 677 arquivos versionados não editados nesta revisão: hashes preservados.
- 1.046 arquivos locais de evidência/configuração: hashes preservados, inclusive credenciais ignoradas; valores não foram exibidos.
- Enunciado, aulas, cinco guias, fontes e geradores dos estudos preservados.
- Três raízes/cache Terraform ativos, state, planos, lockfiles, backend e tfvars mantidos.
- Resultados dos testes e dos scans, traces, imagens de conferência e acervo da D-017 mantidos.
- O repositório 03 foi usado somente em leitura.
- Treze diretórios dos alvos, já sem arquivos, ficaram no disco: a revisão automática bloqueou removê-los, retornando apenas “blocked by policy”. Eles não são versionados.

Os documentos originais editados na revisão estão em ../../_ARQUIVO_MORTO/2026-11-09_antes-limpeza_v01/, seguindo a convenção do projeto. O LOG recebeu entradas novas, sem apagar as anteriores.

## Recuperação e referências

[Manifesto completo](manifesto-exclusoes.json): lista cada arquivo, categoria, tamanho, SHA-256, blob e comando de consulta. Fonte anterior à remoção: commit eb408a552ad29529e5af66339a7da6e8e4fa2e69. A árvore não depende de rede para ler esses objetos já presentes.

Para **consultar** um arquivo removido: usar o comando git show individual do manifesto. Para **restaurar** um arquivo versionado, após decidir que voltou a ser necessário: git restore --source=eb408a552ad29529e5af66339a7da6e8e4fa2e69 -- "caminho". Não restaurar pastas inteiras por rotina.

Os inventários/LOG antigos continuam verdadeiros para suas datas. Se citarem caminhos desta lista, usar Git em vez de exigir que a cópia antiga exista. O HTML completo do plano, o resumo do teste OIDC e o relatório da aula continuam no lugar. O comentário de arquitetura que indicava o Ruff sem uso foi ajustado.

## Proteções e verificação

O .gitignore passa a cobrir nomes convencionais de planos JSON (plan.json, *-plan.json, *.tfplan.json), vídeos locais e a distinção entre ignorado e descartável. Os padrões não removem arquivos existentes nem são detector universal de segredo. Usar nome convencional e pasta privada ignorada para novos planos.

Resultados: verificação de preservação, renderização Kustomize das três pastas, Grafana/verificador, preflight 7/7, self-healing 11 cenários, security-check e terraform validate nas três raízes. As saídas brutas ficam em ../validacao-local-limpeza-2026-11-09/ (ignorada). Nenhum apply/destroy, PR/main, envio de notificação ou alteração funcional integra esta limpeza.

O ponto de retomada é o primeiro bloco de PENDENCIAS. A decisão ArgoCD e os tópicos 5/6 continuam abertos; a limpeza não prova implantação no EKS nem resolve riscos da aplicação.
