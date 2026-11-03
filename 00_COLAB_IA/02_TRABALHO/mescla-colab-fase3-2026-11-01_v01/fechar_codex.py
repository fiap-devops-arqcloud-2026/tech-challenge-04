"""Fecha somente P-016 após comprovação do arquivamento. Preserva sessões antigas."""
from pathlib import Path
from datetime import datetime
import json, re

ROOT=Path(__file__).resolve().parents[3]
WORK=Path(__file__).resolve().parent
COLAB=ROOT/'00_COLAB_IA'
def read(p): return p.read_text(encoding='utf-8')
def write(p,t): p.write_text(t.rstrip()+'\n',encoding='utf-8')
checks=json.loads(read(WORK/'verificacao-codex-depois.json'))
assert checks['ok'] and checks['checks']['originals']==39
stamp=datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')

pending=read(COLAB/'PENDENCIAS_E_PROXIMOS_PASSOS.md')
start=pending.index('## P-016 —')
end=pending.index('## P-015 —',start)
pending=pending[:start]+'''## P-016 — Mesclar a colaboração da Fase 3 e retirar a pasta redundante (concluída, 2026-11-01)

Pedido autorizado do usuário em 2026-11-01, iniciado pelo Claude e concluído pelo Codex após a interrupção. Relatório: [MESCLA_COLAB_FASE3_2026-11-01_v01.md](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md).

- [x] Reaproveitar extração dos 39 arquivos, rascunhos e backups, sem repetir a importação de código.
- [x] Revisar e incorporar 59 decisões F3-D/F3-SN, dossiê §20, pendências herdadas e regras de colaboração/organização. Índice rastreia 158 conhecimentos e 39 registros de pendência (inclui duplicatas/históricos).
- [x] Atualizar ponteiros CLAUDE.md, LEIA-PRIMEIRO e DOSSIE; preservar registros antigos e registrar retificações.
- [x] Resolver com o usuário o conflito público: referências a agentes/IDs ficam no diário, D-018. Aplicação pública transferida ao B6/P-017, sem pendência de decisão.
- [x] Executar verificador Claude e verificador independente; 39/39 originais preservados, 716 outros arquivos anteriores inalterados e 34 ausências anteriores mantidas. Links, fontes, IDs e histórico conferidos.
- [x] Mover docs/00_COLAB_IA para _ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA; retirar somente a pasta ativa redundante, sem commit/stage/push.
- [x] Relatório final, LOG incremental e teste de handoff. Próximo agente não deve refazer P-016.

Retomar B0/B1 da P-015 e P-017 conforme dados/decisões já registrados. As 34 ausências preexistentes fora da colaboração, publicações Git, custos e implantação continuam separados. P-013/P-014 têm resultados salvos e fechamento documental pendente. Guia SaaS entregue pelo Claude continua orientação, sem testes externos realizados nesta mescla.

'''+pending[end:]
pending=re.sub(r'^TL;DR:.*$', 'TL;DR: P-016 concluída em 2026-11-01: memória da Fase 3 consolidada e 39 originais arquivados. D-018 aprovada; aplicação pública no B6/P-017. Retomar B0/B1; P-013/P-014 ainda precisam de fechamento documental.',pending,count=1,flags=re.M)
write(COLAB/'PENDENCIAS_E_PROXIMOS_PASSOS.md',pending)

log=read(COLAB/'LOG_DE_TRABALHO.md')
assert 'Codex — P-016 concluída' not in log
entry=f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — P-016 concluída: memória consolidada, originais preservados e decisão pública

Feito: aproveitadas as extrações do Claude; incorporadas 59 decisões F3-D/F3-SN em DECISOES, síntese temática no DOSSIE §20, regras no LEIA/ORGANIZACAO e pendências herdadas. Índice completo de 158 conhecimentos e 39 registros de pendência, com duplicatas/históricos identificados. As contagens são da extração, não novos requisitos FIAP.
Decisões/Por quê: D-017 mantém uma colaboração vigente e arquivo integral recuperável. D-018 foi confirmada pelo usuário após explicação simples: referências a assistentes e IDs internos ficam no diário; aplicar aos documentos públicos na revisão B6/P-017, sem apagar histórico. Não reperguntar essa preferência.
Arquivos: sete documentos de contexto atualizados (CLAUDE e seis em 00_COLAB_IA); relatório 02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md; índice, manifesto, scripts e verificações em 02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/. Originais desses documentos antes da edição em _ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/retomada-codex-1809/.
De-para: docs/00_COLAB_IA/ → 00_COLAB_IA/_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/. Movidos os 39 arquivos completos, após validar os caminhos absolutos e ausência de reparse points. SHA-256 exato e blobs do commit 3b21e65 conferidos. Nenhuma exclusão permanente. O Git mostra 39 remoções locais adicionais da origem, sem stage, além das 34 ausências anteriores fora da pasta, que não foram tocadas.
Descobertas/retificações: use_lockfile existe desde Terraform 1.10.0 (>=1.11 é restrição do projeto); S3 Bucket Key pertence ao SSE-KMS; chart ArgoCD 7.7.11 tem appVersion v2.13.2 e antecede correção da CVE-2025-55190 (fonte oficial, não prova de exploração). Corrigidas sínteses de permissões, exposição de prefixos de segredos, estado AWS por relato versus inventário, kustomize instalado versus gate de validação, prazo de reconciliação e hipóteses de diagnóstico. Código permanece como antes; melhorias em P-017 e achados P-015.
Verificação: verificador independente e Claude aprovados. 39/39 originais preservados, 716 outros arquivos anteriores inalterados, 34 ausências preservadas, 59 IDs únicos e referências de origem/links conferidos (contagens finais no JSON). O aviso de e-mail do verificador Claude é falso positivo: trivy-action@0.28.0 na narrativa histórica, não endereço pessoal. LOG anterior preservado integralmente. HEAD/dev/main e índice sem alterações. Verificação de dados pessoais limitada a padrões/valores derivados dos originais; acervo preserva o conteúdo antigo. Os 7 PNGs e 1 PDF foram inventariados, não relidos visualmente nesta mescla.
Estado p/ o próximo agente: P-016 fechada. Retomar B0: F-024 (log de 156 MB), correção do lint já medida e decisões de Git/34 ausências/custos; B1/E1 externa depende de chave local New Relic, sem pedir segredo no chat. Aplicar D-018 aos documentos públicos no B6/P-017. P-013 e P-014 têm evidências prontas mas fechamento documental pendente; não repetir consultas AWS/extrações sem necessidade. Nenhuma alteração de código, AWS, CI remoto, publicação Git ou envio de mensagem/incidente nesta retomada. Não foi agendado evento às 19:00.

'''
# TL;DR atual no cabeçalho; todo o texto anterior, inclusive metadados antigos, permanece.
header='# Log de trabalho\n\nTL;DR: P-016 concluída; retomar B0/B1 e P-017. Ver relatório e PENDENCIAS para escopo e pendências.\n\nÚltima atualização: 2026-11-01, Codex.\n\n'
(COLAB/'LOG_DE_TRABALHO.md').write_text(header+entry+log.partition('\n\n')[2],encoding='utf-8')

inc=json.loads(read(WORK/'incorporacao-codex.json'))
inc['status']='P-016 concluída: incorporado, arquivado e verificado; D-018 aplicada como política, revisão pública pendente em P-017'
write(WORK/'incorporacao-codex.json',json.dumps(inc,ensure_ascii=False,indent=2))
print('P-016 fechada; D-018 registrada; histórico anterior preservado.')
