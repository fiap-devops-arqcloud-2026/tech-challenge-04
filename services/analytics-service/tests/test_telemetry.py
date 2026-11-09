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

SERVICE = "analytics-service"
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


class ConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import importlib.util
        with patch.dict(os.environ, {"AWS_REGION": "us-east-2", "AWS_SQS_URL": "", "OTEL_SDK_DISABLED": "true"}):
            specification = importlib.util.spec_from_file_location("analytics_under_test", Path(__file__).resolve().parents[1] / "app.py")
            cls.app = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(cls.app)

    def setUp(self):
        from unittest.mock import Mock
        EXPORTER.clear()
        self.output = io.StringIO()
        self.handler = logging.StreamHandler(self.output)
        self.handler.setFormatter(telemetry.JsonFormatter())
        self.old_handlers = self.app.log.handlers
        self.app.log.handlers = [self.handler]
        self.app.sqs_client = Mock()
        self.app.dynamodb_client = Mock()
        self.app.DYNAMODB_TABLE_NAME = "LocalAnalytics"
        self.app.SQS_QUEUE_URL = "http://sqs.invalid/local-events"
        self.app.QUEUE_NAME = "local-events"
        self.message = {
            "MessageId": "synthetic-message", "ReceiptHandle": "synthetic-receipt",
            "Body": json.dumps({"user_id": "synthetic-private-user", "flag_name": "synthetic-private-flag",
                                "result": True, "timestamp": "2026-10-22T00:00:00Z"}),
            "MessageAttributes": {
                "traceparent": {"DataType": "String", "StringValue": "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"},
                "tracestate": {"DataType": "String", "StringValue": "vendor=opaque"},
            },
        }

    def tearDown(self):
        self.app.log.handlers = self.old_handlers

    def test_consumer_parent_persistence_then_ack_and_safe_logs(self):
        calls = []
        self.app.dynamodb_client.put_item.side_effect = lambda **kwargs: calls.append("persist")
        self.app.sqs_client.delete_message.side_effect = lambda **kwargs: calls.append("ack")
        self.app.process_message(self.message)
        self.assertEqual(calls, ["persist", "ack"])
        spans = EXPORTER.get_finished_spans()
        consumers = [span for span in spans if span.kind == SpanKind.CONSUMER]
        self.assertEqual(len(consumers), 1)
        consumer = consumers[0]
        self.assertEqual(format(consumer.context.trace_id, "032x"), "0123456789abcdef0123456789abcdef")
        self.assertEqual(format(consumer.parent.span_id, "016x"), "0123456789abcdef")
        self.assertEqual(consumer.context.trace_state.get("vendor"), "opaque")
        self.assertEqual(len(spans), 3)
        self.assertTrue(all(span.parent.span_id == consumer.context.span_id for span in spans if span != consumer))
        item = self.app.dynamodb_client.put_item.call_args.kwargs["Item"]
        self.assertEqual(set(item), {"event_id", "user_id", "flag_name", "result", "timestamp"})
        self.assertEqual(item["user_id"], {"S": "synthetic-private-user"})
        self.assertNotIn("synthetic-private", self.output.getvalue())
        self.assertNotIn("synthetic-receipt", self.output.getvalue())
        event = json.loads(self.output.getvalue().splitlines()[-1])
        self.assertEqual(event["trace_id"], "0123456789abcdef0123456789abcdef")

    def test_dynamodb_failure_does_not_ack_or_record_exception_payload(self):
        from botocore.exceptions import ClientError
        self.app.dynamodb_client.put_item.side_effect = ClientError(
            {"Error": {"Code": "ProvisionedThroughputExceededException", "Message": "synthetic-private-error"}}, "PutItem")
        self.app.process_message(self.message)
        self.app.sqs_client.delete_message.assert_not_called()
        spans = EXPORTER.get_finished_spans()
        self.assertEqual(len(spans), 2)
        self.assertTrue(all(span.status.status_code == StatusCode.ERROR for span in spans))
        self.assertNotIn("synthetic-private-error", self.output.getvalue())
        self.assertTrue(all("exception.message" not in event.attributes for span in spans for event in span.events))

    def test_invalid_json_does_not_persist_or_ack(self):
        self.message["Body"] = "not-json"
        self.app.process_message(self.message)
        self.app.dynamodb_client.put_item.assert_not_called()
        self.app.sqs_client.delete_message.assert_not_called()
        span = EXPORTER.get_finished_spans()[0]
        self.assertEqual(span.attributes["error.type"], "JSONDecodeError")

    def test_message_without_context_still_processes(self):
        self.message.pop("MessageAttributes")
        self.app.process_message(self.message)
        self.app.dynamodb_client.put_item.assert_called_once()
        self.app.sqs_client.delete_message.assert_called_once()
        consumer = next(span for span in EXPORTER.get_finished_spans() if span.kind == SpanKind.CONSUMER)
        self.assertIsNone(consumer.parent)


if __name__ == "__main__":
    unittest.main()
