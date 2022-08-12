
# Constants
CREATE = "create"
DELETE = "delete"
UPDATE = "update"
OBJECT = "object"
ENTRY  = "entry"
FROM   = "from"
IN     = "in"

PRIM_CMDS = [CREATE, DELETE, UPDATE]

# HTTP keywords
HEAD = b"head"
PAYLOAD = b"payload"
CONTENT_TYPE = b"content-type"
CONTENT_LEN = b"content-length"

# HTTP Request constants
GET = "GET"
POST = "POST"

# HTTP file types
sup_types = ["html", "css", "js", "jpg", "png"]
types = {
	"html": b"text/html",
	"css" : b"text/css",
	"js"  : b"text/js",
	"jpg" : b"image/jpeg",
	"png" : b"image/png"
}

