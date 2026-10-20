"""Điều khiển app mobile trên Android Emulator qua adb (không cần Appium):
đọc cây giao diện (uiautomator dump), chạm, nhập chữ, chụp màn hình.
"""
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ADB = str(Path.home() / "Android" / "Sdk" / "platform-tools" / "adb")


def adb(*args, check=True):
    return subprocess.run([ADB, *args], check=check, capture_output=True, text=True).stdout


def nodes():
    """Danh sách phần tử trên màn hình: text, hint, class, bounds (tâm), password, clickable."""
    for _ in range(3):
        adb("shell", "uiautomator", "dump", "/sdcard/ui.xml", check=False)
        xml = adb("shell", "cat", "/sdcard/ui.xml", check=False)
        if xml.strip().startswith("<?xml"):
            break
        time.sleep(0.5)
    root = ET.fromstring(xml[xml.index("<?xml"):])
    out = []
    for n in root.iter("node"):
        x1, y1, x2, y2 = map(int, re.findall(r"\d+", n.get("bounds")))
        out.append({"text": n.get("text", ""), "hint": n.get("hint", ""), "desc": n.get("content-desc", ""),
                    "cls": n.get("class", ""), "password": n.get("password") == "true",
                    "clickable": n.get("clickable") == "true", "center": ((x1 + x2) // 2, (y1 + y2) // 2),
                    "bounds": (x1, y1, x2, y2)})
    return out


def texts():
    return [n["text"] for n in nodes() if n["text"]]


def find(text=None, hint=None, cls=None, exact=True):
    for n in nodes():
        if cls and n["cls"] != cls:
            continue
        if text is not None and not (n["text"] == text if exact else text in n["text"]):
            continue
        if hint is not None and n["hint"] != hint and n["text"] != hint:
            continue
        return n
    return None


def wait_for(text, timeout=10, exact=False):
    end = time.time() + timeout
    while time.time() < end:
        n = find(text=text, exact=exact)
        if n:
            return n
        time.sleep(0.5)
    return None


def tap(node_or_xy):
    x, y = node_or_xy["center"] if isinstance(node_or_xy, dict) else node_or_xy
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(0.6)


def type_text(value):
    """Nhập chữ vào ô đang được chọn; `input text` cần thay dấu cách bằng %s và thoát ký tự đặc biệt của shell."""
    if value == "":
        return
    escaped = value.replace("%", "\\%").replace(" ", "%s")
    escaped = re.sub(r"([\\\\'\"`$&|;<>()!*?#~{}\[\]])", r"\\\1", escaped)
    adb("shell", f"input text {escaped}")
    time.sleep(0.3)


def clear_field(node):
    """Chọn ô rồi xóa nội dung hiện có."""
    tap(node)
    adb("shell", "input", "keyevent", "KEYCODE_MOVE_END")
    adb("shell", "input", "keyevent", *(["KEYCODE_DEL"] * max(len(node["text"]) + 2, 2)))


def fill(node, value):
    clear_field(node)
    type_text(value)


def hide_keyboard():
    if "mInputShown=true" in adb("shell", "dumpsys", "input_method", check=False):
        adb("shell", "input", "keyevent", "KEYCODE_BACK")
        time.sleep(0.3)


def screenshot(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        subprocess.run([ADB, "exec-out", "screencap", "-p"], check=True, stdout=f)


def dismiss_dialogs():
    """Đóng hộp thoại không thuộc app: menu Expo ("Continue"), "System UI isn't responding" ("Wait")."""
    for label in ("Continue", "Wait"):
        n = find(text=label, exact=True)
        if n:
            tap(n)


def reload_app(tries=3):
    """Mở lại app Expo (xóa trạng thái trong bộ nhớ: giỏ hàng, phiên đăng nhập lưu trong state).
    Lệnh mở ngay sau force-stop đôi khi không khởi động được Expo Go, nên thử lại tối đa `tries` lần."""
    for _ in range(tries):
        adb("shell", "am", "force-stop", "host.exp.exponent", check=False)
        time.sleep(1)
        adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "exp://10.0.2.2:8081",
            "host.exp.exponent", check=False)
        end = time.time() + 8
        while time.time() < end:  # chờ trang chủ tải xong danh sách sản phẩm
            dismiss_dialogs()
            if find(text="Hiển thị 5 sản phẩm", exact=False):
                time.sleep(1)
                dismiss_dialogs()
                return True
            time.sleep(1)
    return False
