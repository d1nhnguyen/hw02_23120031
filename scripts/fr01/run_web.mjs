// Chạy test case FR-01 trên giao diện Web (thủ tục P-WEB), dùng Chrome hệ thống.
// Yêu cầu: backend vừa khởi động lại, Web chạy ở http://localhost:5173, đã chạy `python3 cases.py`.
//   node fr01/run_web.mjs               lần chạy 1: dữ liệu đúng như thiết kế
//   node fr01/run_web.mjs --workaround  lần chạy 2 (khảo sát, không tính verdict): test case không nhắm vào mật khẩu,
//                                       mật khẩu thay "@" bằng dấu cách vì form Web chỉ nhận dấu cách là ký tự đặc biệt
// Kết quả: evidence/FR-01/web_results[_workaround].json + ảnh evidence/FR-01/web/<ID>[_wa].png
import { chromium } from 'playwright-core';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const EVIDENCE = join(HERE, '..', '..', 'evidence', 'FR-01');
const WEB = 'http://localhost:5173';
const API = 'http://localhost:3000/api';
const SEED_PASSWORD = 'Test1234!';
const WORKAROUND = process.argv.includes('--workaround');
const FIELDS = ['name', 'email', 'password', 'confirm'];
mkdirSync(join(EVIDENCE, 'web'), { recursive: true });

// Lý do từ chối suy ra từ câu thông báo (đặc tả không quy định câu chữ – A7)
function reasonOf(message) {
  const m = message.toLowerCase();
  if (/xác nhận|không khớp|confirm|match/.test(m)) return 'confirm';
  if (/tồn tại|đã được|đã sử dụng|exist|already|duplicate|unique/.test(m)) return 'dup';
  if (/mật khẩu|password/.test(m)) return 'password';
  if (/email/.test(m)) return 'email';
  if (/họ|tên|name/.test(m)) return 'name';
  return 'unknown';
}

let cases = JSON.parse(readFileSync(join(HERE, 'cases.json'), 'utf8')).filter((c) => c.channels.includes('web'));
if (WORKAROUND) {
  cases = cases.filter((c) => c.web_workaround_password)
    .map((c) => ({ ...c, password: c.web_workaround_password, confirm: c.web_workaround_confirm }));
}

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage();
const api = page.request;
const admin = await (await api.post(`${API}/login`, { data: { email: 'admin@eshop.com', password: 'Admin123!' } })).json();
const users = async () =>
  (await api.get(`${API}/admin/users`, { headers: { Authorization: `Bearer ${admin.token}` } })).json();
const login = async (email, password) => {
  const r = await api.post(`${API}/login`, { data: { email, password } });
  return r.status() === 200 && Boolean((await r.json().catch(() => ({}))).token);
};
const countEmail = async (email) =>
  (await users()).filter((u) => String(u.email ?? '').toLowerCase() === email.toLowerCase()).length;

