"""Dựng bộ dữ liệu FR-10 (mục 3.1): khởi động lại backend, đăng ký User B, tạo 7 đơn ở đúng trạng thái.

Dùng như module (setup()) hoặc chạy trực tiếp: in JSON {"ok", "statuses", "problems"}.
"""
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from cases import FIXTURE, USER_B

BASE = "http://localhost:3000/api"
RESTART = Path(__file__).resolve().parents[1] / "restart_backend.sh"
STEPS = {"pending": [], "confirmed": ["confirmed"], "shipping": ["confirmed", "shipping"],
         "delivered": ["confirmed", "shipping", "delivered"], "canceled": ["canceled"]}


def call(method, path, body=None, token=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data, timeout=10) as r:
            status, raw = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read().decode()
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, raw


def token(email, password):
    status, body = call("POST", "/login", {"email": email, "password": password})
    assert status == 200, (email, status, body)
    return body["token"]


def statuses(admin_token):
    status, body = call("GET", "/admin/orders", token=admin_token)
    assert status == 200, (status, body)
    return {o["id"]: o["status"] for o in body}


def setup():
    # không bắt output: tiến trình node chạy nền sẽ giữ pipe và làm subprocess chờ mãi
    subprocess.run([str(RESTART)], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    call("POST", "/register", USER_B)
    tokens = {"admin": token("admin@eshop.com", "Admin123!"), "test": token("test@eshop.com", "Test1234!"),
              "userb": token(USER_B["email"], USER_B["password"])}
    for oid, (owner, state) in sorted(FIXTURE.items()):
        status, body = call("POST", "/checkout", {"total_amount": 1000000 * oid, "shipping_address": f"Dia chi don {oid}"},
                            tokens[owner])
        assert status == 200 and body.get("orderId") == oid, (oid, status, body)
        for step in STEPS[state]:
            call("PUT", f"/admin/orders/{oid}/status", {"status": step}, tokens["admin"])
    got = statuses(tokens["admin"])
    problems = [f"đơn #{oid}: cần {state}, thực tế {got.get(oid)}" for oid, (_, state) in FIXTURE.items()
                if got.get(oid) != state]
    return {"ok": not problems, "statuses": got, "problems": problems, "tokens": tokens}


if __name__ == "__main__":
    result = setup()
    result.pop("tokens")
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["ok"] else 1)
