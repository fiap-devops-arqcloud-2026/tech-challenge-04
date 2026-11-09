"""Falha proposital da Fase 4: estado so em memoria e /health sempre saudavel.

Roda sem banco e sem auth-service: o pool do psycopg2 e a chamada ao
/validate sao substituidos por dubles.
"""
import importlib
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

# O CI roda os testes a partir da pasta do servico.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

AUTH = {"Authorization": "Bearer chave-de-teste"}
AMBIENTE = {
    "DATABASE_URL": "postgresql://teste.invalid/flags",
    "AUTH_SERVICE_URL": "http://auth.invalid",
    "OTEL_SDK_DISABLED": "true",
}


def carregar_app():
    """Importa app.py como um processo novo faria, sem conectar no banco."""
    with patch.dict(os.environ, AMBIENTE), patch("psycopg2.pool.SimpleConnectionPool") as pool:
        cursor = pool.return_value.getconn.return_value.cursor.return_value
        cursor.fetchall.return_value = []
        cursor.fetchone.return_value = {"name": "x"}
        if "app" in sys.modules:
            return importlib.reload(sys.modules["app"])
        return importlib.import_module("app")


class FalhaPropositalTests(unittest.TestCase):
    def setUp(self):
        self.modulo = carregar_app()
        self.cliente = self.modulo.app.test_client()
        # auth-service sempre aceita a chave: o assunto aqui e a falha.
        validacao = patch("requests.get", return_value=MagicMock(status_code=200))
        validacao.start()
        self.addCleanup(validacao.stop)

    def ligar(self, valor):
        return self.cliente.post("/admin/fault", json={"enabled": valor}, headers=AUTH)

    def test_comeca_desligada_e_as_rotas_funcionam(self):
        resposta = self.cliente.get("/admin/fault", headers=AUTH)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), {"enabled": False, "since": None})
        self.assertEqual(self.cliente.get("/flags", headers=AUTH).status_code, 200)

    def test_ligada_responde_5xx_nas_rotas_de_flags(self):
        self.assertEqual(self.ligar(True).status_code, 200)
        respostas = {
            "GET /flags": self.cliente.get("/flags", headers=AUTH),
            "GET /flags/<name>": self.cliente.get("/flags/x", headers=AUTH),
            "POST /flags": self.cliente.post("/flags", json={"name": "x"}, headers=AUTH),
        }
        for rota, resposta in respostas.items():
            with self.subTest(rota=rota):
                self.assertTrue(500 <= resposta.status_code < 600, resposta.status_code)
                # Corpo JSON, como o resto da API: quem chama (evaluation)
                # e o painel de logs nao devem receber HTML de erro.
                self.assertIsNotNone(resposta.get_json(silent=True))

    def test_health_continua_saudavel_com_a_falha(self):
        # Se /health falhasse, o liveness probe reiniciaria o pod sozinho e
        # o self-healing do projeto nao teria o que curar no ensaio.
        self.ligar(True)
        self.assertEqual(self.cliente.get("/health").status_code, 200)

    def test_controle_continua_acessivel_e_desliga(self):
        self.ligar(True)
        estado = self.cliente.get("/admin/fault", headers=AUTH).get_json()
        self.assertTrue(estado["enabled"])
        self.assertIsNotNone(estado["since"])
        self.assertEqual(self.ligar(False).status_code, 200)
        self.assertEqual(self.cliente.get("/flags", headers=AUTH).status_code, 200)

    def test_processo_novo_nasce_saudavel(self):
        # E exatamente o que o rollout restart faz: troca o processo.
        self.ligar(True)
        novo = carregar_app()
        self.assertEqual(novo.fault_state, {"enabled": False, "since": None})

    def test_controle_exige_autenticacao(self):
        resposta = self.cliente.post("/admin/fault", json={"enabled": True})
        self.assertEqual(resposta.status_code, 401)
        self.assertFalse(self.modulo.fault_state["enabled"])

    def test_corpo_invalido_e_recusado(self):
        for corpo in ({}, {"enabled": "sim"}, [True]):
            with self.subTest(corpo=corpo):
                resposta = self.cliente.post("/admin/fault", json=corpo, headers=AUTH)
                self.assertEqual(resposta.status_code, 400)
        self.assertFalse(self.modulo.fault_state["enabled"])


if __name__ == "__main__":
    unittest.main()
