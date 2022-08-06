from .config import *
from .util   import *


#TODO: [ ] Write the cmd parser
#TODO: [ ] Create a handable object for cmds
#TODO: [ ] Patch it into a query


"""
Query Syntax:

CREATE OBJECT student

CREATE ENTRY ram IN student
payload = {}

UPDATE ENTRY ram IN student

"""

class Database:
	def __init__(self):
		self.root = os.path.expanduser("~")
		self.path = self.root + "/" + DATABASE_DIR

		self.__create_dir()
		self.memory = {}
	
	# Startups
	def __create_dir(self):
		if not os.path.exists(self.path):
			os.mkdir(self.path)
			server_sucess(f"Created new database directory: {self.path}")

	# Database handler
	def __handle_create(self, qry: Query) -> Result:
		# When creating a new object
		if qry.cmd["what"] == OBJECT:
			obj_name = qry.cmd["name"]
			path = self.path + "/" + obj_name + ".json"

			# If object already exists
			if os.path.exists(path):
				res = Result(status = "409 Conflicting object", content_type = "application/json", payload = {"log": f"Object with name `{obj_name}` already exists."})
				return res

			json.dump({}, open(path, "w"), indent=4)
			res = Result("200 OK", "application/json", {"log": f"Sucessfully created object `{obj_name}`"})
			return res


	# Database commands
	def query(self, qry: Query) -> Query:
		if qry.cmd["cmd"] == CREATE:
			return self.__handle_create(qry)
		elif qry.cmd["cmd"] == UPDATE:
			pass


