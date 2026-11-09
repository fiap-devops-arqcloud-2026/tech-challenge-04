"""Tracing OTLP/HTTP e logs JSON do aplicativo (Fase 4, 2026-10-22).

A inicializacao acontece no import da aplicacao, depois do fork do Gunicorn
atual (sem --preload). Sem endpoint explicito, nao ha exportacao ou threads
OTel. Os tres contextos Docker possuem este mesmo arquivo de proposito.
"""

import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone

from opentelemetry import trace
from opentelemetry.propagate import set_global_textmap
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

_service_name = ""
_provider = None
_configured = False


class JsonFormatter(logging.Formatter):
    """Somente campos controlados; nao serializa headers, corpos ou excecoes."""

    def format(self, record):
        document = {
            "time": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "service.name": _service_name,
            "message": record.getMessage(),
        }
        span_context = trace.get_current_span().get_span_context()
        if span_context.is_valid:
            document["trace_id"] = format(span_context.trace_id, "032x")
            document["span_id"] = format(span_context.span_id, "016x")
        for field, attribute in (
            ("http.method", "http_method"),
            ("http.route", "http_route"),
            ("http.status_code", "http_status_code"),
            ("error.type", "error_type"),
            ("error.code", "error_code"),
        ):
            value = getattr(record, attribute, None)
            if value is not None:
                document[field] = value
        return json.dumps(document, ensure_ascii=False)


def configure_telemetry(default_service_name, *, postgres=False, requests_client=False):
    """Opt-in por endpoint; SDK_DISABLED=true tem precedencia.

    SDK/exporter/instrumentadores sao configurados uma unica vez por processo.
    Manter o Gunicorn sem --preload: pools, threads SQS e SDK nascem no worker.
    """
    global _service_name, _provider, _configured
    _service_name = os.getenv("OTEL_SERVICE_NAME", default_service_name)
    logger = logging.getLogger(f"togglemaster.{default_service_name}")
    if _configured:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    _configured = True

    # Nao propagar baggage: pode conter dados de usuario sem necessidade.
    set_global_textmap(TraceContextTextMapPropagator())
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if os.getenv("OTEL_SDK_DISABLED", "false").lower() == "true" or not endpoint:
        return logger

    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource.create({
        "service.name": _service_name,
        "service.namespace": "togglemaster",
    })
    _provider = TracerProvider(resource=resource)
    _provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(_provider)

    if requests_client:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        RequestsInstrumentor().instrument(tracer_provider=_provider)
    if postgres:
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
        Psycopg2Instrumentor().instrument(
            tracer_provider=_provider,
            capture_parameters=False,
            enable_commenter=False,
        )
    return logger


def instrument_flask(app):
    """Um span SERVER por request e log correlacionado, excluindo /health."""
    if _provider is None:
        return

    from flask import request
    from opentelemetry.instrumentation.flask import FlaskInstrumentor

    logger = logging.getLogger(f"togglemaster.{app.config['TELEMETRY_SERVICE_NAME']}")

    def response_hook(span, status, _headers):
        if span is None:
            return
        # O hook recebe a rota-modelo, nunca query string ou caminho do usuario.
        route = request.url_rule.rule if request.url_rule else "unmatched"
        with trace.use_span(span, end_on_exit=False):
            logger.info("http.request.completed", extra={
                "http_method": request.method,
                "http_route": route,
                "http_status_code": int(status.split(" ", 1)[0]),
            })

    FlaskInstrumentor().instrument_app(
        app,
        tracer_provider=_provider,
        excluded_urls=r".*/health(?:\?.*)?$",
        response_hook=response_hook,
        enable_commenter=False,
    )


def record_error(span, error):
    """Classe util do erro, sem mensagem/stacktrace que pode expor dados."""
    error_type = type(error).__name__
    span.set_attribute("error.type", error_type)
    span.set_status(Status(StatusCode.ERROR))
    span.add_event("exception", {"exception.type": error_type})


@contextmanager
def traced_operation(name, *, kind=SpanKind.INTERNAL, context=None, attributes=None):
    """Operacoes manuais do worker; evita registrar payload em excecoes."""
    tracer = trace.get_tracer(_service_name or "togglemaster")
    with tracer.start_as_current_span(
        name,
        kind=kind,
        context=context,
        attributes=attributes,
        record_exception=False,
        set_status_on_exception=False,
    ) as span:
        try:
            yield span
        except Exception as error:
            record_error(span, error)
            raise
