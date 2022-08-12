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

	def __get_error_html(self, error: str) -> bytes:
		html = bytes(f"""
			<html>
			<body>
				<h1>{error}</h1>
			</body>
			</html>
		""", encoding=FORMAT)
		return html

	def __construct_bytes(self, req: dict) -> bytes:
		# Converts json request to string
		http_res = b""
		head    = req.pop(HEAD) + b"\r\n"
		payload = req.pop(PAYLOAD)

		http_res += head
		for key in req:
			http_res += key + b": " + req[key] + b"\r\n" 

		http_res += b"\r\n" + payload + b"\r\n"
		return http_res

	# Request handlers
	def __get_handler(self, req: dict) -> dict:
		ret_req	= {}

		if req["path"] == "/":
			try:
				with open(f"{WEB_DIR}/{ROOT_FILE}", "rb") as f:
					content = f.read()

				ret_req.update({PAYLOAD: content})
				ret_req.update({HEAD: b"HTTP/1.1 200 OK"})
				ret_req.update({CONTENT_TYPE: types["html"]})
				ret_req.update({CONTENT_LEN: f"{len(content)}".encode(FORMAT)})

			except Exception as e:
				ret_req.update({PAYLOAD: self.__get_error_html(e)})
				ret_req.update({HEAD: bytes(f"HTTP/1.1 500 Failed to open {ROOT_FILE}", encoding=FORMAT)})

		else:
			path = req["path"]

			try:
				ext = path.split(".")[-1]
				full_path = f"{WEB_DIR}{path}"
				if ext not in sup_types: raise Exception(f"Extension: {ext} is not supported yet.")

				with open(full_path, "rb") as f:
					content = f.read()

				ret_req.update({HEAD: b"HTTP/1.1 200 OK"})
				ret_req.update({PAYLOAD: content})
				ret_req.update({CONTENT_LEN: f"{os.path.getsize(full_path)}".encode(FORMAT)})
				ret_req.update({CONTENT_TYPE: types[ext]})

			except Exception as e:
				# If failed to open the sugessted file
				ret_req.update({PAYLOAD: self.__get_error_html(f"Unknown endpoint {path}")})
				ret_req.update({HEAD: b"HTTP/1.1 500 Unknown endpoint"})
				server_error(e)
		return ret_req

	def __post_handler(self, req: dict) -> dict:
		ret_req = {}
		payload = req["payload"]

		server_sucess(f"Payload received")
		server_warning(f"{payload}")

		qry = Query(payload["cmd"], payload["payload"])
		res = self.database.query(qry)

		ret_req.update({HEAD: f"HTTP/1.1 {res.status}".encode(FORMAT)})
		ret_req.update({CONTENT_TYPE: res.content_type})
		ret_req.update({CONTENT_LEN: res.content_len})
		ret_req.update({PAYLOAD: res.payload})

	def parse(self, req: dict) -> str:

		# Get request handler
		if req["request"] == GET:
			ret_req = self.__get_handler(req)
		elif req["request"] == POST:
			ret_req = self.__post_handler(req)
		else:
			_req = req["request"]
			ret_req.update({PAYLOAD: self.__get_error_html(f"Unknown request {_req}")})
			ret_req.update({HEAD: bytes(f"HTTP/1.1 500 Unknown request", encoding=FORMAT)})

		return self.__construct_bytes(ret_req)

