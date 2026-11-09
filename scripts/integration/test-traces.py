"""Prova de traces reais HTTP/SQS, contratos e sanitização no laboratório local."""
import base64
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


COMPOSE = ["docker", "compose", "--env-file", ".env.example"]
SERVICES = {"auth-service", "flag-service", "targeting-service",
            "evaluation-service", "analytics-service"}
POSTGRES_SERVICES = {"auth-service", "flag-service", "targeting-service"}
TRACE_DIR = Path(os.environ.get("OTEL_TRACE_DIR", "00_COLAB_IA/02_TRABALHO/qa-otel"))
TRACE_FILE = TRACE_DIR / "traces.jsonl"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def request(port, path, method="GET", body=None, key=None, traceparent=None, status=200):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    if traceparent:
        headers["traceparent"] = traceparent
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}", method=method, headers=headers,
        data=None if body is None else json.dumps(body).encode(),
    )
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        payload = response.read().decode()
        check(response.code == status, f"Unexpected HTTP status {response.code} for {method}")
        return json.loads(payload) if payload and status < 400 else None


def compose(*args, **kwargs):
    return subprocess.run(COMPOSE + list(args), check=True, text=True, **kwargs)


def hex_id(value, length):
    # OTLP JSON normally uses hex; accept base64 only for exporter compatibility.
    if len(value) == length and all(c in "0123456789abcdefABCDEF" for c in value):
        return value.lower()
    return base64.b64decode(value).hex()


def attributes(items):
    return {item["key"]: next(iter(item["value"].values()), None) for item in items}


def read_trace(trace_id):
    found = []
    if not TRACE_FILE.exists():
        return found
    for line in TRACE_FILE.read_text(encoding="utf-8").splitlines():
        try:
            batch = json.loads(line)
        except json.JSONDecodeError:
            continue  # A concurrent write may have left the final line incomplete.
        for resource in batch.get("resourceSpans", []):
            attrs = attributes(resource.get("resource", {}).get("attributes", []))
            for scope in resource.get("scopeSpans", []):
                for span in scope.get("spans", []):
                    if hex_id(span["traceId"], 32) == trace_id:
                        found.append({"resource": attrs, "span": span})
    return found


def wait_for_trace(trace_id, predicate, timeout=40):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        spans = read_trace(trace_id)
        if predicate(spans):
            return spans
        time.sleep(1)
    summary = sorted({item["resource"].get("service.name", "unknown") for item in spans})
    raise AssertionError(f"Collector trace incomplete after timeout: {len(spans)} spans, {summary}")


def kind(span):
    value = span.get("kind", 0)
    return {"SPAN_KIND_SERVER": 2, "SPAN_KIND_CLIENT": 3,
            "SPAN_KIND_PRODUCER": 4, "SPAN_KIND_CONSUMER": 5}.get(value, value)


def postgres_services(items):
    found = set()
    for item in items:
        attrs = attributes(item["span"].get("attributes", []))
        system = attrs.get("db.system.name", attrs.get("db.system"))
        if kind(item["span"]) == 3 and system == "postgresql":
            found.add(item["resource"].get("service.name"))
    return found


