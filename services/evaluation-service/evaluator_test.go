package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/alicebob/miniredis/v2"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/request"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/go-redis/redis/v8"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
)

type capturedMessage struct {
	input    *sqs.SendMessageInput
	ctxErr   error
	deadline time.Time
}
type fakeSQS struct {
	messages chan capturedMessage
	err      error
}

func (f *fakeSQS) SendMessageWithContext(ctx aws.Context, input *sqs.SendMessageInput, _ ...request.Option) (*sqs.SendMessageOutput, error) {
	deadline, _ := ctx.Deadline()
	f.messages <- capturedMessage{input: input, ctxErr: ctx.Err(), deadline: deadline}
	return &sqs.SendMessageOutput{}, f.err
}

func TestSQSPreservesParentAfterRequestCancelAndBusinessBody(t *testing.T) {
	exporter := testTracing(t)
	var logs bytes.Buffer
	slog.SetDefault(newJSONLogger(&logs, "evaluation-service"))
	fake := &fakeSQS{messages: make(chan capturedMessage, 1)}
	app := &App{SqsSvc: fake, SqsQueueURL: "http://local-sqs/PRIVATE_QUEUE"}
	remote := propagation.TraceContext{}.Extract(context.Background(), propagation.MapCarrier{
		"traceparent": "00-11111111111111111111111111111111-2222222222222222-01",
		"tracestate":  "vendor=value",
		"baggage":     "user=PRIVATE_BAGGAGE",
	})
	ctx, parent := otel.Tracer("test").Start(remote, "http.request")
	ctx, cancel := context.WithCancel(ctx)
	cancel()
	before := time.Now()
	app.publishEvaluationEvent(ctx, "PRIVATE_USER", "PRIVATE_FLAG", true)
	app.producers.Wait()
	message := <-fake.messages
	if message.ctxErr != nil {
		t.Fatalf("publish canceled by HTTP: %v", message.ctxErr)
	}
	if remaining := message.deadline.Sub(before); remaining <= 0 || remaining > 5*time.Second+time.Second {
		t.Fatalf("own timeout missing: %s", remaining)
	}
	if len(message.input.MessageAttributes) != 2 {
		t.Fatalf("message attributes=%v", message.input.MessageAttributes)
	}
	carrier := propagation.MapCarrier{}
	for key, attr := range message.input.MessageAttributes {
		if aws.StringValue(attr.DataType) != "String" {
			t.Fatalf("attribute type=%v", attr)
		}
		carrier[key] = aws.StringValue(attr.StringValue)
	}
	propagated := trace.SpanContextFromContext(propagation.TraceContext{}.Extract(context.Background(), carrier))
	spans := exporter.GetSpans()
	if len(spans) != 1 {
		t.Fatalf("producer span count=%d", len(spans))
	}
	producer := spans[0]
	if producer.SpanKind != trace.SpanKindProducer || producer.Parent.SpanID() != parent.SpanContext().SpanID() || producer.SpanContext.TraceID() != propagated.TraceID() || producer.SpanContext.SpanID() != propagated.SpanID() {
		t.Fatalf("producer ancestry mismatch: %+v", producer)
	}
	if carrier["tracestate"] != "vendor=value" || carrier["baggage"] != "" {
		t.Fatalf("W3C carrier=%v", carrier)
	}
	var body map[string]any
	if err := json.Unmarshal([]byte(aws.StringValue(message.input.MessageBody)), &body); err != nil {
		t.Fatal(err)
	}
	if len(body) != 4 || body["user_id"] != "PRIVATE_USER" || body["flag_name"] != "PRIVATE_FLAG" || body["result"] != true || body["timestamp"] == nil {
		t.Fatalf("business body changed: %v", body)
	}
	parent.End()
	if strings.Contains(logs.String(), "PRIVATE") {
		t.Fatalf("sensitive log=%s", logs.String())
	}
	if !strings.Contains(logs.String(), producer.SpanContext.SpanID().String()) {
		t.Fatal("SQS log must correlate to producer")
	}
}

func TestSQSErrorLogsAreStatic(t *testing.T) {
	exporter := testTracing(t)
	var logs bytes.Buffer
	slog.SetDefault(newJSONLogger(&logs, "evaluation-service"))
	fake := &fakeSQS{messages: make(chan capturedMessage, 1), err: errors.New("PRIVATE_URL_AND_AUTH")}
	app := &App{SqsSvc: fake, SqsQueueURL: "PRIVATE_QUEUE"}
	app.publishEvaluationEvent(context.Background(), "PRIVATE_USER", "PRIVATE_FLAG", false)
	app.producers.Wait()
	if strings.Contains(logs.String(), "PRIVATE") || !strings.Contains(logs.String(), "sqs.publish.failed") {
		t.Fatalf("unsafe SQS log=%s", logs.String())
	}
	for _, span := range exporter.GetSpans() {
		if strings.Contains(span.Status.Description, "PRIVATE") || len(span.Events) != 0 {
			t.Fatalf("unsafe error detail=%v", span)
		}
	}
}

