# Pendências e progresso

TL;DR: o vídeo foi gravado em 2026-11-11 e o [relatório v03](../docs/relatorio/README.md) está pronto; falta só o link do vídeo. O cluster continua no ar por decisão do usuário (D-025). Os blocos antigos desta lista foram para o [arquivo morto](_ARQUIVO_MORTO/2026-11-09_blocos-historicos_v01/PENDENCIAS_blocos-ate-2026-11-09.md).

Última atualização: 2026-11-11, Claude (Opus 5.5).

## Pedido vigente — 2026-11-11 12:57, Claude

Pedido: relatório e prints exigidos pela FIAP, projeto atualizado, push na dev, PR para a main e merge. O cluster não será destruído agora.

- [x] Gravação do vídeo, por relato do usuário. A cadeia completa aparece nos registros: falha às 00:58:48, Firing às 01:00:50, restart às 01:01:09, HTTP 200 às 01:01:38 e Resolved às 01:03:00, com a execução 42956432177.
- [x] Relatório v03 em `docs/relatorio`, 17 páginas: capa com participantes, os quatro prints, justificativas, linha do tempo e matriz.
- [x] Índices `docs/relatorio/README.md` e `docs/evidencias/README.md`; README, requisitos, ARQUITETURA e roteiro atualizados.
- [x] Revisão do commit `e2e3930` do usuário: Grafana `$values`, eixo de 0 a 100%, logs dos Collectors e nomes dos workflows; CI da dev verde.
- [ ] Link do vídeo: preencher `video_url` em `docs/relatorio/dados-entrega.json`, gerar o PDF de novo e atualizar o README.
- [x] PR #2 dev → main com 29 checks verdes e merge em 2026-11-11 13:04 (`6c71277`); pipelines da main e sincronização da dev em seguida.
- [x] Depois do merge: alerta com `$values` no cluster, seis Applications Synced/Healthy e logs dos agents do Collector no Loki (REQ-OBR-08).
- [ ] **Usuário:** submeter código, vídeo e relatório no canal oficial (Q-05/Q-06).
- [ ] **Encerrar, quando o usuário decidir:** destroy de k8s e cluster com plano salvo e NAT desligado ([guia](02_TRABALHO/GUIA_DEPLOY_E_GRAVACAO_2026-11-09_v01.md), Parte 4). O cluster custa cerca de US$ 0,41/h ligado.

## Pedido anterior — 2026-11-09 20:26, Codex

Gravação prevista pelo usuário para **2026-11-10**. Revisão e fechamento em andamento; push dev, PR main e merge autorizados novamente. Ver entrada 20:26 do LOG para divisão de trabalho e verificação final.

Retomar pelo [handoff detalhado](02_TRABALHO/HANDOFF_GRAVACAO_2026-11-09_v01.md). Ensaio completo comprovado; serviço recuperado automaticamente. O controle do navegador foi interrompido por falha em confirmar a URL do Brave. Artefatos ainda em revisão; não publicar rascunho do relatório.

- [x] Enunciado e implantação atual conferidos; dev sincronizada com main.
- [x] Capturar os quatro tipos de evidência atuais; registrar limitações de enquadramento.
- [x] Ensaio automático EKS → Firing → PagerDuty/Slack → Actions → restart → HTTP 200.
- [ ] Corrigir annotation $$values e validar regressão; melhorar escala do gráfico.
- [ ] Roteiro intuitivo PDF + PowerPoint e relatório PDF.
- [ ] README, documentação e apresentação dos workflows.
- [ ] VERIFICAÇÃO dos artefatos, links, segredo e CI.
- [ ] Push dev, PR e merge main autorizados no pedido atual.
- [ ] Handoff e lista de complementos para o usuário.


## Retomada vigente — 2026-11-09, Claude

Feito em 2026-11-09, a pedido do usuário:
- [x] ArgoCD no chart 7.7.23 com a imagem v2.13.9, que corrige a CVE-2025-55190 (`1388e6d`, D-023).
- [x] P1 e P2, e as 89 cópias, pelo Codex (`e54023d`, `8526088`, D-022). PDFs da FIAP preservados, por decisão do usuário.
- [x] READMEs dos serviços e PyYAML sem uso (`a0ee523`).
- [x] P6 possível antes do deploy:
  - documentos públicos sem agentes, IDs internos e links ao diário (`3269b68`);
  - relatório da Fase 3 fora da árvore e `CLAUDE.md` em `.claude/` (`bed88f5`);
  - 116 auxiliares antigos no arquivo morto (`e94d8c9`).
