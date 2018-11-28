# Pets
An application that lets you add, update, and delete pets. 


## Resources
### Pets DB
```
CREATE TABLE IF NOT EXISTS "pets" (
	`ID`			INTEGER UNIQUE,
	`name`			TEXT,
	`owner`			TEXT,
	`age`			INTEGER,
	`gender`		TEXT,
	`type`			TEXT,
	PRIMARY KEY(`ID`)
);
```


### Pets DB
- `ID (int)` primary key
- `name (text)`
- `owner (text)`
- `age (int)`
- `gender (test)`
- `type (text)`


### Users DB
```
CREATE TABLE IF NOT EXISTS "users" (
	`userId`				INTEGER UNIQUE,
	`first_name`				TEXT,
	`last_name`				TEXT,
	`email`					TEXT,
	`enctyptedPassword`			TEXT,
	PRIMARY KEY(`userId`)
);
```


### Users DB
- `userId (int)` primary key
- `first_name (text)`
- `last_name (text)`
- `email (int)`
- `encryptedPassword (test)`




## Web App Endpoints 
### GET
- `/pets`: returns a JSON representation of the whole collection.
- `/pets/${id}`: returns a JSON representation of a one item in the collection, if it exists according to the id. 

### POST
- `/pets`: creates a new pet based on the input name, owner, age, gender, and type. 
- `/sessions`: creates a session and log in the current user, if authorized. 
- `/users`: creates a new user if email is unique.

### PUT
- `/pets/${id}`: updates a member of the collection based on the id passed in, if it exists. 

### DELETE
- `/pets/${id}`: deletes a member of the collection based on the id passed in, if it exists. 

## Password Encryption
- Uses passlib's `bcrypt` for encrypting and verifying passwords.
