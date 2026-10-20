// Tái hiện các bug FR-15 và chụp bằng chứng vào bugs/screenshots/.
// Yêu cầu: Web Admin (5174) đang chạy; script tự khởi động lại backend trước khi tái hiện.
// Mỗi bug có một "thẻ bằng chứng": request, response và sản phẩm được lưu (GET sau khi gửi), kèm ảnh giao diện nếu có.
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, unlinkSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const OUT = join(ROOT, 'bugs', 'screenshots');
const ADMIN = 'http://localhost:5174';
const API = 'http://localhost:3000/api';
mkdirSync(OUT, { recursive: true });
execFileSync(join(ROOT, 'scripts', 'restart_backend.sh'), { stdio: 'ignore' });

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const card = await browser.newPage({ viewport: { width: 1100, height: 400 } });
const api = page.request;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const shot = join(OUT, '_tmp.png');
const token = (await (await api.post(`${API}/login`, { data: { email: 'admin@eshop.com', password: 'Admin123!' } })).json()).token;
const auth = { Authorization: `Bearer ${token}` };
const short = (v) => (typeof v === 'string' && v.length > 40 ? `"${v.slice(0, 12)}…" (${v.length} ký tự)` : JSON.stringify(v));
const showBody = (b) => `{${Object.entries(b).filter(([k]) => ['name', 'price', 'category_id'].includes(k)).map(([k, v]) => `"${k}": ${short(v)}`).join(', ')}}`;

async function evidence(file, title, rows, image) {
  const img = image ? `<img src="data:image/png;base64,${readFileSync(image).toString('base64')}">` : '';
  const body = rows.map((r) => `<tr><td><pre>${esc(r.req)}</pre></td><td class="s${String(r.status)[0]}">${esc(r.status)}</td><td><pre>${esc(r.res)}</pre></td></tr>`).join('');
  await card.setContent(`<html><body style="font:14px sans-serif;margin:16px">
    <h3 style="margin:0 0 4px">${esc(title)}</h3>
    <div style="color:#555;margin-bottom:8px">Ghi nhận lúc ${new Date().toLocaleString('vi-VN')} · ${API} · token admin</div>
    ${rows.length ? `<table style="border-collapse:collapse;width:100%"><tr><th>Request</th><th>HTTP</th><th>Response · sản phẩm lưu trong hệ thống</th></tr>${body}</table>` : ''}
    ${img}
    <style>td,th{border:1px solid #bbb;padding:4px 6px;text-align:left;vertical-align:top}pre{margin:0;white-space:pre-wrap;word-break:break-all;font-size:12px}
    .s2{color:#b00;font-weight:bold}.s4{color:#070}img{margin-top:10px;border:1px solid #bbb;max-width:100%}</style></body></html>`);
  await card.screenshot({ path: join(OUT, file), fullPage: true });
  console.log(file);
}

// Đọc lại từ danh sách GET /api/products (endpoint Admin dùng); GET /api/products/:id thuộc FR-06
async function stored(id) {
  const p = (await (await api.get(`${API}/products`)).json()).find((x) => String(x.id) === String(id));
  if (!p) return `không có sản phẩm id ${id} trong GET /api/products`;
  return `lưu: name=${short(p.name)}, price=${JSON.stringify(p.price)}, category_id=${JSON.stringify(p.category_id)}`;
}

async function add(data) {
  const body = { description: 'Mô tả kiểm thử FR-15', imageUrl: 'https://placehold.co/300x300/png?text=FR15', ...data };
  const r = await api.post(`${API}/products`, { data: body, headers: auth });
  const res = await r.json();
  return { req: `POST /api/products ${showBody(body)}`, status: r.status(), res: `${JSON.stringify(res)}\n${res.id ? await stored(res.id) : ''}` };
}

async function edit(id, data) {
  const current = (await (await api.get(`${API}/products`)).json()).find((x) => String(x.id) === String(id)) ?? {};
  const body = { ...current, ...data };
  delete body.id;
  const r = await api.put(`${API}/products/${id}`, { data: body, headers: auth });
  return { req: `PUT /api/products/${id} ${showBody(body)}`, status: r.status(), res: `${await r.text()}\n${await stored(id)}` };
}

async function openProducts() {
  await page.goto(ADMIN);
  if (await page.getByRole('button', { name: 'Login' }).count()) {
    await page.getByRole('textbox', { name: 'Email' }).fill('admin@eshop.com');
    await page.getByRole('textbox', { name: 'Password' }).fill('Admin123!');
    await page.getByRole('button', { name: 'Login' }).click();
  }
  await page.getByText('Sản phẩm', { exact: true }).click();
  await page.locator('tbody tr').first().waitFor();
}

