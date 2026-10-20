// Tái hiện các bug FR-01 và chụp bằng chứng vào bugs/screenshots/.
// Yêu cầu: backend vừa khởi động lại; Web (5173) và Web Admin (5174) đang chạy.
// Mỗi bug có một "thẻ bằng chứng": các bước, request và response thật ghi nhận lúc chạy, kèm ảnh giao diện nếu có.
import { chromium } from 'playwright-core';
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, '..', '..', 'bugs', 'screenshots');
const WEB = 'http://localhost:5173';
const ADMIN = 'http://localhost:5174';
const API = 'http://localhost:3000/api';
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1100, height: 760 } });
const card = await browser.newPage({ viewport: { width: 1100, height: 400 } });
const api = page.request;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const show = (v) => JSON.stringify(v).replace(/ /g, '␣');

async function post(path, data) {
  const r = await api.post(`${API}${path}`, { data });
  return { status: r.status(), body: await r.json().catch(async () => r.text()) };
}

// Thẻ bằng chứng: tiêu đề, các dòng request -> response, ảnh đính kèm (tùy chọn)
async function evidence(file, title, rows, image) {
  const img = image ? `<img src="data:image/png;base64,${readFileSync(image).toString('base64')}">` : '';
  const body = rows.map((r) => `<tr><td><pre>${esc(r.req)}</pre></td><td class="s${String(r.status)[0]}">${esc(r.status)}</td><td><pre>${esc(r.res)}</pre></td></tr>`).join('');
  await card.setContent(`<html><body style="font:14px sans-serif;margin:16px">
    <h3 style="margin:0 0 4px">${esc(title)}</h3>
    <div style="color:#555;margin-bottom:8px">Ghi nhận lúc ${new Date().toLocaleString('vi-VN')} · ${API}</div>
    ${rows.length ? `<table style="border-collapse:collapse;width:100%">
      <tr><th>Request</th><th>HTTP</th><th>Response</th></tr>${body}</table>` : ''}
    ${img}
    <style>td,th{border:1px solid #bbb;padding:4px 6px;text-align:left;vertical-align:top}pre{margin:0;white-space:pre-wrap;word-break:break-all;font-size:12px}
    .s2{color:#b00;font-weight:bold}.s4{color:#070}img{margin-top:10px;border:1px solid #bbb;max-width:100%}</style></body></html>`);
  await card.screenshot({ path: join(OUT, file), fullPage: true });
  console.log(file);
}

async function register(name, email, password) {
  const r = await post('/register', { name, email, password });
  return { req: `POST /api/register ${show({ name, email, password })}`, status: r.status, res: JSON.stringify(r.body) };
}

// FR01-B1: form Web từ chối mật khẩu hợp lệ
const shot = join(OUT, '_tmp.png');
await page.goto(`${WEB}/register`);
let inputs = page.locator('form input');
await inputs.nth(0).fill('Nguyen Van A');
await inputs.nth(1).fill('fr01.b1@example.com');
await inputs.nth(2).fill('Abcdef1@');
await page.locator('form button[type=submit]').click();
await page.waitForTimeout(800);
await inputs.nth(2).evaluate((e) => { e.type = 'text'; }); // chỉ để ảnh hiện rõ mật khẩu đã nhập
await page.screenshot({ path: shot });
await evidence('FR01-B1.png', 'FR01-B1 – Form Web báo "Mật khẩu quá yếu!" với mật khẩu hợp lệ Abcdef1@ (ô mật khẩu được chuyển sang hiển thị để chụp)', [], shot);

// FR01-B2: không có ô Xác nhận mật khẩu
await page.goto(`${WEB}/register`);
await page.screenshot({ path: shot });
await evidence('FR01-B2.png', 'FR01-B2 – Form Đăng ký chỉ có Họ Tên, Email, Mật khẩu; không có ô Xác nhận mật khẩu', [], shot);

// FR01-B7: ô Email type="text", form gửi email sai định dạng đi mà không cảnh báo
await page.goto(`${WEB}/register`);
inputs = page.locator('form input');
const emailType = await inputs.nth(1).getAttribute('type');
await inputs.nth(0).fill('Nguyen Van A');
await inputs.nth(1).fill('fr01.b7example.com');
await inputs.nth(2).fill('Abcdef1 ');
await page.screenshot({ path: shot });
const sent = page.waitForResponse((r) => r.url().includes('/api/register'), { timeout: 3000 }).catch(() => null);
await page.locator('form button[type=submit]').click();
const res7 = await sent;
await evidence('FR01-B7.png', `FR01-B7 – Ô Email có type="${emailType}"; form gửi email "fr01.b7example.com" đi không cảnh báo`, [
  { req: 'Form Web gửi POST /api/register với email "fr01.b7example.com"', status: res7?.status() ?? 'không gửi', res: res7 ? await res7.text() : '' },
], shot);

