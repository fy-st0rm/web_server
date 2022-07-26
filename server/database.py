from .config import *
from .util   import *


class Database:
	def __init__(self):
		self.root = os.path.expanduser("~")

		# Paths
		self.data_path     = self.root + "/" + DATABASE_DIR
		self.img_path      = WEB_DIR + "/" + IMG_DIR
		self.users_path    = self.data_path + "/" + USERS
		self.category_path = self.data_path + "/" + CATEGORY
		self.posts_path    = self.data_path + "/" + POSTS
		self.comments_path = self.data_path + "/" + COMMENTS

		# Memories
		self.users    = {}
		self.category = {}
		self.posts    = {}
		self.comments = {}

		# Startups
		self.__create_dir()
		self.__create_objects()
		self.__load_database()

	# Startups
	def __create_dir(self):
		if not os.path.exists(self.data_path):
			os.mkdir(self.data_path)
			server_sucess(f"Created new database directory: {self.data_path}")

		if not os.path.exists(self.img_path):
			os.mkdir(self.img_path)
			server_sucess(f"Created new image database directory: {self.img_path}")
	
	def __create_objects(self):
		if not os.path.exists(self.users_path):
			json.dump(self.users, open(self.users_path, "w"))
			server_sucess(f"Created new objects `{USERS}` on database directory: {self.data_path}.")

		if not os.path.exists(self.category_path):
			json.dump(self.category, open(self.category_path, "w"))
			server_sucess(f"Created new objects `{CATEGORY}` on database directory: {self.data_path}.")

		if not os.path.exists(self.posts_path):
			json.dump(self.posts, open(self.posts_path, "w"))
			server_sucess(f"Created new objects `{POSTS}` on database directory: {self.data_path}.")

		if not os.path.exists(self.comments_path):
			json.dump(self.comments, open(self.comments_path, "w"))
			server_sucess(f"Created new objects `{COMMENTS}` on database directory: {self.data_path}.")

	def __load_database(self):
		self.users    = json.load(open(self.users_path, "r"))
		self.category = json.load(open(self.category_path, "r"))
		self.posts    = json.load(open(self.posts_path, "r"))
		self.comments = json.load(open(self.comments_path, "r"))
		server_sucess(f"Sucessfully loaded all the database into memory.")

	# Database handler
	def __save_database(self):
		json.dump(self.users, open(self.users_path, "w"), indent=4)
		json.dump(self.posts, open(self.posts_path, "w"), indent=4)
		json.dump(self.category, open(self.category_path, "w"), indent=4)
		json.dump(self.comments, open(self.comments_path, "w"), indent=4)
		server_sucess("Backedup database.")

	def __save_image(self, qry: Query) -> Result:
		# Saves image into a database
		img_data = qry.payload["data"]
		uid = str(uuid.uuid4()) + ".png"
		while True:
			try:
				open(f"{self.img_path}/{uid}")
			except FileNotFoundError:
				break

		with open(f"{self.img_path}/{uid}", "wb") as f:
			f.write(base64.decodebytes(img_data.encode()))

		return Result("200 Stored", types["json"].decode(FORMAT), {"id": uid})

	def __handle_upload(self, qry: Query) -> Result:
		payload = qry.payload

		# Extracting data
		user        = payload["user"]
		title       = payload["title"]
		description = payload["description"]
		category    = payload["category"]
		content     = payload["content"]

		# Creating a new post
		uid = str(uuid.uuid4())
		while uid in self.posts: uid = str(uuid.uuid4())

		self.posts.update({
			uid: {
				"title": title,
				"description": description,
				"date": str(datetime.datetime.now()),
				"content": content,
				"comment": []
			}
		})

		# Adding it to the users list
		#TODO: Remove this when adding loging system
		if user  not in self.users: self.users.update({user: []})
		if uid   not in self.users[user]: self.users[user].append(uid)

		# Adding it to the category
		if category not in self.category: self.category.update({category: []})
		if uid      not in self.category[category]: self.category[category].append(uid)

		# Saving in different thread
		save_thread = threading.Thread(target = self.__save_database)
		save_thread.start()

		result = Result("200 OK", types["json"].decode(FORMAT), {"log": f"Sucessfully uploaded post with title `{title}`"})
		return result

	def __handle_load(self, qry: Query) -> Result:
		payload = qry.payload

		# Extracting data
		uid = payload["uid"]

		# Loading from memory
		if uid in self.posts:
			response = self.posts[uid]
			comments = response["comment"]
			response["comment"] = [self.comments[i] for i in comments]
			return Result("200 OK", types["json"].decode(FORMAT), response)
		else:
			return Result("400 Not found", types["json"].decode(FORMAT), {"log": f"Cannot find the post with uid `{uid}`."})

	def __handle_query(self, qry: Query) -> Result:
		cmd     = qry.payload["cmd"]
		payload = qry.payload["arg"]

		if cmd == QUERY_BY_AMT:
			amt = int(payload)
			keys = list(self.posts.keys())[:amt]
			result = Result("200 OK", types["json"].decode(FORMAT), {"log": f"Sucessfully queried.", "data": keys})
			return result

		elif cmd == QUERY_BY_NAME:
			result = Result("200 OK", types["json"].decode(FORMAT), {"log": f"Not implemented yet."})
			return result

	def __handle_comment(self, qry: Query) -> Result:
		payload = qry.payload

		# Extracting data
		to      = payload["to"]
		_from   = payload["from"]
		content = payload["content"]
		date    = str(datetime.datetime.now())

		# Checking for post
		if to not in self.posts: 
			return Result("400 Not found", types["json"].decode(FORMAT), {"log": f"Couldnt find the post with title `{to}`"})

		# Generating a comment id
		uid = str(uuid.uuid4())
		while uid in self.comments: uid = str(uuid.uuid4())

		# Saving to memory
		self.comments.update({
				uid: {
					"from": _from,
					"upvote": 0,
					"solved": 0,
					"content": content
				}
			})
		self.posts[to]["comment"].append(uid)

		# Saving in different thread
		save_thread = threading.Thread(target = self.__save_database)
		save_thread.start()

		result = Result("200 OK", types["json"].decode(FORMAT), {"log": f"Sucessfully commented on post `{to}`"})
		return result

	# Database commands
	def query(self, qry: Query) -> Query:
		if qry.cmd == UPLOAD:
			return self.__handle_upload(qry)
		elif qry.cmd == LOAD:
			return self.__handle_load(qry)
		elif qry.cmd == QUERY:
			return self.__handle_query(qry)
		elif qry.cmd == COMMENT:
			return self.__handle_comment(qry)
		elif qry.cmd == SV_IMG:
			return self.__save_image(qry)


