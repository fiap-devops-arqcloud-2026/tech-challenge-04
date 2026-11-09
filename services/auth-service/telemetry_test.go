package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/sdk/trace/tracetest"
	"go.opentelemetry.io/otel/trace"
	collector "go.opentelemetry.io/proto/otlp/collector/trace/v1"
	"google.golang.org/protobuf/proto"
)

func testTracing(t *testing.T) *tracetest.InMemoryExporter {
	t.Helper()
	previousProvider, previousPropagator, previousLogger := otel.GetTracerProvider(), otel.GetTextMapPropagator(), slog.Default()
	exporter := tracetest.NewInMemoryExporter()
	provider := sdktrace.NewTracerProvider(sdktrace.WithSyncer(exporter))
	otel.SetTracerProvider(provider)
	otel.SetTextMapPropagator(propagation.TraceContext{})
	t.Cleanup(func() {
		_ = provider.Shutdown(context.Background())
		otel.SetTracerProvider(previousProvider)
		otel.SetTextMapPropagator(previousPropagator)
		slog.SetDefault(previousLogger)
	})
	return exporter
}

func TestOTLPHTTPParentHealthAndCorrelatedJSON(t *testing.T) {
	for _, specific := range []bool{false, true} {
		name := "base_endpoint"
		if specific {
			name = "traces_endpoint"
		}
		t.Run(name, func(t *testing.T) {
			previousProvider, previousPropagator, previousLogger := otel.GetTracerProvider(), otel.GetTextMapPropagator(), slog.Default()
			t.Cleanup(func() {
				otel.SetTracerProvider(previousProvider)
				otel.SetTextMapPropagator(previousPropagator)
				slog.SetDefault(previousLogger)
			})
			requests := make(chan *collector.ExportTraceServiceRequest, 2)
			paths := make(chan string, 2)
			receiver := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				body, err := io.ReadAll(r.Body)
				if err != nil {
					t.Error(err)
					w.WriteHeader(500)
					return
				}
				var batch collector.ExportTraceServiceRequest
				if err := proto.Unmarshal(body, &batch); err != nil {
					t.Error(err)
					w.WriteHeader(500)
					return
				}
				requests <- &batch
				paths <- r.URL.Path
				w.Header().Set("Content-Type", "application/x-protobuf")
				w.WriteHeader(200)
			}))
			defer receiver.Close()
			t.Setenv("OTEL_SDK_DISABLED", "false")
			t.Setenv("OTEL_SERVICE_NAME", "go-service-test")
			t.Setenv("OTEL_EXPORTER_OTLP_ENDPOINT", receiver.URL)
			t.Setenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "")
			expectedPath := "/v1/traces"
			if specific {
				expectedPath = "/custom-traces"
				t.Setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:1")
				t.Setenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", receiver.URL+expectedPath)
			}
			shutdown, err := initTelemetry(context.Background(), "unused")
			if err != nil {
				t.Fatal(err)
			}
			var logs bytes.Buffer
			slog.SetDefault(newJSONLogger(&logs, "go-service-test"))
			mux := http.NewServeMux()
			var seen trace.SpanContext
			mux.HandleFunc("/work", func(w http.ResponseWriter, r *http.Request) {
				seen = trace.SpanContextFromContext(r.Context())
				w.WriteHeader(http.StatusAccepted)
			})
			mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) { w.WriteHeader(http.StatusOK) })
			handler := instrumentHandler(mux)
			req := httptest.NewRequest("GET", "/work?user_id=PRIVATE_USER&flag_name=PRIVATE_FLAG", nil)
			req.Header.Set("Authorization", "Bearer PRIVATE_KEY")
			req.Header.Set("Baggage", "user=PRIVATE_BAGGAGE")
			req.Header.Set("traceparent", "00-11111111111111111111111111111111-2222222222222222-01")
			response := httptest.NewRecorder()
			handler.ServeHTTP(response, req)
			if response.Code != http.StatusAccepted {
				t.Fatalf("status: %d", response.Code)
			}
			if seen.TraceID().String() != "11111111111111111111111111111111" {
				t.Fatalf("wrong trace: %s", seen.TraceID())
			}
			handler.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest("GET", "/health", nil))
			ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()
			if err := shutdown(ctx); err != nil {
				t.Fatal(err)
			}
			select {
			case batch := <-requests:
				count := 0
				foundName := false
				for _, rs := range batch.ResourceSpans {
					for _, attr := range rs.Resource.Attributes {
						if attr.Key == "service.name" && attr.Value.GetStringValue() == "go-service-test" {
							foundName = true
						}
					}
					for _, scope := range rs.ScopeSpans {
						for _, span := range scope.Spans {
							count++
							if !bytes.Equal(span.ParentSpanId, bytes.Repeat([]byte{0x22}, 8)) {
								t.Fatalf("parent: %x", span.ParentSpanId)
							}
						}
					}
				}
				if count != 1 || !foundName {
					t.Fatalf("exported spans=%d, service.name=%v", count, foundName)
				}
			case <-ctx.Done():
				t.Fatal("no OTLP export")
			}
			if path := <-paths; path != expectedPath {
				t.Fatalf("path=%s", path)
			}
			var entry map[string]any
			if err := json.Unmarshal(bytes.TrimSpace(logs.Bytes()), &entry); err != nil {
				t.Fatalf("JSON log: %v: %s", err, logs.String())
			}
			if entry["service.name"] != "go-service-test" || entry["trace_id"] != seen.TraceID().String() || entry["span_id"] != seen.SpanID().String() || entry["event"] != "http.request.completed" {
				t.Fatalf("correlation missing: %v", entry)
			}
			if strings.Contains(logs.String(), "PRIVATE") {
				t.Fatalf("sensitive log: %s", logs.String())
			}
		})
	}
}

