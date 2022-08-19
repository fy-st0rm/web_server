
export class WebSV
{
	constructor(url)
	{
		this.url = url;
		this.buff_sz = 40_000;
	}

	// Function to parse strings
	parse(content)
	{
		var content = content;
		var content_temp = content.toString();
		var content = content_temp.replace(/,/g, '","');
		var content = '"' + content + '"';
		return content;
	}

	// Convert string to json
	to_json(text)
	{
		let obj = text;
		obj = obj.replace(/["']/g, "\"");
		obj = JSON.parse(obj);
		return obj;
	}

	// Constructs chunks out of images of required sizes
	construct_chunks(data, sz)
	{
		// Calculates the padding needed
		var padd = sz - (data.length % sz);
		data = data.concat(" ".repeat(padd));

		const chunks = [];
		var amt = data.length / sz;
		var start = 0;
		
		// Generates the chunks
		for (let i = 0; i < amt; i++)
		{
			chunks.push(data.slice(start, start + sz));
			start += sz;
		}
		return [chunks, padd];
	}

	// Image sending functions
	async upload_image(images)
	{
		var img_ids = [];
		var sz = images.length;
		for (let i = 0; i < sz; i++)
		{
			var image = images[i];

			// Generating chunks for each images
			image = image.split(",")
			var data   = this.construct_chunks(image[1], this.buff_sz);
			var chunks = data[0];
			var padd   = data[1];
			var c_len  = chunks.length;

			// Circling through every chunk and sending it to the server
			for (let j = 0; j < c_len; j++) 
			{
				var stat = "continue";
				if (j == c_len - 1) stat = "end";

				// Creating a post request for image
				var payload = `{
					"status": "${stat}",
					"padding": "${padd}",
					"data": "${chunks[j]}"
				}`;

				var res = await fetch(this.url + "/image", {
					method: 'POST', 
					headers: {
						"Content-Type": "text/plain",
						"Accept": "application/json",
					},
					body: payload
				});

				let obj = this.to_json(await res.text());
				if ("id" in obj)
					img_ids.push(obj["id"]);
			}
		}
		return img_ids;
	}

	// Server interaction functions
	async send(data)
	{
		const res = await fetch(this.url + "/database", {
			method: 'POST', 
			headers: {
				"Content-Type": "text/plain",
				"Accept": "application/json"
			},
			body: data
		})
		let obj = this.to_json(await res.text());
		return obj;
	}

	async upload(user, title, description, category, content)
	{
		var user = user;
		var title = title;
		var description = description;
		var category = category;
		var content = content;

		var content = this.parse(content);

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
		let obj = this.send(data);
		return obj;
	}

	async load(title){
		var title = title;

		var data = `{
			"cmd": "load",
			"payload": {
				"title": "${title}"
			}
		}`;
		
		let obj = this.send(data);
		return obj;
	}

	async query(user, title, description, category, content)
	{
		var user = user;
		var title = title;
		var description = description;
		var category = category;
		var content = content;

		var content =  this.parse(content);

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

		let obj = this.send(data);
		return obj;
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

		let obj = this.send(data);
		return obj;
	}
}

