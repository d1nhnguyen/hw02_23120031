---
name: ai-audit-log
description: Build the AI usage record required by the FIT@HCMUS AI policy after an AI-assisted testing session - extract a timestamped verbatim prompt log from Claude Code transcripts and draft the AI Audit Report table (template AI-02, one row per artifact) from git commits that follow the `[FEATURE][Bn]` / `[FEATURE][Bn-review]` convention. Use when the user asks to update the prompt log, prepare the AI Audit Report, or log AI usage for a homework.
---

# Ghi nhật ký sử dụng AI (prompt log + AI Audit Report)

## 1. Prompt log (Phụ lục A)

```bash
python3 scripts/export_prompt_log.py --since <YYYY-MM-DDTHH:MM> --out ai/prompt_log.md
```

- Đọc transcript `~/.claude/projects/<dự án>/*.jsonl`, giữ **nguyên văn** prompt của sinh viên và câu trả lời của AI, thời gian GMT+7, model, danh sách hành động công cụ (thu gọn).
- Bỏ: nội dung harness tự chèn (`<system-reminder>`, IDE selection), thông báo tác vụ nền (`promptSource = system`), phần suy luận ẩn, nội dung file / output lệnh mà AI đọc.
- `--since` để loại các phiên không thuộc bài (vd phiên làm thử trước khi bắt đầu). Kiểm tra bảng mục lục đầu file: số lượt phải bằng số prompt sinh viên thực sự gõ.
- Chạy lại sau mỗi phiên, commit `[ai-log] …`.

## 2. Nháp bảng AI Audit Report (mẫu AI-02)

```bash
python3 scripts/audit_draft.py <repo> --prompt-log ai/prompt_log.md > ai/audit_draft.md
```

- Mỗi hàng = một artifact AI sinh ở một bước (`[F][Bn]`); cột (5) lấy từ commit `[F][Bn-review]`. Commit `[skill]` / `[report]` mỗi commit một hàng.
- `--prompt-log`: cột (1) ghi lượt prompt gần nhất trước commit (đọc bảng mục lục của prompt log), cột (5) ghi lượt prompt dẫn tới bản sửa.
- Verdict gợi ý: VALID (không sửa) / INCOMPLETE (có sửa sau rà soát); sinh viên đổi thành INVALID nếu artifact bị loại.
- Sinh viên điền cột (4) "Lý do" có dẫn chiếu slide / ISTQB, và đối chiếu từng dòng với `git diff <ai>..<review>`.
- Tổng hợp mục 4 (số lượng / tỉ lệ VALID / INVALID / INCOMPLETE) từ bảng đã duyệt.

## 3. Các mục khác của bộ hồ sơ AI

| File | Nội dung | Ai viết |
| --- | --- | --- |
| `ai/AI_Audit_Report.md` | Bảng audit đã duyệt, tổng kết độ chính xác, kết luận 80–150 chữ, Mandatory Disclosure | AI nháp bảng, sinh viên duyệt và viết kết luận |
| `ai/AI_Disclosure_Form.md` | Công cụ, giai đoạn dùng AI, 2–3 prompt chính, phần AI đóng góp, cách xác minh, trích dẫn IEEE | Sinh viên (AI gợi ý từ prompt log) |
| `ai/AI_Critique.md` | 200–300 từ: AI sai ở đâu, vì sao, nguyên tắc rút ra – dựa trên mục 6 (gap analysis) của các báo cáo | Sinh viên |
| `ai/AI_Privacy_Checklist.md` | Bảng kiểm trước khi nộp | Sinh viên đánh dấu |

Không tự điền họ tên, chữ ký, điểm tự chấm; không tự khẳng định thay sinh viên những việc sinh viên chưa làm.