def assert_privacy_processor():
    """Sentinel is synthetic, not a credential; it must disappear before persistence."""
    probe_id = uuid.uuid4().hex
    sentinel = "TC04_SYNTHETIC_PRIVATE_CANARY_" + uuid.uuid4().hex
    start = time.time_ns()
    values = {
        "http.route": "/privacy-probe", "http.method": "GET",
        "http.url": "https://example.invalid/?token=" + sentinel,
        "url.full": "https://example.invalid/?token=" + sentinel,
        "http.target": "/privacy-probe?token=" + sentinel,
        "url.query": sentinel, "db.statement": "SELECT '" + sentinel + "'",
        "db.connection_string": sentinel, "user.id": sentinel,
        "http.request.header.authorization": sentinel, "error.type": "RuntimeError",
    }
    payload = {"resourceSpans": [{
        "resource": {"attributes": [
            {"key": "service.name", "value": {"stringValue": "privacy-probe"}},
            {"key": "private.attribute", "value": {"stringValue": sentinel}},
        ]},
        "scopeSpans": [{"scope": {"name": "tc04-local-verification"}, "spans": [{
            "traceId": probe_id, "spanId": uuid.uuid4().hex[:16],
            "name": "privacy-probe", "kind": 2,
            "startTimeUnixNano": str(start), "endTimeUnixNano": str(start + 1000),
            "attributes": [{"key": key, "value": {"stringValue": val}}
                           for key, val in values.items()],
            "status": {"code": 2, "message": sentinel},
            "events": [{"timeUnixNano": str(start), "name": "exception", "attributes": [
                {"key": "exception.type", "value": {"stringValue": "RuntimeError"}},
                {"key": "exception.message", "value": {"stringValue": sentinel}},
                {"key": "exception.stacktrace", "value": {"stringValue": sentinel}},
            ]}],
        }]}],
    }]}
    request(4318, "/v1/traces", "POST", payload)
    exported = wait_for_trace(probe_id, bool)
    check(sentinel not in json.dumps(exported), "Sanitization leaked a synthetic private value")
    span = exported[0]["span"]
    check(span["status"]["code"] == 2, "Sanitization must preserve the error status")
    check(attributes(span["attributes"])["error.type"] == "RuntimeError", "Lost error type")
    check(attributes(span["events"][0]["attributes"])["exception.type"] == "RuntimeError",
          "Lost exception type")
    print("PASS: Collector sanitizes URLs, headers, SQL, identifiers and exception details", flush=True)


