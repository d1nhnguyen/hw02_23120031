// Chạy test case FR-10 trên Web Admin (P-WEB-ADMIN) và Web khách hàng (P-WEB-USER), dùng Chrome hệ thống.
// Bộ dữ liệu được dựng lại trước mỗi test case bằng fixture.py. Không chạy song song với run_api.py.
//   node fr10/run_web.mjs   ·   ONLY=FR10-DT-01 node fr10/run_web.mjs
// Kết quả: evidence/FR-10/web_results.json + ảnh evidence/FR-10/web/<ID>.png
import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const EVIDENCE = join(HERE, '..', '..', 'evidence', 'FR-10');
const ADMIN = 'http://localhost:5174';
const WEB = 'http://localhost:5173';
const API = 'http://localhost:3000/api';
const ONLY = process.env.ONLY ? process.env.ONLY.split(',') : null;
const LABEL = { pending: 'Chờ xác nhận', confirmed: 'Đã xác nhận', shipping: 'Đang giao', delivered: 'Đã giao', canceled: 'Đã hủy' };
const ADMIN_BUTTONS = { pending: ['Xác nhận', 'Hủy'], confirmed: ['Giao hàng', 'Hủy'], shipping: ['Hoàn thành'], delivered: [], canceled: [] };
const USER_BUTTONS = { pending: ['Hủy đơn'], confirmed: ['Hủy đơn'], shipping: [], delivered: [], canceled: [] };
// Nút trên Web Admin dùng cho từng cặp (trạng thái hiện tại, trạng thái đích)
const BUTTON = { 'pending>confirmed': 'Xác nhận', 'confirmed>shipping': 'Giao hàng', 'shipping>delivered': 'Hoàn thành',
  'pending>canceled': 'Hủy', 'confirmed>canceled': 'Hủy', 'canceled>delivered': 'Đánh dấu Đã giao' };
const FIXTURE_STATES = { 1: 'pending', 2: 'confirmed', 3: 'shipping', 4: 'delivered', 5: 'canceled' };
mkdirSync(join(EVIDENCE, 'web'), { recursive: true });

const cases = JSON.parse(readFileSync(join(HERE, 'cases.json'), 'utf8'))
  .filter((c) => c.channels.includes('web') && (!ONLY || ONLY.includes(c.id)));
const browser = await chromium.launch({ channel: 'chrome' });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await context.newPage();
const dialogs = [];
page.on('dialog', async (d) => { dialogs.push(d.message()); await d.accept(); });

async function statuses() {
  const admin = await (await page.request.post(`${API}/login`, { data: { email: 'admin@eshop.com', password: 'Admin123!' } })).json();
  const list = await (await page.request.get(`${API}/admin/orders`, { headers: { Authorization: `Bearer ${admin.token}` } })).json();
  return Object.fromEntries(list.map((o) => [o.id, o.status]));
}

async function openAdminOrders() {
  await page.goto(ADMIN);
  if (await page.getByRole('button', { name: 'Login' }).count()) {
    await page.getByRole('textbox', { name: 'Email' }).fill('admin@eshop.com');
    await page.getByRole('textbox', { name: 'Password' }).fill('Admin123!');
    await page.getByRole('button', { name: 'Login' }).click();
  }
  await page.getByText('Đơn hàng', { exact: true }).click();
  await page.locator('tbody tr').first().waitFor();
}

async function openUserOrders() {
  await page.goto(`${WEB}/login`);
  const inputs = page.locator('form input');
  if (await inputs.count()) {
    await inputs.nth(0).fill('test@eshop.com');
    await inputs.nth(1).fill('Test1234!');
    await page.locator('form button[type=submit]').click();
    await page.waitForTimeout(800);
  }
  await page.goto(`${WEB}/profile`);
  await page.getByText('Lịch sử đơn hàng').waitFor();
  await page.waitForTimeout(800);
}

// Tìm dòng theo ô mã đơn khớp chính xác "#<id>" (textContent của cả dòng nối liền các ô, vd "#110/20/2026…")
const rowOf = (id) => page.locator('tr').filter({ has: page.locator('td', { hasText: new RegExp(`^#${id}$`) }) });
const buttonsOf = async (id) => (await rowOf(id).locator('button').allInnerTexts()).map((b) => b.trim());

