// Chụp trang GitHub issue (repo public, không cần đăng nhập) -> bugs/screenshots/BUG-NN_issue.png
// Dùng: node scripts/issue_shots.mjs '[{"bug":"BUG-15","url":"https://github.com/…/issues/15"}]'  (gọi từ github_issues.py fill --shots)
import { chromium } from 'playwright-core';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'bugs', 'screenshots');
const targets = JSON.parse(process.argv[2]);

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
for (const t of targets) {
  await page.goto(t.url, { waitUntil: 'networkidle' });
  await page.screenshot({ path: join(OUT, `${t.bug}_issue.png`), fullPage: true });
  console.log(`${t.bug}_issue.png`);
}
await browser.close();
