"""Snapshot local da retomada P-016; não acessa cloud, serviços ou segredos ignorados."""
from pathlib import Path
import hashlib, json, subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
BACK = ROOT / '00_COLAB_IA/_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/retomada-codex-1809'
CONTEXT = ['CLAUDE.md'] + ['00_COLAB_IA/' + n + '.md' for n in ['LEIA-PRIMEIRO', 'PENDENCIAS_E_PROXIMOS_PASSOS', 'LOG_DE_TRABALHO', 'DOSSIE_CONTEXTO', 'DECISOES', 'ORGANIZACAO_DE_PASTAS']]

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

if __name__ == '__main__':
    target = WORK / 'snapshot-retomada-codex.json'
    if target.exists():
        raise SystemExit('Snapshot já existe; não sobrescrever.')
    paths = sorted(set(git('ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')) - {''})
    files = {}
    for rel in paths:
        p = ROOT / rel
        files[rel] = {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size} if p.is_file() else None
    source = ROOT / 'docs/00_COLAB_IA'
    refs = git('ls-tree', '-r', '--name-only', '-z', '3b21e65', '--', 'docs/00_COLAB_IA').decode().split('\0')
    originals = []
    for rel in filter(None, refs):
        p = ROOT / rel
        raw = git('cat-file', 'blob', '3b21e65:' + rel)
        # Git pode converter LF -> CRLF no checkout; bytes do checkout serão preservados exatamente.
        same_git = git('hash-object', '--path=' + rel, rel).decode().strip() == git('rev-parse', '3b21e65:' + rel).decode().strip()
        assert same_git, rel
        originals.append({'path': rel, 'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size, 'blob': git('rev-parse', '3b21e65:' + rel).decode().strip()})
    assert len(originals) == 39
    assert len(list(source.rglob('*'))) >= 39
    for rel in CONTEXT:
        dest = BACK / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        assert not dest.exists()
        dest.write_bytes((ROOT / rel).read_bytes())
    data = {'date': datetime.now().astimezone().isoformat(), 'root': str(ROOT), 'branch': git('branch', '--show-current').decode().strip(), 'head': git('rev-parse', 'HEAD').decode().strip(), 'main': git('rev-parse', 'main').decode().strip(), 'files': files, 'originals': originals, 'context_backups': str(BACK)}
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK / 'git-status-retomada.txt').write_bytes(git('status', '--porcelain=v1', '-uall'))
    log = ROOT / '00_COLAB_IA/LOG_DE_TRABALHO.md'
    entry = '''## 2026-11-01 18:09 (America/Sao_Paulo, UTC-03:00) — Codex — Retomada da P-016 após interrupção do Claude

Feito: lidos protocolo, pendências e LOG; identificada P-016 como trabalho mais recente. Conferidos os 39 arquivos de docs/00_COLAB_IA contra os blobs de 3b21e65 (normalização Git); snapshot e cópias exatas dos sete documentos de contexto preservados antes de editar.
Decisões/Por quê: continuar a mescla já autorizada pelo usuário, preservando a pasta integral no arquivo morto antes de retirá-la do caminho ativo. Rascunhos são insumos: decisões históricas não viram novas autorizações. P-014/P-013 têm fechamento documental pendente e não serão confundidas com a tarefa atual.
Arquivos: 02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/{retomar_codex.py,snapshot-retomada-codex.json,git-status-retomada.txt}; backups em _ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/retomada-codex-1809/.
Descobertas: rascunhos contêm afirmações que precisam de ressalva (permissões herdadas, segredos em prefixos, estado antigo da AWS, kustomize no CI). Sem alteração funcional, commit, push, PR ou operação remota.
Estado p/ o próximo agente: revisar e incorporar 59 decisões, conhecimentos e pendências com namespace F3; validar referências e preservação; arquivar pasta histórica e fechar P-016 com de-para e limites.

'''
    old = log.read_text(encoding='utf-8')
    log.write_text(old.replace('# Log de trabalho\n\n', '# Log de trabalho\n\n' + entry, 1), encoding='utf-8')
    print(json.dumps({'branch': data['branch'], 'source_files_checked': len(originals), 'snapshot_paths': len(files), 'backup': str(BACK)}, ensure_ascii=False))
