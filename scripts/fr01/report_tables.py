"""Sinh các bảng của report/FR-01_Dang_ky.md từ cases.py và file kết quả trong evidence/FR-01/.

Mỗi bảng nằm giữa hai mốc <!-- BEGIN:<mã> --> và <!-- END:<mã> --> trong báo cáo:
  T32 Minimum Set · T33 bảng phủ phân vùng · T42 Boundary Value Test Cases · T62 test case bổ sung
  T53 kết quả theo test case · T55 tổng hợp
Dùng: python3 report_tables.py T32 T33   (không truyền mã nào = sinh tất cả)
"""
import json
import re
import sys
from pathlib import Path

from cases import BY_ID, CASES, PREFIX

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "report" / "FR-01_Dang_ky.md"
EVIDENCE = ROOT / "evidence" / "FR-01"
FIELD_VN = {"name": "Họ Tên", "email": "Email", "password": "Mật khẩu", "confirm": "Xác nhận mật khẩu"}

# Thứ tự bảng BVA: test case BV mới xen với các điểm biên đã có trong Minimum Set (dẫn chiếu, không chạy lại)
BV_ORDER = [
    ("DT-19", "EC17 – độ dài 0"),
    "BV-01", "BV-02",
    ("DT-20", "EC19 – độ dài 6 (UB-1)"),
    "BV-03",
    ("DT-01", "EC19/EC18 – độ dài 8 (LB của EC18); EC20, EC24, EC26 – đúng 1 chữ hoa, 1 chữ số, 1 ký tự đặc biệt (LB); "
              "số khoảng trắng đầu email = 0"),
    "BV-04", "BV-05",
    ("DT-21", "EC21 – 0 chữ hoa; `@`/`A` (`@` là ký tự liền trước `A`, LB-1 chữ hoa)"),
    ("DT-22", "EC23 – 0 chữ thường"),
    ("DT-23", "EC25 – 0 chữ số"),
    ("DT-24", "EC27 – 0 ký tự đặc biệt"),
    "BV-06", "BV-07", "BV-08", "BV-09", "BV-10", "BV-11", "BV-12", "BV-13",
    ("DT-08", "EC3 – Họ Tên độ dài 0"),
    "BV-14", "BV-15", "BV-16", "BV-17", "BV-18", "BV-19", "BV-20", "BV-21",
]


def code(value):
    """Giá trị trong ô bảng: dấu cách hiện thành ␣, rỗng ghi rõ (rỗng)."""
    if value == "":
        return "(rỗng)"
    v = value.replace(" ", "␣").replace("|", "\\|")
    longest = max((len(m) for m in re.findall(r"`+", v)), default=0)
    fence = "`" * (longest + 1)
    pad = " " if v.startswith("`") or v.endswith("`") else ""
    return f"{fence}{pad}{v}{pad}{fence}"


def cell(c, field):
    if field in c["show"]:
        return c["show"][field]
    if field == "confirm" and c["confirm"] == c["password"] and "password" in c["show"]:
        return c["show"]["password"]
    return code(c[field])


def channel(c):
    return "Web, API" if "api" in c["channels"] else "Web"


def design_row(c, tc_id=None, covers=None, origin=None):
    return (f"| {tc_id or c['id']} | {c['title']} | {covers or c['covers']} | {cell(c, 'name')} | {cell(c, 'email')} "
            f"| {cell(c, 'password')} | {cell(c, 'confirm')} | {c['expected']} | {channel(c)} | {origin or c['origin']} |")


