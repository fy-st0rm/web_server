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
		console.log(size);
		console.log(type);
		console.log(data);
	});
	reader.readAsDataURL(this.files[0]);
})
