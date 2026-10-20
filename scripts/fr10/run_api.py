"""Chạy test case FR-10 trên kênh API (thủ tục P-API). Bộ dữ liệu được dựng lại trước mỗi test case.

Kết quả: evidence/FR-10/api_results.json   ·   ONLY=FR10-DT-01,FR10-BV-02 python3 run_api.py
"""
import json
import os
from datetime import datetime
from pathlib import Path

from cases import CASES, MISSING
from fixture import call, setup, statuses

ROOT = Path(__file__).resolve().parents[2]
ONLY = os.environ["ONLY"].split(",") if os.environ.get("ONLY") else None
OUT = ROOT / "evidence" / "FR-10" / (f"api_results_{'_'.join(ONLY)}.json" if ONLY else "api_results.json")


def run_case(c):
    fx = setup()
    r = {"id": c["id"], "expect": c["expect"]}
    if not fx["ok"]:
        return {**r, "verdict": "Blocked", "notes": fx["problems"], "status": None, "body": None}
    before, tokens = fx["statuses"], fx["tokens"]
    if c["action"] == "status":
        body = {} if c["status"] == MISSING else {"status": c["status"]}
        status, resp = call("PUT", f"/admin/orders/{c['order']}/status", body, tokens["admin"])
    else:
        status, resp = call("PUT", f"/orders/{c['order']}/cancel", None, tokens["test"])
    after = statuses(tokens["admin"])
    changed = {oid: (before.get(oid), after.get(oid)) for oid in set(before) | set(after) if before.get(oid) != after.get(oid)}
    r.update(status=status, body=resp, changed={str(k): v for k, v in changed.items()}, after=after.get(c["order"]))
    message = (resp.get("error") or resp.get("message") or "") if isinstance(resp, dict) else str(resp)
    notes = []
    if c["expect"] == "accept":
        ok = 200 <= status < 300 and changed == {c["order"]: (c["from_state"], c["target_state"])}
    elif c["expect"] == "notfound":
        ok = status == 404 and not changed
    else:
        ok = 400 <= status < 500 and not changed and bool(message)
        if 400 <= status < 500 and not changed and not message:
            notes.append("bị từ chối nhưng không có thông báo")
    for oid, (old, new) in changed.items():
        if c["expect"] != "accept" or oid != c["order"]:
            notes.append(f"đơn #{oid} bị chuyển `{old}` → `{new}`")
    r["verdict"] = "Pass" if ok else "Fail"
    r["notes"] = notes
    return r


def main():
    results = []
    for c in CASES:
        if "api" not in c["channels"] or (ONLY and c["id"] not in ONLY):
            continue
        r = run_case(c)
        results.append(r)
        print(f"{c['id']:11} {c['actor']:6} {c['action']:7} #{str(c['order']):5} {str(c['status']):12} "
              f"HTTP {r['status']} -> {r['verdict']:7} {str(r['body'])[:50]} {'; '.join(r['notes'])}", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"run_at": datetime.now().isoformat(timespec="seconds"), "results": results},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    count = lambda v: sum(r["verdict"] == v for r in results)
    print(f"\n{len(results)} test case: {count('Pass')} Pass, {count('Fail')} Fail, {count('Blocked')} Blocked -> {OUT}")


if __name__ == "__main__":
    main()
