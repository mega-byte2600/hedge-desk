#!/usr/bin/env python3
import argparse
import json
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def percentile(values, q):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(q * len(ordered)) - 1))
    return ordered[index]


def hit(url, timeout):
    started = time.perf_counter()
    status = 0
    try:
        request = Request(url, headers={"User-Agent": "emporion-load-test/1.0"})
        with urlopen(request, timeout=timeout) as response:
            response.read()
            status = response.status
    except HTTPError as exc:
        status = exc.code
    except (URLError, TimeoutError, OSError):
        status = 0
    return (time.perf_counter() - started) * 1000, status


def run_level(base_url, paths, concurrency, requests, timeout):
    urls = [base_url.rstrip("/") + path for path in paths]
    latencies = []
    statuses = []
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(hit, urls[index % len(urls)], timeout) for index in range(requests)]
        for future in as_completed(futures):
            latency, status = future.result()
            latencies.append(latency)
            statuses.append(status)
    elapsed = time.perf_counter() - started
    failures = sum(1 for status in statuses if not 200 <= status < 400)
    return {
        "concurrency": concurrency,
        "requests": requests,
        "failures": failures,
        "error_rate": round(failures / requests, 6),
        "throughput_rps": round(requests / elapsed, 2) if elapsed else 0.0,
        "p50_ms": round(percentile(latencies, 0.50), 2),
        "p95_ms": round(percentile(latencies, 0.95), 2),
        "p99_ms": round(percentile(latencies, 0.99), 2),
        "max_ms": round(max(latencies) if latencies else 0.0, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Dependency-free Emporion HTTP concurrency test")
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--concurrency", default="25,50,100")
    parser.add_argument("--requests-per-level", type=int, default=200)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--max-p95-ms", type=float, default=750.0)
    parser.add_argument("--max-error-rate", type=float, default=0.01)
    parser.add_argument("--output")
    args = parser.parse_args()

    levels = [int(value) for value in args.concurrency.split(",") if value.strip()]
    if not levels or any(value <= 0 for value in levels):
        raise SystemExit("Concurrency levels must be positive integers")
    if args.requests_per_level <= 0:
        raise SystemExit("requests-per-level must be positive")

    paths = ["/", "/styles.css", "/api/candidates", "/api/risk-dashboard"]
    results = [
        run_level(args.base_url, paths, level, args.requests_per_level, args.timeout)
        for level in levels
    ]
    payload = {
        "base_url": args.base_url,
        "thresholds": {
            "max_p95_ms": args.max_p95_ms,
            "max_error_rate": args.max_error_rate,
        },
        "results": results,
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")

    failed = any(
        row["p95_ms"] > args.max_p95_ms or row["error_rate"] > args.max_error_rate
        for row in results
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
