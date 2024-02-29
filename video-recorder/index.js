/**
 * @license
 * Copyright 2017 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');


let counter = 0;


(async () => {

    let browser = await puppeteer.launch();

    let page = await browser.newPage();

    const character_names = ['dors.glb'];

    for (const char of character_names) {

        for (const queue_num of [7]) {

            const queue_data = JSON.parse(fs.readFileSync(path.join('..', 'queues', `queue${queue_num}.json`), 'utf8'));

            for (const task of queue_data) {
                // console.log(task)

                const [anim_name, elev, azim, current_time_step] = task

                const folder_name = path.join('data', char, anim_name, elev + '', azim + '');

                const filename = path.join(folder_name, `${current_time_step}.jpg`);

                try {

                    if (!fs.existsSync(folder_name)) {
                        fs.mkdirSync(folder_name, { recursive: true });
                    }
                    // console.log(`Folder ${folder_name} created successfully`);
                } catch (err) {
                    console.error('Error creating folder:', err);
                }

                // check if file already exists
                if (fs.existsSync(filename)) {
                    console.log(`File ${filename} already exists`);
                    continue;
                }

                // request the animation at each time step
                const url = `http://localhost:5173/${encodeURIComponent(char)}/${encodeURIComponent(anim_name)}/${encodeURIComponent(current_time_step)}/${encodeURIComponent(elev)}/${encodeURIComponent(azim)}`;

                console.log(`Request to ${url}`);

                await page.goto(url);

                await page.waitForSelector('#done', { visible: true });

                console.log(`Saving ${filename}`);

                await page.screenshot({ path: filename });

                if (counter % 100 == 0) {
                    await browser.close();

                    browser = await puppeteer.launch();

                    page = await browser.newPage();
                }

                counter += 1;
            }
        }
    }

})();