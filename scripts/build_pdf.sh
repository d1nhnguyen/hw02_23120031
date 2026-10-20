#!/bin/bash
# Xuất PDF ("Save-As-PDF") cho các file Markdown: pandoc -> HTML (nhúng ảnh) -> Chrome headless.
# Dùng: scripts/build_pdf.sh file1.md [file2.md ...]   -> tạo file1.pdf cạnh file1.md
set -euo pipefail
CSS="$(cd "$(dirname "$0")" && pwd)/pdf.css"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for md in "$@"; do
  dir="$(cd "$(dirname "$md")" && pwd)"
  name="$(basename "$md" .md)"
  title="$(grep -m1 '^# ' "$md" | sed 's/^# //')"
  # chạy trong thư mục của file để đường dẫn ảnh tương đối được nhúng đúng
  (cd "$dir" && pandoc "$name.md" -f gfm -t html5 -s --embed-resources --css "$CSS" \
     --metadata title="${title:-$name}" -V title= -o "$TMP/$name.html")
  google-chrome --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$dir/$name.pdf" "file://$TMP/$name.html" 2>/dev/null
  echo "$dir/$name.pdf"
done
