from server.server import *

if __name__ == "__main__":
	server = Server("127.0.0.1", 6969)
	server.start()
