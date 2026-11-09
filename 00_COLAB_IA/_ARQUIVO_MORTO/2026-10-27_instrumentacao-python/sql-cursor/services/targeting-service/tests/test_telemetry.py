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


if __name__ == "__main__":
    unittest.main()
