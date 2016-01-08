from system.core.model import Model
import re

class Uwhere(Model):
	def __init__(self):
		super(Uwhere, self).__init__()

	def register_user(self, user):
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		errors = []
		if not user['name']:
			errors.append('Name cannot be blank')
		elif len(user['name']) < 3:
			errors.append('Name must be at least 3 characters long')
		if not user['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(user['email']):
			errors.append('Email format is invalid')
		if not user['phone']:
			errors.append('Phone number is invalid')
		if not user['password']:
			errors.append('Password cannot be blank')
		elif len(user['password']) < 8:
			errors.append('Password must be at least 8 characters long')
		elif user['password'] != user['cpassword']:
			errors.append('Password and Confirmation must match!')
		if errors:
			return {'status': False, 'errors': errors}
		else:
			password = user['password']
			pw_hash = self.bcrypt.generate_password_hash(password)
			query = "INSERT INTO users (name, phone, email, pw_hash) VALUES ('{}', '{}', '{}', '{}')".format(user['name'], user['phone'], user['email'], pw_hash)
			self.db.query_db(query)
			find = "SELECT id FROM users ORDER BY id DESC LIMIT 1"
			users = self.db.query_db(find)
			return {'errors': True, 'user': users[0]}

	def login_user(self, user_info):
		errors = []
		query = "SELECT * FROM users WHERE email = '{}'".format(user_info['email'])
		password = user_info['password']
		user = self.db.query_db(query)
		if user: 
			if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
				return {'status': True, 'user': user[0]}
			else:
				errors.append('Password is incorrect')
				return {'status': False, 'errors': errors}
		else:
			errors.append('Invalid Email/Password')
			return {'status': False, 'errors': errors}

	def friends_list(self):
		return self.db.query_db("SELECT * FROM users ORDER BY name")

	def get_places(self, id):
		query = "SELECT * FROM users LEFT JOIN places ON users.id = places.user_id WHERE users.id = '{}'".format(id)
		return self.db.query_db(query)

	def add_place(self, place):
		query = "INSERT INTO places (address, created_at, user_id) VALUES ('{}', NOW(), '{}')".format(place['place'], place['id'])
		return self.db.query_db(query)