func TestTelemetryOptInAndDisabled(t *testing.T) {
	for _, disabled := range []bool{false, true} {
		t.Run(map[bool]string{false: "no_endpoint", true: "sdk_disabled"}[disabled], func(t *testing.T) {
			previousProvider, previousPropagator, previousLogger := otel.GetTracerProvider(), otel.GetTextMapPropagator(), slog.Default()
			defer func() {
				otel.SetTracerProvider(previousProvider)
				otel.SetTextMapPropagator(previousPropagator)
				slog.SetDefault(previousLogger)
			}()
			t.Setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
			t.Setenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "")
			t.Setenv("OTEL_SDK_DISABLED", "false")
			if disabled {
				t.Setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:1")
				t.Setenv("OTEL_SDK_DISABLED", "TrUe")
			}
			shutdown, err := initTelemetry(context.Background(), "test")
			if err != nil {
				t.Fatal(err)
			}
			_, span := otel.Tracer("test").Start(context.Background(), "work")
			if span.IsRecording() {
				t.Fatal("tracing must be opt-in")
			}
			span.End()
			if err := shutdown(context.Background()); err != nil {
				t.Fatal(err)
			}
		})
	}
}

// Simula SIGTERM durante um handler: a drenagem e os produtores antecedem o SDK.
func TestGracefulShutdownDrainsRequestsThenProducers(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	entered, release := make(chan struct{}), make(chan struct{})
	afterRequests, releaseProducers := make(chan struct{}), make(chan struct{})
	served := make(chan error, 1)
	go func() {
		served <- serveHTTPListener(ctx, listener, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			close(entered)
			<-release
			w.WriteHeader(202)
		}), func() { close(afterRequests); <-releaseProducers })
	}()
	responseDone := make(chan error, 1)
	go func() {
		client := &http.Client{Timeout: 2 * time.Second}
		resp, err := client.Get("http://" + listener.Addr().String())
		if err == nil {
			_ = resp.Body.Close()
			if resp.StatusCode != 202 {
				err = fmt.Errorf("status=%d", resp.StatusCode)
			}
		}
		responseDone <- err
	}()
	select {
	case <-entered:
	case <-time.After(time.Second):
		t.Fatal("handler not started")
	}
	cancel()
	select {
	case <-afterRequests:
		t.Fatal("producers awaited before active handler finished")
	case <-time.After(20 * time.Millisecond):
	}
	close(release)
	select {
	case err := <-responseDone:
		if err != nil {
			t.Fatal(err)
		}
	case <-time.After(time.Second):
		t.Fatal("handler not drained")
	}
	select {
	case <-afterRequests:
	case <-time.After(time.Second):
		t.Fatal("producer drain not reached")
	}
	select {
	case <-served:
		t.Fatal("service ended before producers drained")
	default:
	}
	close(releaseProducers)
	select {
	case err := <-served:
		if err != nil {
			t.Fatal(err)
		}
	case <-time.After(time.Second):
		t.Fatal("graceful shutdown not completed")
	}
}
