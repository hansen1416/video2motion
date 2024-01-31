/**
 * @license
 * Copyright 2017 Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

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

    console.log(animatiom_names.length)

    // const elevation = [60, 90, 120];
    // const azimuth = [0, 45, 90, 135, 180, 225, 270, 315];
    const elevation = [90];
    const azimuth = [0, 90, 180, 270];

    // sort `animatiom_names` alphabetically
    animatiom_names.sort()

    let counter = 0;

    let queue_num = 0;

    let data = []

    for (let model_name of model_names) {
        for (let anim_name of animatiom_names) {
            for (let elev of elevation) {
                for (let azim of azimuth) {
                    // read the json file
                    const animation_data = JSON.parse(fs.readFileSync(path.join(animation_dir, anim_name), 'utf8'));

                    const lengest_track = get_longest_track(animation_data.tracks);

                    let current_time_step = 0;

                    while (current_time_step < lengest_track[1]) {

                        data.push([model_name, anim_name, elev, azim, current_time_step])

                        // 20 frames per second
                        current_time_step += 3;
                    }

                }
            }

            counter += 1;

            if (counter >= 300) {

                // save data to a local file named queue0.json
                fs.writeFileSync(path.join('queue', `queue${queue_num}.json`), JSON.stringify(data));

                queue_num += 1;

                counter = 0;

                data = [];
            }
        }
    }


})();