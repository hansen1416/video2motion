<script>
	import { onDestroy, onMount } from "svelte";
	import * as THREE from "three";
	import _ from "lodash";
	import ThreeScene from "../lib/ThreeScene";
	import Stats from "three/examples/jsm/libs/stats.module.js";
	import { invokeCamera } from "../utils/ropes";
	import PlayerController from "../lib/PlayerController";
	import PoseDetector from "../lib/PoseDetector";

	import { derived } from "svelte/store";
	import animation_queue from "../store/animationQueueStore";
	import animation_data from "../store/animationDataStore";
	import conversation from "../store/conversationStore";
	import { diva, shadow, scenery } from "../store/archetypeStore";

	/** @type {HTMLVideoElement} */
	let video;
	/** @type {HTMLCanvasElement} */
	let canvas;

	/** @type {ThreeScene} */
	let threeScene;
	/** @type {Stats} */
	let stats;

	/** @type {PoseDetector} */
	let poseDetector = new PoseDetector();
	/** @type {PlayerController} */
	let playerController = undefined;

	let capture_pose = false;
	let detector_ready = false;
	let show_video = false;
	let animation_pointer = 0;

	/** @type {THREE.AnimationMixer} */
	let diva_mixer;
	/** @type {THREE.AnimationAction} */
	let diva_action;

	const clock = new THREE.Clock();

	function animate() {
		if (diva_mixer && diva_action) {
			diva_mixer.update(clock.getDelta());
		}

		// update physics world and threejs renderer
		threeScene.onFrameUpdate(stats);

		if (detector_ready && capture_pose) {
			// todo try to run prediction asynchrously
			poseDetector.predict(video);
		}

		animation_pointer = requestAnimationFrame(animate);
	}

	onMount(() => {
		threeScene = new ThreeScene(
			canvas,
			document.documentElement.clientWidth,
			document.documentElement.clientHeight,
		);
		// -100 is ground level
		threeScene.scene.position.set(0, -100, 0);

		if (import.meta.env.DEV) {
			stats = new Stats();
			stats.showPanel(1);
			document.body.appendChild(stats.dom);
		}
		// initialize camera
		invokeCamera(video, () => {});
		// initialize pose detector
		Promise.all([poseDetector.init(poseCallback)]).then(([_]) => {
			detector_ready = true;
		});

		animate();
	});

	/**
	 *
	 * @param {Array<{x: number, y: number, z: number, visibility: number}>} keypoints3D
	 */
	function poseCallback(keypoints3D) {
		if (playerController) {
			playerController.applyPose2Bone(keypoints3D, true);
		}
	}

	const unsubscribe_scenery = scenery.subscribe((scenery) => {
		if (!threeScene) {
			return;
		}

		if (typeof scenery !== "object" || scenery.isObject3D !== true) {
			// scenery is not ready, do nothing
			return;
		}

		if (threeScene.scene.getObjectByName("scenery")) {
			// scenery is already in the scene, do nothing
			return;
		}

		scenery.name = "scenery";

		threeScene.scene.add(scenery);

		console.log("add scenery to scene");
	});

	const unsubscribe_diva = diva.subscribe((diva) => {
		if (!threeScene) {
			return;
		}

		if (typeof diva !== "object" || diva.isObject3D !== true) {
			// diva is not ready, do nothing
			return;
		}

		if (threeScene.scene.getObjectByName("diva")) {
			// diva is already in the scene, do nothing
			return;
		}

		diva.name = "diva";

		diva_mixer = new THREE.AnimationMixer(diva);

		diva_mixer.addEventListener("finished", (e) => {
			// when one animation finished, remove the first animation from queue
			// this will trigger the watch function on `animation_queue` below
			animation_queue.update((a_queue) => {
				return _.tail(a_queue);
			});
		});

		threeScene.scene.add(diva);
	});

	const unsubscribe_shadow = shadow.subscribe((shadow) => {
		if (!threeScene) {
			return;
		}

		if (typeof shadow !== "object" || shadow.isObject3D !== true) {
			// shadow is not ready, do nothing
			return;
		}

		if (threeScene.scene.getObjectByName("shadow")) {
			// shadow is already in the scene, do nothing
			return;
		}

		shadow.name = "shadow";

		playerController = new PlayerController(shadow);

		threeScene.scene.add(shadow);
	});

	// we need to watch both animation_queue and animation_data, make sure they both complete
	const _derived_queue_data = derived(
		[animation_queue, animation_data],
		([_animation_queue, _animation_data]) => {
			return [_animation_queue, _animation_data];
		},
	);

	/**
	 * watch animation_queue, when it changes,
	 * check all the resouces needed for the animation is ready
	 * check whether animation in play
	 * if no, play the first animation
	 * if yes, do nothing
	 */
	const unsubscribe_queue_data = _derived_queue_data.subscribe(
		([_animation_queue, _animation_data]) => {
			// when animation_queue and animation_data are both ready
			// we can start to play the animation
			if (
				!_animation_queue ||
				!_animation_data ||
				_animation_queue.length === 0
			) {
				// animation_queue or animation_data is not ready, do nothing
				return;
			}

			// another animation is playing, do nothing
			if (diva_action && diva_action.isRunning()) {
				return;
			}

			// diva is not ready, do nothing
			if (!diva_mixer) {
				return;
			}

			if (!threeScene) {
				return;
			}

			const animation_name = _animation_queue[0].name;
			const animation_repeat = _animation_queue[0].repeat;
			const animation_text = _animation_queue[0].text;

			if (!_animation_data[animation_name]) {
				// animation data is not ready, do nothing
				return;
			}

			// check is current animation item has a `message` field, if yes, render TextBubble component
			if (animation_text) {
				conversation.set([animation_text]);
			} else {
				conversation.set(null);
			}

			console.log(
				`start animation: ${animation_name}, repeat: ${animation_repeat}`,
			);

			diva_mixer.stopAllAction();

			// play the first animation in queue, the animation_data should be prepared before hand
			const animation_json = JSON.parse(_animation_data[animation_name]);

			const animation_clip = THREE.AnimationClip.parse(animation_json);

			diva_action = diva_mixer.clipAction(animation_clip);

			diva_action.reset();

			diva_action.setLoop(THREE.LoopRepeat, animation_repeat);

			// keep model at the position where it stops
			diva_action.clampWhenFinished = true;

			diva_action.enabled = true;

			// diva_action.fadeIn(0.5);

			diva_action.play();

			console.log("play animation", animation_name);
		},
	);

	/**
	 * Out of onMount, beforeUpdate, afterUpdate and onDestroy,
	 * this is the only one that runs inside a server-side component.
	 */
	onDestroy(() => {
		cancelAnimationFrame(animation_pointer);

		diva_mixer.stopAllAction();

		diva_mixer.removeEventListener("finished", () => {});

		threeScene.dispose();

		// unsubscribe all stores
		unsubscribe_scenery();
		unsubscribe_diva();
		unsubscribe_shadow();
		unsubscribe_queue_data();
	});
</script>

<!-- section is not needed, only for readablity -->
<section>
	<canvas bind:this={canvas} />

	<video
		bind:this={video}
		autoPlay={true}
		width={480 / 2}
		height={360 / 2}
		style="position: absolute; top:0; left: 0; display: {show_video
			? 'block'
			: 'none'}"
	>
		<track label="English" kind="captions" default />
	</video>

	<div class="controls">
		<div>
			<button
				on:click={() => {
					threeScene.resetControl();
				}}>Reset Control</button
			>
			<!-- 
			{#if show_video}
				<button
					on:click={() => {
						show_video = !show_video;
					}}>hide video</button
				>
			{:else}
				<button
					on:click={() => {
						show_video = !show_video;
					}}>show video</button
				>
			{/if} -->

			<button
				class={capture_pose ? "active" : ""}
				on:click={() => {
					capture_pose = !capture_pose;
				}}><img src="/svg/camera.svg" alt="Play" /></button
			>

			<button on:click={() => {}}>
				<img src="/svg/play.svg" alt="Camera" />
			</button>
		</div>
	</div>
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
