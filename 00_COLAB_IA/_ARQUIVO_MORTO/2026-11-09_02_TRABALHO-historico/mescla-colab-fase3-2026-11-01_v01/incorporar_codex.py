"""Incorpora P-016 a partir de rascunhos preservados. Não modifica código nem Git."""
from pathlib import Path
from collections import Counter
import json, re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
COLAB = ROOT / '00_COLAB_IA'
DRAFT = WORK / 'rascunhos'
ARCHIVE = '_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA'
REPORT = '02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md'

def read(p): return p.read_text(encoding='utf-8')
def write(p, text): p.write_text(text.rstrip() + '\n', encoding='utf-8')
def change(text, old, new):
    assert old in text, old[:100]
    return text.replace(old, new)
def metadata(text, summary):
    text = re.sub(r'^TL;DR:.*$', 'TL;DR: ' + summary, text, count=1, flags=re.M)
    return re.sub(r'^Última atualização:.*$', 'Última atualização: 2026-11-01, Codex (continuação do Claude).', text, count=1, flags=re.M)

def source_link(src):
    path, _, lines = src.rpartition(':')
    if not re.fullmatch(r'\d+(?:-\d+)?', lines):
        path, lines = src, ''
    rel = path.removeprefix('docs/00_COLAB_IA/')
    return f'[{rel}]({quote(ARCHIVE + "/" + rel)})' + (f' (linhas {lines} do original)' if lines else '')

if (WORK / 'incorporacao-codex.json').exists():
    raise SystemExit('Incorporação já executada. Não repetir nem duplicar seções.')
assert (WORK / 'snapshot-retomada-codex.json').exists()

decision_data = json.loads(read(DRAFT / 'consolidar_decisoes.json'))
decisions = decision_data['decisoes']
assert len(decisions) == 59
knowledge, pending = [], []
for file in sorted(DRAFT.glob('consolidar_*-*.json')):
    data = json.loads(read(file))
    for theme in data['temas']:
        for item in theme['itens']:
            knowledge.append({'lote': file.stem, 'tema': theme['tema'], **item})
    pending.extend({'lote': file.stem, **p} for p in data['pendencias'])
assert len(knowledge) == 158 and len(pending) == 39

# O índice conserva a extração do Claude sem transformar sua classificação em aprovação.
index = ['# Índice de rastreabilidade da mescla', '', 'TL;DR: 158 itens de conhecimento e 39 registros de pendências da consolidação Claude; duplicatas e estados históricos permanecem identificados.', '', 'Última atualização: 2026-11-01, Codex.', '', 'As sínteses revistas estão nos documentos vigentes. Os JSONs em rascunhos preservam a extração anterior, inclusive afirmações retificadas pelo relatório final. Não são instruções executáveis nem evidência atual da nuvem.', '', '## Conhecimentos', '', '| ID de índice | Título | Destino proposto na extração | Lote / item |', '|---|---|---|---|']
for n, item in enumerate(knowledge, 1):
    item['id_indice'] = f'F3-K-{n:03}'
    index.append(f"| {item['id_indice']} | {item['titulo'].replace('|', '/')} | {item['destino']} | {item['lote']} |")
index += ['', '## Pendências de origem', '', '39 registros; há sobreposição entre PROC-A-01/F3-P-059 e PF3-01/F3-D-015. Não são 39 novos bloqueios independentes.', '', '| ID de índice | ID na consolidação | Aplicabilidade sugerida | Tema |', '|---|---|---|---|']
for n, item in enumerate(pending, 1):
    item['id_indice'] = f'F3-H-{n:03}'
    index.append(f"| {item['id_indice']} | {item['id']} | {item['aplicavel_fase4']} | {item['descricao'].replace('|', '/').replace(chr(10), ' ')} |")
index += ['', '## Como aprofundar', '', 'Cada lote está no JSON de mesmo nome em `rascunhos/`; cada item contém fontes originais com linha, justificativa e relação com a Fase 4. Os originais estão no acervo integral indicado no relatório final. O índice é navegação da extração, não novo catálogo de requisitos FIAP.']
write(WORK / 'INDICE_RASTREABILIDADE_2026-11-01_v01.md', '\n'.join(index))
# Apenas índice estrutural; não duplicar textos com dados financeiros pessoais da fonte.
write(WORK / 'indice-rastreabilidade.json', json.dumps({'conhecimentos': [{'id': x['id_indice'], 'titulo': x['titulo'], 'lote': x['lote'], 'destino_original': x['destino'], 'fontes': x['fontes']} for x in knowledge], 'pendencias': [{'id': x['id_indice'], 'id_original': x['id'], 'lote': x['lote'], 'aplicavel_original': x['aplicavel_fase4'], 'fontes': x['fontes']} for x in pending]}, ensure_ascii=False, indent=2))

