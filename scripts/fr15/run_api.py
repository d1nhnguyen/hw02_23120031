"""Chạy test case FR-15 trên kênh API (thủ tục P-API). Backend được khởi động lại trước mỗi test case.

Kết quả: evidence/FR-15/api_results.json   ·   ONLY=FR15-DT-01,FR15-BV-02 python3 run_api.py
"""
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from cases import CASES, EXTRA, MISSING

BASE = "http://localhost:3000/api"
ROOT = Path(__file__).resolve().parents[2]
RESTART = ROOT / "scripts" / "restart_backend.sh"
ONLY = os.environ["ONLY"].split(",") if os.environ.get("ONLY") else None
OUT = ROOT / "evidence" / "FR-15" / (f"api_results_{'_'.join(ONLY)}.json" if ONLY else "api_results.json")
FIELDS = ("name", "price", "category_id", "description", "imageUrl")


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
    """Lý do từ chối suy ra từ câu thông báo (đặc tả không quy định câu chữ – A6)."""
    m = message.lower()
    for reason, pattern in (("id", r"không tìm thấy|không tồn tại|not found|not exist"),
                            ("category", r"danh mục|category"),
                            ("price", r"giá|price"),
                            ("name", r"tên|name")):
        if re.search(pattern, m):
            return reason
    return "unknown"


def snapshot():
    status, body = call("GET", "/products")
    assert status == 200, (status, body)
    return {p["id"]: {k: p.get(k) for k in FIELDS} for p in body}


def same_value(a, b):
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return a == b


def matches(product, c):
    return (product["name"] == c["name"] and same_value(product["price"], c["price"])
            and same_value(product["category_id"], c["category_id"]))


def payload(c, current):
    base = current or {**EXTRA}
    body = {"description": base.get("description"), "imageUrl": base.get("imageUrl")}
    for key in ("name", "price", "category_id"):
        if c[key] != MISSING:
            body[key] = c[key]
    return body


def describe(product):
    return f"Tên “{product['name'][:40]}{'…' if len(product['name'] or '') > 40 else ''}”, Giá {product['price']}, Danh mục {product['category_id']}"


def run_case(c, token):
    for action, pid in c["pre"]:
        if action == "delete":
            call("DELETE", f"/products/{pid}", token=token)
    before = snapshot()
    if c["op"] == "add":
        status, body = call("POST", "/products", payload(c, None), token)
    elif c["op"] == "edit":
        status, body = call("PUT", f"/products/{c['pid']}", payload(c, before.get(c["pid"])), token)
    else:
        status, body = call("DELETE", f"/products/{c['pid']}", token=token)
    after = snapshot()
    r = {"id": c["id"], "op": c["op"], "expect": c["expect"], "status": status, "body": body}
    notes = []
    added = [pid for pid in after if pid not in before]
    removed = [pid for pid in before if pid not in after]
    target = c["pid"] if c["op"] != "add" else (added[0] if added else None)
    others_changed = [pid for pid in before if pid != target and pid in after and before[pid] != after[pid]]
    r.update(added=added, removed=removed, others_changed=others_changed)
    ok2xx = 200 <= status < 300
    if c["expect"] == "accept":
        if c["op"] == "add":
            ok = ok2xx and len(added) == 1 and matches(after[added[0]], c) and not removed and not others_changed
            if added:
                r["stored"] = after[added[0]]
                if not matches(after[added[0]], c):
                    notes.append(f"lưu khác dữ liệu gửi: {describe(after[added[0]])}")
            else:
                notes.append("không tạo sản phẩm")
        elif c["op"] == "edit":
            stored = after.get(c["pid"])
            r["stored"] = stored
            kept = stored and all(stored[k] == before[c["pid"]][k] for k in ("description", "imageUrl"))
            ok = ok2xx and stored is not None and matches(stored, c) and kept and not others_changed and not added
            if stored is not None and not matches(stored, c):
                notes.append(f"lưu khác dữ liệu gửi: {describe(stored)}")
        else:
            ok = ok2xx and removed == [c["pid"]] and not others_changed
            if c["pid"] not in removed:
                notes.append("sản phẩm vẫn còn")
        if others_changed:
            notes.append(f"sản phẩm khác bị thay đổi: id {others_changed}")
    else:
        unchanged = before == after
        message = (body.get("error") or body.get("message") or "") if isinstance(body, dict) else str(body)
        r["reason"] = reason_of(message) if message else None
        if c["expect"] == "notfound":
            ok = status == 404 and unchanged
        else:
            ok = 400 <= status < 500 and unchanged and r["reason"] == c["target"]
            if 400 <= status < 500 and unchanged and r["reason"] != c["target"]:
                notes.append(f"lý do từ chối ({r['reason']}) khác lý do mong đợi ({c['target']})")
        if not unchanged:
            if added:
                notes.append(f"vẫn tạo sản phẩm: {describe(after[added[0]])}")
                r["stored"] = after[added[0]]
            if c["op"] == "edit" and c["pid"] in before and before[c["pid"]] != after.get(c["pid"]):
                notes.append(f"sản phẩm bị sửa thành: {describe(after[c['pid']])}")
                r["stored"] = after[c["pid"]]
            if removed:
                notes.append(f"sản phẩm bị xóa: id {removed}")
    r["verdict"] = "Pass" if ok else "Fail"
    r["notes"] = notes
    return r


def main():
    results = []
    for c in CASES:
        if "api" not in c["channels"] or (ONLY and c["id"] not in ONLY):
            continue
        # không bắt output: tiến trình node chạy nền sẽ giữ pipe và làm subprocess chờ mãi
        subprocess.run([str(RESTART)], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        status, admin = call("POST", "/login", {"email": "admin@eshop.com", "password": "Admin123!"})
        assert status == 200, admin
        r = run_case(c, admin["token"])
        results.append(r)
        print(f"{c['id']:11} {c['op']:6} {c['expect']:8} HTTP {r['status']} -> {r['verdict']:4} "
              f"{str(r['body'])[:60]} {'; '.join(r['notes'])[:120]}", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"run_at": datetime.now().isoformat(timespec="seconds"), "results": results},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    fails = sum(r["verdict"] == "Fail" for r in results)
    print(f"\n{len(results)} test case, {len(results) - fails} Pass, {fails} Fail -> {OUT}")


if __name__ == "__main__":
    main()
