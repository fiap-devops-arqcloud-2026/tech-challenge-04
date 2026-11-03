package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"strings"
	"time"

	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/trace"
	"go.opentelemetry.io/otel/trace/noop"
)

// Os dois servicos Go sao modulos independentes; este bootstrap fica em cada
// contexto Docker para que continuem compilando sem dependencias fora dele.
func initTelemetry(ctx context.Context, defaultService string) (func(context.Context) error, error) {
	service := os.Getenv("OTEL_SERVICE_NAME")
	if service == "" {
		service = defaultService
	}
	slog.SetDefault(slog.New(correlationHandler{Handler: slog.NewJSONHandler(os.Stdout, nil)}).With("service.name", service))
	// Baggage nao faz parte do contrato: nao encaminhar dados de usuario.
	otel.SetTextMapPropagator(propagation.TraceContext{})
	otel.SetTracerProvider(noop.NewTracerProvider())
	shutdown := func(context.Context) error { return nil }
	if strings.EqualFold(os.Getenv("OTEL_SDK_DISABLED"), "true") ||
		(os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT") == "" && os.Getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT") == "") {
		return shutdown, nil
	}
	// O exporter le os endpoints OTEL_*; endpoint base recebe /v1/traces,
	// enquanto TRACES_ENDPOINT e utilizado integralmente. Nenhum destino cloud.
	exporter, err := otlptracehttp.New(ctx)
	if err != nil {
		return shutdown, errors.New("nao foi possivel inicializar exporter OTLP HTTP")
	}
	res, err := resource.New(ctx, resource.WithFromEnv(), resource.WithTelemetrySDK(), resource.WithAttributes(
		attribute.String("service.name", service), attribute.String("service.namespace", "togglemaster"),
	))
	if err != nil {
		_ = exporter.Shutdown(ctx)
		return shutdown, errors.New("nao foi possivel inicializar resource OTel")
	}
	provider := sdktrace.NewTracerProvider(sdktrace.WithResource(res), sdktrace.WithBatcher(exporter))
	otel.SetTracerProvider(provider)
	// Erros de transporte podem conter URL/headers: registrar somente operacao.
	otel.SetErrorHandler(otel.ErrorHandlerFunc(func(error) { slog.Warn("otel.export.failed") }))
	return provider.Shutdown, nil
}

type correlationHandler struct{ slog.Handler }

func (h correlationHandler) Handle(ctx context.Context, record slog.Record) error {
	if sc := trace.SpanContextFromContext(ctx); sc.IsValid() {
		record.AddAttrs(slog.String("trace_id", sc.TraceID().String()), slog.String("span_id", sc.SpanID().String()))
	}
	return h.Handler.Handle(ctx, record)
}

func (h correlationHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return correlationHandler{Handler: h.Handler.WithAttrs(attrs)}
}

func (h correlationHandler) WithGroup(name string) slog.Handler {
	return correlationHandler{Handler: h.Handler.WithGroup(name)}
}

type statusWriter struct {
	http.ResponseWriter
	status int
	wrote  bool
}

func (w *statusWriter) WriteHeader(status int) {
	if !w.wrote {
		w.status, w.wrote = status, true
		w.ResponseWriter.WriteHeader(status)
	}
}

func (w *statusWriter) Write(body []byte) (int, error) {
	if !w.wrote {
		w.WriteHeader(http.StatusOK)
	}
	return w.ResponseWriter.Write(body)
}

func (w *statusWriter) Unwrap() http.ResponseWriter { return w.ResponseWriter }

func instrumentHandler(next http.Handler) http.Handler {
	logged := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		status := &statusWriter{ResponseWriter: w, status: http.StatusOK}
		next.ServeHTTP(status, r)
		if r.URL.Path != "/health" {
			route := r.Pattern
			if route == "" {
				route = "unmatched"
			}
			slog.InfoContext(r.Context(), "http.request.completed", "http.method", r.Method, "http.route", route, "http.status_code", status.status)
		}
	})
	return otelhttp.NewHandler(logged, "http.request", otelhttp.WithFilter(func(r *http.Request) bool { return r.URL.Path != "/health" }))
}

func dependencySpan(ctx context.Context, name, system, operation string) (context.Context, trace.Span) {
	return otel.Tracer("togglemaster").Start(ctx, name, trace.WithSpanKind(trace.SpanKindClient), trace.WithAttributes(
		attribute.String("db.system.name", system), attribute.String("db.operation.name", operation),
	))
}

func markOperationError(span trace.Span, operation string) {
	span.SetStatus(codes.Error, operation+" failed")
	span.SetAttributes(attribute.String("error.type", operation))
}

// Shutdown usa contexto novo: o contexto do sinal ja foi cancelado.
func shutdownTelemetry(shutdown func(context.Context) error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := shutdown(ctx); err != nil {
		slog.Warn("otel.shutdown.failed")
	}
}
