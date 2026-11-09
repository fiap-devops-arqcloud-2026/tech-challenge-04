"""Relatório P-016 derivado do snapshot, decisões e verificações preservadas."""
from pathlib import Path
from urllib.parse import quote
import json

ROOT=Path(__file__).resolve().parents[3]
WORK=Path(__file__).resolve().parent
snap=json.loads((WORK/'snapshot-retomada-codex.json').read_text(encoding='utf-8'))
arc='../_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA'
out=WORK.parent/'MESCLA_COLAB_FASE3_2026-11-01_v01.md'
prefix=WORK.name
result_path=WORK/'verificacao-codex-depois.json'
result=json.loads(result_path.read_text(encoding='utf-8')) if result_path.exists() else None
finished=bool(result and result['ok'])

body=f'''# Mescla da colaboração Fase 3 → Fase 4

TL;DR: a memória útil da Fase 3 foi incorporada à colaboração atual, com 59 decisões identificadas e um índice de 158 conhecimentos/39 registros de pendências. Os 39 originais são preservados integralmente no arquivo morto. A regra pública foi confirmada pelo usuário: nomes de assistentes e IDs internos ficam no diário. {'Consolidação, arquivamento e verificações concluídos.' if finished else 'Incorporação concluída; arquivamento e verificação final em execução.'}

Última atualização: 2026-11-01, Codex (continuação dos rascunhos e extrações de Claude).

## Resultado em linguagem simples

Havia dois diários no projeto: o atual e um importado da Fase 3. O Claude extraiu o conteúdo e foi interrompido antes de terminar a organização. Esta retomada aproveitou essa extração, revisou as sínteses e reuniu o que ajuda a decidir no diário atual. O diário antigo fica guardado, com todos os arquivos, para consulta e recuperação.

Isso conclui a organização do contexto (P-016), não a entrega técnica da Fase 4. A aplicação ainda precisa da stack no EKS, integração externa com New Relic, alertas/PagerDuty/Slack, self-healing e evidências. O lint foi medido pelo Claude, mas sua correção funcional não foi aplicada nesta tarefa.

## Escopo, autorização e estado observado

- Pedido de mesclar e retirar a pasta redundante: registrado pelo Claude no LOG de 2026-11-01 à tarde; retomada solicitada diretamente ao Codex em 2026-11-01. D-017 registra o método e a preservação.
- Repositório real: `C:/Users/Gabriel/Documents/GitHub/tech-challenge-04`; branch `dev`; HEAD `{snap['head']}`; main `{snap['main']}`. Snapshot inicial às {snap['date']}.
- Sem commit, stage, push, PR, mudança de main, aplicação Terraform, consulta autenticada AWS/GitHub, execução de containers ou envio de notificações nesta retomada. Fontes públicas técnicas foram consultadas para as retificações abaixo.
- O escopo de escrita foi contexto, auxiliares da mescla e movimentação local da pasta redundante. README público, código dos serviços, workflows, Terraform, GitOps e materiais FIAP não foram editados.
- As **34 ausências preexistentes** fora de docs/00_COLAB_IA continuam como estavam. Elas não fazem parte dos 39 arquivos desta mescla nem foram aprovadas para commit.

## Conteúdo incorporado e onde continuar

| Conteúdo | Volume da extração | Destino |
|---|---:|---|
| Decisões numeradas e sem número original | 59 = 24 F3-D + 35 F3-SN | [DECISOES](../DECISOES.md), todas com contexto/data, motivo, alternativas, ressalvas e fonte |
| Conhecimentos técnicos, custos históricos, operação e gravação | 122 | [DOSSIE, seção 20](../DOSSIE_CONTEXTO.md) |
| Regras de colaboração/evidência e de organização | 14 + 6 | [LEIA-PRIMEIRO](../LEIA-PRIMEIRO.md) e [ORGANIZACAO](../ORGANIZACAO_DE_PASTAS.md) |
| Conhecimentos que geram pendência | 3 | [PENDENCIAS](../PENDENCIAS_E_PROXIMOS_PASSOS.md), herança F3 e P-017 |
| Conhecimentos apenas históricos | 13 | Índice e extrações preservadas; não viram requisitos da Fase 4 |
| Registros de pendências na consolidação | 39 | Índice completo e tabela herdada no backlog; contém duplicatas/itens inaplicáveis |
| Colisões e divergências | 50 registros brutos, agrupados em 26 temas pelo Claude | Triagem por tema abaixo; não são 50 bloqueios novos |

Os 158 itens são unidades da extração, não número de parágrafos nem requisitos novos. O [índice de rastreabilidade]({prefix}/INDICE_RASTREABILIDADE_2026-11-01_v01.md) lista todos, incluindo 39 registros de pendência. Os JSONs originais contêm fonte/linha e a análise anterior; eles permanecem **rascunhos históricos** onde discordam da revisão final. PROC-A-01/F3-P-059 e PF3-01/F3-D-015 se sobrepõem.

A classificação original das 59 decisões era 23 vigentes, 26 a revisar, 6 superadas e 4 históricas. Ela é preservada para comparação, sem transformar “vigente” em execução comprovada. F3-SN-03, por exemplo, não proíbe o padrão de bucket com conta/região; apenas o identificador da conta antiga deve ser abandonado. Não houve colisão com D-001–D-018 da Fase 4.

## Retificações feitas na síntese

1. **Lock do S3:** `use_lockfile` foi introduzido no Terraform 1.10.0; >=1.11.0 é a restrição escolhida no código. O comentário em terraform/backend.tf:17 ainda precisa ser ajustado, sem necessidade de baixar a versão. Fonte consultada em 2026-11-01: [release oficial 1.10.0](https://github.com/hashicorp/terraform/releases/tag/v1.10.0).
2. **Criptografia:** S3 Bucket Keys pertencem ao SSE-KMS, não ao SSE-S3. Corrigida a síntese do bootstrap; não alterada a configuração do bucket. Fonte consultada em 2026-11-01: [AWS — S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html).
3. **ArgoCD:** terraform/k8s/variables.tf:95 fixa chart 7.7.11. O [Chart.yaml oficial](https://github.com/argoproj/argo-helm/blob/argo-cd-7.7.11/charts/argo-cd/Chart.yaml) indica appVersion v2.13.2. Essa versão antecede 2.13.9, correção da [CVE-2025-55190](https://github.com/argoproj/argo-cd/security/advisories/GHSA-786q-9hcg-v9ff), sobre acesso indevido a credenciais de repositórios por tokens autorizados a projetos. Fonte confirmada em 2026-11-01; não se comprovou implantação, exploração ou exposição atual. TFK-02 permanece para implementação.
4. **Segredos:** removida a sugestão de imprimir prefixos de chaves. Registrado o risco de URL de banco em argumentos de psql/pod e de arquivos de plano/recuperação com dados sensíveis. Não há cópia de valores para as sínteses novas.
5. **Git:** retirada a afirmação de que editar qualquer coisa na dev seria livre. Autorização de importação passada não é autorização permanente de commit/push. O reset --hard do job não deve ser usado no checkout de trabalho.
6. **Estado atual:** não repetir que role/OIDC/ECR só existem por relato: há inventário autenticado de 2026-10-28 (34/34) e teste do trust local (8/8). Bucket segue confirmado pelo usuário em 2026-10-30, não por esta retomada.
7. **Kustomize:** instalação para editar uma tag já existe no CI; gate para renderizar/validar os manifests ainda falta (F-029/CIC-09). São tarefas diferentes.
8. **Operação:** intervalo de reconciliação não é prazo máximo de recuperação; tags diferentes por serviço não comprovam falha; NAT não é requisito universal de acesso ao endpoint privado do EKS; apply parcial exige conferir state e recursos antes de repetir. Diagnósticos históricos não autorizam apagar pods/Secrets/discos.
9. **Contagem de Secrets:** secrets.tf tem cinco recursos, incluindo postgres_targeting; não seis nem um Secret de analytics. Novas credenciais SaaS ainda precisam de contrato.
10. **Evidência e contagens:** P-015 trata 44 itens = 42 obrigatórios + 2 opções; P-014 trata 42 obrigatórios. Teste local concluído pode receber [x] no próprio escopo sem alegar prova de AWS. Preços, créditos, restrições da conta antiga e CVEs antigos não foram promovidos a fatos atuais.

As correções constam das novas sínteses e ressalvas; registros históricos originais não foram reescritos. Há 33 substituições textuais de revisão no dossiê, listadas em [incorporacao-codex.json]({prefix}/incorporacao-codex.json). Nem toda alteração de redação é um achado independente.

## Triagem dos 26 temas de divergência

| Tema | Resultado em 2026-11-01 / próximo tratamento |
|---|---|
| 1. Posse do OIDC manual | P-003/B2: decidir import ou reutilização como data source; não copiar false da conta antiga sem plano |
| 2. Bancos e tipo de nó | Limite/aceite da Fase 3 não transferidos; confirmar capacidade e justificativa na conta atual |
| 3. Dois nós no código versus três no plano | Dimensionar stack e custo antes do deploy; sem alteração nesta mescla |
| 4. Port-forward versus Ingress | Saídas para SaaS não obrigam Ingress por si; consolidar o fluxo escolhido no runbook vigente |
| 5. IDs colidentes | Resolvido na memória: F3-D/F3-P/F3-F/F3-SN; comentários no código ainda serão alinhados |
| 6. Fluxo humano versus robô e publicação | Escopos distintos, não autorização nova; dev → PR → main humano e exceção do robô registrada |
| 7. Self-healing versus CI sem deploy | Definir role/access entry/RBAC próprios; os jobs de imagem já usam AWS por OIDC |
| 8. Congelamento antigo de serviços/workflows | Restrição de outra sessão não anula pedidos posteriores; esta mescla não edita código |
| 9. Referências a IA/IDs em documentação pública | **Resolvido pelo usuário: D-018.** Aplicação aos documentos públicos no B6/P-017 |
| 10. SECURITY.md e trust antigo | F-023 corrigido na árvore local; documentação/publicação ainda pendentes |
| 11. Segredos de terceiros | Ampliar contrato e armazenamento protegido; não confundir ausência de chave AWS estática com ausência de segredos |
| 12. phase=3 e parâmetros antigos | Fase 4 usa phase=4 e phase4/prod; revisar roteiro/consultas, sem editar acervo |
| 13. Data do suporte EKS 1.34 | [INCERTO] fontes divergem 2026-12-01/2026-12-02; consultar AWS antes de aplicar |
| 14. Chart antigo e HPA/Argo | CVE confirmada documentalmente; atualizar versão e tratar disputa de réplicas na implementação |
| 15. Revisão vencida de Trivy | Remedir artefatos finais; não ampliar exceções sem avaliação |
| 16. Repositório privado e credencial ArgoCD | Snapshot remoto de 2026-10-28; conferir credencial somente leitura antes do bootstrap |
| 17. Custos entre sessões | Definir o que preservar/destruir junto da propriedade dos recursos importados |
| 18. 34 materiais ausentes | Permanecem pendentes e distintos dos 39 arquivos arquivados nesta tarefa |
| 19. Dois geradores PDF | Ambos preservados; escolher um quando produzir relatório da Fase 4 |
| 20. Individual versus grupo | Confirmação do tutor ainda pendente; não copiar nomes/identificação da Fase 3 |
| 21. Script de segurança legado | Revisar política e padrões SaaS; evitar falso positivo por acervo/histórico |
| 22. Entregáveis antigos | Aplicar enunciado Fase 4, vídeo até 25 min; prazo 2026-11-17 vem do usuário |
| 23. Teto do provider | Justificativa antiga é [INCERTO]; reavaliar constraints/lockfiles em tarefa de IaC |
| 24. Gatilhos CI na documentação | Workflows atuais prevalecem sobre descrição da Fase 3; corrigir docs vigentes no B6 |
| 25. Memória global | Regra atual prevalece: só com pedido direto; nenhuma atualização global nesta sessão |
| 26. Cookies do capturador antigo | Script preservado, não executado; corrigir comportamento se reutilizado |

## De-para dos originais

De `docs/00_COLAB_IA/` para [`{arc}`]({arc}/). A estrutura interna foi mantida; o movimento não descarta bytes. Os links internos históricos podem depender da localização antiga e não foram reescritos no acervo. Cada arquivo também é recuperável com `git show 3b21e65:docs/00_COLAB_IA/CAMINHO`.

O manifesto registra os hashes SHA-256 dos bytes do checkout; os blobs Git também foram conferidos, considerando a normalização LF/CRLF. Assim, diferença de tamanho em uma extração anterior não é tratada como perda. São {sum(x['bytes'] for x in snap['originals']):,} bytes preservados.

| Arquivo relativo na origem/destino | Bytes do checkout | SHA-256 (prefixo; completo no manifesto) |
|---|---:|---|
'''
manifest=[]
for e in snap['originals']:
    rel=e['path'].removeprefix('docs/00_COLAB_IA/')
    body+=f"| [{rel}]({quote(arc+'/'+rel)}) | {e['bytes']} | `{e['sha256'][:16]}` |\n"
    manifest.append({**e,'destino':'00_COLAB_IA/'+arc.removeprefix('../')+'/'+rel})
