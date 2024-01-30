/**
 * @license
 * Copyright 2017 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

function getFileNames (directoryPath) {
    const files = [];
    const entries = fs.readdirSync(directoryPath);

    for (const entry of entries) {
        const fullPath = path.join(directoryPath, entry);
        const stats = fs.statSync(fullPath);

        if (stats.isFile()) {
            files.push(entry);
        } else if (stats.isDirectory()) {
            files.push(...getFileNames(fullPath)); // Recursively explore subdirectories
        }
    }

    return files;
}

(async () => {

    // models to request
    const model_names = ['x_bot.fbx']

    const animation_dir = path.join('..', 'anim-player', 'public', 'anim-json')
    const animatiom_names = getFileNames(animation_dir)


    const interval = 1 / 30


    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    for (let model_name of model_names) {
        for (let anim_name of animatiom_names) {
            // read the json file
            const animation_data = JSON.parse(fs.readFileSync(path.join(animation_dir, anim_name), 'utf8'));

            // calculate the total time steps
            // todo read this value from the json file. find the largest time step
            const total_time_steps = Math.ceil(animation_data.duration / interval)

            let current_time_step = 0

            // request the animation at each time step
            while (current_time_step < total_time_steps) {
                // request the animation
                const url = `http://localhost:5173/${encodeURIComponent(model_name)}/${encodeURIComponent(anim_name)}/${current_time_step}`

                await page.goto(url);


                await page.screenshot({ path: 'example.png' });

                current_time_step++
            }

            break
        }
    }

    await browser.close();
})();