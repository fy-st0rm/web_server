from engine.req_engine import *

#TODO: Make this shit

class Server:
	def __init__(self, ip: str, port: int):
		self.ip = ip
		self.port = port
		self.running = True
		self.__create_sv()

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

	def __conn_handler(self, conn: socket.socket):
		alive = True
		while alive:
			recv = conn.recv(1024).decode()
			if recv:
				print(recv)
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

if __name__ == "__main__":
	server = Server("127.0.0.1", 6969)
	server.start()

