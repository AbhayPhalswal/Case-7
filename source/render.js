// usage: node render.js in.html out.pdf
const { chromium } = require('playwright');
(async () => {
  const [,, inp, out] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + inp, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  // report any page whose content overflows its fixed A4 box
  const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => ({ page: i + 1, scroll: p.scrollHeight, client: p.clientHeight, over: p.scrollHeight - p.clientHeight })));
  console.log(JSON.stringify(overflow));
  await page.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  await browser.close();
})();