async function addViaWeb(name, price) {
  await openProducts();
  await page.getByPlaceholder('Tên sản phẩm').fill(name);
  await page.getByPlaceholder('Giá tiền').fill(price);
  await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
  await page.waitForTimeout(800);
  const rows = page.locator('tbody tr');
  await rows.last().scrollIntoViewIfNeeded();
  await page.screenshot({ path: shot });
}

// FR15-B1: Giá 0 / âm
await addViaWeb('Gia am tu Web Admin', '-50000');
await evidence('FR15-B1.png', 'FR15-B1 – Hệ thống lưu sản phẩm có Giá bằng 0 hoặc âm (Thêm và Sửa); ảnh: Web Admin sau khi lưu Giá -50000', [
  await add({ name: 'Sac nhanh USB-C 20W', price: 0, category_id: 3 }),
  await add({ name: 'Sac nhanh USB-C 20W', price: -50000, category_id: 3 }),
  await edit(2, { price: -1 }),
], shot);

// FR15-B2: Giá trống / không phải số
await evidence('FR15-B2.png', 'FR15-B2 – Hệ thống lưu sản phẩm khi thiếu Giá hoặc Giá không phải số', [
  await add({ name: 'Sac nhanh USB-C 20W', category_id: 3 }),
  await add({ name: 'Sac nhanh USB-C 20W', price: 'abc', category_id: 3 }),
  await edit(3, { price: 'abc' }),
]);

// FR15-B3: Tên > 255 ký tự
await evidence('FR15-B3.png', 'FR15-B3 – Hệ thống lưu Tên sản phẩm dài hơn 255 ký tự', [
  await add({ name: 'A'.repeat(256), price: 350000, category_id: 3 }),
  await add({ name: 'Ố'.repeat(256), price: 350000, category_id: 3 }),
  await edit(4, { name: 'B'.repeat(300) }),
]);

// FR15-B4: Tên rỗng / chỉ khoảng trắng
await addViaWeb('   ', '350000');
await evidence('FR15-B4.png', 'FR15-B4 – Hệ thống lưu Tên rỗng (API) hoặc chỉ gồm khoảng trắng (Web, API); ảnh: Web Admin sau khi lưu Tên "␣␣␣"', [
  await add({ name: '', price: 350000, category_id: 3 }),
  await add({ name: '   ', price: 350000, category_id: 3 }),
  await edit(5, { name: '' }),
], shot);

// FR15-B5: Danh mục không hợp lệ
await evidence('FR15-B5.png', 'FR15-B5 – Hệ thống lưu sản phẩm khi thiếu Danh mục hoặc Danh mục không có trong danh sách (1, 2, 3)', [
  await add({ name: 'Sac nhanh USB-C 20W', price: 350000 }),
  await add({ name: 'Sac nhanh USB-C 20W', price: 350000, category_id: 99 }),
  await add({ name: 'Sac nhanh USB-C 20W', price: 350000, category_id: 0 }),
  await add({ name: 'Sac nhanh USB-C 20W', price: 350000, category_id: 'abc' }),
  await edit(1, { category_id: 4 }),
]);

// FR15-B6: Sửa / Xóa sản phẩm không tồn tại
const rows6 = [];
for (const id of [9999, 0, 'abc']) {
  const r = await api.put(`${API}/products/${id}`, { data: { name: 'San pham sua thu', price: 1000000, category_id: 1 }, headers: auth });
  rows6.push({ req: `PUT /api/products/${id}`, status: r.status(), res: await r.text() });
}
for (const id of [9999, 0, 'abc']) {
  const r = await api.delete(`${API}/products/${id}`, { headers: auth });
  rows6.push({ req: `DELETE /api/products/${id}`, status: r.status(), res: await r.text() });
}
const count = (await (await api.get(`${API}/products`)).json()).length;
rows6.push({ req: 'GET /api/products', status: 200, res: `${count} sản phẩm (không có sản phẩm nào bị sửa / xóa bởi các request trên)` });
await evidence('FR15-B6.png', 'FR15-B6 – Sửa / Xóa sản phẩm không tồn tại vẫn trả 200 "Product updated" / "Product deleted" thay vì 404', rows6);

// Danh sách sản phẩm trên Web Admin sau khi tái hiện
await openProducts();
await page.setViewportSize({ width: 1280, height: 3000 });
await page.waitForTimeout(500);
await page.screenshot({ path: join(OUT, 'FR15-admin-products.png'), fullPage: true });
console.log('FR15-admin-products.png');

await browser.close();
unlinkSync(shot);
execFileSync(join(ROOT, 'scripts', 'restart_backend.sh'), { stdio: 'ignore' });
