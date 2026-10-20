// Chạy test case FR-15 trên Web Admin (thủ tục P-WEB), dùng Chrome hệ thống. Backend được khởi động lại trước mỗi test case.
// Yêu cầu: Web Admin chạy ở http://localhost:5174, đã chạy `python3 cases.py`. Không chạy song song với run_api.py.
//   node fr15/run_web.mjs             ·   ONLY=FR15-DT-01 node fr15/run_web.mjs
// Kết quả: evidence/FR-15/web_results.json + ảnh evidence/FR-15/web/<ID>.png
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const EVIDENCE = join(ROOT, 'evidence', 'FR-15');
const ADMIN = 'http://localhost:5174';
const API = 'http://localhost:3000/api';
const MISSING = '__MISSING__';
const SEED_NAMES = { 1: 'iPhone 15 Pro Max', 2: 'Samsung Galaxy S24 Ultra', 3: 'MacBook Pro M3', 4: 'Tai nghe AirPods Pro 2', 5: 'Bàn phím cơ Keychron Q1' };
const EXTRA = { description: 'Mô tả kiểm thử FR-15', imageUrl: 'https://placehold.co/300x300/png?text=FR15' };
const ONLY = process.env.ONLY ? process.env.ONLY.split(',') : null;
mkdirSync(join(EVIDENCE, 'web'), { recursive: true });

// Lý do từ chối suy ra từ câu thông báo (đặc tả không quy định câu chữ – A6)
function reasonOf(message) {
  const m = message.toLowerCase();
  if (/không tìm thấy|không tồn tại|not found|not exist/.test(m)) return 'id';
  if (/danh mục|category/.test(m)) return 'category';
  if (/giá|price/.test(m)) return 'price';
  if (/tên|name/.test(m)) return 'name';
  return 'unknown';
}
const sameValue = (a, b) => (a === b) || (a !== null && b !== null && Number(a) === Number(b) && !Number.isNaN(Number(a)));
const matches = (p, c) => p.name === c.name && sameValue(p.price, c.price) && sameValue(p.category_id, c.category_id);
const describe = (p) => `Tên “${String(p.name).slice(0, 40)}${String(p.name).length > 40 ? '…' : ''}”, Giá ${p.price}, Danh mục ${p.category_id}`;

const cases = JSON.parse(readFileSync(join(HERE, 'cases.json'), 'utf8'))
  .filter((c) => c.channels.includes('web') && (!ONLY || ONLY.includes(c.id)));

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const dialogs = [];
page.on('dialog', async (d) => { dialogs.push(d.message()); await d.accept(); });

