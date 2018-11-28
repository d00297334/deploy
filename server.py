import sys
sys.dont_write_bytecode = True

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs
from pets import *
from users import *
from http import cookies
from session_store import SessionStore
from passlib.hash import bcrypt

gSessionStore = SessionStore()

class MyAwesomeHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.load_session()
		#petDB = petDB()
		#userDB = userDB()
		path = self.path.split('/')[-1]
		if self.path == "/pets":
			self.listAllPets()
		elif self.path == "/pets/" + path:
			self.retrievePet(path)
		elif self.path == "/sessionTest":
			if "counter" in self.session:
				self.session["counter"] += 1
			else:
				self.session["counter"] = 1
			self.send_response(200)
			self.send_cookie()
			self.end_headers()
			self.wfile.write(bytes(str(self.session["counter"]), "utf-8"))
		else:
			self.handleNotFound()


	def end_headers(self):
		self.send_cookie()
		self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
		self.send_header("Access-Control-Allow-Credentials", "true")
		BaseHTTPRequestHandler.end_headers(self)


	def do_OPTIONS(self):
		self.load_session()
		self.send_response(200)
		self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, OPTIONS")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()


	def load_session(self):
		self.load_cookie()
		if "sessionId" in self.cookie:
			sessionId = self.cookie["sessionId"].value
			sessionData = gSessionStore.getSession(sessionId)
			if sessionData != None:
				self.session = sessionData
			else:
				sessionId = gSessionStore.createSession()
				self.cookie["sessionId"] = sessionId
				self.session = gSessionStore.getSession(sessionId)
		else:
			sessionId = gSessionStore.createSession()
			self.cookie["sessionId"] = sessionId
			self.session = gSessionStore.getSession(sessionId)


	def load_cookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

	def send_cookie(self):
		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())

	
	

	def retrievePet(self, petId):
		if "userId" not in self.session:
			self.sendError(401, "Not logged in")
			return
		db = petDB()
		data = db.retrieveCurrentPet(petId)
		if db.exists(petId) == False:
			self.handleNotFound()
			return False
		else:
			json_string = json.dumps(data)
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json_string, "utf-8"))


	def listAllPets(self):
		if "userId" not in self.session:
			self.sendError(401, "Not logged in")
			return
		db = petDB()
		data = db.listAllPets()
		json_string = json.dumps(data)
		print(json_string)
		self.send_response(200)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		self.wfile.write(bytes(json_string, "utf-8"))


	def addPet(self):
		if "userId" not in self.session:
			self.sendError(401, "Not logged in")
			return
		length = int(self.headers["Content-length"])
		data = self.rfile.read(length).decode("utf-8")
		parsed_data = parse_qs(data)

		body = {
			"name":parsed_data['name'][0],
			"owner":parsed_data['owner'][0],
			"age":parsed_data['age'][0],
			"type":parsed_data['type'][0],
			"gender":parsed_data['gender'][0]
		}

		self.send_response(201)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		

		db = petDB()
		db.addPet(body)



	def handleUserLogin(self):
		db = userDB()
		self.load_cookie() #could be load_session()?
		length = int(self.headers["Content-length"])
		data = self.rfile.read(length).decode("utf-8")
		parsed_data = parse_qs(data)

		email = parsed_data['email'][0]
		password = parsed_data['password'][0]

		userId = db.exists(email)

		if userId != None:
			p = db.getPassword(userId)
			#checkPassword = bcrypt.verify(password, p)
			if bcrypt.verify(password, p):
				self.session["userId"] = userId
				userId = db.retrieveCurrentUser(email)
				json_string = json.dumps(userId)
				self.send_response(201)
				self.end_headers()
				self.wfile.write(bytes(json_string, "utf-8"))
			else:
				self.send_response(401)
				self.end_headers()
		else:
			self.send_response(401)
			self.end_headers()




	def addUser(self):
		db = userDB()
		
		length = int(self.headers["Content-length"])
		data = self.rfile.read(length).decode("utf-8")
		parsed_data = parse_qs(data)

		#print("parsed data ", parsed_data)
		password = parsed_data['password'][0]
		hashed = bcrypt.encrypt(password)

		body = {
			"first_name":parsed_data['first_name'][0],
			"last_name":parsed_data['last_name'][0],
			"email":parsed_data['email'][0],
			"encryptedPassword":hashed
		}


		email = body['email']
		print(db.exists(email))
		if db.exists(email) == None:
			db.addUser(body)
			self.send_response(201)
			self.end_headers()
			self.wfile.write(bytes("created","utf-8"))

		else:
			self.send_response(422)
			self.end_headers()
			self.wfile.write(bytes("already created, login","utf-8"))
		

		


		
		
	def deletePet(self, petId):
		if "userId" not in self.session:
			self.sendError(401, "Not logged in")
			return
		db = petDB()
		if db.exists(petId) == False:
			self.handleNotFound()
			return False
		else:
			db.deleteCurrentPet(petId)
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()



	def updatePet(self, petId):
		if "userId" not in self.session:
			self.sendError(401, "Not logged in")
			return
		db = petDB()
		if db.exists(petId) == False:
			self.handleNotFound()
			return False
		length = int(self.headers["Content-length"])
		data = self.rfile.read(length).decode("utf-8")
		parsed_data = parse_qs(data)

		
		body = {
			"name":parsed_data["name"][0],
			"owner":parsed_data["owner"][0],
			"age":parsed_data["age"][0],
			"type":parsed_data["type"][0],
			"gender":parsed_data["gender"][0]
		}
		print("parsed data ", parsed_data)
		print("body ", body)
		print('body name', body['name'])
		self.send_response(200)
		self.send_header("Content-Type", "application/json")
		self.end_headers()

		db.updateCurrentPet(petId, body)
		


	def do_POST(self):
		self.load_session()
		if self.path == "/pets":
			self.addPet()
		elif self.path == "/users":
			self.addUser()
		elif self.path =="/sessions":
			self.handleUserLogin()

		else:
			self.handleNotFound()


	def do_PUT(self):
		self.load_session()
		path = self.path.split("/")[-1]
		if self.path == "/pets/" + path:
			self.updatePet(path)
		else:
			self.handleNotFound()
			

	def do_DELETE(self):
		self.load_session()
		path = self.path.split("/")[-1]
		if self.path == "/pets/" + path:
			self.deletePet(path)
		else:
			self.handleNotFound()


	def handleNotFound(self):
		self.send_response(404)
		self.send_header("Content-Type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<h1>Not Found</h1>", "utf-8"))

	def sendError(self, code, error):
		self.send_response(code)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(error.encode("utf-8"))

	
	
	
def main():

	petdb = petDB()
	petdb.createPetsTable()
	userdb = userDB()
	userdb.createUsersTable()


	petdb = None
	userdb = None

	port = 8080
	if len(sys.argv) > 1:
		port = int(sys.argv[1])


	listen = ("0.0.0.0", port)
	server = HTTPServer(listen, MyAwesomeHandler)

	print("Listening on port...")
	server.serve_forever()

main()