func TestEvaluationCacheMissParallelHTTPAndRedisSpans(t *testing.T) {
	exporter := testTracing(t)
	var logs bytes.Buffer
	slog.SetDefault(newJSONLogger(&logs, "evaluation-service"))
	cache := miniredis.RunT(t)
	client := redis.NewClient(&redis.Options{Addr: cache.Addr()})
	defer func() { _ = client.Close() }()
	incoming := make(chan trace.SpanContext, 2)
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := propagation.TraceContext{}.Extract(r.Context(), propagation.HeaderCarrier(r.Header))
		incoming <- trace.SpanContextFromContext(ctx)
		if strings.HasPrefix(r.URL.Path, "/flags/") {
			_, _ = w.Write([]byte(`{"name":"PRIVATE_FLAG","is_enabled":true}`))
		} else {
			_, _ = w.Write([]byte(`{"flag_name":"PRIVATE_FLAG","is_enabled":false}`))
		}
	}))
	defer upstream.Close()
	fake := &fakeSQS{messages: make(chan capturedMessage, 2)}
	app := &App{
		RedisClient: client, SqsSvc: fake, SqsQueueURL: "local-queue",
		FlagServiceURL: upstream.URL, TargetingServiceURL: upstream.URL,
		HttpClient: &http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport), Timeout: time.Second},
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/evaluate", app.evaluationHandler)
	handler := instrumentHandler(mux)
	req := httptest.NewRequest("GET", "/evaluate?user_id=PRIVATE_USER&flag_name=PRIVATE_FLAG", nil)
	req.Header.Set("traceparent", "00-11111111111111111111111111111111-2222222222222222-01")
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, req)
	app.producers.Wait()
	if response.Code != http.StatusOK {
		t.Fatalf("evaluation=%d body=%s", response.Code, response.Body)
	}
	var result EvaluationResponse
	if err := json.Unmarshal(response.Body.Bytes(), &result); err != nil {
		t.Fatal(err)
	}
	if !result.Result || result.UserID != "PRIVATE_USER" || result.FlagName != "PRIVATE_FLAG" {
		t.Fatalf("business response=%v", result)
	}
	for i := 0; i < 2; i++ {
		sc := <-incoming
		if !sc.IsValid() || sc.TraceID().String() != "11111111111111111111111111111111" {
			t.Fatalf("HTTP trace propagation=%s", sc.TraceID())
		}
	}
	response = httptest.NewRecorder()
	handler.ServeHTTP(response, req)
	app.producers.Wait()
	if response.Code != http.StatusOK || !strings.Contains(logs.String(), "cache.hit") || !strings.Contains(logs.String(), "cache.miss") {
		t.Fatalf("cache regression: %d %s", response.Code, logs.String())
	}
	operations := map[string]int{}
	for _, span := range exporter.GetSpans() {
		operations[span.Name]++
		if strings.HasPrefix(span.Name, "redis ") {
			if span.Parent.SpanID().IsValid() == false {
				t.Fatal("orphan redis span")
			}
			for _, attr := range span.Attributes {
				if strings.Contains(attr.Value.AsString(), "PRIVATE") || strings.Contains(string(attr.Key), "statement") {
					t.Fatalf("sensitive redis span=%v", attr)
				}
			}
		}
	}
	if operations["redis GET"] != 2 || operations["redis SET"] != 1 || operations["sqs publish"] != 2 {
		t.Fatalf("span operations=%v", operations)
	}
	if strings.Contains(logs.String(), "PRIVATE") {
		t.Fatalf("sensitive logs=%s", logs.String())
	}
}

func TestParallelHTTPUsesRequestCancellation(t *testing.T) {
	testTracing(t)
	entered := make(chan struct{}, 2)
	exited := make(chan struct{}, 2)
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		entered <- struct{}{}
		<-r.Context().Done()
		exited <- struct{}{}
	}))
	defer upstream.Close()
	app := &App{FlagServiceURL: upstream.URL, TargetingServiceURL: upstream.URL, HttpClient: &http.Client{Timeout: time.Second}}
	ctx, cancel := context.WithCancel(context.Background())
	result := make(chan error, 1)
	go func() { _, err := app.fetchFromServices(ctx, "PRIVATE_FLAG"); result <- err }()
	for i := 0; i < 2; i++ {
		select {
		case <-entered:
		case <-time.After(time.Second):
			t.Fatal("parallel request missing")
		}
	}
	cancel()
	select {
	case err := <-result:
		if err == nil {
			t.Fatal("cancel should fail flag fetch")
		}
	case <-time.After(time.Second):
		t.Fatal("HTTP context cancellation ignored")
	}
	for i := 0; i < 2; i++ {
		select {
		case <-exited:
		case <-time.After(time.Second):
			t.Fatal("upstream not canceled")
		}
	}
}

func TestRedisUsesCanceledRequestContext(t *testing.T) {
	exporter := testTracing(t)
	cache := miniredis.RunT(t)
	// Se GET nao recebesse o contexto cancelado, esse cache hit seria devolvido.
	if err := cache.Set("flag_info:PRIVATE_FLAG", `{"Flag":{"is_enabled":true}}`); err != nil {
		t.Fatalf("seed Redis: %v", err)
	}
	client := redis.NewClient(&redis.Options{Addr: cache.Addr(), MaxRetries: -1})
	defer func() { _ = client.Close() }()
	app := &App{RedisClient: client, HttpClient: &http.Client{Timeout: time.Second}, FlagServiceURL: "http://127.0.0.1:1", TargetingServiceURL: "http://127.0.0.1:1"}
	ctx, parent := otel.Tracer("test").Start(context.Background(), "request")
	ctx, cancel := context.WithCancel(ctx)
	cancel()
	_, err := app.getCombinedFlagInfo(ctx, "PRIVATE_FLAG")
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("Redis/request cancel ignored, error=%v", err)
	}
	spans := exporter.GetSpans()
	if len(spans) != 1 || spans[0].Name != "redis GET" || spans[0].Parent.SpanID() != parent.SpanContext().SpanID() {
		t.Fatalf("redis ancestry=%v", spans)
	}
	parent.End()
}
