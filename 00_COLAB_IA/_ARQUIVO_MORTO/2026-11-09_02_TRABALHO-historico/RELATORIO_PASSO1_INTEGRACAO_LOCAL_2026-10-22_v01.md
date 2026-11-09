# Passo 1 — integração local aprovada

TL;DR: a base importada da Fase 3 funciona no laboratório local. Os cinco serviços responderam corretamente, compartilharam dados e concluíram o fluxo assíncrono até a persistência. Isso permite iniciar a instrumentação sobre uma base comprovada.

Última atualização: 2026-10-22, Codex. Execução concluída às 12:03 (America/Sao_Paulo, UTC-03:00).

## Explicação simples

Montamos uma miniatura do sistema neste computador. Cadastramos uma chave, criamos flags e regras, pedimos avaliações e conferimos se os resultados chegaram ao armazenamento de eventos. Também alteramos uma flag e esperamos o cache vencer: a próxima avaliação refletiu a alteração.

Nada foi criado na AWS. O Moto simulou os serviços de fila e armazenamento usados pelo teste. Nenhuma chave New Relic foi necessária.

## Aplicação técnica

- Branch: `dev`; HEAD inicial `3b21e65`. Nenhum commit/push/PR.
- Docker Desktop: engine Linux, contexto `desktop-linux`, servidor `29.6.1`.
- Projeto exclusivo: `tc04-integration`, sem contêiner preexistente identificado antes da execução.
- Composição: `docker-compose.yaml` + `docker-compose.integration.yaml`, com `.env.example` e credenciais fictícias.
- Execução: Git Bash → `scripts/test-compose.sh` → `scripts/integration/test-flow.py`.
- Cinco aplicações, PostgreSQL, Redis e serviços locais auxiliares; SQS/DynamoDB do fluxo assíncrono simulados pelo Moto. O serviço DynamoDB Local da composição também passou no healthcheck, mas não é o destino dos eventos nesta sobreposição.

## Resultados observados

| Verificação real | Resultado |
|---|---|
| Saúde dos cinco serviços | Aprovada |
| Chave inválida rejeitada e chave nova aceita | Aprovada |
| Flags/regras persistidas via APIs | Aprovada |
| Flag ligada/desligada, rollout 0%/100%, flag inexistente e parâmetro ausente | Aprovada |
| Cache Redis preenchido, TTL entre 1 e 30 segundos | Aprovada |
| Atualização percebida após espera de 31 segundos | Aprovada |
| Eventos consumidos pelo analytics e persistidos no DynamoDB simulado | 7 eventos conferidos; fila esvaziada |
| Resultado final do script | Código de saída 0 |

Evidência bruta local: [passo1-compose.log](qa-passos-locais-2026-10-22/passo1-compose.log). O log não imprime a chave gerada. O teste usa nomes sintéticos exclusivos por execução.

## Correção necessária e preservação

A primeira tentativa falhou antes de iniciar os serviços: no Docker nativo do Windows, o separador padrão de `COMPOSE_FILE` é `;`, enquanto o script usava `:`. Foi explicitado `COMPOSE_PATH_SEPARATOR=:` em `scripts/test-compose.sh`, compatível com Git Bash e Linux. Fonte: [documentação oficial Docker](https://docs.docker.com/compose/how-tos/environment-variables/envvars/), consultada em 2026-10-22.

Original preservado em `../_ARQUIVO_MORTO/2026-10-22_passos-locais/scripts/test-compose.sh`; tentativa inicial em `qa-passos-locais-2026-10-22/passo1-compose-erro-separador.log`. Os serviços ainda não haviam sido instrumentados durante este baseline.

## Limites e próximo passo

Este resultado comprova integração local, não provisionamento AWS, funcionamento do EKS, CI remoto ou aceitação de todos os requisitos da Fase 4. Não houve execução Terraform. Nenhuma exportação New Relic foi testada.

O laboratório será reutilizado no passo 2 para comparar comportamento e comprovar traces HTTP/SQS. A limpeza final ficará restrita aos recursos descartáveis com o rótulo deste projeto; será registrada no relatório do passo 2 e no LOG.

Checklist: [x] base executada; [x] testes funcionais; [x] relatório/resumo antes da instrumentação; [ ] limpeza final compartilhada com o passo 2.
