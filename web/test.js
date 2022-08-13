class web_sv
{
	constructor(url)
	{
		this.url = url;
	}

	prase(content)
	{
		var content = content;		
		var content_temp = content.toString();
		var content = content_temp.replace(/,/g, '","');
		var content = '"' + content + '"';
		return content;
	}

	async  upload(user, title, description, category, content)
	{
		var user = user;
		var title = title;
		var description = description;
		var category = category;
		var content = content;

		var content = this.prase(content);

		var data = `{
			"cmd": "upload",
			"payload": {
				"user": "${user}",
				"title": "${title}",
				"description": "${description}",
				"category": "${category}",
				"content": [${content}]
			}
		}`;
		alert(data);
		let obj;
		const res = await fetch(this.url, {
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

	async load(title){
		var title = title;

		var data = `{
			"cmd": "load",
			"payload": {
				"title": "${title}"
			}
		}`;

		let obj;
		const res = await fetch(this.url, {
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

	async query(user, title, description, category, content)
	{
		var user = user;
		var title = title;
		var description = description;
		var category = category;
		var content = content;

		var content =  this.prase(content);

		var data = `{
			"cmd": "upload",
			"payload": {
				"user": "${user}",
				"title": "${title}",
				"description": "${description}",
				"category": "${category}",
				"content": [${content}]
			}
		}`;

		let obj;
		const res = await fetch(this.url, {
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

	async comment(to, from, content)
	{
		var to = to;
		var from = from;
		var content = content;

		var data = `{
			"cmd": "comment",
			"payload": {
				"to": "${to}",
				"from": "${from}",
				"content": "${content}"
			}
		}`;

		let obj;
		const res = await fetch(this.url, {
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
}

var web_svv;

//sets universal url on startup
window.onload =   function windowLoad()
{
	web_svv =  new web_sv("127.0.0.1:6969");
}

async function upload_t() {
	// test upload stuff
	var content_t = ["this is a content", "this is another content"];	
	web_svv.upload("st0rm2", "physics2","can anyone help me solve this","science2",content_t);
}

async function load_t(){
	// test  loading stuff
	web_svv.load("physics2");
}

async function query_t() {		
	var content_t = ["this is a content", "this is another content"];	
	web_svv.query("st0rm2", "physics2","can anyone help me yeah solve this","science2",content_t);
}

async function comment_t() {
	web_svv.comment("physics2", "FuNK", "you are gae");
}
