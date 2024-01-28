/**
 * @license
 * Copyright 2017 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome', headless: false });
    const page = await browser.newPage();
    await page.goto('https://www.mixamo.com/#/?page=1');

    // Query for an element handle.
    const element = await page.waitForSelector('.jumbotron .home2__hero__buttons > button:last-child');

    // Do something with element...
    await element.click();

    // Dispose of handle
    await element.dispose();

    await page.focus('input[type="email"]')
    await page.keyboard.type('badapplesweetie@gmail.com1')

    // await page.locator('input[type="email"]').fill('badapplesweetie@gmail.com');

    const submit_btn = await page.waitForSelector('#EmailForm .EmailPage__submit .ta-right > button');

    // console.log(submit_btn);

    await submit_btn.click();

    await submit_btn.dispose();

    await page.screenshot({ path: 'example.png' });
    // await browser.close();

    // 2dee24f8-3b49-48af-b735-c6377509eaac
})();