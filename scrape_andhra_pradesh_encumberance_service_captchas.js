// Scrape captchas from Andhra Pradesh Encumberance Service

const { chromium, firefox } = require('playwright');

(async () => {
  // const browser = await chromium.launch({
  //   executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  // });
  const browser = await chromium.launch({
    headless: false
  });

  const page = await browser.newPage();

  // await page.goto('https://rs.ap.gov.in/APCARDECClient/ecSearchByDocAuto.jsp?distcode=&distname=&srocode=&sroname=');
  await page.goto('https://rs.ap.gov.in/APCARDECClient/')

  const submitButton = await page.$('input[type="submit"]');;
  await submitButton.click();

  // const selectElement = await page.$('#docSel');
  // await selectElement.selectOption({ label: 'Document No ' });
  // await selectElement.click();
  // await page.getByText('Select', { exact: true }).click()
  // await page.locator('#docSel').click()
  await page.selectOption('select#docSel', '1');

  await page.getByPlaceholder("Enter the Doc/Memo No").click()
  sro_name = "DWARAKANAGAR (314)"
  await page.getByPlaceholder("Enter the SRO Name").type(sro_name)
  await page.getByPlaceholder("Enter the Doc/Memo No").type("1000")
  await page.getByPlaceholder("Enter the year(xxxx)").type("2021")

  // Close the browser
  // await browser.close();
})();
