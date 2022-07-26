function submit() {
	var url = "127.0.0.1:6969";

	var xhr = new XMLHttpRequest();
	xhr.open("POST", url);
	
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	
	xhr.onreadystatechange = function () {
	   if (xhr.readyState === 4) {
	      console.log(xhr.status);
	      console.log(xhr.responseText);
	   }
	};

	var data = `{
		"cmd": "store",
		"val": ["This is a value"]
	}`;

	xhr.send(data);
}
