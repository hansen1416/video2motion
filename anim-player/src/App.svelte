<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
	import Loader from "./routes/Loader.svelte";
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
	</div>
</Router>
