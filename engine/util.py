from .config import *

# Terminal colors 
class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLACK = '\033[30m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Sucess, Error and warnings 
def server_sucess(msg):
	print(f"{Colors.GREEN}[SERVER SUCESS]: {msg}{Colors.DEFAULT}")

def server_error(msg):
	print(f"{Colors.RED}[SERVER ERROR]: {msg}{Colors.DEFAULT}")

def server_warning(msg):
	print(f"{Colors.YELLOW}[SERVER WARNING]: {msg}{Colors.DEFAULT}")



"""
Database query result is returned in the form of `Result` class.
"""

class Result:
	def __init__(self, status: str, content_type: str, payload: dict):
		self.status = status.encode(FORMAT)
		self.content_type = content_type.encode(FORMAT)
		self.payload = f"{payload}".encode(FORMAT)
		self.content_len = f"{len(str(payload))}".encode(FORMAT)
	
	def __str__(self):
		return f"Result (\n  status: {self.status}\n  content-type: {self.content_type}\n  content-length: {self.content_len}\n  payload: {self.payload}\n)"


"""
Database query is done using `Query` class.
"""

class Query:
	def __init__(self, cmd: str, payload: dict):
		self.cmd = cmd
		self.payload = payload

	def __str__(self) -> str:
		return f"Query (\n  cmd: {self.cmd}\n  payload: {self.payload}\n)"


