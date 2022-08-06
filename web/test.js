async function submit() {
	var url = "127.0.0.1:6969";

	var data = `{
		"cmd": "create object person",
		"payload": {}
	}`;
	
	let obj;
	const res = await fetch(url, {method: 'POST', body: data})
	obj = await res.json();
	console.log(obj)
}


async function new_object() {
	var url = "127.0.0.1:6969";
	var data = `{
		"cmd": "create object new_person",
		"payload": {}
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

async function new_entry() {
	var url = "127.0.0.1:6969";

	var data = `{
		"cmd": "create entry ram in person",
		"payload": {}
	}`;

	let obj;
	const res = await fetch(url, {method: 'POST', body: data})
	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}

async function update_entry() {
	var url = "127.0.0.1:6969";

	var data = `{
		"cmd": "update entry ram in person",
		"payload": {
			"age": 40,
			"status": "employed"
		}
	}`;

	let obj;
	const res = await fetch(url, {method: 'POST', body: data})
	obj = await res.text();
	obj = obj.replace(/["']/g, "\"");
	obj = JSON.parse(obj);
	console.log(obj);
}
