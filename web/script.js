import { WebSV } from "/api.js";

var websv = new WebSV("http://localhost:6969");

const image_input = document.querySelector("#image_input");
var uploaded_image = "";

function append_image(images)
{
	const div = document.getElementById("image");
	for (let i = 0; i < images.length; i++)
	{
		const img = document.createElement("img");
		img.src = "image/" + images[i];
		div.appendChild(img);
	}
}


async function upload(images)
{
	var img_ids = await websv.upload_image(images);
	console.log(img_ids);
	append_image(img_ids);
}

image_input.addEventListener("change", function(){
	var images = [];
	var len = this.files.length
	for (let i = 0; i < len; i++)
	{
		var reader = new FileReader();  
		reader.onload = function(e) {
			var bin = e.target.result;
			images.push(bin);
			if (images.length == len) upload(images);
		}
		reader.readAsDataURL(this.files[i]);
	}
})

const submit = document.querySelector("#submit");
submit.addEventListener("click", async function() {
	var content_t = ["this is a content", "this is another content"];	
	var res = await websv.upload("st0rm2", "physics2","can anyone help me solve this","science2",content_t);
	console.log(res);
})