# DECISOES: todos os 59 IDs têm decisão, motivo, alternativas e fonte; não importar
# como atuais as conclusões do rascunho que não foram revalidadas.
dec = metadata(read(COLAB / 'DECISOES.md'), 'D-001–D-016 preservadas; D-017 registra a mescla e D-018 a regra pública aprovada em 2026-11-01. Herança F3 abaixo é histórica e não concede novas permissões.')
dec += f'''
## D-017 — Consolidar a memória da Fase 3 e arquivar os originais (aplicada, 2026-11-01)

Contexto: o usuário pediu ao Claude mesclar o conhecimento de docs/00_COLAB_IA nesta pasta e descartar a duplicata; pediu ao Codex continuar após a interrupção. Fonte: LOG de 2026-11-01 (tarde) e pedido direto de retomada.

Decisão: incorporar sínteses revistas, registrar os 59 IDs F3-D/F3-SN e mover os 39 originais, byte a byte, para [{ARCHIVE}]({ARCHIVE}/). Remover somente a pasta ativa redundante. Preservar rascunhos, extrações, registros antigos e backups; nenhum commit ou push.

Alternativas: manter duas pastas ativas (ambiguidade na retomada); apagar os originais e depender apenas do Git (pior recuperação local). Motivo: uma memória vigente com rastreabilidade completa. As 34 ausências preexistentes fora dessa pasta não fazem parte da autorização de descarte.

Verificação e de-para: [relatório da mescla]({REPORT}). Esta decisão não autoriza AWS, publicação Git, correções funcionais ou adoção automática das propostas herdadas.

## D-018 — Referências a assistentes e IDs internos só no diário (aceita pelo usuário, 2026-11-01)

Contexto: a regra pública da Fase 3 divergia do README atual. Após explicação simples, o usuário respondeu: “Sim, deixar essas referências só no diário interno (recomendado)”.

Decisão: na revisão dos documentos públicos, retirar referências ao Codex/Claude e aos IDs internos de decisões/achados/pendências. Manter autoria, cronologia e referências completas em 00_COLAB_IA. Não apagar histórico nem retirar créditos/licenças de terceiros. CLAUDE.md continua como ponteiro interno conforme as instruções globais atuais.

Alternativas: manter anotações de agentes no README (não escolhida). Motivo: documentos para o avaliador explicam o projeto; o diário explica o trabalho entre agentes. Status: política decidida; aplicação aos documentos públicos fica no B6/P-017. Esta mescla não reescreveu README público nem relatórios antigos.

## Decisões herdadas da Fase 3 — registro histórico revisado em 2026-11-01

24 decisões numeradas (F3-D-001–024) e 35 decisões sem ID original (F3-SN-01–35). “SN” é classificação da consolidação Claude, não um número dado pelo usuário na época. Fontes abaixo apontam para os originais arquivados, com linhas originais. Datas indicam a decisão histórica; não são datas de nova aprovação.

Os rótulos da extração são preservados para comparação: 23 vigentes, 26 a revisar, 6 superadas e 4 históricas. **“Vigente” significa compatível com o desenho ou processo descrito, não recurso implantado nem autorização para executar comandos.** Havendo ressalva abaixo, ela prevalece sobre o rótulo herdado. A numeração sem F3 é reservada à Fase 4.
'''
notes = {
 'F3-D-004': 'As 34 ausências de materiais anteriores continuam pendentes; arquivar a colaboração não decide o destino desses outros arquivos.',
 'F3-D-006': 'Prazo e grupo são da Fase 3. Na Fase 4 o usuário informou 2026-11-17; a condição individual ainda requer confirmação do tutor.',
 'F3-D-009': 'Na Fase 4 a tag é phase=4. Não reutilizar filtros, contas, states ou lifecycle antigo sem revisar.',
 'F3-D-012': 'Acesso por port-forward é o desenho herdado. Saída para SaaS não implica, por si, obrigação de Ingress. Reavaliar com o fluxo final.',
 'F3-D-015': 'Limites e aceite do professor são relatos da conta/Fase 3; comprovante escrito não localizado. Não transferir a exceção automaticamente à Fase 4.',
 'F3-D-016': 'Dois nós são o padrão no código; o plano menciona três. Dimensionar a stack e orçamento da conta atual antes de implantar.',
 'F3-D-018': 'O código atual tem cinco recursos de Secret em secrets.tf: auth, flag, targeting, postgres_targeting e evaluation; não são seis nem um Secret para analytics. Novos segredos SaaS ainda precisam de contrato.',
 'F3-D-020': 'Fluxo humano dev → PR → main preservado. Não constitui autorização de commit/push/PR nesta retomada.',
 'F3-D-021': 'Exceção do robô é distinta do fluxo humano. Nunca executar reset --hard do job no checkout de trabalho do usuário.',
 'F3-D-022': 'Provedor novo já inventariado em 2026-10-28; decidir importação versus data source antes do apply. False não impede destruir um recurso que já esteja gerenciado no estado e seja removido da configuração: revisar o plano.',
 'F3-D-023': 'Plan salvo é prévia, apply salvo executa sem confirmação interativa; revisar e obter a autorização de execução antes. Nenhum destroy foi autorizado por esta retomada.',
 'F3-D-024': 'Trava histórica de services/workflows não anula autorizações posteriores. A regra pública foi confirmada como D-018. Não há autorização genérica de editar qualquer código na dev.',
 'F3-SN-02': 'Correção: S3 Bucket Key é recurso SSE-KMS, não SSE-S3. Estado pode conter segredos; persistência remota não elimina arquivos locais excepcionais de recuperação. Ver fontes técnicas no relatório.',
 'F3-SN-03': 'O rótulo “superada” só afasta o identificador da conta antiga. A convenção com conta/região ainda pode ser usada na nova, em backend.hcl ignorado; não há proibição desse padrão.',
 'F3-SN-04': 'Correção: lock nativo S3 existe desde Terraform 1.10.0. >=1.11.0 é a restrição deste projeto, não a primeira versão do recurso. Comentários no código ainda precisam de ajuste.',
 'F3-SN-06': 'Escolha de preservação da base versus destroy completo continua aberta e depende da posse dos recursos manuais. Custos históricos não estimam a conta atual.',
 'F3-SN-07': 'Roteiro histórico; definir antes os namespaces/PVCs da stack e os recursos que devem sobreviver. Não executar remoções ao ler esta seção.',
 'F3-SN-08': 'Adiar recursos cobrados não dispensa respeitar dependências técnicas. NAT desligado antes do cluster precisa ser revisto para rede privada sem endpoints substitutos.',
 'F3-SN-10': '[INCERTO] data exata de fim de suporte EKS 1.34; verificar fonte AWS antes da implantação. Não presumir custos atuais a partir das cifras antigas.',
 'F3-SN-11': 'Sem chaves AWS estáticas não significa ausência de segredos de aplicação/SaaS. OIDC da árvore local já foi corrigido e testado offline em 2026-10-28; CI real segue sem prova.',
 'F3-SN-13': 'Confirmado documentalmente em 2026-11-01: chart 7.7.11 tem appVersion v2.13.2, versão anterior à correção da CVE-2025-55190 (2.13.9). Isso não prova exploração nem versão executada na conta atual. Atualização é pendência TFK-02.',
 'F3-SN-14': 'Procedimento de duas fases deve usar planos salvos, conforme F3-D-023. -target é expediente de bootstrap, não rotina para ocultar mudanças.',
 'F3-SN-16': 'Repositório 04 privado foi confirmado em 2026-10-28. Token somente leitura e acesso do ArgoCD devem ser testados sem imprimir credenciais; não houve nova consulta nesta sessão.',
 'F3-SN-17': 'sensitive oculta a exibição normal, mas não retira o valor do state. Ler um Secret para uso local não autoriza mostrá-lo em vídeo/chat.',
 'F3-SN-18': 'ignore_changes protege contra atualização do campo, não contra perda do banco nem recriação do Secret. Testar seed e restart; não garantir recuperação só por existir lifecycle.',
 'F3-SN-19': 'Comando histórico transporta segredo em argumentos do processo/pod; não copiar literalmente para o runbook novo. Preferir mecanismo que não exponha a URL em argv, YAML ou log e revisar o acesso.',
 'F3-SN-20': 'Exceções devem ser reavaliadas no artefato final. Data de revisão vencida não é prova de vulnerabilidade explorável nem aprovação de novas exceções.',
 'F3-SN-21': 'CVE e versões antigas são relato histórico, não nova checagem de vulnerabilidades de todos os serviços.',
 'F3-SN-22': 'Claude mediu em 2026-11-01: lint atual reprova sem dependências; requirements + pytest elevou notas acima do corte. Correção ainda não aplicada.',
 'F3-SN-23': 'Self-healing por Actions é escopo novo; exige identidade e RBAC próprios. Instalar kustomize para editar tag não equivale a renderizar/validar manifests no CI.',
 'F3-SN-25': 'O CI de Terraform sem credenciais é diferente dos jobs de imagens, que já assumem role. Não afirmar que todo o CI está sem acesso AWS.',
 'F3-SN-28': 'Preferência histórica não recomenda AdministratorAccess permanente nem chaves estáticas para a conta nova. Avaliar identidade temporária e menor privilégio.',
 'F3-SN-29': 'Custos antigos são referência de método. Nova estimativa deve incluir a observabilidade e a condição real de cobrança.',
 'F3-SN-30': 'Ambos os geradores foram preservados integralmente; escolha futura não exige reconstruir a extração.',
 'F3-SN-31': 'Preservação/retirada dos 34 materiais ausentes continua independente desta mescla.',
 'F3-SN-32': 'Garantir acesso real ao avaliador; Não listado é uma opção, não requisito literal de plataforma da FIAP.',
 'F3-SN-35': 'Lição: não usar estratégia de conflitos para descartar alterações silenciosamente; importação da Fase 4 já foi concluída, não repetir.'
}
for d in decisions:
    fields = {k: str(d[k]).replace('US$ 70,33', 'crédito histórico não reproduzido') for k in ['titulo','data','decisao','motivo','alternativas','vigencia']}
    # Retificações factuais da síntese; a fonte original permanece intacta.
    if d['id'] == 'F3-SN-02': fields['decisao'] = fields['decisao'].replace('SSE-S3 (AES256) com Bucket Key', 'SSE-S3 (AES256); a menção original a Bucket Key está incorreta')
    if d['id'] == 'F3-SN-04': fields['motivo'] = 'Lock evita gravações concorrentes do estado. O projeto fixou mínimo 1.11.0, mas o recurso foi introduzido na 1.10.0; a justificativa original confundia essas versões.'
    if d['id'] == 'F3-D-018': fields['decisao'] = fields['decisao'].replace('os 5 Secrets dos serviços e o do postgres-targeting', 'os Secrets dos serviços que precisam de credenciais e o do postgres-targeting')
    dec += f"\n### {d['id']} — {fields['titulo']}\n\nContexto/data: Fase 3, {fields['data']}. Status herdado: **{fields['vigencia']}**.\n\nDecisão histórica: {fields['decisao']}\n\nMotivo registrado: {fields['motivo']}\n\nAlternativas registradas: {fields['alternativas']}\n"
    dec += '\nAplicação na Fase 4: ' + notes.get(d['id'], 'Preservar como referência; verificar compatibilidade na tarefa de implementação. Não comprova execução externa atual.') + '\n'
    dec += '\nFontes: ' + '; '.join(source_link(s) for s in d['fontes']) + '.\n'
