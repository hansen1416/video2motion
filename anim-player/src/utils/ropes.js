import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { FBXLoader } from "three/examples/jsm/loaders/FBXLoader.js";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js";
import { BVHLoader } from "three/examples/jsm/loaders/BVHLoader.js";
// import BVHLoader from "../lib/bvhloader.js";

export function loadBVH (url) {
    return new Promise((resolve) => {
        const loader = new BVHLoader();
        loader.load(url,
            (result) => resolve(result),
            (xhr) => {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            (error) => {
                console.log(error);
            });
    });
}

export function loadGLTF (url) {
    return new Promise((resolve) => {
        const loader = new GLTFLoader();
        loader.load(url, (gltf) => resolve(gltf));
    });
}

export function loadFBX (url) {
    return new Promise((resolve) => {
        const fbxLoader = new FBXLoader();
        fbxLoader.load(
            url,
            (object) => {
                resolve(object);
            },
            (xhr) => {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            (error) => {
                console.log(error);
            }
        );
    });
}

export function loadJSON (url) {
    return new Promise((resolve) => {
        fetch(url).then((response) => resolve(response.json()));
    });
}

export function loadObj (url) {
    return new Promise((resolve) => {
        const loader = new OBJLoader();
        loader.load(url, (fbx) => resolve(fbx));
    });
}