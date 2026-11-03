package main

import (
	"context"
	"encoding/json"
	"log/slog"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/request"
	"github.com/aws/aws-sdk-go/service/sqs"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
)

// Interface minima: o fake de teste usa a mesma chamada do SDK real.
type messageSender interface {
	SendMessageWithContext(aws.Context, *sqs.SendMessageInput, ...request.Option) (*sqs.SendMessageOutput, error)
}

// Contrato de negocio preservado: contexto W3C vai somente em MessageAttributes.
type EvaluationEvent struct {
	UserID    string    `json:"user_id"`
	FlagName  string    `json:"flag_name"`
	Result    bool      `json:"result"`
	Timestamp time.Time `json:"timestamp"`
}

func (a *App) publishEvaluationEvent(ctx context.Context, userID, flagName string, result bool) {
	a.producers.Add(1)
	// O request pode terminar logo apos a resposta. Sem transportar cancelamento,
	// conservamos o parent span e limitamos a publicacao ao proprio prazo de 5s.
	publishCtx, cancel := context.WithTimeout(context.WithoutCancel(ctx), 5*time.Second)
	go func() {
		defer a.producers.Done()
		defer cancel()
		a.sendEvaluationEvent(publishCtx, userID, flagName, result)
	}()
}

func (a *App) sendEvaluationEvent(ctx context.Context, userID, flagName string, result bool) {
	if a.SqsSvc == nil || a.SqsQueueURL == "" {
		slog.InfoContext(ctx, "sqs.disabled")
		return
	}
	ctx, span := otel.Tracer("togglemaster").Start(ctx, "sqs publish", trace.WithSpanKind(trace.SpanKindProducer), trace.WithAttributes(
		attribute.String("messaging.system", "aws_sqs"), attribute.String("messaging.operation.name", "publish"),
	))
	defer span.End()
	event := EvaluationEvent{UserID: userID, FlagName: flagName, Result: result, Timestamp: time.Now().UTC()}
	body, err := json.Marshal(event)
	if err != nil {
		markOperationError(span, "sqs.encode")
		slog.ErrorContext(ctx, "sqs.encode.failed")
		return
	}
	carrier := propagation.MapCarrier{}
	otel.GetTextMapPropagator().Inject(ctx, carrier)
	attrs := make(map[string]*sqs.MessageAttributeValue, 2)
	for _, key := range []string{"traceparent", "tracestate"} {
		if value := carrier.Get(key); value != "" {
			attrs[key] = &sqs.MessageAttributeValue{DataType: aws.String("String"), StringValue: aws.String(value)}
		}
	}
	_, err = a.SqsSvc.SendMessageWithContext(ctx, &sqs.SendMessageInput{
		MessageBody: aws.String(string(body)), QueueUrl: aws.String(a.SqsQueueURL), MessageAttributes: attrs,
	})
	if err != nil {
		markOperationError(span, "sqs.publish")
		slog.ErrorContext(ctx, "sqs.publish.failed")
		return
	}
	slog.InfoContext(ctx, "sqs.published")
}
