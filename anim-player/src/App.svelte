<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
	import Loader from "./routes/Loader.svelte";
</script>

<Router>
	<div>
		<Route path="/:model/:anim/:step" let:params>
			<Home model={params.model} anim={params.anim} step={params.step} />
		</Route>
		<Route path="/" component={Loader} />
	</div>
</Router>
