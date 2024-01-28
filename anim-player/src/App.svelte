<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
	import Loader from "./routes/Loader.svelte";
</script>

<Router>
	<div>
		<Route path="/:model/:anim" let:params>
			<Home model={params.model} anim={params.anim} />
		</Route>
		<Route path="/" component={Loader} />
	</div>
</Router>
