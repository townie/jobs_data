from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jobs_data.db.schema import Job, Base, engine

if __name__ == "__main__":

	# Bind the engine to the metadata of the Base class so that the
	# declaratives can be accessed through a DBSession instance
	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)
	# A DBSession() instance establishes all conversations with the database
	# and represents a "staging zone" for all the objects loaded into the
	# database session object. Any change made against the objects in the
	# session won't be persisted into the database until you call
	# session.commit(). If you're not happy about the changes, you can
	# revert all of them back to the last commit by calling
	# session.rollback()
	session = DBSession()

	# Insert a Person in the person table
	new_job = Job(
	title = 'new job',
	description = 'stuff here',
	location =  'text',
	post_url = 'url/url',
	company_id = 10)

	session.add(new_job)
	session.commit()

	# Insert an Address in the address table

