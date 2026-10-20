// Tái hiện các bug Mobile – Đăng nhập và chụp bằng chứng vào bugs/screenshots/.
// Dùng ảnh app từ evidence/Mobile (chạy run_mobile.py trước) + gọi API thật để ghi bộ đếm / thời gian khóa.
// Không chạy song song với run_mobile.py / run_api.py (script khởi động lại backend).
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const OUT = join(ROOT, 'bugs', 'screenshots');
const EV = join(ROOT, 'evidence', 'Mobile');
const API = 'http://localhost:3000/api';
mkdirSync(OUT, { recursive: true });
const restart = () => execFileSync(join(ROOT, 'scripts', 'restart_backend.sh'), { stdio: 'ignore' });

const browser = await chromium.launch({ channel: 'chrome' });
const card = await browser.newPage({ viewport: { width: 1200, height: 400 } });
const api = card.request;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

async function evidence(file, title, rows, images = [], head = ['Request / bước', 'HTTP', 'Kết quả']) {
  const imgs = images.map(([path, caption]) => `<figure><img src="data:image/png;base64,${readFileSync(path).toString('base64')}"><figcaption>${esc(caption)}</figcaption></figure>`).join('');
  const body = rows.map((r) => `<tr>${r.map((v, i) => `<td class="${i === 1 ? `s${String(v)[0]}` : ''}"><pre>${esc(v)}</pre></td>`).join('')}</tr>`).join('');
  await card.setContent(`<html><body style="font:14px sans-serif;margin:16px">
    <h3 style="margin:0 0 4px">${esc(title)}</h3>
    <div style="color:#555;margin-bottom:8px">Ghi nhận lúc ${new Date().toLocaleString('vi-VN')} · ${API}</div>
    ${rows.length ? `<table><tr>${head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr>${body}</table>` : ''}
    <div class="imgs">${imgs}</div>
    <style>table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:4px 6px;text-align:left;vertical-align:top}
    pre{margin:0;white-space:pre-wrap;word-break:break-all;font-size:12px}.s2{color:#b00;font-weight:bold}.s4{color:#070}
    .imgs{display:flex;gap:12px;margin-top:10px;align-items:flex-start}figure{margin:0;width:340px}img{width:340px;border:1px solid #bbb}
    figcaption{font-size:12px;color:#333}</style></body></html>`);
  await card.screenshot({ path: join(OUT, file), fullPage: true });
  console.log(file);
}

async function login(email, password) {
  const r = await api.post(`${API}/login`, { data: { email, password } });
  const b = await r.json();
  return { status: r.status(), text: b.token ? '{"message":"Login successful","token":"…"}' : JSON.stringify(b) };
}
async function state() {
  const admin = (await (await api.post(`${API}/login`, { data: { email: 'admin@eshop.com', password: 'Admin123!' } })).json()).token;
  const u = (await (await api.get(`${API}/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })).json()).find((x) => x.email === 'test@eshop.com');
  return u;
}
const row = async (label, email, password) => {
  const r = await login(email, password);
  const s = await state();
  return [`${label}: POST /api/login {"email": "${email}", "password": "${password}"}`, r.status,
    `${r.text}\nlogin_attempts = ${s.login_attempts}, locked_until = ${s.locked_until ?? 'null'}`];
};

// MOB-B1: thanh tiêu đề bị thanh trạng thái che (Pixel 6)
await evidence('MOB-B1.png', 'MOB-B1 – Trên Pixel 6 (thanh trạng thái cao 128 px) thanh tiêu đề của app (y = 37–108) bị che, chạm "Đăng nhập" không mở màn hình Đăng nhập', [
  ['Pixel 6, Android 14: adb shell input tap 808 72 (tâm chữ "Đăng nhập")', '–', 'không chuyển màn hình'],
  ['Pixel 6: adb shell input tap 808 95 (mép dưới chữ "Đăng nhập")', '–', 'không chuyển màn hình (vẫn nằm trong vùng thanh trạng thái y < 128)'],
  ['Pixel 2, Android 14 (thanh trạng thái 63 px): adb shell input tap 808 85', '–', 'mở màn hình "Đăng Nhập"'],
], [[join(EV, 'B1_pixel6_header_bi_che.png'), 'Pixel 6: chữ "Đăng nhập", "Giỏ (0)" nằm dưới thanh trạng thái'],
    [join(EV, 'B1_pixel2_man_hinh_dang_nhap.png'), 'Pixel 2: chạm được phần dưới chữ "Đăng nhập" → màn hình Đăng nhập']], ['Bước', 'HTTP', 'Kết quả']);

// MOB-B2: bộ đếm tăng 2 mỗi lần sai, khóa sau 2 lần
restart();
const rows2 = [await row('Sai lần 1', 'test@eshop.com', 'Sai12345!'), await row('Sai lần 2', 'test@eshop.com', 'Sai12345!'),
  await row('Đúng sau 2 lần sai', 'test@eshop.com', 'Test1234!')];
await evidence('MOB-B2.png', 'MOB-B2 – Mỗi lần đăng nhập sai bộ đếm tăng 2 (không phải 1); tài khoản bị khóa ngay sau lần sai thứ 2', rows2,
  [[join(EV, 'web', 'MOB-BV-02.png'), 'Mobile (MOB-BV-02): sai 2 lần rồi nhập đúng → vẫn "Đăng nhập thất bại"']]);

// MOB-B3: khóa 180 giây thay vì 30 giây
restart();
await login('test@eshop.com', 'Sai12345!');
const t0 = new Date();
await login('test@eshop.com', 'Sai12345!');
const s3 = await state();
const seconds = Math.round((new Date(s3.locked_until) - t0) / 1000);
await new Promise((resolve) => setTimeout(resolve, 35000));
const after35 = await login('test@eshop.com', 'Test1234!');
await evidence('MOB-B3.png', `MOB-B3 – Tài khoản bị khóa ${seconds} giây thay vì 30 giây`, [
  [`Khóa lúc ${t0.toISOString()} (lần sai thứ 2 – xem MOB-B2)`, '–', `locked_until = ${s3.locked_until} → khóa ${seconds} giây`],
  ['Sau 35 giây: POST /api/login {"email": "test@eshop.com", "password": "Test1234!"}', after35.status, after35.text],
], [[join(EV, 'web', 'MOB-DT-04.png'), 'Mobile (MOB-DT-04): sau 35 giây vẫn không đăng nhập được']]);

// MOB-B4: email khác hoa / thường, có khoảng trắng
restart();
await evidence('MOB-B4.png', 'MOB-B4 – Đăng nhập thất bại khi email đúng nhưng khác chữ hoa / thường hoặc có khoảng trắng đầu / cuối', [
  await row('Email chữ hoa', 'TEST@eshop.com', 'Test1234!'), await row('Email có khoảng trắng', ' test@eshop.com ', 'Test1234!'),
], [[join(EV, 'web', 'MOB-DT-02.png'), 'Mobile (MOB-DT-02): email TEST@eshop.com → "Đăng nhập thất bại"']]);

// MOB-B5: nhãn tiếng Anh
await evidence('MOB-B5.png', 'MOB-B5 – Màn hình Đăng nhập dùng nhãn tiếng Anh "Username" cho ô Email và nút "Sign In"', [],
  [[join(EV, 'B1_pixel2_man_hinh_dang_nhap.png'), 'Nhãn "Username" phía trên ô Email; nút "Sign In"']]);

await browser.close();
restart();
