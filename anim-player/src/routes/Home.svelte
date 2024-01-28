<script>
	import _ from "lodash";
	import { onDestroy, onMount } from "svelte";
	import * as THREE from "three";
	import ThreeScene from "../lib/ThreeScene";
	import { loadFBX, loadBVH } from "../utils/ropes";
	import * as SkeletonUtils from "three/addons/utils/SkeletonUtils.js";

	/** @type {HTMLCanvasElement} */
	let canvas;

	/** @type {ThreeScene} */
	let threeScene;

	/** @type {THREE.AnimationMixer} */
	let anim_mixer;
	/** @type {THREE.AnimationAction} */
	let anim_action;

	let animation_pointer = 0;

	const clock = new THREE.Clock();

	export let model;
	export let anim;

	function animate() {
		if (anim_mixer && anim_action) {
			anim_mixer.update(clock.getDelta());
		}

		// update physics world and threejs renderer
		threeScene.onFrameUpdate();

		animation_pointer = requestAnimationFrame(animate);
	}

	onMount(() => {
		threeScene = new ThreeScene(
			canvas,
			document.documentElement.clientWidth,
			document.documentElement.clientHeight,
		);

		// -100 is ground level
		threeScene.scene.position.set(0, -50, 0);

		Promise.all([
			loadFBX(`/fbx/${model}.fbx`),
			loadFBX(`/fbx-None-Keyframe-Reduction_2/${anim}.fbx`),
			loadFBX(`/fbx-unity-t-pose-non-reduct/${anim}.fbx`),
			loadBVH(`/bvh_t_pose/${anim}.bvh`),
		]).then(([fbx_model, fbx2, fbx1, bvh_data1]) => {
			console.log("fbx_model", fbx_model);

			// fbx1.children.push(fbx_model.children[1]);
			// fbx1.children.push(fbx_model.children[2]);

			fbx1.children[0].traverse((child) => {
				child.name = "mixamorig" + child.name;
				// console.log(child.name);
			});

			fbx_model.children[0] = fbx_model.children[0];

			console.log("fbx1", fbx1);

			console.log("fbx2", fbx2);

			anim_mixer = new THREE.AnimationMixer(fbx_model);
			// console.log(fbx_unity_anim);
			threeScene.scene.add(fbx_model);

			const clip = fbx1.animations[0];
			// const clip = fbx2.animations[0];

			// console.log(clip);
			// console.log(bvh_data1);
			const tracks = [];
			for (let i = 0; i < clip.tracks.length; i++) {
				// console.log(bvh_data.clip.tracks[i]);
				// if (clip.tracks[i].name.includes(".position")) {
				// 	// tracks.push(bvh_data.clip.tracks[i]);
				// } else {
				clip.tracks[i].name = "mixamorig" + clip.tracks[i].name;
				// const values = bvh_data.clip.tracks[i].values;
				// for (let j = 0; j < values.length; j += 4) {
				// 	// swap 0 and 2, 4 and 6, 8 and 10 and so on
				// 	// if (j % 4 === 0) {
				// 	const temp = values[j];
				// 	values[j] = values[j + 2];
				// 	values[j + 2] = temp;
				// 	// }
				// }
				// bvh_data.clip.tracks[i].values = values;
				tracks.push(clip.tracks[i]);
				// }
			}
			// console.log(tracks);
			clip.tracks = tracks;

			// console.log(bvh_data.clip.toJSON());
			// console.log(fbx_model.animations[0].toJSON());
			// anim_action = anim_mixer.clipAction(bvh_data.clip);
			// // anim_action = anim_mixer.clipAction(fbx_model.animations[0]);

			anim_action = anim_mixer.clipAction(clip);
			anim_action.reset();
			anim_action.setLoop(THREE.LoopRepeat);
			// keep model at the position where it stops
			anim_action.clampWhenFinished = true;
			anim_action.enabled = true;
			// anim_action.fadeIn(0.5);
			anim_action.play();
		});

		animate();
	});

	onDestroy(() => {
		// unsubscribe all stores
		cancelAnimationFrame(animation_pointer);

		threeScene.dispose();
	});
</script>

<section>
	<canvas bind:this={canvas} />
</section>

<style>
	canvas {
		/* this will only affect <canvas> elements in this component */
		z-index: -1;
		position: absolute;
		top: 0;
		left: 0;
		bottom: 0;
		right: 0;
	}
</style>
