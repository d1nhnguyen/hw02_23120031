"""Phần dùng chung của runner Mobile – Đăng nhập: gọi API, khởi động lại backend, đọc bộ đếm khóa."""
import json
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "http://localhost:3000/api"
ROOT = Path(__file__).resolve().parents[2]
RESTART = ROOT / "scripts" / "restart_backend.sh"
EVIDENCE = ROOT / "evidence" / "Mobile"


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


def restart_backend():
    # không bắt output: tiến trình node chạy nền sẽ giữ pipe và làm subprocess chờ mãi
    subprocess.run([str(RESTART)], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def lock_state(email="test@eshop.com"):
    """(login_attempts, locked_until, còn khóa?) của tài khoản, đọc qua API Admin (A4)."""
    _, admin = call("POST", "/login", {"email": "admin@eshop.com", "password": "Admin123!"})
    _, users = call("GET", "/admin/users", token=admin["token"])
    u = next(x for x in users if x["email"] == email)
    until = u.get("locked_until")
    locked = bool(until) and datetime.fromisoformat(until.replace("Z", "+00:00")) > datetime.now(timezone.utc)
    return u.get("login_attempts"), until, locked


def write_results(name, results):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    out = EVIDENCE / name
    out.write_text(json.dumps({"run_at": datetime.now().isoformat(timespec="seconds"), "results": results},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    count = lambda v: sum(r["verdict"] == v for r in results)
    print(f"\n{len(results)} test case: {count('Pass')} Pass, {count('Fail')} Fail, {count('Blocked')} Blocked -> {out}")


def judge(c, success, message, counter, locked, pre_message=None):
    """Kết luận chung cho cả hai kênh từ: đăng nhập thành công?, thông báo, bộ đếm, trạng thái khóa."""
    notes = []
    if c["expect"] == "accept":
        ok = success
        if not success:
            notes.append(f"đăng nhập thất bại: “{message}”")
        if success and counter not in (0, None):
            ok = False
            notes.append(f"bộ đếm sau khi đăng nhập đúng = {counter}, không về 0")
    else:
        ok = not success
        if success:
            notes.append("đăng nhập thành công dù mong đợi bị từ chối")
        if not success and not message:
            ok = False
            notes.append("bị từ chối nhưng không có thông báo")
        if c["counter"] is not None and counter != c["counter"]:
            ok = False
            notes.append(f"bộ đếm = {counter}, mong đợi {c['counter']}")
        if c["lock_expected"] and not locked:
            ok = False
            notes.append("tài khoản chưa bị khóa")
        if c["lock_expected"] is None and c["expect"] == "fail" and c["counter"] is not None and c["counter"] < 3 and locked:
            ok = False
            notes.append("tài khoản bị khóa dù chưa đủ 3 lần sai")
        if c["same_message_as_pre"] and pre_message is not None and message != pre_message:
            ok = False
            notes.append(f"thông báo khác lần sai mật khẩu (“{pre_message}” ≠ “{message}”)")
    return ok, notes