// FR01-B3: trường bắt buộc rỗng vẫn được API chấp nhận
await evidence('FR01-B3.png', 'FR01-B3 – API chấp nhận Họ Tên / Email / Mật khẩu rỗng', [
  await register('', 'fr01.dt08@example.com', 'Abcdef1@'),
  await register('Nguyen Van A', '', 'Abcdef1@'),
  await register('Nguyen Van A', 'fr01.dt19@example.com', ''),
]);

// FR01-B4: email sai định dạng
const badEmails = ['fr01.dt11example.com', '@example.com', 'fr01.dt13@', 'fr01.dt14@example', 'fr01@dt15@example.com', 'fr01 dt16@example.com'];
const rows4 = [];
for (const e of badEmails) rows4.push(await register('Nguyen Van A', e, 'Abcdef1@'));
await evidence('FR01-B4.png', 'FR01-B4 – API chấp nhận email sai định dạng', rows4);

// FR01-B5: mật khẩu không đủ mạnh
const weak = ['@', 'Abcde1@', 'abcdef1@', 'ABCDEF1@', 'Abcdefg@', 'Abcdefg1', 'Abcdef1#', 'Abcdef1 ', '[bcdef1@'];
const rows5 = [];
for (const [i, p] of weak.entries()) rows5.push(await register('Nguyen Van A', `fr01.b5.${i}@example.com`, p));
await evidence('FR01-B5.png', 'FR01-B5 – API chấp nhận mật khẩu không đủ mạnh', rows5);

// FR01-B6: email trùng
const rows6 = [await register('Nguyen Van B', 'test@eshop.com', 'Newpass1@'), await register('Nguyen Van C', 'TEST@eshop.com', 'Newpass1@')];
for (const pw of ['Test1234!', 'Newpass1@']) {
  const r = await post('/login', { email: 'test@eshop.com', password: pw });
  rows6.push({ req: `POST /api/login ${show({ email: 'test@eshop.com', password: pw })}`, status: r.status, res: JSON.stringify(r.body).slice(0, 80) });
}
await evidence('FR01-B6.png', 'FR01-B6 – API cho đăng ký email đã tồn tại (test@eshop.com); tài khoản trùng mới không đăng nhập được', rows6);

// FR01-B8: email không được bỏ khoảng trắng đầu/cuối
const rows8 = [await register('Nguyen Van A', ' fr01.b8@example.com ', 'Abcdef1@')];
const l8 = await post('/login', { email: 'fr01.b8@example.com', password: 'Abcdef1@' });
rows8.push({ req: `POST /api/login ${show({ email: 'fr01.b8@example.com', password: 'Abcdef1@' })}`, status: l8.status, res: JSON.stringify(l8.body).slice(0, 80) });
await evidence('FR01-B8.png', 'FR01-B8 – Email được lưu kèm khoảng trắng; đăng nhập bằng email bình thường thất bại', rows8);

// FR01-B9: Họ Tên chỉ gồm khoảng trắng
await evidence('FR01-B9.png', 'FR01-B9 – API chấp nhận Họ Tên chỉ gồm khoảng trắng', [await register('   ', 'fr01.dt09@example.com', 'Abcdef1@')]);

// Danh sách người dùng trên Web Admin sau khi tái hiện
await page.goto(ADMIN);
await page.getByRole('textbox', { name: 'Email' }).fill('admin@eshop.com');
await page.getByRole('textbox', { name: 'Password' }).fill('Admin123!');
await page.getByRole('button', { name: 'Login' }).click();
await page.getByText('Người dùng', { exact: true }).click();
await page.setViewportSize({ width: 1100, height: 2200 }); // bảng nằm trong vùng cuộn riêng
await page.waitForTimeout(800);
await page.screenshot({ path: join(OUT, 'FR01-admin-users.png'), fullPage: true });
console.log('FR01-admin-users.png');

await browser.close();
const { unlinkSync } = await import('node:fs');
unlinkSync(shot);