def design_table(cases, covers_header="Phân vùng phủ"):
    head = (f"| ID | Tên test case (Action + Function + Condition) | {covers_header} | Họ Tên | Email | Mật khẩu "
            "| Xác nhận | Kết quả mong đợi | Kênh | Origin |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    return "\n".join([head] + [design_row(c) for c in cases])


def t32():
    dt = [c for c in CASES if c["section"] == "DT"]
    valid = [c for c in dt if c["expect"] == "accept"]
    invalid = [c for c in dt if c["expect"] == "reject"]
    return ("**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:\n\n" + design_table(valid)
            + "\n\n**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:\n\n"
            + design_table(invalid))


def compress(ids):
    """FR01-DT-01, 03, 04, 05 -> 'FR01-DT-01, FR01-DT-03…FR01-DT-05'."""
    nums = sorted(int(i.rsplit("-", 1)[1]) for i in ids)
    groups, start = [], None
    for k, n in enumerate(nums):
        if start is None:
            start = n
        if k + 1 == len(nums) or nums[k + 1] != n + 1:
            groups.append((start, n))
            start = None
    name = lambda n: f"{PREFIX}-DT-{n:02d}"
    return ", ".join(name(a) if a == b else f"{name(a)}, {name(b)}" if b == a + 1 else f"{name(a)}…{name(b)}"
                     for a, b in groups)


def t33():
    cover, extra = {}, {}
    for c in CASES:
        target = cover if c["section"] == "DT" else extra if c["section"] == "GAP" else None
        if target is None:
            continue
        for ec in re.findall(r"EC(\d+)", c["covers"]):
            target.setdefault(int(ec), []).append(c["id"])
    rows = []
    for n in range(1, 47):
        text = compress(cover.get(n, []))
        if n in extra:
            text += f"; bổ sung: {', '.join(extra[n])} (mục 6.2)"
        rows.append((f"EC{n}", text))
    half = (len(rows) + 1) // 2
    lines = ["| EC | Test case phủ | | EC | Test case phủ |", "| --- | --- | --- | --- | --- |"]
    for (a, x), (b, y) in zip(rows[:half], rows[half:] + [("", "")]):
        lines.append(f"| {a} | {x} | | {b} | {y} |")
    covered = sum(1 for n in range(1, 47) if cover.get(n))
    dt = [c for c in CASES if c["section"] == "DT"]
    valid = sum(c["expect"] == "accept" for c in dt)
    return ("\n".join(lines) + f"\n\n{covered} / 46 lớp được phủ bởi {len(dt)} test case Minimum Set ({valid} valid, "
            f"{len(dt) - valid} invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp invalid có đúng một "
            "test case riêng. Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`.")


def t42():
    rows = []
    for item in BV_ORDER:
        if isinstance(item, tuple):
            c = BY_ID[f"{PREFIX}-{item[0]}"]
            rows.append(design_row(c, tc_id=f"({c['id']})", covers=item[1], origin="xem 3.2"))
        else:
            rows.append(design_row(BY_ID[f"{PREFIX}-{item}"]))
    head = design_table([], covers_header="Partition tested")
    new = sum(1 for i in BV_ORDER if not isinstance(i, tuple))
    refs = len(BV_ORDER) - new
    return (head + "\n" + "\n".join(rows) + f"\n\nTổng: {new} test case BVA mới ({PREFIX}-BV-01…{PREFIX}-BV-21); "
            f"{refs} dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case Minimum Set (mục 3.2), "
            "chỉ dẫn chiếu, không chạy lại.")


def t62():
    return design_table([c for c in CASES if c["section"] == "GAP"])


def load(name):
    path = EVIDENCE / name
    return {r["id"]: r for r in json.loads(path.read_text(encoding="utf-8"))["results"]} if path.exists() else {}


def bugs_for(c, ch, verdict):
    if verdict != "Fail":
        return []
    t = c["target"]
    if ch == "web":
        if t == "confirm":
            return ["FR01-B2"]
        return ["FR01-B1"] if c["expect"] == "accept" or t == "password" else ["?"]
    if t == "name":
        return ["FR01-B3"] if c["name"] == "" else ["FR01-B9"]
    if t == "email":
        return ["FR01-B3"] if c["email"] == "" else ["FR01-B4"]
    if t == "dup":
        return ["FR01-B6"] + (["FR01-B8"] if c["email"] != c["email"].strip() else [])
    if t == "password" and c["expect"] == "reject":
        return ["FR01-B3"] if c["password"] == "" else ["FR01-B5"]
    if t == "mixed":
        return ["FR01-B8"]
    return ["?"]


def first_sentence(text):
    return text.split("!")[0] + "!" if "!" in text else text


def web_actual(r):
    parts = []
    if r["target"] == "confirm" and not r["confirm_field"]:
        parts.append("không có ô Xác nhận mật khẩu")
    if r["request_sent"]:
        parts.append(f"form gửi request, HTTP {r['status']}, chuyển tới `{r['url_after']}`")
    else:
        native = [m for m in r["messages"] if m["source"].startswith("native")]
        page = [m for m in r["messages"] if m["source"] == "page"]
        if native:
            parts.append(f"trình duyệt chặn ô {FIELD_VN[native[0]['reason']]}: “{native[0]['text']}”")
        elif page:
            parts.append(f"form báo “{first_sentence(page[0]['text'])}”, không gửi request")
        else:
            parts.append("không gửi request, không có thông báo")
    parts.append("tạo tài khoản" if r["created"] else "không tạo tài khoản")
    if r.get("login_ok") is not None and r["created"]:
        parts.append("đăng nhập được" if r["login_ok"] else "không đăng nhập được")
    text = "; ".join(parts)
    if r["verdict"] == "Blocked":
        text += " – bị lỗi mật khẩu che, chưa tới điều kiện cần kiểm tra"
    return text[0].upper() + text[1:]


def api_actual(r):
    body = r["body"]
    msg = (body.get("message") or body.get("error")) if isinstance(body, dict) else str(body)
    parts = [f"HTTP {r['status']} “{msg}”"]
    if r["created"]:
        parts.append("tạo tài khoản")
    elif r["status"] == 200:
        parts.append("tài khoản lưu với email chưa bỏ khoảng trắng")
    else:
        parts.append("không tạo tài khoản")
    if r.get("login_ok") is not None:
        parts.append("đăng nhập được" if r["login_ok"] else "không đăng nhập được bằng email đã bỏ khoảng trắng")
    if r.get("seed_login_ok"):
        parts.append("tài khoản gốc vẫn đăng nhập được")
    return "; ".join(parts)


def t53():
    web, api = load("web_results.json"), load("api_results.json")
    lines = ["| TC | Web | Kết quả thực tế – Web | API | Kết quả thực tế – API | Bằng chứng | Bug |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for c in CASES:
        w, a = web.get(c["id"]), api.get(c["id"])
        bugs = []
        for ch, r in (("web", w), ("api", a)):
            for b in bugs_for(c, ch, r["verdict"] if r else None):
                if b not in bugs:
                    bugs.append(b)
        proof = f"[ảnh Web](../evidence/FR-01/web/{c['id']}.png)" + (" · `api_results.json`" if a else "")
        lines.append(f"| {c['id']} | {w['verdict'] if w else '–'} | {web_actual(w) if w else '–'} "
                     f"| {a['verdict'] if a else '–'} | {api_actual(a) if a else 'Không áp dụng (A8)'} "
                     f"| {proof} | {', '.join(bugs) or '–'} |")
    return "\n".join(lines)


def t55():
    web, api = load("web_results.json"), load("api_results.json")
    count = lambda res, v: sum(r["verdict"] == v for r in res.values())
    n = len(CASES)
    na = n - len(api)
    total = len(web) + len(api)
    lines = ["| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |",
             "| --- | --- | --- | --- | --- | --- | --- |",
             f"| Web | {n} | {len(web)} | {count(web, 'Pass')} | {count(web, 'Fail')} | {count(web, 'Blocked')} | 0 |",
             f"| API | {n} | {len(api)} | {count(api, 'Pass')} | {count(api, 'Fail')} | 0 | {na} (biến Xác nhận mật khẩu, A8) |",
             f"| **Tổng lượt chạy** | | **{total}** | **{count(web, 'Pass') + count(api, 'Pass')}** "
             f"| **{count(web, 'Fail') + count(api, 'Fail')}** | **{count(web, 'Blocked')}** | |"]
    per_tc = {"Pass": 0, "Fail": 0, "Blocked": 0}
    for c in CASES:
        verdicts = [r["verdict"] for r in (web.get(c["id"]), api.get(c["id"])) if r]
        key = "Fail" if "Fail" in verdicts else "Blocked" if "Blocked" in verdicts else "Pass"
        per_tc[key] += 1
    sections = {s: sum(c["section"] == s for c in CASES) for s in ("DT", "BV", "GAP")}
    return ("\n".join(lines) + f"\n\n{n} test case = {sections['DT']} Minimum Set (mục 3.2) + {sections['BV']} BVA "
            f"(mục 4.2) + {sections['GAP']} bổ sung sau rà soát (mục 6.2). Gộp 2 kênh theo test case (Fail nếu Fail ở "
            f"bất kỳ kênh nào, Blocked nếu còn kênh bị Blocked): {per_tc['Pass']} Pass, {per_tc['Fail']} Fail, "
            f"{per_tc['Blocked']} Blocked.")


TABLES = {"T32": t32, "T33": t33, "T42": t42, "T62": t62, "T53": t53, "T55": t55}


def main(codes):
    text = REPORT.read_text(encoding="utf-8")
    for key in codes or TABLES:
        begin, end = f"<!-- BEGIN:{key} -->", f"<!-- END:{key} -->"
        if begin not in text:
            print(f"bỏ qua {key}: không có mốc trong báo cáo")
            continue
        i, j = text.index(begin) + len(begin), text.index(end)
        text = text[:i] + "\n" + TABLES[key]() + "\n" + text[j:]
        print(f"đã sinh {key}")
    REPORT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
