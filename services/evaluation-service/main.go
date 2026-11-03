package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

// App permite injetar clientes reais ou fakes locais nos testes.
type App struct {
	RedisClient         *redis.Client
	SqsSvc              messageSender
	SqsQueueURL         string
	HttpClient          *http.Client
	FlagServiceURL      string
	TargetingServiceURL string
	producers           sync.WaitGroup
}

func main() {
	if err := run(); err != nil {
		slog.Error("service.start.failed")
		os.Exit(1)
	}
}

func run() error {
	_ = godotenv.Load()
	shutdown, err := initTelemetry(context.Background(), "evaluation-service")
	if err != nil {
		return err
	}
	defer shutdownTelemetry(shutdown)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8004"
	}
	redisURL, flagSvcURL, targetingSvcURL := os.Getenv("REDIS_URL"), os.Getenv("FLAG_SERVICE_URL"), os.Getenv("TARGETING_SERVICE_URL")
	if redisURL == "" || flagSvcURL == "" || targetingSvcURL == "" {
		return errors.New("missing configuration")
	}
	sqsQueueURL, awsRegion := os.Getenv("AWS_SQS_URL"), os.Getenv("AWS_REGION")
	if sqsQueueURL == "" {
		slog.Info("sqs.disabled")
	}
	if awsRegion == "" && sqsQueueURL != "" {
		return errors.New("missing region")
	}
	opt, err := redis.ParseURL(redisURL)
	if err != nil {
		return err
	}
	rdb := redis.NewClient(opt)
	defer func() {
		if err := rdb.Close(); err != nil {
			slog.Warn("redis.close.failed")
		}
	}()
	pingCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if _, err := rdb.Ping(pingCtx).Result(); err != nil {
		return err
	}
	slog.Info("redis.connected")
	var sqsSvc messageSender
	if sqsQueueURL != "" {
		sess, err := session.NewSession(&aws.Config{Region: aws.String(awsRegion)})
		if err != nil {
			return err
		}
		sqsConfig := aws.NewConfig()
		// Apenas o laboratorio local define SQS_ENDPOINT.
		if endpoint := os.Getenv("SQS_ENDPOINT"); endpoint != "" {
			sqsConfig.WithEndpoint(endpoint)
		}
		sqsSvc = sqs.New(sess, sqsConfig)
		slog.Info("sqs.initialized")
	}
	app := &App{
		RedisClient: rdb, SqsSvc: sqsSvc, SqsQueueURL: sqsQueueURL,
		HttpClient:     &http.Client{Timeout: 5 * time.Second, Transport: otelhttp.NewTransport(http.DefaultTransport)},
		FlagServiceURL: flagSvcURL, TargetingServiceURL: targetingSvcURL,
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/health", app.healthHandler)
	mux.HandleFunc("/evaluate", app.evaluationHandler)
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	slog.Info("service.started")
	// Nenhum produtor pode iniciar apos todos os handlers terminarem.
	return serveHTTP(ctx, ":"+port, instrumentHandler(mux), app.producers.Wait)
}
