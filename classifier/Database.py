#https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/

import mysql.connector as mysql

config = {
			'port': 8889,
			'user': 'liz',
			'password': None,
			'host': 'localhost',
			'database': 'petfriend_database',
			'raise_on_warnings': True,
		}
data = {
	'gender': 'Male',
	'breed': 'Unknow',
	'name' : 'Lucy',
	'contact': "lucy123@email.com",
	'location': "Turlock, CA",
	'states' : "Found",
	'image' : 'C:/Users/Work/Documents/gitHub/csProject/DogImages/Chihuahua/yuki.png',
	'animal': "dog"
}


#conn = mysql.connect(**config)

class Database:
	def __init__(self,confg):
		self.confg = confg
		self.conn = mysql.connect(**self.confg)
		self.cursor = self.conn.cursor()

	def checkConnection(self):
		return self.conn.is_connected()

	def add(self, table, data):
		vars = tuple(data.keys())
		val = tuple(data.values())
		cursor = self.conn.cursor()
		self.cursor.execute(
			'INSERT INTO pet (' + ','.join(vars) + ') VALUES (%' + ', %'.join('s' * len(val)) + ')', val)
		self.conn.commit()

	def getTable(self,table):
		self.cursor.execute("SELECT * FROM "+table)
		return self.cursor.fetchall()

	def close(self):
		self.cursor.close()
		self.conn.close()

	def remove(self, table, data):
		pass

def converToBinaryData(filename):
	with open(filename,'rb') as file:
		binaryData = file.read()
	return binaryData

def readBlob():
	pass 


imgURL = data['image']
data['image'] = converToBinaryData(data['image'])
print(imgURL)
print(data)

#db = Database(config)
#if db.checkConnection():
#	print("adding ....")
#	db.add("pet", data)
