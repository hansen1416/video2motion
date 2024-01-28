<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
</script>

<Router>
	<div>
		<Route path="/:model/:anim" let:params>
			<Home model={params.model} anim={params.anim} />
		</Route>
	</div>
</Router>
