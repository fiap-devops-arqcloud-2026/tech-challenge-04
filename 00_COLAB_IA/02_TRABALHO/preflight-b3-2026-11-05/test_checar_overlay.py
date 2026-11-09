"""Ensaio sem rede: render real do overlay + exemplos fictícios de outputs e tags."""

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import checar_overlay as gate


ROOT = Path(__file__).resolve().parents[3]
SHA = "abc1234" + "0" * 33
FILA = "https://sqs.us-east-2.amazonaws.com/123456789012/togglemaster-events"
REDIS = "redis://cache.exemplo.cache.amazonaws.com:6379"
ROLES = {s: f"arn:aws:iam::123456789012:role/togglemaster-{s}-irsa" for s in ("evaluation", "analytics")}
REPOS = {s: f"123456789012.dkr.ecr.us-east-2.amazonaws.com/{s}-service" for s in gate.SERVICOS}


class TestPreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = list(yaml.safe_load_all(gate.executar(ROOT, ["kubectl", "kustomize", "gitops/overlays/prod"])))

    def setUp(self):
        self.docs = copy.deepcopy(self.original)
        self.obj = {(d["kind"], d["metadata"]["name"]): d for d in self.docs}
        for svc, repo in REPOS.items():
            self.container(svc)["image"] = repo + ":v1.0.0-" + SHA[:7]
        for svc, arn in ROLES.items():
            self.obj["ServiceAccount", svc + "-service"]["metadata"]["annotations"]["eks.amazonaws.com/role-arn"] = arn
            self.obj["ConfigMap", svc + "-service-config"]["data"]["AWS_SQS_URL"] = FILA
        self.obj["ConfigMap", "evaluation-service-config"]["data"]["REDIS_URL"] = REDIS

    def container(self, svc):
        return self.obj["Deployment", svc + "-service"]["spec"]["template"]["spec"]["containers"][0]

    def render(self, sync=False):
        return gate.conferir_render(self.docs, FILA, REDIS, ROLES, REPOS if sync else None, SHA if sync else None)

    def test_primeira_publicacao_e_fila_no_consumidor(self):
        self.assertEqual(len(self.render(True)), 5)
        self.obj["ConfigMap", "analytics-service-config"]["data"]["AWS_SQS_URL"] += "-fila-errada"
        with self.assertRaisesRegex(gate.Falha, "analytics-service / AWS_SQS_URL"):
            self.render()

    def test_imagem_sentinela_so_bloqueia_pre_sync(self):
        self.container("flag")["image"] = "registry.conta-pendente.invalid/flag-service:conta-pendente"
        self.render()
        with self.assertRaisesRegex(gate.Falha, "flag-service / imagem"):
            self.render(True)

    def test_redis_sobreposto_no_deployment(self):
        self.container("evaluation")["env"].append({"name": "REDIS_URL", "value": "redis://outro:6379"})
        with self.assertRaisesRegex(gate.Falha, "evaluation-service / REDIS_URL"):
            self.render()

    def test_associacao_irsa_errada(self):
        self.obj["Deployment", "analytics-service"]["spec"]["template"]["spec"]["serviceAccountName"] = "default"
        with self.assertRaisesRegex(gate.Falha, "analytics-service / ServiceAccount"):
            self.render()

    def test_arn_sentinela(self):
        sa = self.obj["ServiceAccount", "evaluation-service"]
        sa["metadata"]["annotations"]["eks.amazonaws.com/role-arn"] = "arn:aws:iam::CONTA_AWS_PENDENTE:role/teste"
        with self.assertRaisesRegex(gate.Falha, "evaluation-service / anotação IRSA"):
            self.render()

    def test_cli_ecr_exige_tag_exata(self):
        imagens = self.render(True)
        def ecr(pasta, args):
            self.assertEqual(args[:3], ["aws", "ecr", "describe-images"])
            self.assertEqual(args[args.index("--image-ids") + 1], "imageTag=v1.0.0-" + SHA[:7])
            return json.dumps([{"tags": ["v1.0.0-" + SHA[:7]], "digest": "sha256:" + "a" * 64}])
        with patch.object(gate, "executar", side_effect=ecr) as aws:
            gate.conferir_tags(ROOT, imagens)
            self.assertEqual(aws.call_count, 5)
        falso = json.dumps([{"tags": ["latest"], "digest": "sha256:" + "a" * 64}])
        with patch.object(gate, "executar", return_value=falso), self.assertRaisesRegex(gate.Falha, "ECR"):
            gate.conferir_tags(ROOT, imagens)

    def test_checkout_exige_main_atual_e_gitops_limpo(self):
        with patch.object(gate, "executar", side_effect=["", "b" * 40, "a" * 40 + "\trefs/heads/main"]):
            with self.assertRaisesRegex(gate.Falha, "main remota"):
                gate.conferir_checkout(ROOT)
        with patch.object(gate, "executar", return_value=" M gitops/overlays/prod/kustomization.yaml"):
            with self.assertRaisesRegex(gate.Falha, "mudanças locais"):
                gate.conferir_checkout(ROOT)


if __name__ == "__main__":
    unittest.main()
