"""Chạy test case Mobile – Đăng nhập trên kênh API (thủ tục P-API). Backend được khởi động lại trước mỗi test case.

Kết quả: evidence/Mobile/api_results.json   ·   ONLY=MOB-DT-01 python3 run_api.py
"""
import os
import time

from cases import CASES, PASSWORD
from common import call, judge, lock_state, restart_backend, write_results

ONLY = os.environ["ONLY"].split(",") if os.environ.get("ONLY") else None


def attempt(email, password):
    status, body = call("POST", "/login", {"email": email, "password": password})
    message = (body.get("error") or body.get("message") or "") if isinstance(body, dict) else str(body)
    token = isinstance(body, dict) and bool(body.get("token"))
    return status, message, token


def run_case(c):
    restart_backend()
    pre_message, last = None, time.time()
    for email, password in c["pre"]:
        status, pre_message, _ = attempt(email, password)
        last = time.time()
        if password == PASSWORD and status != 200:
            return {"id": c["id"], "expect": c["expect"], "status": None, "message": pre_message, "token": False,
                    "verdict": "Blocked", "notes": [f"tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“{pre_message}”)"]}
    if c["wait"]:
        time.sleep(max(0.0, last + c["wait"] - time.time()))
    status, message, token = attempt(c["email"], c["password"])
    counter, until, locked = lock_state()
    success = status == 200 and token
    ok, notes = judge(c, success, message, counter, locked, pre_message)
    if not success and not 400 <= status < 500:
        ok = False
        notes.append(f"HTTP {status}")
    return {"id": c["id"], "expect": c["expect"], "status": status, "message": message, "token": token,
            "login_attempts": counter, "locked_until": until, "locked": locked, "pre_message": pre_message,
            "verdict": "Pass" if ok else "Fail", "notes": notes}


def main():
    results = []
    for c in CASES:
        if ONLY and c["id"] not in ONLY:
            continue
        r = run_case(c)
        results.append(r)
        print(f"{c['id']:10} {c['expect']:6} HTTP {r['status']} attempts={r.get('login_attempts')} locked={r.get('locked')} "
              f"-> {r['verdict']:4} “{r['message']}” {'; '.join(r['notes'])}", flush=True)
    write_results(f"api_results{'_' + '_'.join(ONLY) if ONLY else ''}.json", results)


if __name__ == "__main__":
    main()