- [x] P5: esta lista encurtada e retificações datadas em LEIA-PRIMEIRO, DOSSIE e ORGANIZACAO.
- [x] Conferências: histórico inteiro sem segredos (152 commits); plano real da base com 8 import, 29 add, 7 change e 0 destroy; CI verde.

A fazer:
- [ ] **Tópico 5, usuário:** subir o ambiente ([guia](02_TRABALHO/GUIA_DEPLOY_E_GRAVACAO_2026-11-09_v01.md), Parte 1).
- [ ] **Tópico 6, usuário:** ensaiar, gravar e tirar os prints (guia, Partes 2 e 3). O trial do PagerDuty vai até 2026-11-11, por relato.
- [ ] **Encerrar, com autorização:** destroy de k8s e cluster, conferir volumes EBS e desligar o NAT (guia, Parte 4). O destroy da base é decisão à parte.
- [ ] Depois do destroy confirmado: apagar os `.terraform` das 3 camadas e os `*.tfplan`.
- [ ] **B6, até 2026-11-16:**
  - relatório PDF: nomes, RMs, usernames, links, prints e justificativas (F3-P-059: não há gerador vigente);
  - links do vídeo e do relatório no README, e evidências do deploy nos READMEs;
  - matriz dos 42 em `docs/requisitos` com o estado real;
  - `docs/ARQUITETURA.md` e `docs/GUIA_DE_REPRODUCAO.md`: atualizar para a Fase 4 ou manter como históricos;
  - Q-03, Q-05 e Q-06: entrega individual ou em grupo, horário e canal, com o tutor;
  - F-022: revisão do `.trivyignore`, vencida em 2026-10-15;
  - fechamento documental de P-013 e P-014.
- [ ] **Decisão do usuário, repositório público:** o histórico do Git guarda nomes e RMs do grupo da Fase 3 e o ID da conta antiga. Tirar exige reescrever o histórico. Não há segredo nele (varredura de 2026-11-09).

Não aprovados, ficam como estão: IDs internos em comentários de código (workflows, Terraform e GitOps) e 39 menções a agentes nos 5 guias de estudo em HTML.

Limitações da aplicação, fora do exigido: F-017 (falha do targeting libera a flag no evaluation) e F-018 (o auth responde 401 a qualquer erro de banco). Registrar no relatório, se couber.

## Autorizações do usuário (2026-11-03)

- [x] D1 — Git autorizado: commits curados na dev e push para origin/dev. PR e merge para a main só no B3.
- [x] D2 — Não restaurar os 34 materiais da Fase 3 (remoção commitada em 9b3119a).
- [x] D3 — Log de 156 MB resumido em `offline-test-resumo.txt`. Com o "pode apagar" do usuário (2026-11-03), foi para a Lixeira do Windows, recuperável; esvaziar a Lixeira fica com ele. Os caches de cerca de 1,9 GB continuam.
- [x] D4 — Plano gratuito novo da AWS com US$ 100 de créditos. Se os créditos acabarem, a conta é suspensa; criar orçamento com alertas antes do B3.
- [x] D5 — Chaves gravadas no `.env` local (ignorado pelo Git).

D-020 e D-021 continuam valendo. Com o repositório público, o token do ArgoCD deixa de ir para o cluster (D-023).

## Calendário revisto em 2026-11-09

| Bloco | Data | Entrega |
|---|---|---|
| B3 e B4 | 2026-11-09 | Ambiente no ar, cadeia ensaiada e gravada |
| B5 | até 2026-11-10 | Vídeo revisado e destroy logo depois da gravação |
| B6 | até 2026-11-16 | Relatório PDF, documentação final, matriz dos 42 e envio |
| Entrega | até 2026-11-17 | Prazo informado pelo usuário; não consta no PDF |

Atualização de 2026-11-09 na tabela abaixo: F3-P-112, F3-P-114 e F3-P-122 foram resolvidos; F3-P-121, nos comentários citados; F3-P-104 e F3-P-105 saíram da árvore, mas seguem no histórico. As linhas abaixo mantêm o texto de 2026-11-01.

