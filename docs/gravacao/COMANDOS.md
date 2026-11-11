# ⌨️ Comandos para a gravação

**Atualizado em 2026-11-10. Shell: Git Bash.** Para a sequência cena por cena, com túneis que se reabrem sozinhos e consultas do Loki conferidas no cluster, use [PASSO_A_PASSO_POR_CENA.md](PASSO_A_PASSO_POR_CENA.md). Execute um bloco por vez. Este arquivo é roteiro operacional; não é prova de execução. O ambiente, as tabelas, a chave e a flag `novo-painel` devem estar preparados antes de gravar.

## 1. Túneis, cada um em uma janela

```bash
# ArgoCD: mantenha o processo aberto.
kubectl -n argocd port-forward svc/argocd-server 8080:80
```

```bash
# Grafana: mantenha o processo aberto.
kubectl -n observability port-forward svc/grafana 3000:80
```

```bash
# Evaluation: recebe a requisição de demonstração.
kubectl -n togglemaster port-forward svc/evaluation-service 8004:8004
```

Se a porta já estiver ocupada, confira o túnel existente. Não encerre todos os processos kubectl, pois isso derrubaria os outros túneis. Faça login antes de gravar; não mostre comandos de extração de senhas.

## 2. Provas de infraestrutura

```bash
# Nós de trabalho.
kubectl get nodes
# Aplicações do ToggleMaster.
kubectl get pods -n togglemaster
# Componentes de observabilidade.
kubectl get pods -n observability
# Estado de sincronização e saúde no GitOps.
kubectl get applications -n argocd
```

## 3. Trace sem cache

O cache é por **nome da flag**, com TTL de 30 segundos (`services/evaluation-service/evaluator.go`). Trocar apenas `user_id` não garante um cache miss. O bloco abaixo cria uma flag exclusiva no ensaio, usando a chave já existente dentro do pod `trafego`; nenhum valor de chave é mostrado ou colocado no histórico do terminal local.

```bash
# Cria flag/regra exclusivas; anote o nome impresso, por exemplo video-1794240000.
kubectl exec -n togglemaster trafego -- sh -c 'NOME="video-$(date +%s)"; curl --fail-with-body -s -X POST http://flag-service:8002/flags -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"name\":\"$NOME\",\"description\":\"Demonstracao Fase 4\",\"is_enabled\":true}" && curl --fail-with-body -s -X POST http://targeting-service:8003/rules -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"flag_name\":\"$NOME\",\"is_enabled\":true,\"rules\":{\"type\":\"PERCENTAGE\",\"value\":100}}" && printf "\nFlag criada: %s\n" "$NOME"'
```

Na gravação, use o nome que foi realmente criado no lugar de `NOME_DA_FLAG_CRIADA`:

```bash
# Requisição de teste exibida no vídeo; depois procure seu horário no APM.
curl --fail-with-body -s "http://localhost:8004/evaluate?flag_name=NOME_DA_FLAG_CRIADA&user_id=video-1"
```

Selecione no New Relic o trace iniciado em `GET /evaluate`, com os cinco serviços, e expanda os spans. Um trace curto de cache é válido, mas não demonstra todas as dependências. O envio para o APM pode levar alguns segundos.

## 4. Logs no Loki

No **Grafana → Explore → Loki → Code**, execute:

```logql
{k8s_namespace_name="togglemaster"}
```

A consulta inicial mostra o namespace inteiro. Para focar um serviço, selecione seu rótulo disponível no Explore, sem presumir que o nome esteja no corpo de todas as linhas. Use um período com tráfego. Mostre a linha e o horário; um `trace_id` permite correlacionar logs e trace, quando presente.

## 5. Falha controlada e recuperação

Pré-condições: tráfego em HTTP 200; regra normal; serviço fora do cooldown de 600 s; PagerDuty, Slack e Actions acessíveis. O pod `trafego` deve conter a variável `CHAVE` já configurada na preparação.

```bash
# Terminal A: acompanha o tráfego durante a falha e a recuperação.
kubectl logs -f trafego -n togglemaster
```

```bash
# Terminal B: acompanha a troca do pod provocada pela automação.
kubectl get pods -n togglemaster -l app=flag-service -w
```

```bash
# Terminal C: ativa a falha transitória autenticada, sem exibir a chave.
kubectl exec -n togglemaster trafego -- sh -c 'curl --fail-with-body -s -X POST http://flag-service:8002/admin/fault -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"enabled\":true}"'
```

Espere: HTTP 503 → regra `FlagService5xxAlto` em Firing → incidente e Slack → run por `repository_dispatch` → `restarted` → pod Running → HTTP 200 → alerta normal/incidente resolvido. O `for: 1m`, a janela da métrica e o tempo do runner tornam a duração variável; ensaie antes.

Se a automação falhar, registre a falha e investigue o run. **Não apresente uma recuperação manual como automática.** Para encerrar apenas a falha controlada, use o bloco de contingência e identifique no vídeo que houve intervenção:

```bash
# Contingência manual; não conta como prova do self-healing.
kubectl exec -n togglemaster trafego -- sh -c 'curl --fail-with-body -s -X POST http://flag-service:8002/admin/fault -H "Authorization: Bearer $CHAVE" -H "Content-Type: application/json" -d "{\"enabled\":false}"'
```

Não mostre `kubectl describe pod trafego`, pois a variável pode conter uma chave. `Ctrl+C` encerra a visualização de logs/watch sem excluir os pods. Não faça destroy antes de capturar e revisar todas as evidências.
