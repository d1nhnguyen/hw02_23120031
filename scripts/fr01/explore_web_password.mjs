// Khảo sát (exploratory): form /register phía Web chấp nhận những mật khẩu nào?
// Phần 1: mỗi mật khẩu = "Abcdef1" + 1 ký tự đặc biệt. Phần 2: các mật khẩu có dấu cách để mô tả quy tắc form đang áp dụng.
// Ghi nhận form có gửi request /api/register hay không (không gửi = form chặn với thông báo "Mật khẩu quá yếu!").
// Kết quả: evidence/FR-01/explore_web_password.json
import { chromium } from 'playwright-core';
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SPECIALS = [...'@$!%*?&', ...'#^-_.~+=/\\()[]{}<>|:;,\'"`', ' '];
const WITH_SPACE = ['Abcdef1@ ', 'Abc def1', ' Abcdef1', 'abcdef1 ', 'ABCDEF1 ', 'Abcdefg ', 'Abcde1 ', 'Abcd1 ', 'A1 ', '        '];
const PASSWORDS = [...SPECIALS.map((ch) => `Abcdef1${ch}`), ...WITH_SPACE];

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage();
const results = [];
for (const [i, password] of PASSWORDS.entries()) {
  await page.goto('http://localhost:5173/register');
  const inputs = page.locator('form input');
  await inputs.nth(0).fill('Khao Sat');
  await inputs.nth(1).fill(`fr01.explore${i}@example.com`);
  await inputs.nth(2).fill(password);
  const response = page.waitForResponse((r) => r.url().includes('/api/register'), { timeout: 2000 }).catch(() => null);
  await page.locator('form button[type=submit]').click();
  const res = await response;
  results.push({ password, request_sent: Boolean(res), status: res?.status() ?? null });
  console.log(`${JSON.stringify(password).padEnd(14)} gửi request=${res ? res.status() : 'không'}`);
}
await browser.close();
writeFileSync(join(HERE, '..', '..', 'evidence', 'FR-01', 'explore_web_password.json'), JSON.stringify(results, null, 1));
