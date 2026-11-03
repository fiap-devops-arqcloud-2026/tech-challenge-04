package main

import (
	"context"
	"database/sql"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	_ "github.com/jackc/pgx/v4/stdlib"
	"github.com/joho/godotenv"
)

// App permite injetar o banco nos handlers.
type App struct {
	DB        *sql.DB
	MasterKey string
}

func main() {
	if err := run(); err != nil {
		// Mensagens de startup sao estaticas: URLs/credenciais nao vao ao log.
		slog.Error("service.start.failed")
		os.Exit(1)
	}
}

func run() error {
	_ = godotenv.Load()
	shutdown, err := initTelemetry(context.Background(), "auth-service")
	if err != nil {
		return err
	}
	defer shutdownTelemetry(shutdown)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8001"
	}
	databaseURL, masterKey := os.Getenv("DATABASE_URL"), os.Getenv("MASTER_KEY")
	if databaseURL == "" || masterKey == "" {
		return errors.New("missing configuration")
	}
	db, err := connectDB(databaseURL)
	if err != nil {
		return err
	}
	defer func() {
		if err := db.Close(); err != nil {
			slog.Warn("db.close.failed")
		}
	}()
	app := &App{DB: db, MasterKey: masterKey}
	mux := http.NewServeMux()
	mux.HandleFunc("/health", app.healthHandler)
	mux.HandleFunc("/validate", app.validateKeyHandler)
	mux.Handle("/admin/keys", app.masterKeyAuthMiddleware(http.HandlerFunc(app.createKeyHandler)))
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	slog.Info("service.started")
	return serveHTTP(ctx, ":"+port, instrumentHandler(mux), nil)
}

func connectDB(databaseURL string) (*sql.DB, error) {
	db, err := sql.Open("pgx", databaseURL)
	if err != nil {
		return nil, err
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err = db.PingContext(ctx); err != nil {
		_ = db.Close()
		return nil, err
	}
	slog.Info("db.connected")
	return db, nil
}