(WORK/'manifesto-arquivamento.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
body+=f'''
Manifesto completo: [manifesto-arquivamento.json]({prefix}/manifesto-arquivamento.json). Cópias anteriores dos sete documentos editados: [`retomada-codex-1809`](../_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/retomada-codex-1809/). Backups anteriores do Claude também foram preservados.

## Verificações e limites

'''
if finished:
    c=result['checks']
    body+=f'''- Verificador independente aprovado: **{c['originals']}/39 originais com SHA-256 idêntico**, árvore de origem removida, blobs Git recuperáveis e 39 remoções locais esperadas.
- **{c['preserved_other_files']} outros arquivos anteriores inalterados** por hash; **{c['preexisting_absences']} ausências preexistentes preservadas**. HEAD, main, branch e índice sem alteração.
- **{c['decision_ids']} decisões F3 únicas**, 158 itens no índice, 39 registros de pendência, **{c['local_links']} links locais** e **{c['source_references']} referências estruturadas de origem** conferidas. Linhas de origem dentro do alcance dos arquivos. Links históricos em crases e URLs externas não fazem parte dessa contagem de links locais.
- Histórico anterior do LOG preservado integralmente; novos documentos em UTF-8, sem marcador de verificação pendente. Dados de participantes/conta antiga não propagados às sínteses novas no escopo dos padrões verificados.
- Resultado detalhado: [verificacao-codex-depois.json]({prefix}/verificacao-codex-depois.json). Verificador original Claude executado separadamente; sua saída está no diretório de trabalho.
'''
else:
    body+='Validação final em execução; o resultado será registrado após verificar os destinos e arquivar os originais. Nenhuma declaração de aprovação deve ser inferida deste estado intermediário.\n'
body+=f'''
Limites: o Claude registrou leitura integral de 31 arquivos textuais; os 7 PNGs e 1 PDF foram inventariados, não reinspecionados visualmente nesta mescla. A retomada reviu as sínteses e referências, sem refazer a leitura integral de cada original. Hash comprova preservação, não fidelidade semântica de toda frase. Nem todos os 112 achados da P-015 foram revalidados. O arquivo morto preserva dados antigos já presentes no repositório; o movimento não é saneamento de histórico nem certificação global de ausência de segredos. O guia SaaS anterior foi preservado e não constitui prova de integração executada.

## Handoff: onde retomar

1. P-016 {'concluída' if finished else 'em fechamento'}: não repetir a extração, importar código novamente ou recriar a pasta histórica ativa.
2. Próxima frente funcional: B0 (F-024, lint, decisões de Git/34 ausências e contas); depois E1 externa com New Relic. Não enviar chaves ao chat; configuração local protegida. O trial PagerDuty termina aproximadamente em 2026-11-11 por relato; confirmar a data real na conta.
3. Antes da AWS: P-003/B2 para tfvars, posse/import dos recursos manuais, orçamento e plano; depois stack, alertas e self-healing. Não foi executado init/import/plan/apply real nesta retomada.
4. P-013 e P-014 têm resultados salvos e fechamento documental pendente. Usar [catálogo Codex](auditoria-codex-2026-10-30_v01/CATALOGO_ACHADOS.md), [matriz Codex](auditoria-codex-2026-10-30_v01/MATRIZ_REQUISITOS.md) e [análise Claude](ANALISE_COMPLETA_FASE4_2026-10-31_v01.md); comparar escopos, não somar achados duplicados. F-031 (variáveis do terminal herdadas pelo ensaio) não tinha equivalente na P-015.
5. P-017/B6 aplica D-018 aos documentos públicos e revisa os comentários/explicações apontados. O usuário já decidiu a regra pública: não perguntar novamente.

LOG + PENDENCIAS indicam o estado e as próximas ações; DOSSIE/DECISOES e este relatório fornecem fontes e ressalvas. Nenhum evento às 19:00 foi agendado e nenhuma mensagem foi enviada ao Claude.
'''
out.write_text(body,encoding='utf-8')
print(json.dumps({'report':str(out),'final':finished,'source_files':len(manifest)},ensure_ascii=False))