write(COLAB / 'DECISOES.md', dec)

# DOSSIE: aproveita a síntese temática completa, com correções explícitas.
dos = read(DRAFT / 'dossie.md')
intro = f'''\n**Escopo desta seção:** relato histórico extraído pelo Claude, revisto pelo Codex em 2026-11-01. Fontes e medições da Fase 3 não provam recursos da conta atual. Comandos são referências para um runbook futuro, não ordem de execução. As referências de código “conferidas em 2026-11-01” vêm da extração do Claude, exceto retificações explicitadas; não houve nova auditoria dos cinco serviços. Acervo integral: [{ARCHIVE}]({ARCHIVE}/). [Índice dos 158 itens]({quote('02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/INDICE_RASTREABILIDADE_2026-11-01_v01.md')}) (122 destinados a este dossiê; demais distribuídos por protocolo/organização/pendências/histórico).\n\n**Retificação atual:** inventário autenticado AWS/GitHub de 2026-10-28: 34/34 verificações; trust OIDC local: 8/8 testes offline. ECR e provedor não estão apenas “por relato”. O bucket segue confirmado pelo usuário em 2026-10-30, sem nova checagem AWS. Contas SaaS criadas por relato; ingestão, alertas e CI remoto ainda não comprovados. As seções anteriores mantêm snapshots datados.\n'''
dos = dos.replace('\n\n', '\n' + intro + '\n', 1)
replacements = [
 ('Tags diferentes entre serviços indicam pipeline que falhou.', 'Tags diferentes entre serviços são esperadas quando apenas alguns mudam; conferir os runs antes de concluir que houve falha.'),
 ('O ArgoCD aplica em até 30 s.', '30 s é intervalo configurado de reconciliação, não prazo máximo garantido de aplicação.'),
 ('e o ArgoCD aplica em até 30 s.', 'e o ArgoCD reconcilia com intervalo configurado de 30 s, sem garantia de conclusão nesse prazo.'),
 ('A exceção 2 RDS + pod foi aceita.', 'A exceção 2 RDS + pod foi aceita por relato na Fase 3, sem comprovante escrito localizado.'),
 ('A conta da Fase 3 e não vale para a nova.', 'A conta da Fase 3 e não vale para a nova.'),
 ('O crédito de US$ 70,33 (~190 h) era da conta da Fase 3 e não vale para a nova.', 'O saldo de crédito da conta antiga não foi transportado para esta memória vigente e não prova saldo na conta nova.'),
 ('O NAT sozinho custa', 'Na estimativa histórica, o NAT sozinho custava'),
 ('Com IPv4 público e tráfego, custa', 'Com IPv4 público, a estimativa citava'),
 ('O plano de controle do EKS custa', 'A fonte histórica atribuía ao plano de controle do EKS'),
 ('Sessões curtas e destroy ao fim.', 'Sessões curtas e encerramento planejado.'),
 ('destruí-lo ao fim de cada uma e manter a base com o NAT desligado.', 'prever o encerramento de cada sessão. A política atual de manter base/NAT ou destruir tudo ainda depende da posse dos recursos e da autorização de execução.'),
 ('O self-healing que gravar no Git deve seguir o padrão', 'Se adotado, o self-healing que gravar no Git deve considerar concorrência/idempotência; reset --hard só em checkout descartável de CI, nunca na árvore local. Referência'),
 ('`[x]` só quando o item existe na AWS ou rodou verde no CI com evidência.', 'No checklist de infraestrutura da Fase 3, `[x]` exigia prova AWS/CI. Na Fase 4, marcar cada tarefa conforme seu próprio aceite: uma tarefa local concluída não depende de AWS; um requisito externo depende de prova externa.'),
 ('O que falta é o método de varredura.', 'Busca por palavra é apoio; ausência da palavra não substitui leitura integral do enunciado.'),
 ('- **Sincronizar a dev com a main antes de editar.** Rodar `git switch dev`, `git fetch origin` e `git merge --ff-only origin/main`, e parar se o merge for recusado.', '- **Sincronização histórica da dev.** O roteiro da Fase 3 sugeria `git switch dev`, `git fetch origin` e `git merge --ff-only origin/main`. Não executar esse bloco automaticamente; conferir divergência e alterações locais e agir dentro da autorização vigente.'),
 ('Na Fase 4: volta a valer quando o CI publicar na main;', 'Na Fase 4: a estratégia deve ser reavaliada quando o CI publicar na main;'),
 ('SSE-S3 com Bucket Key', 'SSE-S3; menção a Bucket Key na fonte é incorreta (Bucket Key pertence ao SSE-KMS)'),
 ('o lock é `use_lockfile`, que exige Terraform 1.11 ou mais novo.', 'o lock é `use_lockfile`; o projeto exige Terraform >=1.11, enquanto o recurso existe desde 1.10.'),
 ('O lock é `use_lockfile`, que exige Terraform 1.11 ou mais novo.', 'O lock é `use_lockfile`; o projeto exige Terraform >=1.11, enquanto o recurso existe desde 1.10.'),
 ('O tfstate guarda senhas em texto puro e nunca fica local nem versionado.', 'O conteúdo do tfstate pode conter senhas. O backend guarda o objeto remotamente, com criptografia em repouso; arquivos locais excepcionais de recuperação e planos também devem ser protegidos e nunca versionados.'),
 ('Bucket na região errada não se move: é preciso apagar e refazer.', 'A região de um bucket existente não muda; planejar outro bucket e eventual migração revisada. Não apagar o bucket atual como correção automática.'),
 ('Reclamação de `use_lockfile`: o Terraform é anterior à 1.11.', 'Erro de argumento `use_lockfile`: conferir a versão executada e o backend; o recurso existe desde Terraform 1.10.0.'),
 ('bucket criado e confirmado em 2026-10-30', 'bucket criado e confirmado pelo usuário em 2026-10-30'),
 ('Com `create_github_oidc_provider=false`, um data source só lê o provedor e o destroy nunca o apaga.', 'Com `create_github_oidc_provider=false`, o data source lê o provedor; isso não transfere automaticamente para fora do estado um recurso anteriormente gerenciado. Conferir plano e propriedade antes de mudar a variável.'),
 ('**Apply que falha no meio não corrompe o estado.** O estado guarda o que deu certo, e o próximo apply mira só no que falta.', '**Apply pode falhar parcialmente.** Normalmente o estado registra recursos concluídos, mas é preciso conferir saída, persistência do state e recursos reais antes de repetir; não presumir integridade automática.'),
 ('ECR, role, policy e OIDC criados à mão exigem import antes do primeiro apply', 'recursos manuais que o Terraform passará a gerenciar exigem import; os apenas reutilizados podem ficar como data sources'),
 ('Qualquer "to destroy" no primeiro plan da base indica estado errado: parar e conferir o backend.', 'Qualquer destroy/replace inesperado no primeiro plan exige parar e investigar backend, estado e configuração; não é diagnóstico automático de estado errado.'),
 ('Sem ele, os nós privados não baixam imagens nem falam com o control plane, e todos os pods ficam em ImagePullBackOff.', 'Sem NAT nem endpoints/rotas substitutos, os nós privados podem perder acesso a registries e serviços externos. Não é correto afirmar que NAT é sempre necessário ao control plane: depende do endpoint privado/público e da rede.'),
 ('PVCs de Prometheus, Loki e Grafana em namespace criado pelo ArgoCD não são apagados pelo destroy da k8s', 'a futura stack ainda não define quais PVCs existirão nem quem os removerá; o roteiro deve comprovar essa remoção antes de destruir o cluster'),
 ('a identidade do CI também serve ao self-healing.', 'a identidade do self-healing ainda será definida; não presumir reutilização da role de imagens.'),
 ('VPC, ECR, SQS, DynamoDB e IAM custam praticamente zero', 'o custo histórico esperado era baixo, mas ECR/S3, solicitações e outros recursos podem continuar cobrando; conferir faturamento e armazenamento'),
 ('O chart argo-cd 7.7.11 ainda era publicado em 2026-09-11.', 'O chart argo-cd 7.7.11 constava dos registros de 2026-09-11.'),
 ('não há `upgrade_policy`, e o chart 7.7.11 instala Argo CD v2.13.2, afetado pela CVE-2025-55190', 'não há `upgrade_policy`. Confirmado em fontes oficiais em 2026-11-01: chart 7.7.11 tem appVersion v2.13.2 e essa versão precede a correção da CVE-2025-55190; não se verificou execução ou exploração na conta atual'),
 ('para uma CVE crítica nova sem mudança de código, registre a exceção', 'para uma CVE crítica nova, investigar aplicabilidade/correção antes de considerar uma exceção'),
 ('Para uma CVE crítica nova sem mudança de código, registre a exceção', 'Para uma CVE crítica nova, investigar aplicabilidade/correção antes de considerar uma exceção'),
 ('O PowerShell 5.1 não tem `&&` e exige `--%` com `-out=arquivo`.', 'O PowerShell 5.1 não suporta `&&`; `--%` é uma alternativa para problemas de passagem de argumentos, não uma exigência universal de -out. Testar o comando no shell indicado.'),
 ('(stack no ar em 05-06/11, gravação até 10/11, destroy depois)', '(proposta: stack em 2026-11-05–2026-11-06, gravação até 2026-11-10, encerramento após prova)'),
 ('em 10-12/11 e B6 para o relatório em 13-16/11', 'em 2026-11-10–2026-11-12 e B6 para o relatório em 2026-11-13–2026-11-16'),
]
applied = []
for old, new in replacements:
    if old in dos:
        dos = dos.replace(old, new)
        if old != new: applied.append(old)
