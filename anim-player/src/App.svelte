<script>
	import { Router, Route } from "svelte-routing";
	import Home from "./routes/Home.svelte";
</script>

<Router>
	<div>
		<Route path="/:name" component={Home} />
	</div>
</Router>
