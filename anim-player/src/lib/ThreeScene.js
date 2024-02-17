import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { MathUtils } from "three/src/math/MathUtils.js";


const CAMERA_DISTANCE = 2;

const CameraOffset = new THREE.Vector3(0, 0.6, CAMERA_DISTANCE);


let instance;

/**
 * @class ThreeScene
 * @description
 * This class is a singleton, so we only have 1 threejs scene
 *
 * @property {THREE.Scene} scene
 * @property {THREE.PerspectiveCamera} camera
 * @property {THREE.WebGLRenderer} renderer
 * @property {OrbitControls} controls
 * @property {THREE.DirectionalLight} light
 * @property {THREE.Clock} clock
 *
 * @method onFrameUpdate
 * @method resetControl
 */
export default class ThreeScene {
	/**
	 *
	 * @param {HTMLCanvasElement} canvas
	 * @param {number} width
	 * @param {number} height
	 * @returns
	 */
	constructor(canvas, width, height) {
		// make it a singleton, so we only have 1 threejs scene
		if (instance) {
			return instance;
		}

		this.scene = new THREE.Scene();

		// this.scene.add(new THREE.AxesHelper(5));

		this.camera = new THREE.PerspectiveCamera(
			75,
			width / height,
			0.01,
			4000
		);
		// camera initial position
		this.camera.position.set(
			CameraOffset.x,
			CameraOffset.y,
			CameraOffset.z
		);

		this.camera.updateProjectionMatrix(); // update the camera's projection matrix

		// env light
		this.scene.add(new THREE.AmbientLight(0xffffff, 1));

		this.scene.background = new THREE.Color(0xcccccc);

		const direct_light = new THREE.DirectionalLight(0xffffff, 1);
		direct_light.position.set(0, 100, 100);
		direct_light.castShadow = true;

		direct_light.target = new THREE.Object3D();
		direct_light.target.position.set(0, 0, 0);

		this.scene.add(direct_light);
		this.scene.add(direct_light.target);

		// env fog
		// this.scene.fog = new THREE.Fog(0x000000, 50, 200);

		this.renderer = new THREE.WebGLRenderer({
			canvas: canvas,
			alpha: true,
			antialias: true,
		});

		this.renderer.shadowMap.enabled = true;
		// this.renderer.shadowMap.type = THREE.BasicShadowMap;
		this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
		this.renderer.toneMappingExposure = 0.5;

		this.controls = new OrbitControls(this.camera, canvas);

		// this.controls.minDistance = 150;
		// this.controls.maxDistance = 800;

		this.renderer.setSize(width, height);

		instance = this;
	}

	dispose () {
		// this.renderer.dispose();
		// this.renderer.forceContextLoss();
		// this.renderer.context = null;
		// this.renderer.domElement = null;
		// this.renderer = null;
	}

	onFrameUpdate (stats) {

		// this.followTarget(0, 270);

		// this.controls.update();

		this.renderer.render(this.scene, this.camera);

		if (stats) {
			stats.update();
		}
	}

	resetControl () {
		this.controls.reset();
	}

	followTarget (elevation = 0, azimuth = 0) {
		// NOTE Assuming the camera is direct child of the Scene
		const object_position = new THREE.Vector3();
		const diva = this.scene.getObjectByName("diva");

		if (!diva) {
			return;
		}

		diva.children[0].getWorldPosition(object_position)

		CameraOffset.x = Math.sin(MathUtils.degToRad(azimuth)) * CAMERA_DISTANCE;
		CameraOffset.y = Math.sin(MathUtils.degToRad(elevation)) * CAMERA_DISTANCE;
		CameraOffset.z = Math.cos(MathUtils.degToRad(azimuth)) * CAMERA_DISTANCE;

		const target_pos = new THREE.Vector3().addVectors(object_position, CameraOffset);

		this.camera.position.set(target_pos.x, target_pos.y, target_pos.z);

		this.camera.lookAt(object_position);
	}

	setCamera (target, elevation, azimuth) {
		// Create a Spherical object and assign it the internal values of OrbitControls.
		const spherical = new THREE.Spherical();

		// set Spherical position
		// spherical.position.set(position);


		// Set the new values on the Spherical object.
		spherical.radius = CAMERA_DISTANCE;
		spherical.phi = MathUtils.degToRad(elevation);
		spherical.theta = MathUtils.degToRad(azimuth);

		// Update the camera position.
		this.camera.position.setFromSpherical(spherical);

		this.camera.position.x += target.position.x;
		this.camera.position.y += target.position.y;

		this.camera.lookAt(target.position);
	}

	/**
	 * 
	loadFbx(url) {
		const fbxLoader = new FBXLoader();
		fbxLoader.load(
			url,
			(object) => {
				// object.traverse(function (child) {
				//     if ((child as THREE.Mesh).isMesh) {
				//         // (child as THREE.Mesh).material = material
				//         if ((child as THREE.Mesh).material) {
				//             ((child as THREE.Mesh).material as THREE.MeshBasicMaterial).transparent = false
				//         }
				//     }
				// })
				// object.scale.set(.01, .01, .01)

				// Create an AnimationMixer, and get the list of AnimationClip instances
				this.mixer = new THREE.AnimationMixer(object);

				this.mixer.clipAction(object.animations[0]).play();

				this.scene.add(object);

				// // console.log(object);

				// // const clips = mesh.animations;

				// mixer.clipAction(object.animations[0]);
			},
			(xhr) => {
				console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
			},
			(error) => {
				console.log(error);
			}
		);
	}
	
	unload(target:THREE.Object3D){
		target.removeFromParent();
		target.traverse((child:any) => {
			// disposing materials
			if (child.material && !child.material._isDisposed){
				// disposing textures
				for (const value of Object.values(child.material) as any[]){
					if (!value) continue;
					if (value.dispose && !value._isDisposed){
						value.dispose();
						value._isDisposed = true;
					}
				}
				child.material.dispose();
				child.material._isDisposed = true;
			}
			// disposing geometries
			if (child.geometry?.dispose && !child.geometry._isDisposed){
				child.geometry.dispose();
				child.geometry._isDisposed = true;
			}
		});
	}

	missing child.skeleton.boneTexture.dispose(); and you all set :+1:
	but if you never use skinned mesh, you can skip this.
	*/
}
