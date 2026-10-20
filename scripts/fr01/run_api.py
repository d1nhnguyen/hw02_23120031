"""Chạy test case FR-01 trên kênh API (thủ tục P-API).

Yêu cầu: backend vừa khởi động lại (dữ liệu seed).
Kết quả: evidence/FR-01/api_results.json
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from cases import CASES, SEED_PASSWORD

BASE = "http://localhost:3000/api"
# ONLY=DT-29 python3 run_api.py -> chỉ chạy các test case liệt kê, ghi ra file kết quả riêng
ONLY = os.environ["ONLY"].split(",") if os.environ.get("ONLY") else None
OUT = Path(__file__).resolve().parents[2] / "evidence" / "FR-01" / (
    f"api_results_{'_'.join(ONLY)}.json" if ONLY else "api_results.json")


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


def reason_of(message):
    """Lý do từ chối suy ra từ câu thông báo (đặc tả không quy định câu chữ – A7)."""
    m = message.lower()
    for reason, pattern in (("confirm", r"xác nhận|không khớp|confirm|match"),
                            ("dup", r"tồn tại|đã được|đã sử dụng|exist|already|duplicate|unique"),
                            ("password", r"mật khẩu|password"),
                            ("email", r"email"),
                            ("name", r"họ|tên|name")):
        if re.search(pattern, m):
            return reason
    return "unknown"


def login(mail, password):
    status, body = call("POST", "/login", {"email": mail, "password": password})
    return status == 200 and isinstance(body, dict) and bool(body.get("token"))


def users(admin_token):
    status, body = call("GET", "/admin/users", token=admin_token)
    assert status == 200 and isinstance(body, list), (status, body)
    return body


def run():
    admin_status, admin = call("POST", "/login", {"email": "admin@eshop.com", "password": "Admin123!"})
    assert admin_status == 200, admin
    token = admin["token"]
    results = []
    for c in CASES:
        if "api" not in c["channels"] or (ONLY and c["id"] not in ONLY):
            continue
        stored = c["email"].strip()
        before = [u for u in users(token) if str(u.get("email", "")).lower() == stored.lower()]
        status, body = call("POST", "/register", {"name": c["name"], "email": c["email"], "password": c["password"]})
        after = [u for u in users(token) if str(u.get("email", "")).lower() == stored.lower()]
        created = len(after) > len(before)
        r = {"id": c["id"], "expect": c["expect"], "status": status, "body": body,
             "created": created, "matching_accounts_after": len(after)}
        notes = []
        if c["expect"] == "accept":
            r["login_ok"] = login(stored, c["password"])
            ok = status == 200 and created and r["login_ok"]
            if status == 200 and not created:
                notes.append(f"tài khoản không lưu dưới email {stored!r} (không bỏ khoảng trắng đầu/cuối)")
        else:
            message = (body.get("error") or body.get("message") or "") if isinstance(body, dict) else str(body)
            r["reason"] = reason_of(message) if message else None
            ok = 400 <= status < 500 and not created
            if not ok:
                notes.append(f"HTTP {status}" if 400 <= status < 500 and created else
                             "email trùng vẫn được chấp nhận" if c["duplicate_of"] else "dữ liệu không hợp lệ vẫn được chấp nhận")
            elif r["reason"] != c["target"]:
                ok = False
                notes.append(f"lý do từ chối ({r['reason']}) khác lý do mong đợi ({c['target']})")
            if c["duplicate_of"]:
                r["seed_login_ok"] = login(c["duplicate_of"], SEED_PASSWORD)
                if not r["seed_login_ok"]:
                    ok = False
                    notes.append("tài khoản gốc không còn đăng nhập được")
        r["verdict"] = "Pass" if ok else "Fail"
        r["notes"] = notes
        results.append(r)
        print(f"{c['id']:6} {c['expect']:6} HTTP {status} created={created} -> {r['verdict']:4}  {str(body)[:70]} {'; '.join(notes)}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"run_at": datetime.now().isoformat(timespec="seconds"), "results": results},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    fails = sum(r["verdict"] == "Fail" for r in results)
    print(f"\n{len(results)} test case, {len(results) - fails} Pass, {fails} Fail -> {OUT}")


if __name__ == "__main__":
    sys.exit(run())
