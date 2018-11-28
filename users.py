import os
import psycopg2
import psycopg2.extras
import urllib.parse
import sqlite3
import json

def dict_factory(cursor, row):
	d = {}
	for i, col in enumerate(cursor.description):
		d[col[0]] = row[i]
	return d


class userDB:
	def __init__(self):
		# self.connection = sqlite3.connect("users.db")
		# self.connection.row_factory = dict_factory
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

		self.connection = psycopg2.connect(
			cursor_factory=psycopg2.extras.RealDictCursor,
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)


		self.cursor = self.connection.cursor()


	def __del__(self):
		self.connection.close()


	def addUser(self, body):
		self.createUsersTable()
		self.cursor.execute("INSERT INTO users(first_name, last_name, email, encrypted_password) VALUES (%s, %s, %s, %s)", (body['first_name'], body['last_name'], body['email'], body['encrypted_password']))
		self.connection.commit()


	def createUsersTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fist_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), encrypted_password VARCHAR(255))")
		self.connection.commit()


	def listAllUsers(self):
		self.createUsersTable()
		self.cursor.execute("SELECT * FROM users")
		data = self.cursor.fetchall()
		self.connection.commit()
		return data


	def retrieveCurrentUser(self, email):
		self.createUsersTable()
		self.cursor.execute("SELECT * FROM users WHERE email = %s", (email, ))
		data = self.cursor.fetchall()
		self.connection.commit()
		return data


	def getPassword(self, userId):
		self.createUsersTable()
		self.cursor.execute("SELECT * FROM users where userId = %s", (userId, ))
		data = self.cursor.fetchone()
		if data is None:
			return False
		return data['encryptedPassword']


	def exists(self, email):
		self.createUsersTable()
		self.cursor.execute('select * from users where email = %s;', (email,))
		data = self.cursor.fetchone()
		if data is None:
			return None
		return data['userId']
		