dos += f'''\n### 20.7 Retificações e limites da retomada Codex — 2026-11-01

- Fontes primárias das correções de Terraform/S3/ArgoCD: [relatório da mescla]({REPORT}). A restrição >=1.11 no código permanece; só a justificativa histórica estava incorreta. Correções funcionais ficam pendentes.
- Diagnósticos da seção 20.4 são hipóteses históricas: ImagePullBackOff também pode ser IAM, DNS, egress ou imagem ausente; PVC Pending também pode ser provisionador, zona e capacidade. Consultar eventos e estado antes de apagar pods, Secrets ou volumes. Não tratar a tabela como receita destrutiva.
- URL de banco em argumento de psql/kubectl pode aparecer em processos/especificação de pod, mesmo sem eco no terminal; revisar transporte de segredos no novo runbook. Não mostrar sequer prefixos de chaves.
- Campos da API e resultados dos cinco serviços foram relatados nas fontes anteriores; não houve revisão nova desses códigos nesta retomada. CVEs antigos citados nas narrativas não foram todos rechecados.
- P-015 analisa 44 itens = 42 obrigatórios + 2 opções; P-014 tem matriz de 42 obrigatórios. As categorias de status e os escopos diferem; não comparar totais como nota ou regressão.
- D-018 resolve o conflito da documentação pública: referências a assistentes e IDs internos só no diário. Aplicação pública ainda em P-017/B6. As 34 ausências anteriores e decisões de publicação, custos e implantação continuam separadas.
- O guia SaaS já entregue pelo Claude continua orientação. A consolidação não criou chaves, enviou eventos, confirmou plano da conta nem validou integrações externas.
'''
current_dos = metadata(read(COLAB / 'DOSSIE_CONTEXTO.md'), 'P-016 consolida herança da Fase 3 na seção 20 e preserva o acervo integral. Importação e OTel locais concluídos; AWS/GitHub inventariados em 2026-10-28, bucket por relato em 2026-10-30. Stack, APM externo e publicação continuam pendentes.')
current_dos = change(current_dos, 'a colaboração histórica em `docs/00_COLAB_IA` não substitui esta pasta.', f'a colaboração histórica em `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo em 2026-11-01, com originais preservados em `{ARCHIVE}` (D-017).')
write(COLAB / 'DOSSIE_CONTEXTO.md', current_dos + '\n' + dos)

