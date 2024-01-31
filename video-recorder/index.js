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

function get_longest_track (tracks) {
    let max_len = 0;
    let max_name = '';

    for (const v of tracks) {

        if (v.times.length > max_len) {
            max_len = v.times.length
            max_name = v.name
        }
    }

    return [max_name, max_len]
}

(async () => {

    // models to request
    const model_names = ['x_bot.fbx']

    const animation_dir = path.join('..', 'anim-player', 'public', 'anim-json')
    const animatiom_names = getFileNames(animation_dir)

    // const elevation = [60, 90, 120];
    // const azimuth = [0, 45, 90, 135, 180, 225, 270, 315];
    const elevation = [90];
    const azimuth = [0, 45, 90, 135, 180, 225, 270, 315];

    // sort `animatiom_names` alphabetically
    animatiom_names.sort()

    for (let model_name of model_names) {
        for (let anim_name of animatiom_names) {
            for (let elev of elevation) {

                const browser = await puppeteer.launch();

                const page = await browser.newPage();

                for (let azim of azimuth) {
                    // read the json file
                    const animation_data = JSON.parse(fs.readFileSync(path.join(animation_dir, anim_name), 'utf8'));

                    const folder_name = path.join('data', model_name, anim_name, elev + '', azim + '');

                    try {

                        if (!fs.existsSync(folder_name)) {
                            fs.mkdirSync(folder_name, { recursive: true });
                        }

                        // console.log(`Folder ${folder_name} created successfully`);
                    } catch (err) {
                        if (err.code === 'EEXIST') {
                            console.log('Folder already exists');
                        } else {
                            console.error('Error creating folder:', err);
                        }
                    }

                    const lengest_track = get_longest_track(animation_data.tracks);

                    let current_time_step = 0;

                    while (current_time_step < lengest_track[1]) {

                        const filename = path.join(folder_name, `${current_time_step}.png`);

                        // check if file already exists
                        if (fs.existsSync(filename)) {
                            console.log(`File ${filename} already exists`);
                            current_time_step++;
                            continue;
                        }

                        // request the animation at each time step
                        const url = `http://localhost:5173/${encodeURIComponent(model_name)}/${encodeURIComponent(anim_name)}/${encodeURIComponent(current_time_step)}/${encodeURIComponent(elev)}/${encodeURIComponent(azim)}`;

                        console.log(`Request to ${url}`);

                        await page.goto(url);

                        await page.waitForSelector('#done', { visible: true });

                        console.log(`Saving ${filename}`);

                        await page.screenshot({ path: filename });

                        // 20 frames per second
                        current_time_step += 3;
                    }

                }

                await browser.close();
            }

            break
        }
    }


})();