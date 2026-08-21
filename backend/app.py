"""Servidor web minimo de MediLogic, construido solo con Python estandar."""

from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from prolog_service import PrologError, run_named_query

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/query":
            params = {key: values[0] for key, values in parse_qs(parsed.query).items()}
            name = params.pop("name", "diagnostico")
            try:
                payload = run_named_query(name, params)
                status = 200
            except PrologError as exc:
                payload = {"error": str(exc)}
                status = 400
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


if __name__ == "__main__":
    print("MediLogic disponible en http://localhost:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