# Protocolo: reescrever só a nova seção proposta, nunca entradas históricas.
leia = read(DRAFT / 'leia.md')
leia = change(leia, 'Consolidadas em 2026-11-01 a partir de `docs/00_COLAB_IA/`.', 'Consolidadas em 2026-11-01 a partir da pasta mesclada e removida `docs/00_COLAB_IA/`.')
leia = change(leia, 'Os originais ficam em `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO` e no repositório tech-challenge-03. As fontes F3 são relativas a `docs/00_COLAB_IA/`.', f'Os originais da pasta removida ficam em `{ARCHIVE}` e em `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`. As referências à pasta removida usam as linhas originais.')
leia = change(leia, '**Só com pedido explícito do usuário:**', '**Escopo e autorização:** pedidos e autorizações já dados prevalecem; não perguntar de novo sobre ações cobertas pelo pedido. A retomada atual abrange consolidação e arquivamento local. Operações fora desse escopo incluem')
leia = change(leia, 'A leitura é livre:', 'Leituras compatíveis com o escopo podem incluir:')
leia = change(leia, '  - `terraform plan -out=arquivo` exige `--%`.', '  - `--%` é alternativa de passagem de argumentos; não é exigência universal de `terraform plan -out=arquivo`.')
leia = change(leia, 'Para conferir, mostrar só um prefixo (`${CHAVE:0:12}...`) ou o protocolo e o host.', 'Para conferir, mostrar apenas presença/ausência e resultado de validação; não imprimir valor nem prefixo de chave. Hosts também devem ser avaliados antes de exibir.')
leia = change(leia, 'Token do GitHub só em variável `TF_VAR_`.', 'Token do GitHub em mecanismo local protegido; `TF_VAR_github_token` é o mecanismo previsto no projeto, sem eco nem Git.')
leia = change(leia, '**O assistente não faz add, commit, push, mv, rm, stash ou checkout sem pedido explícito.**', '**Ações Git e destrutivas respeitam o pedido vigente.** Nesta retomada não há commit/push/PR; a movimentação da pasta histórica foi expressamente autorizada. Não ampliar permissões com base em um roteiro antigo.')
leia = change(leia, 'Regra superada. Vira ordem de execução: editar na dev é livre; a main só recebe as mudanças com role, ECR e Variables prontos (F3-P-140)', 'Restrição histórica de outra etapa; edições seguem o pedido atual, sem liberdade genérica. Publicação depende de autorização e preparo de role/ECR/Variables (F3-P-140)')
leia = change(leia, 'O usuário decide (P-016)', 'Resolvido pelo usuário em 2026-11-01: D-018. Referências internas ficam no diário; aplicação pública no B6/P-017')
leia = change(leia, 'o provedor foi criado à mão (por relato)', 'o provedor manual foi inventariado em 2026-10-28')
leia = change(leia, 'Registrar em DECISOES uma exceção explícita e restrita.', 'Projetar e registrar a identidade/RBAC da automação; não atribuir a todo CI a ausência de AWS (os jobs de imagem já usam OIDC).')
cur = metadata(read(COLAB / 'LEIA-PRIMEIRO.md'), 'Colaboração vigente nesta pasta. P-016 consolidada; herança F3 arquivada com manifesto. Seguir LOG/PENDENCIAS, preservar trabalho na dev e distinguir relato, validação local e prova externa.')
cur = change(cur, '`docs/00_COLAB_IA` é acervo histórico importado e não altera o estado/instruções atuais.', f'`docs/00_COLAB_IA` foi mesclada e removida do caminho ativo; originais em `{ARCHIVE}`. A herança não altera permissões atuais (D-017).')
write(COLAB / 'LEIA-PRIMEIRO.md', cur + '\n' + leia)

