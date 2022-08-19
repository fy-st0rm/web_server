from .req_engine import *

#TODO: Make this shit

class Server:
	def __init__(self, ip: str, port: int):
		self.ip = ip
		self.port = port
		self.running = True
		self.__create_sv()

		self.temp_buff = ""

		# Engine
		self.http_parser = HTTP_Parser()
		self.req_engine  = Request_Engine()

	def __create_sv(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			self.server.bind((self.ip, self.port))
		except Exception as e:
			server_error(f"Failed to start server.\nReason: {e}")
			quit()

	# Function to resolve incomplete request
	def __resolve(self, recv: str) -> bool:
		# Splits lines
		lines = recv.split("\r\n")
		meta_lines = lines[0]

		# Parsing the first line to get the request type
		meta_lines = meta_lines.split("\r\n")
		cmd_line = meta_lines.pop(0)
		cmd_line = cmd_line.split(" ")
		req = cmd_line[0]

		if req == POST:
			if len(recv) < HTTP_BUFF:
				self.temp_buff = recv
				return False
			else:
				self.temp_buff = ""

		return True

	def __conn_handler(self, conn: socket.socket):
		alive = True
		while alive:
			recv = conn.recv(RECV_BUFF).decode()
			if recv:
				if self.temp_buff:
					self.temp_buff += recv
					recv = self.temp_buff

				if not self.__resolve(recv):
					continue

				req = self.http_parser.parse(recv)
				res = self.req_engine.parse(req)
				conn.send(res)
			else:
				alive = False

		server_warning(f"{conn} Disconnected.")

	def start(self):
		server_sucess(f"Server has been started on addr {self.ip} {self.port}")

		self.server.listen()
		while self.running:
			conn, addr = self.server.accept()
			server_sucess(f"{addr} connected.")
			new_thread = threading.Thread(target = self.__conn_handler, args = (conn,))
			new_thread.start()

