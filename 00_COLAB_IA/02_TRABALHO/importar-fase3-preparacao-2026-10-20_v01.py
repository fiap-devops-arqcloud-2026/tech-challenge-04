from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]; W=Path(__file__).parent
src=R.parent/'tech-challenge-03'
def git(*args,cwd=R):
    return subprocess.check_output(['git',*args],cwd=cwd,text=True,encoding='utf8').strip()
assert git('branch','--show-current')=='dev'
assert not git('status','--porcelain',cwd=src)
baseline={'date':datetime.now(timezone(timedelta(hours=-3))).isoformat(),'source_commit':git('rev-parse','main',cwd=src),'phase4_main':git('rev-parse','main'),'phase4_dev':git('rev-parse','dev'),'source_status':git('status','--porcelain',cwd=src),'files':[]}
for p in sorted(R.rglob('*')):
    if not p.is_file() or '.git' in p.relative_to(R).parts or '__pycache__' in p.parts:continue
    baseline['files'].append({'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size})
dest=W/'preservacao-importacao-2026-10-20_v01.json'
assert not dest.exists();dest.write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf8')

archive=R/'00_COLAB_IA/_ARQUIVO_MORTO/2026-10-20_inicio-importacao';archive.mkdir(parents=True,exist_ok=True)
for name in ['LEIA-PRIMEIRO.md','LOG_DE_TRABALHO.md','PENDENCIAS_E_PROXIMOS_PASSOS.md']:
    p=R/'00_COLAB_IA'/name;t=p.read_text(encoding='utf8');p.rename(archive/name)
    if name=='LEIA-PRIMEIRO.md':
        t+='''
## Escopo autorizado em 2026-10-20 — importação

O usuário autorizou expressamente importar o código/histórico do 03 para o 04, criar a branch exata `import-fase3`, ajustar README/CI/CD/ArgoCD e fazer merge local para `dev`. Isso autoriza os commits e edições necessários nos caminhos de código do 04 e prevalece sobre as restrições anteriores da etapa de estudos. Preservar todo o trabalho atual; 03 permanece somente leitura. Sem push, PR ou merge na main nesta etapa. Dados da nova conta AWS pendentes; nenhuma implantação autorizada. Memória global pode receber nota durável, pois foi pedida explicitamente nesta sessão.
'''
    elif name=='LOG_DE_TRABALHO.md':
        i=t.index('## 2026-');stamp=datetime.now(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M')
        t=t[:i]+f'''## {stamp} (America/Sao_Paulo, UTC-03:00) — Codex — Início da importação autorizada

Feito: autorização explícita recebida para importação, branch import-fase3, commits/merge local na dev e ajustes README/CI/CD/ArgoCD. Conferido source 61008794090f582c098e2edc42041339c556f14c, limpo; 04 dev=9696185/main=003a707. Manifesto SHA-256 de todos os arquivos atuais salvo antes da importação, inclusive auxiliares locais.

Decisões/Por quê: D-013 passou de proposta para método autorizado nesta sessão. Só commits necessários locais; não publicar nem abrir PR; não tocar main ou Fase3. Dados AWS pendentes: preservar infraestrutura como código e remover dependência operacional de conta antiga, sem deploy.

Arquivos/de-para: snapshot inicial de LEIA-PRIMEIRO/LOG/PENDENCIAS em _ARQUIVO_MORTO/2026-10-20_inicio-importacao; manifesto 02_TRABALHO/preservacao-importacao-2026-10-20_v01.json. Mantidos todos os arquivos existentes.

Estado p/ o próximo agente: preparar checkpoint curado e importar histórico em import-fase3; depois ajustar CI/Argo/README, validar, integrar na dev e atualizar contexto/memória. Checklist incremental em P-004.

'''+t[i:]
    else:
        t=t.replace('- [ ] Preparar checkpoint revisável dos arquivos atuais do 04 e confirmar autorização para commits antes de executá-los.','- [x] Autorização recebida em 2026-10-20: branch import-fase3, commits e merge local na dev; sem push/PR/main.\n- [ ] Preparar checkpoint curado e importar a base 6100879 preservando histórico.')
        t=t.replace('Método ainda proposto; não há branch/importação/commit/push novos.','Método autorizado nesta sessão; execução e validação em andamento.')
    p.write_text(t,encoding='utf8')
print('Manifesto salvo:',len(baseline['files']),'arquivos;',sum(x['size'] for x in baseline['files']),'bytes. Autorização registrada.')