org = read(DRAFT / 'organizacao.md')
org = change(org, '| Saída de gerador e rascunho | `output/`, `tmp/` | Ignorados (.gitignore:90 e :95); nunca linkar em documento público |', '| Saída de gerador e rascunho | `00_COLAB_IA/02_TRABALHO/` | Regra vigente da Fase 4; output/tmp eram convenção histórica. Não linkar artefato ignorado na entrega pública |')
org = change(org, 'Em 2026-11-01, o `git status` tinha 149 entradas.', 'A contagem do Git muda com os artefatos; consultar snapshot-retomada-codex.json para o recorte desta sessão.')
org = change(org, 'Isso vale para a remoção de `docs/00_COLAB_IA`: commit próprio, de-para no LOG e caminho de recuperação registrado', 'A remoção de `docs/00_COLAB_IA` foi feita somente na árvore local (sem commit); futura publicação deve separar a movimentação das mudanças funcionais. De-para no LOG e caminho de recuperação registrado')
org = change(org, 'O usuário decide (P-016).', 'Resolvido em D-018: referências internas no diário; revisão pública no B6/P-017. CLAUDE.md permanece como ponteiro interno, conforme as instruções globais atuais.')
cur = metadata(read(COLAB / 'ORGANIZACAO_DE_PASTAS.md'), 'Uma colaboração vigente em 00_COLAB_IA. Auxiliares em 02_TRABALHO e originais/versionamento em _ARQUIVO_MORTO; não criar outra memória ativa em docs.')
cur = change(cur, 'Não criar diretórios genéricos vazios nem CLAUDE.md na raiz sem autorização específica.', 'Não criar diretórios genéricos vazios. CLAUDE.md já existe como ponteiro interno e é mantido conforme as instruções globais atuais; a regra de 2026-09-16 dizia respeito ao setup inicial de estudos.')
write(COLAB / 'ORGANIZACAO_DE_PASTAS.md', cur + '\n' + org + f'\nAcervo integral da mescla: [{ARCHIVE}]({ARCHIVE}/). As referências históricas em crases mantêm o caminho da época; novos links ativos usam o destino arquivado.\n')

