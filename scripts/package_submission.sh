#!/bin/bash
# Đóng gói bài nộp <MSSV>_HW02_AI_DomainTesting_<điểm>.zip ở thư mục cha của repo, từ commit HEAD (cây làm việc phải sạch).
# - bỏ file nội bộ (danh sách đối chiếu, kịch bản demo, .gitignore, liên kết skills); thêm git_commit_log.txt
# - ảnh PNG giảm còn 256 màu (giới hạn Moodle 20 MB / file); mỗi file .md có bản PDF cùng tên
# Dùng: scripts/package_submission.sh <điểm tự chấm 3 chữ số, vd 100>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GRADE="${1:?điểm tự chấm 3 chữ số, vd 100}"
[[ "$GRADE" =~ ^[0-9]{3}$ ]] || { echo "điểm phải có 3 chữ số (000–100)"; exit 1; }
NAME="23120031_HW02_AI_DomainTesting_${GRADE}"
ZIP="$(dirname "$ROOT")/$NAME.zip"
[ -z "$(git -C "$ROOT" status --porcelain)" ] || { echo "còn thay đổi chưa commit"; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
STAGE="$TMP/$NAME"
mkdir -p "$STAGE"
git -C "$ROOT" archive HEAD | tar -x -C "$STAGE"
rm -f "$STAGE/DOI_CHIEU_TRUOC_KHI_NOP.md" "$STAGE/KICH_BAN_DEMO.md" "$STAGE/.gitignore" "$STAGE/evidence/.gitkeep" "$STAGE/skills"
git -C "$ROOT" log --reverse --date=iso > "$STAGE/git_commit_log.txt"

python3 - "$STAGE" <<'EOF'
import sys
from pathlib import Path
from PIL import Image
before = after = 0
for f in Path(sys.argv[1]).rglob("*.png"):
    data = f.stat().st_size
    q = Image.open(f).quantize(colors=256, method=Image.Quantize.FASTOCTREE)
    tmp = f.with_suffix(".q.png")
    q.save(tmp, optimize=True)
    if tmp.stat().st_size < data:
        tmp.replace(f)
    else:
        tmp.unlink()
    before += data
    after += f.stat().st_size
print(f"ảnh PNG: {before / 1e6:.1f} MB -> {after / 1e6:.1f} MB")
EOF

find "$STAGE" -name '*.md' -print0 | sort -z | xargs -0 "$ROOT/scripts/build_pdf.sh" > /dev/null
echo "PDF: $(find "$STAGE" -name '*.pdf' | wc -l) / $(find "$STAGE" -name '*.md' | wc -l) file .md"

rm -f "$ZIP"
(cd "$TMP" && zip -r -q -9 "$ZIP" "$NAME")
echo "$ZIP ($(du -h "$ZIP" | cut -f1))"
