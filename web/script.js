import { web_sv } from "/api.js";

const image_input = document.querySelector("#image_input");
var uploaded_image = "";

image_input.addEventListener("change", function(){
	const reader = new FileReader();
	reader.addEventListener("load", () => {
		uploaded_image = reader.result;

		var file = this.files[0];
		var size = file.size;
		var type = file.type;
		var data = uploaded_image;

		// TODO: Implement image transfer
		var content = [data];
		var websv = new web_sv("http://localhost:50500/");
		websv.upload("st0rm", "asdF", "Asdf", "asd", content);
		
	});
	reader.readAsDataURL(this.files[0]);
})
