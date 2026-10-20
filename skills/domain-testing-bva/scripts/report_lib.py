"""Phần chung để sinh bảng báo cáo Domain Testing / BVA từ cases.py của từng feature.

Mỗi bảng trong báo cáo nằm giữa <!-- BEGIN:<mã> --> và <!-- END:<mã> -->:
  T32 Minimum Set · T33 bảng phủ phân vùng · T42 Boundary Value Test Cases · T62 test case bổ sung
  T53 kết quả theo test case · T55 tổng hợp
Feature cung cấp một đối tượng `Feature` mô tả cột dữ liệu và cách diễn giải kết quả.
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

MISSING = "__MISSING__"  # trường không được gửi (API) / để trống (Web)


def code(value):
    """Giá trị trong ô bảng: dấu cách hiện thành ␣, rỗng ghi rõ (rỗng)."""
    if value is None:
        return "–"
    if value == MISSING:
        return "(bỏ trống / không gửi)"
    if value == "":
        return "(rỗng)"
    v = str(value).replace(" ", "␣").replace("|", "\\|")
    longest = max((len(m) for m in re.findall(r"`+", v)), default=0)
    fence = "`" * (longest + 1)
    pad = " " if v.startswith("`") or v.endswith("`") else ""
    return f"{fence}{pad}{v}{pad}{fence}"


def esc_cell(text):
    """Văn bản tự do trong ô bảng: không để Markdown / HTML diễn giải nhầm (vd tên chứa <b>)."""
    return str(text).replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


@dataclass
class Feature:
    prefix: str                          # vd "FR01"
    cases: list                          # danh sách dict từ cases.py
    fields: list                         # [(khóa, nhãn cột)] các biến đầu vào hiển thị trong bảng
    report: Path                         # file báo cáo
    evidence: Path                       # thư mục bằng chứng (chứa web_results.json, api_results.json, web/)
    n_ec: int                            # số lớp tương đương (EC1…ECn)
    bv_order: list = field(default_factory=list)  # thứ tự bảng BVA; tuple (short_id, partition) = dòng dẫn chiếu
    web_actual: Callable = None          # (kết quả Web, case) -> mô tả kết quả thực tế
    api_actual: Callable = None          # (kết quả API, case) -> mô tả kết quả thực tế
    bugs_for: Callable = None            # (case, kênh, verdict) -> [mã bug]
    display: Callable = None             # (case, khóa) -> chuỗi hiển thị riêng (tùy chọn)
    na_text: str = "Không áp dụng"       # ô kết quả khi test case không chạy trên kênh đó
    na_note: str = ""                    # ghi chú cột "Không áp dụng" của kênh API trong bảng tổng hợp
    web_label: str = "Web"               # tên kênh giao diện trong bảng kết quả (vd "Mobile")

    @property
    def by_id(self):
        return {c["id"]: c for c in self.cases}

    # ---- thiết kế ----
    def cell(self, c, key):
        if key in c.get("show", {}):
            return c["show"][key]
        if self.display:
            custom = self.display(c, key)
            if custom is not None:
                return custom
        return code(c.get(key))

    @staticmethod
    def channel(c):
        return "Web, API" if c["channels"] == ["web", "api"] else "API" if c["channels"] == ["api"] else "Web"

    def design_row(self, c, tc_id=None, covers=None, origin=None):
        cells = " | ".join(self.cell(c, k) for k, _ in self.fields)
        return (f"| {tc_id or c['id']} | {c['title']} | {covers or c['covers']} | {cells} | {c['expected']} "
                f"| {self.channel(c)} | {origin or c['origin']} |")

    def design_table(self, cases, covers_header="Phân vùng phủ"):
        labels = " | ".join(label for _, label in self.fields)
        sep = " | ".join("---" for _ in range(len(self.fields) + 6))
        head = (f"| ID | Tên test case (Action + Function + Condition) | {covers_header} | {labels} "
                f"| Kết quả mong đợi | Kênh | Origin |\n| {sep} |")
        return "\n".join([head] + [self.design_row(c) for c in cases])

    @staticmethod
    def is_valid(c):
        # "ui": kiểm tra giao diện chỉ cho phép hành vi đúng – xếp cùng nhóm valid
        return c["expect"] in ("accept", "ui")

    def t32(self):
        dt = [c for c in self.cases if c["section"] == "DT"]
        valid = [c for c in dt if self.is_valid(c)]
        invalid = [c for c in dt if not self.is_valid(c)]
        return ("**Test case valid** – mỗi test case phủ nhiều lớp valid nhất có thể:\n\n" + self.design_table(valid)
                + "\n\n**Test case invalid** – mỗi test case phủ đúng một lớp invalid, các biến còn lại hợp lệ:\n\n"
                + self.design_table(invalid))

    def compress(self, ids):
        nums = sorted(int(i.rsplit("-", 1)[1]) for i in ids)
        groups, start = [], None
        for k, n in enumerate(nums):
            start = n if start is None else start
            if k + 1 == len(nums) or nums[k + 1] != n + 1:
                groups.append((start, n))
                start = None
        name = lambda n: f"{self.prefix}-DT-{n:02d}"
        return ", ".join(name(a) if a == b else f"{name(a)}, {name(b)}" if b == a + 1 else f"{name(a)}…{name(b)}"
                         for a, b in groups)

    def t33(self):
        cover, extra = {}, {}
        for c in self.cases:
            target = cover if c["section"] == "DT" else extra if c["section"] == "GAP" else None
            if target is None:
                continue
            for ec in re.findall(r"EC(\d+)", c["covers"]):
                target.setdefault(int(ec), []).append(c["id"])
        rows = []
        for n in range(1, self.n_ec + 1):
            text = self.compress(cover.get(n, []))
            if n in extra:
                text += f"; bổ sung: {', '.join(extra[n])} (mục 6.2)"
            rows.append((f"EC{n}", text))
        half = (len(rows) + 1) // 2
        lines = ["| EC | Test case phủ | | EC | Test case phủ |", "| --- | --- | --- | --- | --- |"]
        for (a, x), (b, y) in zip(rows[:half], rows[half:] + [("", "")]):
            lines.append(f"| {a} | {x} | | {b} | {y} |")
        covered = sum(1 for n in range(1, self.n_ec + 1) if cover.get(n))
        dt = [c for c in self.cases if c["section"] == "DT"]
        valid = sum(self.is_valid(c) for c in dt)
        note = " Các đại diện bổ sung sau rà soát (mục 6.2) ghi sau dấu `;`." if extra else ""
        return ("\n".join(lines) + f"\n\n{covered} / {self.n_ec} lớp được phủ bởi {len(dt)} test case Minimum Set "
                f"({valid} valid, {len(dt) - valid} invalid). Lớp valid chỉ tính các test case valid phủ nó; mỗi lớp "
                f"invalid có test case riêng.{note}")

    def t42(self):
        rows = []
        for item in self.bv_order:
            if isinstance(item, tuple):
                c = self.by_id[f"{self.prefix}-{item[0]}"]
                rows.append(self.design_row(c, tc_id=f"({c['id']})", covers=item[1], origin="xem 3.2"))
            else:
                rows.append(self.design_row(self.by_id[f"{self.prefix}-{item}"]))
        new = [i for i in self.bv_order if not isinstance(i, tuple)]
        return (self.design_table([], covers_header="Partition tested") + "\n" + "\n".join(rows)
                + f"\n\nTổng: {len(new)} test case BVA mới ({self.prefix}-{new[0]}…{self.prefix}-{new[-1]}); "
                f"{len(self.bv_order) - len(new)} dòng có ID trong ngoặc là điểm biên đã được phủ bởi test case "
                "Minimum Set (mục 3.2), chỉ dẫn chiếu, không chạy lại.")

    def t62(self):
        return self.design_table([c for c in self.cases if c["section"] == "GAP"])

    # ---- kết quả ----
    def load(self, name):
        path = self.evidence / name
        if not path.exists():
            return {}
        return {r["id"]: r for r in json.loads(path.read_text(encoding="utf-8"))["results"]}

    def t53(self):
        web, api = self.load("web_results.json"), self.load("api_results.json")
        wl = self.web_label
        lines = [f"| TC | {wl} | Kết quả thực tế – {wl} | API | Kết quả thực tế – API | Bằng chứng | Bug |",
                 "| --- | --- | --- | --- | --- | --- | --- |"]
        rel = f"../evidence/{self.evidence.name}"
        for c in self.cases:
            w, a = web.get(c["id"]), api.get(c["id"])
            bugs = []
            for ch, r in (("web", w), ("api", a)):
                for b in self.bugs_for(c, ch, r["verdict"] if r else None):
                    if b not in bugs:
                        bugs.append(b)
            proof = " · ".join(([f"[ảnh {wl}]({rel}/web/{c['id']}.png)"] if w else []) + (["`api_results.json`"] if a else []))
            na = self.na_text
            lines.append(f"| {c['id']} | {w['verdict'] if w else '–'} | {esc_cell(self.web_actual(w, c)) if w else na} "
                         f"| {a['verdict'] if a else '–'} | {esc_cell(self.api_actual(a, c)) if a else na} "
                         f"| {proof} | {', '.join(bugs) or '–'} |")
        return "\n".join(lines)

    def t55(self):
        web, api = self.load("web_results.json"), self.load("api_results.json")
        count = lambda res, v: sum(r["verdict"] == v for r in res.values())
        n = len(self.cases)
        lines = ["| Kênh | Thiết kế | Đã chạy | Pass | Fail | Blocked | Không áp dụng |",
                 "| --- | --- | --- | --- | --- | --- | --- |",
                 f"| {self.web_label} | {n} | {len(web)} | {count(web, 'Pass')} | {count(web, 'Fail')} | {count(web, 'Blocked')} "
                 f"| {n - len(web)} |",
                 f"| API | {n} | {len(api)} | {count(api, 'Pass')} | {count(api, 'Fail')} | {count(api, 'Blocked')} "
                 f"| {n - len(api)}{self.na_note} |",
                 f"| **Tổng lượt chạy** | | **{len(web) + len(api)}** | **{count(web, 'Pass') + count(api, 'Pass')}** "
                 f"| **{count(web, 'Fail') + count(api, 'Fail')}** | **{count(web, 'Blocked') + count(api, 'Blocked')}** | |"]
        per_tc = {"Pass": 0, "Fail": 0, "Blocked": 0}
        for c in self.cases:
            verdicts = [r["verdict"] for r in (web.get(c["id"]), api.get(c["id"])) if r]
            per_tc["Fail" if "Fail" in verdicts else "Blocked" if "Blocked" in verdicts else "Pass"] += 1
        sections = {s: sum(c["section"] == s for c in self.cases) for s in ("DT", "BV", "GAP")}
        parts = f"{sections['DT']} Minimum Set (mục 3.2) + {sections['BV']} BVA (mục 4.2)"
        if sections["GAP"]:
            parts += f" + {sections['GAP']} bổ sung sau rà soát (mục 6.2)"
        return ("\n".join(lines) + f"\n\n{n} test case = {parts}. Gộp các kênh theo test case (Fail nếu Fail ở bất kỳ "
                f"kênh nào, Blocked nếu còn kênh bị Blocked): {per_tc['Pass']} Pass, {per_tc['Fail']} Fail, "
                f"{per_tc['Blocked']} Blocked.")

    # ---- ghi vào báo cáo ----
    def update(self, codes, extra=None):
        tables = {"T32": self.t32, "T33": self.t33, "T42": self.t42, "T62": self.t62, "T53": self.t53,
                  "T55": self.t55, **(extra or {})}
        text = self.report.read_text(encoding="utf-8")
        for key in codes or tables:
            begin, end = f"<!-- BEGIN:{key} -->", f"<!-- END:{key} -->"
            if begin not in text:
                print(f"bỏ qua {key}: không có mốc trong báo cáo")
                continue
            i, j = text.index(begin) + len(begin), text.index(end)
            text = text[:i] + "\n" + tables[key]() + "\n" + text[j:]
            print(f"đã sinh {key}")
        self.report.write_text(text, encoding="utf-8")
