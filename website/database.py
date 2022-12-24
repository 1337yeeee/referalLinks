from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

from website import app

engine = create_engine(app.config['DATABASE_URI'],
					   convert_unicode=True,
					   **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
										 autoflush=False,
										 bind=engine))


def init_db():
	Model.metadata.create_all(bind=engine)


Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class User(Model):
	__tablename__ = 'users'
	id = Column('user_id', Integer, primary_key=True)
	password = Column('password', String(200))
	login = Column('login', String(200), unique=True)
	name = Column(String(200))

	def __init__(self, name, login, password):
		self.name = name
		self.login = login
		self.password = password

	def to_json(self):
		return dict(name=self.name, is_admin=self.is_admin, login=self.login)

	# @property
	# def is_admin(self):
	#     return self.openid in app.config['ADMINS']

	def __eq__(self, other):
		return type(self) is type(other) and self.id == other.id

	def __ne__(self, other):
		return not self.__eq__(other)


class RefLink(Model):
	__tablename__ = 'ref_links'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.user_id'))
	link = Column(String(255), unique=True)

	# user = relation(User, backref='ref_links')

	def __init__(self, user_id):
		self.user_id = user_id
		self.link = RefLink.generateLink()

	@staticmethod
	def generateLink():
		import random, string
		symbols = string.ascii_letters + string.digits
		link = ''.join(random.choice(symbols) for i in range(10))
		
		while db_session.execute("""SELECT COUNT(*) FROM ref_links
									WHERE link=:link""", {'link': link}).first()[0] != 0:
			link = ''.join(random.choice(symbols) for i in range(10))

		return link


class Referral(Model):
	__tablename__ = 'referrals'
	id = Column(Integer, primary_key=True)
	owner_id = Column(Integer, ForeignKey('users.user_id'))
	user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)

	# owner = relation(User, backref='referrals')
	# user = relation(User, backref='referrals')

	def __init__(self, owner, user):
		self.owner = owner
		self.user = user

	def to_json(self):
		return dict(id=self.id,
					owner=self.owner.to_json(),
					user=self.user.to_json())