## Pendências herdadas da Fase 3 — triagem de 2026-11-01

Levantamento de 2026-11-01 a partir de `docs/00_COLAB_IA/`. Os originais ficam no commit 3b21e65 (`git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`) e no repositório tech-challenge-03. Caminhos "Fonte F3" são relativos a `docs/00_COLAB_IA/`. As linhas de código vêm da consolidação Claude em 2026-11-01; os números mudam conforme as edições. Não são uma nova auditoria dos serviços pelo Codex. A tabela só traz itens que ainda se aplicam ("sim") ou que podem se aplicar ("talvez").

| ID F3 | Pendência | Ainda se aplica? | Ação sugerida | Relação na Fase 4 |
|---|---|---|---|---|
| F3-D-015 | Desvio na topologia dos bancos: 2 RDS e o banco do targeting em StatefulSet, em vez de 3 RDS. O professor aceitou o arranjo em 2026-08-27, para a Fase 3, por causa do limite da conta antiga. Em 2026-09-09 o comprovante escrito não foi localizado. O arranjo continua no código (terraform/README.md:12; terraform/cluster/main.tf:74). Fonte F3: DECISOES.md (170-182); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (28). | sim | Verificar o limite de RDS na conta nova. Se o desvio continuar, justificá-lo no relatório da Fase 4. Nesse caso, registrar a ressalva do aceite verbal ou obter a confirmação do tutor por escrito. | DOC-01, DOC-08, P-003. docs/RELATORIO_DE_ENTREGA.md:41 e :48 (relatório histórico). |
| F3-P-059 | Gerador do PDF do relatório. Os dois geradores da Fase 3 só existem em `_ARQUIVO_MORTO`: gerar-relatorio-pdf_2026-09-11_v00.py (markdown e weasyprint) e build-report-fase3_2026-09-14.py (reportlab, o canônico desde 2026-09-14). As fontes da Fase 3 divergem sobre qual era o canônico. Em 2026-09-15 o reportlab não estava instalado, e o README apontava para um PDF em output/, pasta ignorada (link quebrado no GitHub). Não há gerador em scripts/. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (820-824); _ARQUIVO_MORTO/build-report-fase3_2026-09-14.py (3-21); LOG_DE_TRABALHO.md (196, 201). | sim | Geradores preservados no acervo integral; também recuperar por: `git show 3b21e65:docs/00_COLAB_IA/_ARQUIVO_MORTO/<arquivo>`. Escolher a ferramenta da Fase 4, com uma única fonte de texto, e testá-la cedo. O PDF final vai para uma pasta versionada; nunca linkar output/. | REQ-OBR-32 (relatório em PDF); DOC-01; P-015 B6. |
| F3-P-053 | Encerramento da conta da Fase 3. Inclui desativar usuários IAM e credenciais manuais, que os estados não removem. As camadas foram destruídas em 2026-09-15; restaram F3-P-100 e F3-P-101. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (208-218); LOG_DE_TRABALHO.md (67-71). | talvez | O usuário confere no console da conta antiga se ainda há custo e desativa as identidades manuais, sem usar essas credenciais no trabalho da Fase 4. No fim da Fase 4, repetir a limpeza na conta nova, conferindo o provedor OIDC antes de excluí-lo. | P-015 B5 (destroy depois da gravação); TFC-05. |
| F3-P-103 | Composição do grupo e acesso do avaliador. Na Fase 3 a confirmação independente não veio, e o [INCERTO] ficou no relatório. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (14); DECISOES.md (15). | sim | Confirmar com o tutor, por escrito, se a entrega é individual ou em grupo, e registrar no LOG com data. Garantir que o avaliador acesse o repositório 04 (privado) antes da submissão. Não copiar a tabela de integrantes da Fase 3. | D-009 (implementação solo) contra REQ-OBR-41 (em grupo) [INCERTO]; Q-03; DOC-08; TFK-11; B6. |
| F3-P-104 | Dados pessoais em material versionado. Um relatório preliminar arquivado traz usuários de Discord, e uma decisão da Fase 3 traz um caminho local com o nome do usuário. docs/RELATORIO_DE_ENTREGA.md (histórico) traz nomes e RMs dos integrantes. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (15). | sim | Na mescla, não copiar esses dados para a pasta vigente. Apagar docs/00_COLAB_IA não limpa o histórico do Git. O usuário decide se aceita o histórico como está, com o repositório privado. Reescrever o histórico só com pedido explícito. | DOC-12. |
| F3-P-105 | Metadado "generated using python-pptx" nas propriedades de docs/apresentacao/ToggleMaster_Fase3.pptx, que continua no repositório (conferido em 2026-11-01). Item opcional. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (16). | talvez | Decidir se a apresentação da Fase 3 fica no repo 04. Conferir metadados de gerador no material novo. | Ligada à regra de documento público, na linha abaixo. |
| Regra F3 (sem ID) | Documento público sem IA, assistentes, o nome 00_COLAB_IA ou códigos internos (D-, F-, P-, O-, R-, S-). O README da Fase 4 cita Codex (README.md:5) e D-009, D-012 e D-014 (README.md:14-16, 43, 184-186 e 226). terraform/README.md, gitops/README.md e observability/README.md também citam esses termos. O CLAUDE.md está versionado na raiz, contra 00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md:18. Fonte F3: INSTRUCOES_ASSISTENTES.md (39); LEIA-PRIMEIRO.md (28). | talvez | Resolvido pelo usuário em D-018: retirar referências internas dos documentos públicos na revisão B6/P-017. Manter diário e CLAUDE.md interno; não reescrever histórico. | P-015 B6; XCL-04. |
| F3-P-110 | Comentários desatualizados nos workflows reutilizáveis. Um fala em "git pull --rebase", mas o job refaz fetch e reset em laço. Outro diz "única permissão de escrita", mas jobs sem bloco permissions herdam o teto do chamador. Ainda em .github/workflows/_ci-go.yml:499 e :524 e em _ci-python.yml:529 e :554. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (24). | sim | Corrigir junto com F3-P-111 na dev. Levar à main só com a role do CI e o ECR da conta nova prontos (F3-P-140). | CIC-03, CIC-16. |
| F3-P-111 | Falta declarar permissions por job em build, lint, sast e sca. O topo dos workflows de serviço dá id-token: write e contents: write (ex.: .github/workflows/analytics-service.yml:76-82). Só image e gitops redefinem as permissões (_ci-go.yml:335 e :497). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (25). | sim | Declarar contents: read nos jobs de verificação. Aplicar a mesma regra ao workflow de self-healing. | CIC-03. |
| F3-P-112 (inclui P-024) | READMEs de services/ herdados da Fase 2: Go 1.21, Python 3.9, us-east-1 e chaves AWS estáticas. Em 2026-11-01: services/analytics-service/README.md:16-17, :52 e :58; services/evaluation-service/README.md:57 e :60; services/flag-service/README.md:11. A região do projeto é us-east-2. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (26); INSTRUCOES_ASSISTENTES.md (116); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (160-161, 414). | sim | Reescrever junto com a documentação da instrumentação OTel, sem chaves estáticas e com a região certa. Qualquer edição em services/&lt;svc&gt;/** dispara o pipeline e, na main, tenta OIDC. Por isso, agrupar com outra mudança do serviço. | DOC-07; CIC-16. |
| F3-P-113 | Flask, gunicorn e setuptools sem versão fixa em services/analytics-service/requirements.txt (:1, :2 e :5). As dependências OTel do mesmo arquivo já estão fixadas. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (27). | sim | Fixar versões compatíveis com Python 3.12. Depois, rodar de novo o SCA e o ensaio local. | CIC-11; D-016. |
| F3-P-114 | PyYAML==6.0.1 em services/flag-service/requirements.txt:8. É sobra da demonstração de CVE; o serviço não usa YAML. As fontes divergem: o guia de 2026-09-11 mandava remover, e o plano de 2026-09-15 mandava manter até a Cena 6. O Apêndice B do guia histórico usa essa linha (docs/GUIA_DE_REPRODUCAO.md:746-841). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (28); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (980-982); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (414-415). | sim | Decidir se a demonstração de CVE entra no vídeo da Fase 4. Se não entrar, remover a dependência. A mudança gera imagem nova na main. | Sem achado P-015 específico. |
| F3-P-115 | Comentários ainda citam o ESO e o externalsecret.yaml: gitops/base/auth-service/deployment.yaml:67-68, gitops/base/evaluation-service/deployment.yaml:61 e gitops/base/flag-service/deployment.yaml:51. Os Secrets vêm de terraform/k8s/secrets.tf. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (29). | sim | Corrigir quando os deployments receberem as variáveis OTEL_*. | GIT-08, GIT-02. |
| F3-P-120 | terraform/terraform.tfvars.example:41 traz enable_nat_gateway = false, ao contrário do padrão true. Copiado sem ajuste, quebra uma recriação do zero: os pods ficam em ImagePullBackOff. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (35); INSTRUCOES_ASSISTENTES.md (129). | sim | Corrigir o exemplo ou garantir true no tfvars local da base antes do primeiro apply. | XCL-03, TFK-10; B2. |
| F3-P-121 | Comentários sobre EKS 1.31, "repositório privado" e "evita o provider helm", além da ordem das camadas sem a k8s: terraform/modules/eks/main.tf:73-74, terraform/cluster/main.tf:55, terraform/modules/eks/variables.tf:24 e terraform/cluster/outputs.tf:27. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (36). | sim | Corrigir antes do apply, junto com a revisão de versão do EKS (F3-P-131). | TFC-03, TFC-06. |
| F3-P-122 | Comentário cita o GUIA-AWS.md da Fase 2, que não existe (terraform/modules/messaging/main.tf:90). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (37). | sim | Remover a referência. | CIC-16. |
| F3-P-123 | ecr_image_tag_mutability = MUTABLE (terraform/variables.tf:143; terraform/terraform.tfvars.example:63). Os ECR da conta nova foram criados à mão, e o inventário autenticado de 2026-10-28 confirmou MUTABLE; revalidar antes da adoção pelo Terraform. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (38). | sim | Decidir entre MUTABLE e IMMUTABLE antes do import dos ECR, para o plan não propor mudança inesperada. | TFB-01, XCL-03. |
| F3-P-124 (inclui P-049/F-048) | scripts/security-check.sh desatualizado. A exclusão ':!*.example.*' não cobre .env.example (:51). A regra de conta legada só procura o ID da Fase 2 (:70-78). Um comentário traz o ID da Fase 3 (:11). O script não cobre os segredos da Fase 4. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (39); LOG_DE_TRABALHO.md (251). | sim | Bloquear &lt;CONTA_FASE3&gt; sem escrever o ID em claro e tirá-lo do comentário. Cobrir chaves de New Relic, PagerDuty e Slack. Avaliar varredura de segredos no CI. | CIC-05, XCL-14. |
| F3-P-130 | Revisar as 3 exceções do perl-base no .trivyignore. A revisão estava marcada para 2026-10-15 e venceu (.trivyignore:58). As imagens Python ganharam dependências OTel. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (45); INSTRUCOES_ASSISTENTES.md (105). | sim | Rodar o Trivy, na versão usada pelo CI, sobre as imagens finais. Manter ou remover cada exceção, com nova data (exp: na própria linha). | CIC-08; F-022. |
| F3-P-131 (inclui P-050/F-049) | Versão do EKS e estimativa de custo. Fora do suporte padrão, o plano de controle custa 6 vezes mais: US$ 0,60/h contra US$ 0,10/h (registro de 2026-09-15). O fim do suporte padrão do 1.34 diverge entre as fontes: 2026-12-01 (Fase 3) ou 2026-12-02 (P-015, TFC-03) [INCERTO]. As duas datas ficam depois da entrega. A estimativa de 2026-09-11 (US$ 0,385/h; US$ 281,03/mês) não inclui a observabilidade. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (46); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (1589-1592). | sim | Antes do apply, rodar `aws eks describe-cluster-versions` e avaliar upgrade_policy STANDARD. Refazer a estimativa e o print na conta nova, com data. | TFC-01, TFC-03, XCL-10, DOC-01. |
| F3-P-132 | Cerca de 30 dias depois de cada run [INCERTO], o GitHub deixa de aceitar gh run rerun dos runs de push na main. workflow_dispatch não publica imagens. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (47); INSTRUCOES_ASSISTENTES.md (123). | talvez | Publicar as imagens por commit na main do repo 04 (B3), com autorização. | CIC-13, GIT-03. |
| F3-P-140 | Ordem de merge na main. Mudanças em services/** ou .github/workflows/** que chegam à main antes da role OIDC e do ECR geram runs vermelhos. Em 2026-09-14 o flag-service falhou ao assumir a role. Na Fase 4, a role foi criada à mão e conferida no inventário P-013 de 2026-10-28, e o CI remoto não foi testado. Fonte F3: LOG_DE_TRABALHO.md (14, 107); DECISOES.md (12, 24). | sim | Levar à main só depois de conferir role, ECR e Variables. É uma ordem de execução, não uma proibição de editar na dev. | XCL-08; B3. |
| F3-P-040 (inclui F-047) | Preencher o overlay prod depois do apply: REDIS_URL, AWS_SQS_URL, ARNs de IRSA e imagens. Hoje os valores são sentinelas (gitops/overlays/prod/patches/endpoints.yaml:31, :39 e :49). A hipótese sobre o identificador do ElastiCache não foi confirmada. Fonte F3: LOG_DE_TRABALHO.md (250, 288); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (260-285). | sim | Substituir pelos outputs reais, conforme gitops/README.md:24-36, e conferir a cada recriação. | GIT-03, TFK-03. |
| F3-P-041 (inclui P-042 e P-047/F-044) | Ensaio completo com o cluster no ar: apply das camadas, schemas de auth e flag nos RDS, seed (chave, SERVICE_API_KEY, flag e regra), ArgoCD Synced/Healthy e uma tag nova sincronizada. RDS novos nascem vazios. Schemas e seed manuais levavam cerca de 15 min por sessão. Fonte F3: LOG_DE_TRABALHO.md (271, 305); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (331-345); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (1003-1012). | sim | Incluir no runbook da Fase 4 e avaliar um Job ou script. No primeiro apply, medir o tempo de criação da base do zero. Esse tempo nunca foi medido; o guia reservava 10 min. | B3, B4, DOC-02; F-021. |
| F3-P-046 (F-043) | Instalar o ArgoCD (CRD) separado da criação da Application: etapa A com -target=helm_release.argocd e etapa B em seguida. O procedimento histórico resolve isso (docs/GUIA_DE_REPRODUCAO.md:446-452), mas nunca foi ensaiado na conta nova. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (42-48). | sim | Manter as duas etapas no runbook e ensaiá-las no B3. | TFK-05. |
| F3-P-048 (F-046) | Dono único da SERVICE_API_KEY, para que apply ou restart não desfaçam o seed. O desfecho na Fase 3 não foi confirmado [INCERTO]. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (58-70); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (39, 51). | sim | Definir quem grava a chave (Terraform ou passo manual). Testar o reinício do evaluation depois do seed. O self-healing reinicia pods, e com a chave provisória o /evaluate responde 502. | CIC-01, GIT-07. |
| F3-P-052 (inclui P-051) | O robô do CI faz push de tags direto na main, e o GitHub não tinha proteção de branch. A disciplina dev → PR → main era só processual. Foi encerrada na Fase 3 como exceção intencional (F3-D-021). O push na main continua em .github/workflows/_ci-go.yml:606 e _ci-python.yml:636. Fonte F3: DECISOES.md (65-109); LOG_DE_TRABALHO.md (265, 284). | sim | Decidir a política (push do robô ou PR de promoção) antes de ativar a proteção e antes de criar o workflow de self-healing. Não alterar regras remotas sem autorização. | CIC-07, XCL-08, CIC-01. |
| F3-P-034 | Runbook de sessão e de custo: subir, semear, gravar e derrubar a camada cara. Não há roteiro vigente para a conta nova. O guia importado é da Fase 3 e tem comandos incompatíveis com o código atual. Fonte F3: LOG_DE_TRABALHO.md (389); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (7). | sim | Escrever o runbook da Fase 4 com a stack de observabilidade, no formato que funcionou em 2026-09-15. Medir tempos e custos em vez de copiá-los. | DOC-02; F-021. |
| F3-F-014 | ID da conta no nome do bucket e em arquivo versionado. Na Fase 3 foi um risco aceito, mitigado com repositório privado. Na conta nova está mitigado: bucket e região ficam em backend.hcl ignorado (terraform/README.md:17). O ID da Fase 3 ainda aparece em docs/GUIA_DE_REPRODUCAO.md (10 ocorrências), em scripts/security-check.sh:11 e em cópias em 00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879 e 02_TRABALHO. Fonte F3: LOG_DE_TRABALHO.md (423); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (416). | talvez | Decidir antes de dar acesso ao avaliador. Avaliar a troca do ID por marcador no guia histórico. Remover docs/00_COLAB_IA reduz as ocorrências, mas não limpa o histórico. | DOC-12, XCL-14. |
| F3-S-03 (S-03, S-04, S-07, R-08) | Sugestões não implementadas na Fase 3: scan de IaC (Checkov, tfsec ou Trivy config), Prowler, CloudTrail e logs do EKS, SonarCloud. Até onde foi conferido, o enunciado da Fase 4 não as exige. Fonte F3: _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (99, 103, 112-116). | talvez | Avaliar só o que tem justificativa direta (scan de IaC e logs do plano de controle do EKS). Não inflar o escopo. | CIC-06, TFC-07. |

Não se aplicam à Fase 4:

- F3-P-100: excluir o bucket de estado da Fase 3 (togglemaster-tfstate-&lt;CONTA_FASE3&gt;-us-east-2-an).
- F3-P-101: excluir a VPC da Fase 2 que sobrou na conta antiga.
- Os dois são da conta antiga, proibida na Fase 4. Ficam como limpeza e possível custo, a critério do usuário e fora deste repositório. A exclusão do bucket é permanente.
- F3-P-102: vídeo e relatório da Fase 3. Não preencher o relatório histórico. Lição para a Fase 4: incluir no relatório o link do vídeo testado em aba anônima.
- F3-P-074: a referência histórica ao bootstrap não deve reabrir a criação do bucket novo. Na Fase 4 ele foi confirmado completo pelo usuário em 2026-10-30; proteções, nome e tags ainda não foram consultados pelo agente nesta retomada. Backend local existe; init/import/apply não executados.
- F3-P-035/P-036: addons, StorageClass gp3 e instalação do kustomize standalone para editar a tag existem no código. Isso não resolve o gate de renderização dos manifests no CI (F-029/CIC-09), que permanece pendente.
- F3-F-050: conflito sobre o destroy da camada k8s, já resolvido em terraform/README.md:65.
- F3-R-04: testes unitários, superado. Em 2026-10-27 foram aprovados 13 testes Go principais, oito subtestes e 20 testes Python.
- F3-RELATORIO-9: badge do Google Cloud Skills Boost, sem equivalente na Fase 4.
## P-017 — Aplicar política pública e retificações da mescla (pendente, 2026-11-01)

- [x] Resolver conflito de autoria/IDs internos: usuário escolheu diário interno; decisão D-018.
- [ ] Na revisão B6, retirar referências a assistentes e IDs internos dos READMEs/documentos públicos vigentes, preservando histórico e créditos/licenças legítimos.
- [ ] Corrigir justificativas nos comentários de Terraform: use_lockfile existe desde 1.10.0; >=1.11.0 é escolha do projeto. Não é necessário baixar a restrição de versão. Bucket Key não é recurso SSE-S3.
- [x] Resolvido em 2026-11-09 (D-023). Antes do deploy, escolher versão mantida e corrigida do ArgoCD; 7.7.11 → appVersion v2.13.2 e CVE-2025-55190 confirmados por fontes oficiais em 2026-11-01. Não houve teste de exploração nem implantação nesta retomada (TFK-02).
- [ ] Revisar runbook futuro: diagnóstico antes de apagar recursos; plano salvo com aprovação antes de aplicar; não imprimir prefixos de chaves nem transportar DATABASE_URL em argumentos visíveis. Diferenciar intervalo de reconciliação de prazo garantido.

Fontes e rastreabilidade: [relatório](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md) e [índice completo](02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/INDICE_RASTREABILIDADE_2026-11-01_v01.md). São melhorias/retificações, não novas exigências da FIAP. 39 registros de pendências herdadas incluem duplicatas e itens fora da Fase 4; não somá-los aos 42 requisitos.
