# 📄 Relatório de entrega — Fase 4

TL;DR: o PDF a submeter é o [**RELATORIO_ENTREGA_2026-11-11_v03.pdf**](RELATORIO_ENTREGA_2026-11-11_v03.pdf), com 17 páginas em A4 paisagem. Ele cobre tudo o que o enunciado pede para o relatório (p. 6). **Antes de submeter, inclua o link do vídeo** e gere o PDF de novo, como descrito abaixo.

Última atualização: 2026-11-11.

## O que o PDF contém

| Exigência do enunciado (p. 6) | Onde está no PDF |
|---|---|
| Nomes, RMs e usernames | Capa |
| Links do repositório e do vídeo | Capa (o link do vídeo depende da publicação) |
| Print do dashboard do Grafana | p. 6–7 |
| Print de um trace distribuído no APM | p. 8–9 |
| Print da notificação de incidente no ChatOps | p. 10 |
| Print do log e da execução do self-healing | p. 11–12 |
| Justificativa: arquitetura do OTel | p. 3 |
| Justificativa: Datadog × New Relic e OpsGenie × PagerDuty | p. 4 |

O PDF também traz:
- a linha do tempo da falha gravada no vídeo (p. 5);
- os prints de apoio: Firing, PagerDuty, ArgoCD e Lens (p. 13–14);
- a matriz de todos os requisitos, com o lugar de cada prova (p. 15–16);
- os limites conhecidos e as referências (p. 17).

## De onde vêm os dados

- **Prints:** ensaio integrado de 2026-11-09, na mesma implantação. Índice em [evidências](../evidencias/README.md). O PDF só recorta as imagens para ampliar a região que comprova cada item; não edita o conteúdo.
- **Linha do tempo da gravação de 2026-11-11:**
  - logs dos pods `trafego` e `flag-service` no Loki;
  - log da [execução 42956432177](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42956432177);
  - mensagens do canal `#incidentes-tech-challenge` lidas pela API do Slack.
- **Identificação, links e horários:** [dados-entrega.json](dados-entrega.json).

## Incluir o link do vídeo e gerar o PDF

1. Preencha `video_url` em [dados-entrega.json](dados-entrega.json) com o link público ou não listado.
2. Na raiz do repositório, rode o gerador. Ele usa Python com Pillow e o Microsoft Edge em modo headless:

```bash
py -3.14 -B 00_COLAB_IA/02_TRABALHO/entrega-relatorio-2026-11-11_v03/build_relatorio.py
```

3. Abra o PDF e confira o link na capa antes de submeter.

## Versões anteriores

[v01](RELATORIO_ENTREGA_2026-11-09_v01.pdf) e [v02](RELATORIO_ENTREGA_2026-11-10_v02.pdf) eram rascunhos de antes da gravação e ficam só como histórico.
