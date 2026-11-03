"""Provas locais da instrumentacao, sem rede/AWS e sem modificar o negocio."""
import io
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, StatusCode

# O CI roda os testes a partir da pasta do servico.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import telemetry

SERVICE = "targeting-service"
EXPORTER = InMemorySpanExporter()
PROVIDER = TracerProvider(resource=Resource.create({"service.name": SERVICE}), shutdown_on_exit=False)
PROVIDER.add_span_processor(SimpleSpanProcessor(EXPORTER))
trace.set_tracer_provider(PROVIDER)
with patch.dict(os.environ, {"OTEL_SDK_DISABLED": "true"}):
    LOGGER = telemetry.configure_telemetry(SERVICE)
telemetry._provider = PROVIDER


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        EXPORTER.clear()
        self.output = io.StringIO()
        self.handler = logging.StreamHandler(self.output)
        self.handler.setFormatter(telemetry.JsonFormatter())
        self.old_handlers = LOGGER.handlers
        LOGGER.handlers = [self.handler]

    def tearDown(self):
        LOGGER.handlers = self.old_handlers

    def make_app(self):
        app = Flask(__name__)
        app.config["TELEMETRY_SERVICE_NAME"] = SERVICE
        telemetry.instrument_flask(app)

        @app.route("/example/<item>")
        def example(item):
            return {"ok": True}

        @app.route("/health")
        def health():
            return {"status": "ok"}
        return app

    def test_http_parent_context_and_safe_json_log(self):
        app = self.make_app()
        parent = "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
        response = app.test_client().get("/example/synthetic-item?secret=synthetic-query", headers={
            "traceparent": parent,
            "Authorization": "Bearer synthetic-secret",
            "baggage": "user.id=synthetic-baggage",
        })
        self.assertEqual(response.status_code, 200)
        spans = EXPORTER.get_finished_spans()
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].kind, SpanKind.SERVER)
        self.assertEqual(format(spans[0].context.trace_id, "032x"), parent[3:35])
        self.assertEqual(format(spans[0].parent.span_id, "016x"), parent[36:52])
        event = json.loads(self.output.getvalue().splitlines()[-1])
        self.assertEqual(event["trace_id"], parent[3:35])
        self.assertEqual(event["service.name"], SERVICE)
        self.assertEqual(event["http.route"], "/example/<item>")
        self.assertEqual(event["http.status_code"], 200)
        for private in ("synthetic-secret", "synthetic-query", "synthetic-item", "synthetic-baggage"):
            self.assertNotIn(private, self.output.getvalue())

    def test_health_does_not_create_spans(self):
        response = self.make_app().test_client().get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EXPORTER.get_finished_spans(), ())

    def test_manual_error_retains_type_without_message(self):
        with self.assertRaises(ValueError):
            with telemetry.traced_operation("test.operation"):
                raise ValueError("synthetic-private-detail")
        span = EXPORTER.get_finished_spans()[0]
        self.assertEqual(span.status.status_code, StatusCode.ERROR)
        self.assertEqual(span.attributes["error.type"], "ValueError")
        self.assertEqual(span.events[0].attributes, {"exception.type": "ValueError"})
        self.assertIsNone(span.status.description)

    def test_no_endpoint_and_explicit_disabled_do_not_create_exporters(self):
        clean_env = {key: value for key, value in os.environ.items() if not key.startswith("OTEL_")}
        program = "import telemetry; telemetry.configure_telemetry('unit-service'); assert telemetry._provider is None"
        for variables in ({}, {"OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:4318", "OTEL_SDK_DISABLED": "true"}):
            result = subprocess.run([sys.executable, "-c", program], env={**clean_env, **variables},
                                    cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)


