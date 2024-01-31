<script>
	/**
	 * load all animation fbx files, and send animation clip json to "http://localhost:2020"
	 * which is a nodejs server, where the json files will be saved
	 */
	import _ from "lodash";
	import axios from "axios";
	import { onDestroy, onMount } from "svelte";
	import * as THREE from "three";
	import ThreeScene from "../lib/ThreeScene";
	import { loadFBX, loadJSON } from "../utils/ropes";

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
			loadJSON(`/filenames.json`),
			loadFBX(`/fbx/x_bot.fbx`),
			loadJSON(`/180 Turn W_ Briefcase (1).json`),
		]).then(([filenames, xbot, test_anim]) => {
			anim_mixer = new THREE.AnimationMixer(xbot);

			threeScene.scene.add(xbot);

			(async () => {
				for (let i = 0; i < filenames.length; i++) {
					const filename = filenames[i];
					const fbx_model = await loadFBX(`/mixamo-fbx/${filename}`);

					const anim_json = fbx_model.animations[0].toJSON();

					const headers = {
						"Content-Type": "application/json",
					};

					const reponse = await axios.post(
						"http://localhost:2020",
						{ data: anim_json, name: filename.replace(".fbx", "") },
						headers,
					);

					console.log(reponse.data.message);

					// // console.log(fbx_model.animations[0]);
					// // const clip = fbx_model.animations[0]
					// const clip = THREE.AnimationClip.parse(anim_json);

					// anim_action = anim_mixer.clipAction(clip);

					// anim_action.reset();
					// anim_action.setLoop(THREE.LoopRepeat, 3);
					// // keep model at the position where it stops
					// anim_action.clampWhenFinished = true;
					// anim_action.enabled = true;
					// // anim_action.fadeIn(0.5);
					// anim_action.play();

					// break;
				}
			})();
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
