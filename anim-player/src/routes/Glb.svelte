<script>
	import _ from "lodash";
	import { onDestroy, onMount } from "svelte";
	import * as THREE from "three";
	import ThreeScene from "../lib/ThreeScene";
	import { loadGLTF, loadJSON } from "../utils/ropes";

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
		threeScene.scene.position.set(0, -1, 0);

		Promise.all([
			loadGLTF(`/glb/dors.glb`),
			loadJSON(`/anim-json/Zombie Walk.json`),
		]).then(([glb_model, anim_data]) => {
			glb_model = glb_model.scene.children[0];

			glb_model.name = "diva";

			anim_mixer = new THREE.AnimationMixer(glb_model);
			// console.log(fbx_unity_anim);
			threeScene.scene.add(glb_model);

			const clip = THREE.AnimationClip.parse(anim_data);

			anim_action = anim_mixer.clipAction(clip);
			anim_action.reset();
			anim_action.setLoop(THREE.LoopRepeat);
			// keep model at the position where it stops
			anim_action.clampWhenFinished = true;
			anim_action.enabled = true;
			// anim_action.fadeIn(0.5);

			anim_action.paused = false;

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