def main():
    # Check the extension, not merely whether the Collector process exists.
    request(13133, "/")
    health_id = uuid.uuid4().hex
    for port in range(8001, 8006):
        request(port, "/health", traceparent=f"00-{health_id}-{uuid.uuid4().hex[:16]}-01")
    run_id = "otel-" + uuid.uuid4().hex[:10]
    key = request(8001, "/admin/keys", "POST", {"name": run_id},
                  key="local-master-key-change-me", status=201)["key"]
    # Key stays in child environment/container memory and is never printed/written.
    compose("up", "-d", "--no-deps", "--force-recreate", "--wait", "evaluation-service",
            env={**os.environ, "SERVICE_API_KEY": key})
    flag = run_id + "-cold"
    request(8002, "/flags", "POST", {"name": flag, "is_enabled": True}, key, status=201)
    request(8003, "/rules", "POST", {
        "flag_name": flag, "rules": {"type": "PERCENTAGE", "value": 100},
    }, key, status=201)
    trace_id, external_parent = uuid.uuid4().hex, uuid.uuid4().hex[:16]
    user_id = run_id + "-synthetic-user"
    query = urllib.parse.urlencode({"flag_name": flag, "user_id": user_id})
    response = request(8004, "/evaluate?" + query,
                       traceparent=f"00-{trace_id}-{external_parent}-01")
    check(response == {"flag_name": flag, "user_id": user_id, "result": True},
          "Instrumentation changed the business response")
    compose("exec", "-T", "analytics-service", "python", "/tests/assert-events.py",
            json.dumps([response]))

    def complete(items):
        # Different SDKs/batches may arrive out of order: wait for the entire tree,
        # not merely a consumer that may have exported before its producer.
        current = [item["span"] for item in items]
        ids = {hex_id(span["spanId"], 16) for span in current}
        parents_present = all(hex_id(span.get("parentSpanId", ""), 16) in ids | {external_parent}
                              for span in current)
        return ({item["resource"].get("service.name") for item in items} == SERVICES
                and sum(kind(span) == 4 for span in current) == 1
                and sum(kind(span) == 5 for span in current) == 1
                and any(item["resource"].get("service.name") == "evaluation-service"
                        and kind(item["span"]) == 2 for item in items)
                and any("dynamodb" in span["name"].lower() for span in current)
                and postgres_services(items) == POSTGRES_SERVICES
                and parents_present)

    exported = wait_for_trace(trace_id, complete)
    spans = [item["span"] for item in exported]
    producers = [span for span in spans if kind(span) == 4]
    consumers = [span for span in spans if kind(span) == 5]
    check(len(producers) == 1 and len(consumers) == 1, "Expected one SQS producer and consumer")
    producer_id = hex_id(producers[0]["spanId"], 16)
    check(hex_id(consumers[0]["parentSpanId"], 16) == producer_id,
          "SQS consumer did not inherit the producer span context")
    ids = {hex_id(span["spanId"], 16) for span in spans}
    check(len(ids) == len(spans), "Duplicate span IDs in the exported trace")
    for span in spans:
        parent = hex_id(span.get("parentSpanId", ""), 16)
        check(parent in ids or parent == external_parent,
              "Unexpected orphan/root span in controlled distributed trace")
        check(int(span["endTimeUnixNano"]) >= int(span["startTimeUnixNano"]), "Invalid duration")
    evaluation_servers = [item["span"] for item in exported
                          if item["resource"]["service.name"] == "evaluation-service"
                          and kind(item["span"]) == 2]
    check(len(evaluation_servers) == 1, "Duplicate/missing evaluation server instrumentation")
    check(hex_id(evaluation_servers[0]["parentSpanId"], 16) == external_parent,
          "Incoming W3C context was not extracted")
    encoded = json.dumps(exported)
    check(key not in encoded and user_id not in encoded and flag not in encoded,
          "Application trace persisted business identifiers or credentials")
    for item in exported:
        check(attributes(item["span"].get("attributes", [])).get("http.route") != "/health",
              "Health endpoint should not create spans")
    print("PASS: one W3C trace connects all five services; HTTP parents and SQS producer/consumer match",
          flush=True)
    print("PASS: PostgreSQL client spans are present for auth, flag and targeting", flush=True)

    log_result = compose("logs", "--no-color", "--no-log-prefix", "--since", "10m",
                         *sorted(SERVICES), capture_output=True)
    logs = log_result.stdout + log_result.stderr
    check(key not in logs, "Application logs leaked the generated credential")
    correlated = set()
    for line in logs.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("trace_id") == trace_id:
            check(event.get("span_id"), "Correlated log has no span ID")
            correlated.add(event.get("service.name"))
    check(correlated == SERVICES, "Expected correlated JSON logs from every participating service")
    print("PASS: all five services emit correlated JSON logs without the generated credential", flush=True)
    assert_privacy_processor()
    check(not read_trace(health_id), "Explicit health requests should not produce persisted spans")
    print("PASS: explicit health probes are excluded from persisted traces", flush=True)
    evidence = {
        "date": time.strftime("%Y-%m-%d"), "trace_id": trace_id,
        "services": sorted(SERVICES), "span_count": len(spans),
        "producer_span_id": producer_id,
        "consumer_span_id": hex_id(consumers[0]["spanId"], 16),
        "http_sqs_parentage": "passed", "business_contract": "passed",
        "postgresql_client_spans": sorted(postgres_services(exported)),
        "correlated_json_logs": sorted(correlated), "privacy_probe": "passed",
        "health_exclusion": "passed",
        "spans": [{"service": item["resource"]["service.name"],
                   "name": item["span"]["name"], "kind": kind(item["span"]),
                   "span_id": hex_id(item["span"]["spanId"], 16),
                   "parent_span_id": hex_id(item["span"].get("parentSpanId", ""), 16)}
                  for item in exported],
    }
    (TRACE_DIR / "resultado-traces.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: observability integration completed ({len(spans)} spans, 5 services)", flush=True)


if __name__ == "__main__":
    main()