const results = [];
for (const c of cases) {
  let fx;
  try {
    fx = JSON.parse(execFileSync('python3', [join(HERE, 'fixture.py')], { cwd: HERE, stdio: ['ignore', 'pipe', 'ignore'] }).toString());
  } catch (e) {
    fx = { ok: false, problems: [String(e.stdout ?? e.message)] };
  }
  const r = { id: c.id, expect: c.expect };
  if (!fx.ok) {
    results.push({ ...r, verdict: 'Blocked', notes: fx.problems });
    console.log(`${c.id} -> Blocked ${fx.problems.join('; ')}`);
    continue;
  }
  const before = Object.fromEntries(Object.entries(fx.statuses).map(([k, v]) => [Number(k), v]));
  dialogs.length = 0;
  const notes = [];
  let ok;
  if (c.action === 'ui_admin' || c.action === 'ui_user') {
    if (c.action === 'ui_admin') await openAdminOrders(); else await openUserOrders();
    const expected = c.action === 'ui_admin' ? ADMIN_BUTTONS : USER_BUTTONS;
    r.buttons = {};
    for (const [id, state] of Object.entries(FIXTURE_STATES)) {
      const got = await buttonsOf(id);
      r.buttons[`#${id} ${LABEL[state]}`] = got;
      if (JSON.stringify(got) !== JSON.stringify(expected[state])) {
        notes.push(`#${id} ${LABEL[state]}: có [${got.join(', ') || 'không có'}], mong đợi [${expected[state].join(', ') || 'không có'}]`);
      }
    }
    ok = notes.length === 0;
  } else {
    const isAdmin = c.action === 'status';
    if (isAdmin) await openAdminOrders(); else await openUserOrders();
    const textBefore = await page.locator('body').innerText();
    const label = isAdmin ? BUTTON[`${c.from_state}>${c.status}`] : 'Hủy đơn';
    const button = rowOf(c.order).getByRole('button', { name: label, exact: true });
    r.button = label;
    if (!(await button.count())) {
      r.button_found = false;
      notes.push(`không có nút "${label}" ở đơn #${c.order}`);
    } else {
      r.button_found = true;
      const response = page.waitForResponse((res) => /\/orders\/\d+\/(status|cancel)/.test(res.url()), { timeout: 3000 }).catch(() => null);
      await button.click();
      const res = await response;
      await page.waitForTimeout(800);
      if (res) Object.assign(r, { status: res.status(), body: await res.text().catch(() => null) });
      const textAfter = await page.locator('body').innerText();
      r.messages = [...dialogs, ...textAfter.split('\n').map((l) => l.trim()).filter((l) => l && !textBefore.includes(l) && l.length < 200)];
    }
    const after = await statuses();
    const changed = Object.keys({ ...before, ...after }).map(Number).filter((id) => before[id] !== after[id]);
    r.changed = Object.fromEntries(changed.map((id) => [id, [before[id], after[id]]]));
    r.after = after[c.order];
    if (c.expect === 'accept') {
      ok = r.button_found && changed.length === 1 && changed[0] === c.order && after[c.order] === c.target_state;
    } else {
      // Từ chối: hoặc giao diện không cho thao tác (không có nút), hoặc có thông báo lỗi và trạng thái giữ nguyên
      ok = changed.length === 0 && (!r.button_found || (r.messages ?? []).length > 0);
      if (r.button_found) notes.push(`giao diện có nút "${label}" cho chuyển đổi không hợp lệ`);
    }
    for (const id of changed) {
      if (c.expect !== 'accept' || id !== c.order) notes.push(`đơn #${id} bị chuyển \`${before[id]}\` → \`${after[id]}\``);
    }
  }
  await page.screenshot({ path: join(EVIDENCE, 'web', `${c.id}.png`), fullPage: true });
  Object.assign(r, { verdict: ok ? 'Pass' : 'Fail', notes });
  results.push(r);
  console.log(`${c.id.padEnd(11)} ${c.action.padEnd(8)} #${String(c.order ?? '').padEnd(4)} -> ${r.verdict.padEnd(4)} ${(r.messages ?? []).join(' | ').slice(0, 60)} ${notes.join('; ').slice(0, 160)}`);
}
await browser.close();

const out = join(EVIDENCE, `web_results${ONLY ? `_${ONLY.join('_')}` : ''}.json`);
writeFileSync(out, JSON.stringify({ run_at: new Date().toISOString(), results }, null, 1));
const count = (v) => results.filter((x) => x.verdict === v).length;
console.log(`\n${results.length} test case: ${count('Pass')} Pass, ${count('Fail')} Fail, ${count('Blocked')} Blocked -> ${out}`);
