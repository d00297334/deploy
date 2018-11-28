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

class petDB:
	def __init__(self):
		# self.connection = sqlite3.connect("pets.db")
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


	def createPetsTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS pets (id SERIAL PRIMARY KEY, name VARCHAR(255), owner VARCHAR(255), age VARCHAR(255), gender VARCHAR(255), type VARCHAR(255))")
		self.connection.commit()

	# def createSquirrelsTable(self):
    #     self.cursor.execute("CREATE TABLE IF NOT EXISTS squirrels (id SERIAL PRIMARY KEY, name VARCHAR(255), size VARCHAR(255))")
    #     self.connection.commit()

	def addPet(self, body):
		self.cursor.execute("INSERT INTO pets(name, owner, age, gender, type) VALUES (%s, %s, %s, %s, %s)", (body['name'], body['owner'], body['age'], body['gender'], body['type']))
		self.connection.commit()

	def listAllPets(self):
		self.cursor.execute("SELECT * FROM pets")
		data = self.cursor.fetchall()
		self.connection.commit()
		return data

	def retrieveCurrentPet(self, id):
		self.cursor.execute("SELECT * FROM pets WHERE ID = %s", (id, ))
		data = self.cursor.fetchall()
		self.connection.commit()
		return data

	def updateCurrentPet(self, id, body):
		if not self.exists(id):
			return False
		self.cursor.execute("UPDATE pets \
			SET \
			name = %s, owner = %s, age = %s, gender = %s, type = %s \
			WHERE id = %s",
			(
			body['name'], 
			body['owner'], 
			body['age'], 
			body['gender'], 
			body['type'], 
			id
			)
		)
		self.connection.commit()
		return True

	def deleteCurrentPet(self, id):
		self.cursor.execute("DELETE FROM pets WHERE ID = %s", (id, ))
		self.connection.commit()

	def exists(self, id):
		self.cursor.execute('select * from pets where id = %s;', (id,))
		data = self.cursor.fetchone()
		if data is None:
			return False
		return data
		