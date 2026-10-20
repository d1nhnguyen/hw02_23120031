#!/bin/bash
# Khởi động môi trường test EShop: backend, web, admin, Android Emulator + Expo Go.
# Dùng: scripts/start_env.sh [web|mobile|all]   (mặc định: all)
# Lưu ý: restart backend = reset toàn bộ dữ liệu về seed.
SUT="$(cd "$(dirname "$0")/../../.." && pwd)/eshop-sut-main"
export ANDROID_HOME="$HOME/Android/Sdk"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
MODE="${1:-all}"

(cd "$SUT/backend" && node server.js) &
sleep 2

if [ "$MODE" = web ] || [ "$MODE" = all ]; then
  (cd "$SUT/frontend-web" && npm run dev -- --port 5173 --strictPort) &
  (cd "$SUT/frontend-admin" && npm run dev) &
fi

if [ "$MODE" = mobile ] || [ "$MODE" = all ]; then
  # App.js:16 phải trỏ API_URL tới http://10.0.2.2:3000/api (host nhìn từ emulator)
  emulator -avd eshop_api34 -no-snapshot-save -no-boot-anim > /dev/null 2>&1 &
  adb wait-for-device
  until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = 1 ]; do sleep 2; done
  (cd "$SUT/frontend-mobile" && npx expo start --android --port 8081) &
fi

wait
