#!/bin/sh
# Reproduz o job lint do _ci-python.yml dentro da imagem do servico (Python 3.12).
# Modo A: venv limpo so com flake8 e pylint (como o CI faz hoje).
# Modo B: Python da imagem, que ja tem o requirements.txt, mais pylint/flake8/pytest (a correcao proposta).
# O repositorio entra montado somente leitura em /src.
SVC="$1"
cd "/src/services/$SVC" || exit 2
FILES="app.py telemetry.py tests/test_telemetry.py"

echo "### $SVC"
python -m venv /tmp/a >/dev/null && /tmp/a/bin/pip install -q --disable-pip-version-check flake8 pylint >/dev/null 2>&1
echo "versoes: $(/tmp/a/bin/pylint --version | head -1) / flake8 $(/tmp/a/bin/flake8 --version | cut -d' ' -f1)"
/tmp/a/bin/flake8 . --count --select=E9,F63,F7,F82 --statistics >/tmp/f.txt 2>&1; echo "flake8 (erros graves): exit=$? total=$(tail -1 /tmp/f.txt)"

/tmp/a/bin/pylint --rcfile=/src/.pylintrc $FILES >/tmp/a.txt 2>&1; ea=$?
echo "A (como o CI hoje): $(grep -o 'rated at [^ ]*' /tmp/a.txt) exit=$ea"
echo "  mensagens: $(grep -oE ': [CRWEF][0-9]{4}' /tmp/a.txt | sort | uniq -c | sort -rn | awk '{printf "%s x%s  ", $3, $1}')"
echo "  E0401 (import-error): $(grep -c 'E0401' /tmp/a.txt)"

pip install -q --disable-pip-version-check pylint flake8 pytest >/dev/null 2>&1
pylint --rcfile=/src/.pylintrc $FILES >/tmp/b.txt 2>&1; eb=$?
echo "B (com requirements + pytest): $(grep -o 'rated at [^ ]*' /tmp/b.txt) exit=$eb"
echo "  mensagens: $(grep -oE ': [CRWEF][0-9]{4}' /tmp/b.txt | sort | uniq -c | sort -rn | awk '{printf "%s x%s  ", $3, $1}')"
echo "  detalhe B:"; grep -E ': [CRWEF][0-9]{4}' /tmp/b.txt | sed 's/^/    /' | head -40
