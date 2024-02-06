<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
	import Loader from "./routes/Loader.svelte";
	import Camera from "./routes/Camera.svelte";
	import Glb from "./routes/Glb.svelte";
</script>

<Router>
	<div>
		<Route path="/:model/:anim/:step/:elevation/:azimuth" let:params>
			<Home
				model={params.model}
				anim={params.anim}
				step={params.step}
				elevation={params.elevation}
				azimuth={params.azimuth}
			/>
		</Route>
		<Route path="/" component={Loader} />
		<Route path="/glb" component={Glb} />
		<Route path="/camera" component={Camera} />
	</div>
</Router>