class RequestsPropagationTests(unittest.TestCase):
    def test_w3c_header_reaches_upstream_without_baggage(self):
        import requests
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        captured = {}

        def fake_send(_session, request, **_kwargs):
            captured.update(request.headers)
            response = requests.Response()
            response.status_code = 200
            response.request = request
            response._content = b"{}"
            return response

        EXPORTER.clear()
        instrumentor = RequestsInstrumentor()
        with patch("requests.sessions.Session.send", new=fake_send):
            instrumentor.instrument(tracer_provider=PROVIDER)
            try:
                with trace.get_tracer("test").start_as_current_span("caller") as parent:
                    requests.get("http://upstream.invalid/validate", timeout=1)
                    self.assertEqual(captured["traceparent"][3:35], format(parent.get_span_context().trace_id, "032x"))
                    self.assertNotIn("baggage", captured)
            finally:
                instrumentor.uninstrument()
        self.assertEqual(sum(span.kind == SpanKind.CLIENT for span in EXPORTER.get_finished_spans()), 1)



class PostgresTracingTests(unittest.TestCase):
    def test_pool_real_dict_cursor_keeps_select_span_and_parameter_privacy(self):
        import importlib.util
        from types import SimpleNamespace
        from psycopg2.extras import RealDictCursor
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

        # Pool, factory RealDictCursor e instrumentador reais; nenhum banco/rede.
        private_name = "synthetic-private-db-name"
        is_flag = SERVICE == "flag-service"
        row = ({"name": private_name, "is_enabled": True} if is_flag else
               {"flag_name": private_name, "rules": {"type": "PERCENTAGE", "value": 100}})
        executed = []
        factories = []

        class FakeConnection:
            closed = False
            info = SimpleNamespace(dbname="unitdb", port=5432, host="db.invalid", user="unit",
                                   transaction_status=0)

            def __init__(self, cursor_factory):
                self.cursor_factory = cursor_factory

            def cursor(self, **kwargs):
                factory = kwargs.get("cursor_factory", self.cursor_factory)
                factories.append(factory)
                return factory.__new__(factory)

            def close(self):
                self.closed = True

        def fake_connect(*_args, **kwargs):
            return FakeConnection(kwargs["cursor_factory"])

        def fake_execute(_cursor, statement, parameters=None):
            executed.append((statement, parameters))

        variables = {"DATABASE_URL": "postgresql://unit@db.invalid/unitdb",
                     "AUTH_SERVICE_URL": "http://upstream.invalid", "OTEL_SDK_DISABLED": "true"}
        instrumentor = Psycopg2Instrumentor()
        EXPORTER.clear()
        with patch.dict(os.environ, variables), \
                patch("psycopg2.connect", new=fake_connect), \
                patch.object(RealDictCursor, "execute", new=fake_execute), \
                patch.object(RealDictCursor, "fetchone", return_value=row), \
                patch.object(RealDictCursor, "close"), \
                patch("requests.get") as upstream:
            instrumentor.instrument(tracer_provider=PROVIDER, capture_parameters=False, enable_commenter=False)
            try:
                app_file = Path(__file__).resolve().parents[1] / "app.py"
                spec = importlib.util.spec_from_file_location("postgres_app_under_test", app_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                upstream.return_value.status_code = 200
                route = "/flags/" if is_flag else "/rules/"
                response = module.app.test_client().get(route + private_name,
                                                        headers={"Authorization": "Bearer synthetic-secret"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), row)
                self.assertTrue(issubclass(factories[0], RealDictCursor))
                spans = EXPORTER.get_finished_spans()
                servers = [span for span in spans if span.kind == SpanKind.SERVER]
                queries = [span for span in spans if span.kind == SpanKind.CLIENT and span.name == "SELECT"]
                self.assertEqual(len(servers), 1)
                self.assertEqual(len(queries), 1)
                self.assertEqual(queries[0].parent.span_id, servers[0].context.span_id)
                self.assertEqual(executed[0][1], (private_name,))
                self.assertNotIn("/*", executed[0][0])
                self.assertNotIn("db.statement.parameters", queries[0].attributes)
                self.assertNotIn(private_name, str(dict(queries[0].attributes)))
            finally:
                instrumentor.uninstrument()



if __name__ == "__main__":
    unittest.main()
