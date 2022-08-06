
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


# Constants
CREATE = "create"
DELETE = "delete"
UPDATE = "update"
OBJECT = "object"
ENTRY  = "entry"
FROM   = "from"
IN     = "in"

PRIM_CMDS = [CREATE, DELETE, UPDATE]

"""
Database query result is returned in the form of `Result` class.
"""

class Result:
	def __init__(self, status: str, content_type: str, payload: dict):
		self.status = status
		self.content_type = content_type
		self.payload = payload
		self.content_len = len(str(payload))
	
	def __str__(self):
		return f"Result (\n  status: {self.status}\n  content-type: {self.content_type}\n  content-length: {self.content_len}\n  payload: {self.payload}\n)"


"""
Database query is done using `Query` class.
"""

class Query:
	def __init__(self, cmd: str, payload: dict):
		self.cmd = self.__parse_cmd(cmd)
		self.payload = payload

	def __parse_create(self, words: list) -> dict:
		res = {"cmd": CREATE}

		if len(words) < 3:
			server_error(f"`{words[0]}` command requires atleast 3 arguments.")
			return {}

		if words[1] not in [OBJECT, ENTRY]:
			server_error(f"Unknown `{words[1]}` to create.");
			return {}

		res.update({"what": words[1]})

		if words[1] == ENTRY:
			if len(words) < 5:
				server_error(f"Creating `{words[1]}` requires 3 arguments.")
				return {}

			if words[3] != IN:
				server_error(f"Expected `IN` got `{words[2]}`.")
				return {}

			res.update({"in": words[4]})

		res.update({"name": words[2]})
		return res

	def __parse_update(self, words: list) -> dict:
		res = {"cmd": UPDATE}

		if len(words) < 5:
			server_error(f"`{words[0]}` command requires atleast 5 arguments.")
			return {}

		if words[1] not in [ENTRY]:
			server_error(f"Unknown `{words[1]}` to update.");
			return {}

		res.update({"what": words[1]})
		res.update({"name": words[2]})

		if words[3] != IN:
			server_error(f"Expected `IN` keyword got `{words[3]}`.")
			return {}
		
		res.update({"in": words[4]})
		return res
	
	def __parse_cmd(self, cmd: str) -> dict:
		words = cmd.split(" ")

		# If the cmd didnt matched
		if words[0] not in PRIM_CMDS: 
			server_error(f"`{words[0]}` is not a valid command.")
			return {}

		# Parsing the cmds
		if words[0] == CREATE:
			return self.__parse_create(words)

		elif words[0] == UPDATE:
			return self.__parse_update(words)
		
		else:
			server_error(f"Unknown command `{words[0]}`.")
			return {};

	def __str__(self) -> str:
		return f"Query (\n  cmd: {self.cmd}\n  payload: {self.payload}\n)"


