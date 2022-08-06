from .config   import *
from .util     import *
from .database import *


# Parser
class HTTP_Parser:
	def parse(self, http: str) -> dict:
		request = {}

		lines = http.split("\r\n\r\n")
		meta_lines = lines[0]
		payload    = lines[1]

		# Parsing the first line 
		meta_lines = meta_lines.split("\r\n")
		cmd_line = meta_lines.pop(0)
		cmd_line = cmd_line.split(" ")
		request.update({"request": cmd_line[0]})
		request.update({"path": cmd_line[1]})

		# Parsing meta data 
		for meta in meta_lines:
			key, val = meta.split(": ")
			request.update({key: val})

		# Adding the payload
		if payload:
			payload = json.loads(payload)
			request.update({"payload": payload})

		return request


# Engine
class Request_Engine:
	def __init__(self):
		self.database = Database()

	def __get_error_html(self, error: str) -> str:
		html = f"""
			<html>
			<body>
				<h1>{error}</h1>
			</body>
			</html>
		"""
		return html

	def __load_img(self, req: dict) -> dict:
		# Searching for images
		img_regex = re.search(r"\{{([A-Za-z0-9_.]+)\}}", req["payload"])

		# If image exists
		if img_regex:
			img_name = img_regex.group(1)

			# Loading image as base64
			with open(f"{WEB_DIR}/{img_name}", "rb") as f:
				img_data = base64.b64encode(f.read()).decode("utf-8")

			# Replace in the html
			req["payload"] = req["payload"].replace(img_regex.group(0), img_data)
			req.update({"Content-Length": len(req["payload"])})

		return req

	def __make_str(self, req: dict) -> str:
		# Converts json request to string
		http_res = ""
		head    = req.pop("head") + "\r\n"
		payload = req.pop("payload")

		http_res += head
		for key in req:
			http_res += f"{key}: {req[key]}\r\n"

		http_res += f"\r\n{payload}\r\n"
		return http_res

	# Request handlers
	def __get_handler(self, req: dict, ret_req: dict):
		# Opening the root file
		if req["path"] == "/":
			try:
				with open(f"{WEB_DIR}/{ROOT_FILE}", "r") as f:
					ret_req.update({"payload": f.read()})
				ret_req.update({"head": "HTTP/1.1 200 OK"})
				ret_req.update({"Content-Type": "text/html"})
				ret_req.update({"Content-Length": len(ret_req["payload"])})
			except Exception as e:
				ret_req.update({"payload": self.__get_error_html(e)})
				ret_req.update({"head": f"HTTP/1.1 500 Failed to open {ROOT_FILE}"})
		else:
			path = req["path"]
			try:
				# Extracting the extension
				ext = path.split(".")[-1]
				with open(f"{WEB_DIR}{path}", "r") as f:
					ret_req.update({"payload": f.read()})
					ret_req.update({"Content-Length": len(ret_req["payload"])})
				ret_req.update({"head": "HTTP/1.1 200 OK"})

				# Adding extra tags
				if ext == "css":
					ret_req.update({"Content-Type": "text/css"})
				elif ext == "html":
					ret_req.update({"Content-Type": "text/html"})
				elif ext == "js":
					ret_req.update({"Content-Type": "text/js"})

			except Exception as e:
				# If failed to open the sugessted file
				ret_req.update({"payload": self.__get_error_html(f"Unknown endpoint {path}")})
				ret_req.update({"head": f"HTTP/1.1 500 Unknown endpoint"})
				server_error(e)

		ret_req = self.__load_img(ret_req)

	def __post_handler(self, req: dict, ret_req: dict):
		payload = req["payload"]

		server_sucess(f"Payload received")
		server_warning(f"{payload}")

		qry = Query(payload["cmd"], payload["payload"])
		res = self.database.query(qry)

		ret_req.update({"head": f"HTTP/1.1 {res.status}"})
		ret_req.update({"Content-Type": res.content_type})
		ret_req.update({"Content-Length": res.content_len})
		ret_req.update({"payload": res.payload})

	def parse(self, req: dict) -> str:
		ret_req = {}

		# Get request handler
		if req["request"] == GET:
			self.__get_handler(req, ret_req)
		elif req["request"] == POST:
			self.__post_handler(req, ret_req)
		else:
			_req = req["request"]
			ret_req.update({"payload": self.__get_error_html(f"Unknown request {_req}")})
			ret_req.update({"head": f"HTTP/1.1 500 Unknown request"})

		return self.__make_str(ret_req)