# PENDENCIAS: manter todos os itens herdados e corrigir estados claramente datados.
pend = read(DRAFT / 'pendencias.md')
pend = change(pend, '### Pendências herdadas da Fase 3', '## Pendências herdadas da Fase 3 — triagem de 2026-11-01')
pend = change(pend, 'As linhas de código citadas foram conferidas em 2026-11-01.', 'As linhas de código vêm da consolidação Claude em 2026-11-01; os números mudam conforme as edições. Não são uma nova auditoria dos serviços pelo Codex.')
pend = change(pend, 'a configuração real não foi conferida.', 'o inventário autenticado de 2026-10-28 confirmou MUTABLE; revalidar antes da adoção pelo Terraform.')
pend = change(pend, 'a role foi criada à mão (P-012, por relato)', 'a role foi criada à mão e conferida no inventário P-013 de 2026-10-28')
pend = change(pend, 'O usuário decide se a regra vale para o README final e o relatório PDF. Se valer, aplicar no B6 e registrar em DECISOES. Decidir também o que fazer com o CLAUDE.md versionado.', 'Resolvido pelo usuário em D-018: retirar referências internas dos documentos públicos na revisão B6/P-017. Manter diário e CLAUDE.md interno; não reescrever histórico.')
pend = change(pend, '- F3-P-035: addons, StorageClass gp3 e kustomize no CI, já resolvidos no código.', '- F3-P-035/P-036: addons, StorageClass gp3 e instalação do kustomize standalone para editar a tag existem no código. Isso não resolve o gate de renderização dos manifests no CI (F-029/CIC-09), que permanece pendente.')
pend = change(pend, '- F3-P-074: bucket de estado da conta nova, concluído em 2026-10-30. Falta só conferir as tags manuais project e phase.', '- F3-P-074: a referência histórica ao bootstrap não deve reabrir a criação do bucket novo. Na Fase 4 ele foi confirmado completo pelo usuário em 2026-10-30; proteções, nome e tags ainda não foram consultados pelo agente nesta retomada. Backend local existe; init/import/apply não executados.')
pend = change(pend, 'Antes de descartar a pasta, registrar no DOSSIE como recuperar:', 'Geradores preservados no acervo integral; também recuperar por:')
cur = metadata(read(COLAB / 'PENDENCIAS_E_PROXIMOS_PASSOS.md'), 'P-016: consolidação local em fechamento, acervo integral preservado e D-018 aprovada. Próximo trabalho funcional é B0/B1; Git, custos, segredos e integrações ainda exigem os dados/decisões registrados. P-013/P-014 têm fechamento documental pendente.')
cur += '\n' + pend
cur += f'''
## P-017 — Aplicar política pública e retificações da mescla (pendente, 2026-11-01)

- [x] Resolver conflito de autoria/IDs internos: usuário escolheu diário interno; decisão D-018.
- [ ] Na revisão B6, retirar referências a assistentes e IDs internos dos READMEs/documentos públicos vigentes, preservando histórico e créditos/licenças legítimos.
- [ ] Corrigir justificativas nos comentários de Terraform: use_lockfile existe desde 1.10.0; >=1.11.0 é escolha do projeto. Não é necessário baixar a restrição de versão. Bucket Key não é recurso SSE-S3.
- [ ] Antes do deploy, escolher versão mantida e corrigida do ArgoCD; 7.7.11 → appVersion v2.13.2 e CVE-2025-55190 confirmados por fontes oficiais em 2026-11-01. Não houve teste de exploração nem implantação nesta retomada (TFK-02).
- [ ] Revisar runbook futuro: diagnóstico antes de apagar recursos; plano salvo com aprovação antes de aplicar; não imprimir prefixos de chaves nem transportar DATABASE_URL em argumentos visíveis. Diferenciar intervalo de reconciliação de prazo garantido.

Fontes e rastreabilidade: [relatório]({REPORT}) e [índice completo](02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/INDICE_RASTREABILIDADE_2026-11-01_v01.md). São melhorias/retificações, não novas exigências da FIAP. 39 registros de pendências herdadas incluem duplicatas e itens fora da Fase 4; não somá-los aos 42 requisitos.
'''
write(COLAB / 'PENDENCIAS_E_PROXIMOS_PASSOS.md', cur)

