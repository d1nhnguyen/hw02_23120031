"""Chạy test case Mobile – Đăng nhập trên app (thủ tục P-MOBILE), Android Emulator Pixel 2 + Expo Go, điều khiển qua adb.
Backend được khởi động lại và app được mở lại trước mỗi test case.

Kết quả: evidence/Mobile/web_results.json (kênh giao diện) + ảnh evidence/Mobile/web/<ID>.png
ONLY=MOB-DT-01 python3 run_mobile.py
"""
import json
import os
import time

import adb_ui as u
from cases import CASES, PASSWORD
from common import EVIDENCE, judge, lock_state, restart_backend, write_results

ONLY = os.environ["ONLY"].split(",") if os.environ.get("ONLY") else None
LOGIN_TAP = (808, 85)  # phần dưới chữ "Đăng nhập" trên thanh tiêu đề (phần trên bị thanh trạng thái che)
BASE_TEXTS = {"EShop Mobile", "Đăng nhập", "Giỏ (0)", "Đăng Nhập", "Username", "Mật khẩu", "Quên mật khẩu?", "Sign In",
              "Chưa có tài khoản? Đăng ký ngay", "Quay Lại", "© 2026 EShop SUT. Dành cho mục đích kiểm thử.", "Email"}


def open_login(tries=3):
    for _ in range(tries):
        u.dismiss_dialogs()
        u.tap(LOGIN_TAP)
        if u.wait_for("Sign In", timeout=5, exact=True):
            return True
    return False


def edit_texts():
    return [n for n in u.nodes() if n["cls"].endswith("EditText")]


def attempt(email, password, deadline=None):
    """Một lần đăng nhập trên màn hình Đăng nhập; trả (thành công?, thông báo, các dòng chữ trên màn hình)."""
    fields = edit_texts()
    u.fill(fields[0], email)
    u.fill([n for n in edit_texts() if n["password"]][0], password)
    u.hide_keyboard()
    if deadline:
        time.sleep(max(0.0, deadline - time.time()))
    u.tap(u.find(text="Sign In", exact=True))
    tapped = time.time()
    time.sleep(2)
    shown = [n["text"] for n in u.nodes() if n["text"]]
    success = "Sign In" not in shown and any(t.startswith("Chào") for t in shown)
    extra = [t for t in shown if t not in BASE_TEXTS and t not in (email, "•" * len(password)) and not t.startswith("•")]
    message = "; ".join(extra) if not success else ""
    ok_button = u.find(text="OK", exact=True)
    if ok_button:  # hộp thoại Alert (nếu có)
        u.tap(ok_button)
    return success, message, tapped, shown


def back_to_login_after_success():
    """Đăng xuất (trang Hồ sơ → Thoát) rồi mở lại màn hình Đăng nhập."""
    greet = next(n for n in u.nodes() if n["text"].startswith("Chào"))
    u.tap((greet["center"][0], greet["bounds"][3] - 6))
    u.wait_for("Thoát", timeout=5, exact=True)
    u.tap(u.find(text="Thoát", exact=True))
    time.sleep(1)
    open_login()


def profile_opens():
    greet = next(n for n in u.nodes() if n["text"].startswith("Chào"))
    u.tap((greet["center"][0], greet["bounds"][3] - 6))
    return u.wait_for("test@eshop.com", timeout=5) is not None


def run_case(c):
    restart_backend()
    u.reload_app()
    r = {"id": c["id"], "expect": c["expect"]}
    if not open_login():
        u.screenshot(EVIDENCE / "web" / f"{c['id']}.png")
        return {**r, "verdict": "Blocked", "notes": ["không mở được màn hình Đăng nhập sau 3 lần thử"]}
    pre_message, last = None, time.time()
    for email, password in c["pre"]:
        success, pre_message, last, _ = attempt(email, password)
        if success:
            back_to_login_after_success()
        elif password == PASSWORD:
            u.screenshot(EVIDENCE / "web" / f"{c['id']}.png")
            return {**r, "verdict": "Blocked", "message": pre_message,
                    "notes": [f"tiền điều kiện không dựng được: lần đăng nhập đúng trong chuỗi bị từ chối (“{pre_message}”)"]}
    deadline = last + c["wait"] if c["wait"] else None
    success, message, _, shown = attempt(c["email"], c["password"], deadline)
    counter, until, locked = lock_state()
    r.update(success=success, message=message, shown=shown, login_attempts=counter, locked_until=until, locked=locked,
             pre_message=pre_message)
    if success:
        r["profile_opens"] = profile_opens()
    u.screenshot(EVIDENCE / "web" / f"{c['id']}.png")
    ok, notes = judge(c, success, message, counter, locked, pre_message)
    if success and not r["profile_opens"]:
        ok = False
        notes.append("không mở được Hồ sơ sau khi đăng nhập")
    return {**r, "verdict": "Pass" if ok else "Fail", "notes": notes}


def main():
    # Ghi kết quả sau từng test case; RESUME=1 bỏ qua các test case đã có trong file tạm (chạy tiếp sau khi bị gián đoạn)
    partial = EVIDENCE / "web_results.partial.jsonl"
    done = {}
    if os.environ.get("RESUME") and partial.exists():
        done = {r["id"]: r for r in map(json.loads, partial.read_text(encoding="utf-8").splitlines())}
    elif partial.exists():
        partial.unlink()
    results = []
    for c in CASES:
        if ONLY and c["id"] not in ONLY:
            continue
        if c["id"] in done:
            results.append(done[c["id"]])
            continue
        r = run_case(c)
        with partial.open("a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        results.append(r)
        print(f"{c['id']:10} {c['expect']:6} success={r.get('success')} attempts={r.get('login_attempts')} "
              f"locked={r.get('locked')} -> {r['verdict']:4} “{r.get('message', '')}” {'; '.join(r['notes'])}", flush=True)
    restart_backend()
    write_results(f"web_results{'_' + '_'.join(ONLY) if ONLY else ''}.json", results)
    if not ONLY:
        partial.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
