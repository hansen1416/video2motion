/**
 * @license
 * Copyright 2017 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // url encode the animation name
    const anim_name = encodeURIComponent('Air Squat Bent Arms');

    console.log(anim_name)

    await page.goto(`http://localhost:5173/x_bot/${anim_name}`);

    // Wait for the animation to finish
    (async () => {
        for (let i = 0; i < 1000000000; i++) {

        }
    })()

    await page.screenshot({ path: 'example.png' });
    await browser.close();
})();