# Ponteiro interno curto: o snapshot anterior foi preservado integralmente.
write(ROOT / 'CLAUDE.md', f'''# Tech Challenge Fase 4 — contexto para assistentes

TL;DR: trabalhar na dev e retomar pelo LOG/PENDENCIAS. P-016 consolida a memória herdada; stack/contas integradas e publicação continuam pendentes.

Última atualização: 2026-11-01, Codex (continuação do Claude).

- Ler `00_COLAB_IA/LEIA-PRIMEIRO.md` → PENDENCIAS → topo do LOG → DOSSIE/DECISOES. `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo; acervo em `00_COLAB_IA/{ARCHIVE}` (D-017).
- Português do Brasil, explicação simples antes da técnica, datas ISO e fonte. Distinguir relato, configuração, teste local, execução externa e evidência de entrega.
- Código/histórico da Fase 3 importados em 2026-10-20. Enunciado, materiais e cinco guias da Fase 4 preservados. `tech-challenge-03` é somente leitura.
- Branch atual dev; sem commit/push/PR/merge main nesta retomada. A autorização antiga de importação foi cumprida e não é permissão permanente de publicar. Movimentação local da pasta de colaboração autorizada em P-016.
- AWS/GitHub: inventário de 2026-10-28 com 34/34 verificações; trust OIDC corrigido localmente e 8/8 testes offline. Bucket novo completo por relato do usuário em 2026-10-30; backend.hcl nas três raízes ignorado. Faltam tfvars, adoção dos recursos manuais e validação da cobrança. Não reutilizar conta/state/segredos da Fase 3.
- P-008 local concluída em 2026-10-27: 19 spans/5 serviços e ensaio integrado. Laboratório encerrado; não repetir como se faltasse instrumentação. E1 externa (New Relic), stack no EKS, alerta/PagerDuty/Slack e self-healing ainda sem comprovação.
- P-015 tem análise Claude de 44 itens (42 obrigatórios + 2 opções); P-014 tem catálogo Codex e matriz de 42 obrigatórios, fechamento documental pendente. Não somar achados repetidos nem tratar os números como nota.
- D-018: documentos públicos focados no projeto; autoria de agentes e IDs internos ficam no diário. Aplicação pública na revisão B6/P-017, sem apagar histórico. Este arquivo é ponteiro interno.
- Auxiliares em `00_COLAB_IA/02_TRABALHO`; versões em `00_COLAB_IA/_ARQUIVO_MORTO`. Não versionar credenciais, estados, caches ou renderizações; revisar arquivo por arquivo antes de futura publicação. Memória global somente quando pedida diretamente.
- Encerrar com LOG incremental, PENDENCIAS, decisões e teste de handoff. Documento da mescla: `00_COLAB_IA/{REPORT}`.
''')

write(WORK / 'incorporacao-codex.json', json.dumps({'date':'2026-11-01', 'decisoes':59, 'conhecimentos':158, 'destinos_propostos_conhecimento':dict(Counter(i['destino'] for i in knowledge)), 'pendencias_origem':39, 'correcoes_dossie':applied, 'user_decision':'D-018', 'status':'incorporado; validar e mover acervo antes de fechar P-016'}, ensure_ascii=False, indent=2))
print(json.dumps({'decisoes':59,'conhecimentos':158,'pendencias_origem':39,'correcoes_dossie':len(applied),'status':'incorporado; falta validar/arquivar'}, ensure_ascii=False))
