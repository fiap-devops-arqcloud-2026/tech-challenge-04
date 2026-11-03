# Passo 1 — integração local e revalidação

TL;DR: os cinco serviços funcionam juntos no laboratório. O baseline anterior à instrumentação passou em 2026-10-22; a mesma regressão funcional passou novamente em 2026-10-27 com o código instrumentado final, antes da prova de traces.

Última atualização: 2026-10-27, Codex. Evidência: execução final encerrada às 11:03, America/Sao_Paulo (UTC-03:00).

## Explicação simples

O teste cadastra uma chave de acesso, cria flags e regras, pede avaliações e confere os dados realmente salvos. Depois altera uma flag e espera o cache vencer: a próxima avaliação precisa refletir a mudança. Por fim, verifica que os eventos atravessaram a fila e foram gravados pelo analytics.

Todos os cenários passaram. A instrumentação acrescentada no passo 2 preservou as respostas e o fluxo de negócio.

## Como foi aplicado

- Projeto Docker exclusivo: `tc04-integration`, em engine Linux 29.6.1.
- Base: `docker-compose.yaml` + `docker-compose.integration.yaml`, com `.env.example` fictício.
- Na revalidação final, acrescentou-se `docker-compose.otel.yaml`, sem trocar os endpoints locais de SQS/DynamoDB por AWS real.
- Comando da execução final: `bash scripts/test-observability.sh`; a primeira parte executa `scripts/integration/test-flow.py`, a regressão funcional da base.
- Moto simula SQS/DynamoDB; PostgreSQL e Redis são contêineres reais locais. A verificação consulta as APIs, o Redis e o armazenamento do consumidor, em vez de escrever o resultado esperado diretamente no banco.

| Verificação executada | Resultado |
|---|---|
| Saúde dos cinco microsserviços | Aprovada |
| Chave inválida rejeitada; chave criada aceita | Aprovada |
| Flags e regras persistidas | Aprovada |
| Flag ligada/desligada, regras 0%/100%, flag ausente e parâmetro ausente | Aprovada |
| Cache Redis e TTL de até 30 segundos | Aprovada |
| Atualização visível após espera de 31 segundos | Aprovada |
| SQS → analytics → DynamoDB simulado | Sete eventos esperados conferidos; fila esvaziada |
| Regressão funcional completa | Saída 0 |

## Ajustes e evidências

A execução inicial de 2026-10-22 exigiu explicitar `COMPOSE_PATH_SEPARATOR=:` para o Docker nativo do Windows reconhecer os dois arquivos Compose usados pelo Git Bash. O original foi preservado. Na reprodução OTel, também se preserva o caminho Linux do argumento de validação do Collector com `MSYS_NO_PATHCONV=1`.

- [Baseline anterior à instrumentação, 2026-10-22](RELATORIO_PASSO1_INTEGRACAO_LOCAL_2026-10-22_v01.md).
- Evidência final local: `qa-passos-locais-2026-10-27/passo2-compose-sql-final.log`.
- Resultado consolidado: [RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json](RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json).

## Limites e encerramento

O teste comprova o laboratório local; não comprova EKS, GitOps em execução, recursos da conta nova ou CI remoto. Nenhum Terraform plan/apply ou comando AWS foi executado.

O laboratório foi encerrado em 2026-10-27 às 11:04: 12 contêineres e dois volumes descartáveis do projeto de teste removidos, sem remover imagens ou evidências em bind mount. Conferência final: nenhum contêiner/volume com o rótulo do projeto permaneceu. O passo 2 detalha a prova de telemetria.

Checklist: [x] execução; [x] regressão; [x] evidência; [x] relatório/resumo; [x] limpeza do laboratório identificado.
