import psycopg2
from dataclasses import dataclass

@dataclass
class foodItem:
	name: str
	sQuantity: float
	sCost: float
	sCal: float
	sFat: float
	sProtein: float
	MFPName: str
	verified: bool
	link: str
	unit: str
	bQuantity: float
	bCost: float
	

class DBController:
	serverip = None

	def __init__(self, serverip):
		self.serverip = serverip

	def getConnection(self):
		return psycopg2.connect(
			database="foodparser",
			user="postgres",
			password="postgres",
			host=self.serverip,
			port="5432")

		self.cur = conn.cursor()

	# Drops and rebuilds tables
	def buildTables(self):
		with self.getConnection() as conn:
			with conn.cursor() as cur:

				# drop tables
				tables = ['DATA','RECEPIES','STOCK']
				for table in tables:
					cur.execute('DROP TABLE IF EXISTS %s CASCADE;' % table)

				# build new tables
				cur.execute('''
					CREATE TABLE DATA
					(NAME CHAR(50) PRIMARY KEY NOT NULL,
					SQUANTITY REAL,
					UNIT CHAR(15),
					SCOST REAL,
					SCAL REAL,
					SFAT REAL,
					SPROTEIN REAL);
				''');

				cur.execute('''
					CREATE TABLE STOCK(
					NAME CHAR(50) PRIMARY KEY NOT NULL,
					FOREIGN KEY(NAME) REFERENCES DATA ON DELETE CASCADE,
					MFPNAME CHAR(50),
					VERIFIED BOOLEAN NOT NULL,
					LINK CHAR(250),
					BQUANTITY REAL,
					BCOST REAL
				);''')

				cur.execute('''
					CREATE TABLE RECEPIES(
					NAME CHAR(50) PRIMARY KEY NOT NULL,
					FOREIGN KEY (NAME) REFERENCES DATA ON DELETE CASCADE,
					INGRTABLE CHAR(60) UNIQUE
				);''')

			conn.commit()

	def _addStock(self, foods):
		pass

	def addStock(self, foodItem):
		with self.getConnection() as conn:
			with conn.cursor() as cur:
				
				cur.execute('''
					INSERT INTO DATA
					(NAME, SQUANTITY, UNIT, SCOST, SCAL, SFAT, SPROTEIN)
					VALUES (%s, %s, %s, %s, %s, %s, %s)
				;''',(
				foodItem.name,
				foodItem.sQuantity,
				foodItem.unit,
				foodItem.sCost,
				foodItem.sCal,
				foodItem.sFat,
				foodItem.sProtein))

				cur.execute('''
					INSERT INTO STOCK
					(NAME, MFPNAME, VERIFIED, LINK, BQUANTITY, BCOST)
					VALUES(%s, %s, %s, %s, %s, %s);''',
					(foodItem.name,
					foodItem.MFPName,
					foodItem.verified,
					foodItem.link,
					foodItem.bQuantity,
					foodItem.bCost))


			conn.commit()

	def _addRecipe(self, foodItem, ingredients):
		with self.getConnection() as conn:
			with conn.cursor() as cur:

				ingrTableName = foodItem.name + "_INGR"

				cur.execute('''
					INSERT INTO RECEPIES
					(NAME, INGRTABLE)
					VALUES(%s, %s);''',(
					foodItem.name,
					ingrTableName))

				cur.execute('DROP TABLE IF EXISTS %s', (ingrTableName,))

				cur.execute('''
					CREATE TABLE %s
					(NAME (50) PRIMARY KEY NOT NULL,
					FOREIGN KEY(NAME) REFERENCES DATA ON DELETE CASCADE
					);''',
					(ingrTableName,))

				for i in ingredients:

					cur.execute('''
						INSERT INTO %s
						(NAME)
						VALUES (%s);''', (i.name,))

			conn.commit()




dbc = DBController('192.168.1.77')
dbc.buildTables();
fi = foodItem(
	'testfood',
	100,
	0.179,
	180,
	90,
	15,
	None,
	False,
	None,
	'g',
	1000,
	1.79)

dbc.addStock(fi)
