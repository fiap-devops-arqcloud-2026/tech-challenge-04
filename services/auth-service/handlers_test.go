package main

import (
	"bytes"
	"context"
	"errors"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/DATA-DOG/go-sqlmock"
	"go.opentelemetry.io/otel"
)

func TestAuthSQLContextSpansAndPrivateLogs(t *testing.T) {
	exporter := testTracing(t)
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatal(err)
	}
	defer func() { _ = db.Close() }()
	var logs bytes.Buffer
	slog.SetDefault(newJSONLogger(&logs, "auth-service"))
	app := &App{DB: db, MasterKey: "PRIVATE_MASTER"}
	ctx, parent := otel.Tracer("test").Start(context.Background(), "request")
	mock.ExpectQuery("SELECT id FROM api_keys").WithArgs(hashAPIKey("PRIVATE_API_KEY")).WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(7))
	req := httptest.NewRequest("GET", "/validate", nil).WithContext(ctx)
	req.Header.Set("Authorization", "Bearer PRIVATE_API_KEY")
	response := httptest.NewRecorder()
	app.validateKeyHandler(response, req)
	if response.Code != http.StatusOK {
		t.Fatalf("validate status=%d", response.Code)
	}
	mock.ExpectQuery("INSERT INTO api_keys").WithArgs("PRIVATE_NAME", sqlmock.AnyArg()).WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(8))
	response = httptest.NewRecorder()
	app.createKeyHandler(response, httptest.NewRequest("POST", "/admin/keys", strings.NewReader(`{"name":"PRIVATE_NAME"}`)).WithContext(ctx))
	if response.Code != http.StatusCreated {
		t.Fatalf("create status=%d, body=%s", response.Code, response.Body)
	}
	// Driver errors may include connection/query details. Only a static event is logged.
	mock.ExpectQuery("SELECT id FROM api_keys").WithArgs(hashAPIKey("PRIVATE_API_KEY")).WillReturnError(errors.New("PRIVATE_DB_CONNECTION"))
	response = httptest.NewRecorder()
	app.validateKeyHandler(response, req)
	if response.Code != http.StatusUnauthorized {
		t.Fatalf("invalid status=%d", response.Code)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatal(err)
	}
	spans := exporter.GetSpans()
	if len(spans) != 3 {
		t.Fatalf("SQL spans=%d", len(spans))
	}
	for _, span := range spans {
		if span.Parent.SpanID() != parent.SpanContext().SpanID() {
			t.Fatalf("SQL parent=%s", span.Parent.SpanID())
		}
		for _, attr := range span.Attributes {
			if strings.Contains(attr.Value.AsString(), "PRIVATE") || strings.Contains(string(attr.Key), "query") {
				t.Fatalf("SQL sensitive attribute=%v", attr)
			}
		}
	}
	parent.End()
	if strings.Contains(logs.String(), "PRIVATE") {
		t.Fatalf("sensitive log=%s", logs.String())
	}
	if !strings.Contains(logs.String(), `"trace_id"`) {
		t.Fatal("business logs are not correlated")
	}
}

func TestAuthSQLUsesRequestCancellation(t *testing.T) {
	testTracing(t)
	db, mock, err := sqlmock.New()
	if err != nil {
		t.Fatal(err)
	}
	defer func() { _ = db.Close() }()
	app := &App{DB: db}
	mock.ExpectQuery("SELECT id FROM api_keys").WillDelayFor(500 * time.Millisecond).WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", "/validate", nil).WithContext(ctx)
	req.Header.Set("Authorization", "Bearer fake-key")
	response := httptest.NewRecorder()
	start := time.Now()
	app.validateKeyHandler(response, req)
	if response.Code != http.StatusUnauthorized || time.Since(start) > 300*time.Millisecond {
		t.Fatalf("QueryRowContext did not honor cancellation; elapsed=%s status=%d", time.Since(start), response.Code)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatal(err)
	}
}
