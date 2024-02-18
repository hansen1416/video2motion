<script>
	import _ from "lodash";
	import { onDestroy, onMount } from "svelte";
	import * as THREE from "three";
	import ThreeScene from "../lib/ThreeScene";
	import { loadFBX, loadGLTF, loadJSON } from "../utils/ropes";

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

	let show_done = false;

	// model file name
	export let model;
	// animation file name
	export let anim;
	// animation step of the longest track
	export let step;

	export let azimuth;

	export let elevation;

	anim = decodeURIComponent(anim);

	// function animate() {
	// 	if (anim_mixer && anim_action) {
	// 		anim_mixer.update(clock.getDelta());
	// 	}

	// 	// update physics world and threejs renderer
	// 	threeScene.onFrameUpdate();

	// 	threeScene.followTarget(elevation, azimuth);

	// 	if (anim_played) {
	// 		show_done = true;
	// 	}

	// 	animation_pointer = requestAnimationFrame(animate);
	// }

	function get_longest_track(tracks) {
		let max_len = 0;
		let max_times = [];

		for (const v of tracks) {
			if (v.times.length > max_len) {
				max_len = v.times.length;
				max_times = v.times;
			}
		}

		return max_times;
	}

	onMount(() => {
		threeScene = new ThreeScene(
			canvas,
			document.documentElement.clientWidth,
			document.documentElement.clientHeight,
		);

		// -100 is ground level
		threeScene.scene.position.set(0, -150, 0);

		// check if model has ".fbx" in it
		let model_task = null;
		let model_type = "";

		if (model.indexOf(".fbx") !== -1) {
			model_task = loadFBX(`/fbx/${model}`);
			model_type = "fbx";
		} else if (model.indexOf(".glb") !== -1) {
			model_task = loadGLTF(`/glb/${model}`);
			model_type = "glb";
		}

		if (model_task === null) {
			throw new Error("Model file type not supported");
		}

		Promise.all([model_task, loadJSON(`/anim-json/${anim}`)]).then(
			([model_mesh, anim_data]) => {
				if (model_type === "glb") {
					model_mesh = model_mesh.scene.children[0];
				}

				model_mesh.name = "diva";

				anim_mixer = new THREE.AnimationMixer(model_mesh);
				// console.log(fbx_unity_anim);
				threeScene.scene.add(model_mesh);

				const clip = THREE.AnimationClip.parse(anim_data);

				anim_action = anim_mixer.clipAction(clip);
				anim_action.reset();
				anim_action.setLoop(THREE.LoopRepeat, 1);
				// keep model at the position where it stops
				anim_action.clampWhenFinished = true;
				anim_action.enabled = true;
				// anim_action.fadeIn(0.5);

				anim_action.paused = true;

				const max_times = get_longest_track(clip.tracks);

				const max_delta = max_times[step];

				anim_action.time = max_delta;

				anim_action.play();

				// 	if (anim_mixer && anim_action) {
				anim_mixer.update(clock.getDelta());
				// }

				// set camera position
				threeScene.followTarget(elevation, azimuth);

				// render the scene
				threeScene.onFrameUpdate();

				show_done = true;
			},
		);

		// animate();
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

{#if show_done}
	<div id="done">Done</div>
{/if}

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
