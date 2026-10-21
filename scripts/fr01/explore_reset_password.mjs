// Khảo sát hộp đen form Đặt lại mật khẩu (FR-03) với cùng bộ mật khẩu đã dùng cho FR01-B1 – để đối chiếu với BUG-01 của nhóm.
// Không có verdict (FR-03 ngoài phạm vi). Đổi mật khẩu test@eshop.com: chạy scripts/restart_backend.sh sau khi chạy.
// Dùng: node scripts/fr01/explore_reset_password.mjs > evidence/FR-01/explore_reset_password.json
import { chromium } from 'playwright-core';
const PWS = ['Abcdef1@', 'Abcdef1$', 'Abcdef1!', 'Abcdef1%', 'Abcdef1*', 'Abcdef1?', 'Abcdef1&', 'Abcdef1 ', 'Abcdefg1'];
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage();
const rows = [];
for (const pw of PWS) {
  await page.goto('http://localhost:5173/forgot-password');
  await page.locator('input').first().fill('test@eshop.com');
  await page.getByRole('button', { name: 'Lấy mã OTP' }).click();
  const otpBox = page.getByText(/Mã OTP của bạn là/);
  await otpBox.waitFor({ timeout: 5000 });
  const otp = (await otpBox.textContent()).match(/(\d+)/)[1];
  await page.locator('input:not([type=password])').first().fill(otp);
  await page.locator('input[type=password]').fill(pw);
  let dialog = null;
  page.once('dialog', async d => { dialog = d.message(); await d.accept(); });
  const before = await page.locator('body').innerText();
  await page.getByRole('button', { name: 'Đặt lại mật khẩu' }).click();
  await page.waitForTimeout(1200);
  const after = await page.locator('body').innerText();
  const newText = after.split('\n').filter(l => l.trim() && !before.includes(l)).join(' | ');
  rows.push({ password: pw, dialog, new_text: newText, url_after: page.url() });
}
await browser.close();
console.log(JSON.stringify({ run_at: new Date().toISOString(), page: 'http://localhost:5173/forgot-password', results: rows }, null, 1));
