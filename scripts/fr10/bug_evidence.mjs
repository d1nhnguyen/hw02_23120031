// Tái hiện các bug FR-10 và chụp bằng chứng vào bugs/screenshots/.
// Yêu cầu: Web (5173), Web Admin (5174) đang chạy; bộ dữ liệu 7 đơn được dựng bằng fixture.py trước mỗi bug.
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, unlinkSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const OUT = join(ROOT, 'bugs', 'screenshots');
const API = 'http://localhost:3000/api';
mkdirSync(OUT, { recursive: true });
const fixture = () => execFileSync('python3', [join(HERE, 'fixture.py')], { cwd: HERE, stdio: ['ignore', 'pipe', 'ignore'] });

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 760 } });
const card = await browser.newPage({ viewport: { width: 1100, height: 400 } });
const api = page.request;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const shot = join(OUT, '_tmp.png');
const token = async (email, password) => (await (await api.post(`${API}/login`, { data: { email, password } })).json()).token;
const statusOf = async (adminToken, id) => (await (await api.get(`${API}/admin/orders`, { headers: { Authorization: `Bearer ${adminToken}` } })).json()).find((o) => o.id === id)?.status;

async function evidence(file, title, rows, image) {
  const img = image ? `<img src="data:image/png;base64,${readFileSync(image).toString('base64')}">` : '';
  const body = rows.map((r) => `<tr><td><pre>${esc(r.req)}</pre></td><td class="s${String(r.status)[0]}">${esc(r.status)}</td><td><pre>${esc(r.res)}</pre></td></tr>`).join('');
  await card.setContent(`<html><body style="font:14px sans-serif;margin:16px">
    <h3 style="margin:0 0 4px">${esc(title)}</h3>
    <div style="color:#555;margin-bottom:8px">Ghi nhận lúc ${new Date().toLocaleString('vi-VN')} · ${API}</div>
    <table style="border-collapse:collapse;width:100%"><tr><th>Request</th><th>HTTP</th><th>Response · trạng thái đơn sau đó</th></tr>${body}</table>
    ${img}
    <style>td,th{border:1px solid #bbb;padding:4px 6px;text-align:left;vertical-align:top}pre{margin:0;white-space:pre-wrap;word-break:break-all;font-size:12px}
    .s2{color:#b00;font-weight:bold}.s4{color:#070}img{margin-top:10px;border:1px solid #bbb;max-width:100%}</style></body></html>`);
  await card.screenshot({ path: join(OUT, file), fullPage: true });
  console.log(file);
}

// FR10-B1: đơn đã hủy chuyển được sang đã giao; Web Admin hiện nút "Đánh dấu Đã giao"
fixture();
await page.goto('http://localhost:5174');
if (await page.getByRole('button', { name: 'Login' }).count()) {
  await page.getByRole('textbox', { name: 'Email' }).fill('admin@eshop.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('Admin123!');
  await page.getByRole('button', { name: 'Login' }).click();
}
await page.getByText('Đơn hàng', { exact: true }).click();
await page.locator('tbody tr').first().waitFor();
await page.screenshot({ path: shot });
let admin = await token('admin@eshop.com', 'Admin123!');
let res = await api.put(`${API}/admin/orders/5/status`, { data: { status: 'delivered' }, headers: { Authorization: `Bearer ${admin}` } });
await evidence('FR10-B1.png', 'FR10-B1 – Đơn đã hủy (#5) chuyển được sang "delivered"; ảnh: Web Admin hiện nút "Đánh dấu Đã giao" ở đơn #5 "Đã hủy"', [
  { req: 'PUT /api/admin/orders/5/status {"status": "delivered"}  (đơn #5 đang "canceled")', status: res.status(), res: `${await res.text()}\ntrạng thái đơn #5 sau đó: ${await statusOf(admin, 5)}` },
], shot);

// FR10-B2: User hủy được đơn đang giao; trang Hồ sơ hiện nút "Hủy đơn"
fixture();
await page.goto('http://localhost:5173/login');
const inputs = page.locator('form input');
await inputs.nth(0).fill('test@eshop.com');
await inputs.nth(1).fill('Test1234!');
await page.locator('form button[type=submit]').click();
await page.waitForTimeout(800);
await page.goto('http://localhost:5173/profile');
await page.getByText('Lịch sử đơn hàng').waitFor();
await page.waitForTimeout(800);
await page.screenshot({ path: shot });
admin = await token('admin@eshop.com', 'Admin123!');
const user = await token('test@eshop.com', 'Test1234!');
res = await api.put(`${API}/orders/3/cancel`, { headers: { Authorization: `Bearer ${user}` } });
await evidence('FR10-B2.png', 'FR10-B2 – User hủy được đơn đang giao (#3); ảnh: trang Hồ sơ hiện nút "Hủy đơn" ở đơn #3 "Đang giao"', [
  { req: 'PUT /api/orders/3/cancel  (token test@eshop.com, đơn #3 đang "shipping")', status: res.status(), res: `${await res.text()}\ntrạng thái đơn #3 sau đó: ${await statusOf(admin, 3)}` },
], shot);

await browser.close();
unlinkSync(shot);
fixture();