async function snapshot() {
  const list = await (await page.request.get(`${API}/products`)).json();
  return Object.fromEntries(list.map((p) => [p.id, { name: p.name, price: p.price, category_id: p.category_id, description: p.description, imageUrl: p.imageUrl }]));
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

async function fillForm(c) {
  const touch = (key) => !c.touch || c.touch.includes(key); // test case Sửa chỉ một ô: các ô khác giữ giá trị form điền sẵn
  if (touch('name')) await page.getByPlaceholder('Tên sản phẩm').fill(c.name);
  if (touch('price')) await page.getByPlaceholder('Giá tiền').fill(c.price === MISSING ? '' : String(c.price));
  if (touch('category_id')) await page.locator('select').selectOption(String(c.category_id));
  if (c.op === 'add') {
    await page.getByPlaceholder('URL Ảnh').fill(EXTRA.imageUrl);
    await page.getByPlaceholder('Mô tả').fill(EXTRA.description);
  }
}

const results = [];
for (const c of cases) {
  execFileSync(join(ROOT, 'scripts', 'restart_backend.sh'), { stdio: 'ignore' });
  await openProducts();
  const admin = await (await page.request.post(`${API}/login`, { data: { email: 'admin@eshop.com', password: 'Admin123!' } })).json();
  for (const [action, pid] of c.pre) {
    if (action === 'delete') await page.request.delete(`${API}/products/${pid}`, { headers: { Authorization: `Bearer ${admin.token}` } });
  }
  if (c.pre.length) await openProducts();
  const before = await snapshot();
  const textBefore = await page.locator('body').innerText();
  dialogs.length = 0;

  const response = page.waitForResponse((r) => /\/api\/products(\/|$)/.test(r.url()) && r.request().method() !== 'GET', { timeout: 3000 }).catch(() => null);
  if (c.op === 'add') {
    await fillForm(c);
    await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
  } else {
    const row = page.locator('tbody tr').filter({ hasText: SEED_NAMES[c.pid] });
    if (c.op === 'edit') {
      await row.getByRole('button', { name: 'Sửa' }).click();
      await fillForm(c);
      await page.getByRole('button', { name: 'Lưu sản phẩm' }).click();
    } else {
      await row.getByRole('button', { name: 'Xóa' }).click();
    }
  }
  const res = await response;
  await page.waitForTimeout(800);
  const r = { id: c.id, op: c.op, expect: c.expect, request_sent: Boolean(res) };
  if (res) Object.assign(r, { status: res.status(), body: await res.text().catch(() => null) });
  const messages = [];
  // Thông báo validation của trình duyệt chỉ có nghĩa khi form không gửi request
  // (sau khi lưu, form được xóa trắng nên ô Tên rỗng cũng báo "Please fill out this field.")
  for (const [placeholder, reason] of (res ? [] : [['Tên sản phẩm', 'name'], ['Giá tiền', 'price']])) {
    const msg = await page.getByPlaceholder(placeholder).evaluate((e) => e.validationMessage).catch(() => '');
    if (msg) messages.push({ source: 'native', text: msg, reason });
  }
  for (const d of dialogs) messages.push({ source: 'dialog', text: d, reason: reasonOf(d) });
  const textAfter = await page.locator('body').innerText();
  for (const line of textAfter.split('\n').map((l) => l.trim()).filter((l) => l && !textBefore.includes(l) && l.length < 200)) {
    const reason = reasonOf(line);
    if (reason !== 'unknown' || /lỗi|error|không hợp lệ|invalid|thất bại|fail/i.test(line)) messages.push({ source: 'page', text: line, reason });
  }
  r.messages = messages;
  if (c.check === 'html_display') {
    const cell = page.locator('tbody tr').filter({ hasText: 'Loa Bluetooth' }).locator('td').nth(1);
    r.displayed_name = (await cell.count()) ? await cell.innerText() : null;
  }
  await page.screenshot({ path: join(EVIDENCE, 'web', `${c.id}.png`), fullPage: true });

  // Kiểm chứng bằng ảnh chụp danh sách sản phẩm trước / sau
  const after = await snapshot();
  const added = Object.keys(after).filter((id) => !(id in before)).map(Number);
  const removed = Object.keys(before).filter((id) => !(id in after)).map(Number);
  const target = c.op === 'add' ? added[0] : c.pid;
  const othersChanged = Object.keys(before).map(Number)
    .filter((id) => id !== target && id in after && JSON.stringify(before[id]) !== JSON.stringify(after[id]));
  Object.assign(r, { added, removed, others_changed: othersChanged });
  const notes = [];
  let ok;
  if (c.expect === 'accept') {
    if (c.op === 'add') {
      ok = added.length === 1 && matches(after[added[0]], c) && !removed.length && !othersChanged.length;
      if (added.length) {
        r.stored = after[added[0]];
        if (!matches(after[added[0]], c)) notes.push(`lưu khác dữ liệu nhập: ${describe(after[added[0]])}`);
      } else notes.push('không tạo sản phẩm');
      if (c.check === 'html_display' && r.displayed_name !== c.name) {
        ok = false;
        notes.push(`danh sách hiển thị “${r.displayed_name}” thay vì nguyên văn`);
      }
    } else if (c.op === 'edit') {
      const stored = after[c.pid];
      r.stored = stored;
      ok = stored && matches(stored, c) && !othersChanged.length && !added.length;
      if (stored && !matches(stored, c)) notes.push(`lưu khác dữ liệu nhập: ${describe(stored)}`);
    } else {
      ok = removed.length === 1 && removed[0] === c.pid && !othersChanged.length;
      if (!removed.includes(c.pid)) notes.push('sản phẩm vẫn còn');
    }
    if (othersChanged.length) notes.push(`sản phẩm khác bị thay đổi: id ${othersChanged}`);
  } else {
    const unchanged = JSON.stringify(before) === JSON.stringify(after);
    const reasons = messages.map((m) => m.reason);
    ok = unchanged && reasons.includes(c.target);
    if (!unchanged) {
      if (added.length) { notes.push(`vẫn tạo sản phẩm: ${describe(after[added[0]])}`); r.stored = after[added[0]]; }
      if (c.op === 'edit' && JSON.stringify(before[c.pid]) !== JSON.stringify(after[c.pid])) {
        notes.push(`sản phẩm bị sửa thành: ${describe(after[c.pid])}`);
        r.stored = after[c.pid];
      }
      if (removed.length) notes.push(`sản phẩm bị xóa: id ${removed}`);
    } else if (!reasons.length) notes.push('không lưu nhưng không có thông báo lỗi');
    else if (!reasons.includes(c.target)) notes.push(`lý do từ chối (${[...new Set(reasons)].join(', ')}) khác lý do mong đợi (${c.target})`);
  }
  r.verdict = ok ? 'Pass' : 'Fail';
  r.notes = notes;
  results.push(r);
  console.log(`${c.id.padEnd(11)} ${c.op.padEnd(6)} ${c.expect.padEnd(8)} req=${r.request_sent ? r.status : '-'} -> ${r.verdict.padEnd(4)} ${messages.map((m) => m.text).join(' | ').slice(0, 70)} ${notes.join('; ').slice(0, 120)}`);
}
await browser.close();
execFileSync(join(ROOT, 'scripts', 'restart_backend.sh'), { stdio: 'ignore' });

const out = join(EVIDENCE, `web_results${ONLY ? `_${ONLY.join('_')}` : ''}.json`);
writeFileSync(out, JSON.stringify({ run_at: new Date().toISOString(), results }, null, 1));
const count = (v) => results.filter((r) => r.verdict === v).length;
console.log(`\n${results.length} test case: ${count('Pass')} Pass, ${count('Fail')} Fail -> ${out}`);
