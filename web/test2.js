
async function upload() {
	var url = "127.0.0.1:6969";
	var data = `{
		"cmd": "upload",
		"payload": {
			"user": "st0rm",
			"title": "Dynamics",
			"description": "Notes of topic Dynamics",
			"category": "Physics",
			"content": []
		}
	}`;

	let obj;
	const res = await fetch(url, {
		method: 'POST', 
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		},
		body: data
	})

	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}

async function load() {
	var url = "127.0.0.1:6969";
	var data = `{
		"cmd": "load",
		"payload": {
			"title": "Dynamics"
		}
	}`;

	let obj;
	const res = await fetch(url, {
		method: 'POST', 
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		},
		body: data
	})

	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}

async function query() {
	var url = "127.0.0.1:6969";
	var data = `{
		"cmd": "upload",
		"payload": {
			"user": "st0rm",
			"title": "Dynamics",
			"description": "Notes of topic Dynamics",
			"category": "Physics",
			"content": []
		}
	}`;

	let obj;
	const res = await fetch(url, {
		method: 'POST', 
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		},
		body: data
	})

	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}

async function comment() {
	var url = "127.0.0.1:6969";
	var data = `{
		"cmd": "comment",
		"payload": {
			"to": "Dynamics",
			"from": "st0rm",
			"content": "Cool!"
		}
	}`;

	let obj;
	const res = await fetch(url, {
		method: 'POST', 
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		},
		body: data
	})

	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}