const results = [];
for (const c of cases) {
  const stored = c.email.trim();
  const before = await countEmail(stored);

  // Bước 1–3: mở trang, nhập dữ liệu
  await page.goto(`${WEB}/register`);
  const inputs = page.locator('form input');
  const fields = await inputs.count();
  const textBefore = await page.locator('body').innerText();
  await inputs.nth(0).fill(c.name);
  await inputs.nth(1).fill(c.email);
  await inputs.nth(2).fill(c.password);
  const confirmField = fields >= 4;
  if (confirmField) await inputs.nth(3).fill(c.confirm);

  // Bước 4: bấm Đăng Ký, ghi nhận request, URL, thông báo
  const response = page.waitForResponse((r) => r.url().includes('/api/register'), { timeout: 3000 }).catch(() => null);
  await page.locator('form button[type=submit]').click();
  const res = await response;
  await page.waitForTimeout(800);
  const r = { id: c.id, expect: c.expect, target: c.target, password_used: c.password, confirm_field: confirmField };
  r.request_sent = Boolean(res);
  if (res) Object.assign(r, { status: res.status(), body: await res.text().catch(() => null) });
  r.url_after = page.url().replace(WEB, '');
  r.messages = [];
  // Chỉ đọc thông báo khi còn ở trang Đăng ký (sau khi chuyển trang, các ô là của form Đăng nhập)
  if (r.url_after.startsWith('/register')) {
    const native = await inputs.evaluateAll((els) => els.map((e) => e.validationMessage));
    r.messages = native.flatMap((msg, i) => (msg ? [{ source: `native:${FIELDS[i]}`, text: msg, reason: FIELDS[i] }] : []));
    const textAfter = await page.locator('body').innerText();
    for (const line of textAfter.split('\n').map((l) => l.trim()).filter((l) => l && !textBefore.includes(l))) {
      r.messages.push({ source: 'page', text: line, reason: reasonOf(line) });
    }
  }
  await page.screenshot({ path: join(EVIDENCE, 'web', `${c.id}${WORKAROUND ? '_wa' : ''}.png`) });

  // Bước 5: kiểm chứng tài khoản
  const after = await countEmail(stored);
  r.created = after > before;
  r.matching_accounts_after = after;
  const notes = [];
  const reasons = r.messages.map((m) => m.reason);
  // Lần chạy 1: test case không nhắm vào mật khẩu mà bị từ chối vì mật khẩu -> bị che, chưa đánh giá được
  const masked = !WORKAROUND && c.web_workaround_password && reasons.includes('password') && c.target !== 'password';
  let verdict;
  if (c.expect === 'accept') {
    r.login_ok = await login(stored, c.password);
    if (r.url_after.startsWith('/login') && r.created && r.login_ok) {
      verdict = 'Pass';
    } else if (masked) {
      verdict = 'Blocked';
      notes.push('bị chặn bởi lỗi mật khẩu hợp lệ bị báo "quá yếu"; xem lần chạy 2');
    } else {
      verdict = 'Fail';
    }
  } else {
    if (r.created || r.url_after.startsWith('/login')) {
      verdict = 'Fail';
      notes.push(c.duplicate_of ? 'email trùng vẫn được chấp nhận' : 'dữ liệu không hợp lệ vẫn được chấp nhận');
    } else if (reasons.length === 0) {
      verdict = 'Fail';
      notes.push('bị từ chối nhưng không có thông báo lỗi');
    } else if (reasons.includes(c.target)) {
      verdict = 'Pass';
    } else if (masked) {
      verdict = 'Blocked';
      notes.push('bị chặn bởi lỗi mật khẩu hợp lệ bị báo "quá yếu"; xem lần chạy 2');
    } else {
      verdict = 'Fail';
      notes.push(`lý do từ chối (${[...new Set(reasons)].join(', ')}) khác lý do mong đợi (${c.target})`);
    }
    if (c.duplicate_of) {
      r.seed_login_ok = await login(c.duplicate_of, SEED_PASSWORD);
      if (!r.seed_login_ok) {
        verdict = 'Fail';
        notes.push('tài khoản gốc không còn đăng nhập được');
      }
    }
  }
  if (c.target === 'confirm' && !confirmField) {
    verdict = 'Fail';
    notes.splice(0, notes.length, 'giao diện không có ô Xác nhận mật khẩu');
  }
  Object.assign(r, { verdict, notes });
  results.push(r);
  console.log(`${c.id.padEnd(6)} ${c.expect.padEnd(6)} req=${r.request_sent ? r.status : '-'} url=${r.url_after} created=${r.created} -> ${verdict.padEnd(7)} ${r.messages.map((m) => m.text).join(' | ').slice(0, 70)} ${notes.join('; ')}`);
}
await browser.close();

const out = join(EVIDENCE, `web_results${WORKAROUND ? '_workaround' : ''}.json`);
writeFileSync(out, JSON.stringify({ run_at: new Date().toISOString(), workaround: WORKAROUND, results }, null, 1));
const count = (v) => results.filter((r) => r.verdict === v).length;
console.log(`\n${results.length} test case: ${count('Pass')} Pass, ${count('Fail')} Fail, ${count('Blocked')} Blocked -> ${out}`);
