/*
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
*/

import { websv } from "/config.js";

/* Importing sv_url variable */
import { sv_url } from "/config.js";


/*post displayer stuff */
async function additems(title, description, date, data) {

	/* ---- MAIN DIV ---- */
	var posts = document.createElement("div");
	posts.className = "flex justify-center py-3";

	/* ---- SECONDARY DIV ---- */
	const post_div = document.createElement("div");
	post_div.className = "rounded-lg flex items-center shadow-2xl";
	post_div.style.cssText = "width: 90%; height: 100px; background-color: #383838;";

	/* ---- POST TITLE ---- */
	const  post_title = document.createElement("H1");
	post_title.className = "font-bold text-2xl pl-3 text-white";
	const title_text = document.createTextNode(title);
	post_title.appendChild(title_text);

	/* ---- POST DESCRIPTION ---- */
	const post_description = document.createElement("H4");
	post_description.className = "font-bold text-l pl-3";
	post_description.style.cssText = "color: grey;";
	const description_text = document.createTextNode(description.substr(0,10) + "..");
	post_description.appendChild(description_text);

	/* ---- VIEWMORE BUTTON ---- */
	const post_button = document.createElement("button");
	post_button.innerHTML = "view more";
	post_button.className = "text-white rounded-full text-md font-bold py-2 px-4";
	post_button.style.cssText = "position: absolute; right: 7%; background-color: #5c92ff;";

	// redirects to post page
	post_button.addEventListener("click", function () {
		window.location.replace(sv_url + "/" + data)
	})

	/* ---- DATE SECTION ---- */
	const  post_date = document.createElement("H4");
	post_date.className = "font-bold text-l pl-3 text-green-300";
	const date_text = document.createTextNode( "Date Added: "+ date);
	post_date.appendChild(date_text);

	/* ---- APPENDING STUFF ---- */
	post_div.appendChild(post_title);
	post_div.appendChild(post_description);
	post_div.appendChild(post_button);
	post_div.appendChild(post_date);
	posts.appendChild(post_div);
	document.body.appendChild(posts);
}


/* --- QUERY STUFF */
window.onload = async function WindowLoad(event)
{
	var res = await websv.query("query_by_amt", 5);
	res = res["data"];
	console.log(res);
	for (let i = 0; i < res.length; i++)
	{
		var res_2 = await websv.load(res[i]);
		additems(res_2["title"], res_2["description"], res_2["date"], res[i]);
	}
}

/* --- BASIC UPLOAD STUFF --- */
const upload = document.querySelector("#upload");
upload.addEventListener("click", async function() {
	var content_t = ["this is another content"];
	const title_data = document.getElementById("title").value;
	const discription_data = document.getElementById("description").value;
	var res = await websv.upload("st0rm", title_data, discription_data, "physics", content_t);
	console.log(res);
})


const load = document.querySelector("#load");
load.addEventListener("click", async function() {
	var res = await websv.load("27cf8433-bdb9-4ac3-8531-957d9e07da6f");
	console.log(res);
})

const query = document.querySelector("#query");
query.addEventListener("click", async function() {
	var res = await websv.query("query_by_amt", 5);
	res = res["data"];
	console.log(res);
	for (let i = 0; i < res.length; i++)
	{
		var res_2 = await websv.load(res[i]);
		console.log(res_2);
	}
	
})




