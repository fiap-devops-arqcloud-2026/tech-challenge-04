"""Verificacoes finais de preservacao, Git, sintaxe e links; sem cloud/mutacoes Git."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "00_COLAB_IA/02_TRABALHO"


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", *args], cwd=cwd, encoding="utf-8")


def deleted(status):
    return {entry[3:] for entry in status.split("\0") if entry.startswith(" D ")}


def main():
    initial = json.loads((WORK / "preservacao-importacao-2026-10-20_v01.json").read_text(encoding="utf-8"))
    protected = [item for item in initial["files"] if item["path"].startswith("docs/")
                 or item["path"] == "POSTECH - Tech Challenge - Fase 4.pdf"]
    failures = []
    for item in protected:
        file = ROOT / item["path"]
        if not file.exists() or hashlib.sha256(file.read_bytes()).hexdigest() != item["sha256"]:
            failures.append("Protected file changed: " + item["path"])
    before = json.loads((WORK / "preservacao-passos-locais-2026-10-22_v01.json").read_text(encoding="utf-8"))
    status = git("status", "--porcelain=v1", "-z")
    check_deletions = deleted(status) == deleted(before["git_status_before"])
    if not check_deletions:
        failures.append("Preexisting deletions differ")
    check_branch = git("branch", "--show-current").strip() == "dev"
    check_head = git("rev-parse", "HEAD").strip() == before["head"]
    check_main = git("rev-parse", "main").strip() == before["main"]
    if not all([check_branch, check_head, check_main]):
        failures.append("Branch/HEAD/main changed unexpectedly")
    source_status = git("status", "--porcelain=v1", cwd=ROOT.parent / "tech-challenge-03").strip()
    if source_status:
        failures.append("Source checkout is not clean")
    links = 0
    for rel in ["README.md", "observability/README.md",
                "00_COLAB_IA/02_TRABALHO/RELATORIO_PASSO1_REVALIDACAO_2026-10-27_v01.md",
                "00_COLAB_IA/02_TRABALHO/RELATORIO_PASSO2_OBSERVABILIDADE_LOCAL_2026-10-27_v01.md"]:
        file = ROOT / rel
        text = file.read_text(encoding="utf-8")
        if text.count("```") % 2:
            failures.append("Unbalanced Markdown fences: " + rel)
        for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = unquote(raw.split("#", 1)[0].strip("<>"))
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            links += 1
            if not (file.parent / target).exists():
                failures.append("Missing local link: " + rel + " -> " + target)
    result = {
        "date": datetime.now().astimezone().isoformat(),
        "phase4_materials_unchanged": len(protected),
        "preexisting_deletions_unchanged": len(deleted(status)) if check_deletions else False,
        "branch": "dev" if check_branch else "unexpected", "head_unchanged": check_head,
        "main_unchanged": check_main, "source03_clean": not source_status,
        "local_markdown_links_checked": links, "failures": failures,
    }
    (WORK / "verificacao-passos-locais-2026-10-27_v01.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
