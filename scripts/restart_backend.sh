#!/bin/bash
# Khởi động lại backend EShop để reset dữ liệu về seed (self cleaning giữa các phiên thực thi).
SUT="$(cd "$(dirname "$0")/../../.." && pwd)/eshop-sut-main"
PID=$(lsof -ti tcp:3000 -sTCP:LISTEN)
if [ -n "$PID" ]; then
  kill $PID
  while lsof -ti tcp:3000 -sTCP:LISTEN > /dev/null; do sleep 0.2; done
fi
# setsid: tách khỏi phiên terminal / VS Code để backend không bị dừng theo
(cd "$SUT/backend" && setsid nohup node server.js > "$SUT/backend/server.log" 2>&1 < /dev/null &)
until curl -s -o /dev/null localhost:3000/api/products; do sleep 0.3; done
echo "backend restarted (seed data)"
