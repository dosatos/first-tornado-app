import os.path
from tornado.options import define, options, parse_command_line # tornado options related imports
define("port", default=8888, help="Port for webserver to run") # need the port to run on
define("db_connection_str", default="sqlite:///database.db", help="Database connection string for application") # db connection string
# define("mysql_host", default="127.0.0.1:3306", help="app database host")
# define("mysql_database", default="app", help="app database name")
# define("mysql_user", default="app", help="app database user")
# define("mysql_password", default="app", help="app database password")
parse_command_line() # firstly, get the above options from command line
from tornado import ioloop, web

# SQL base related libs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base as models_base # get the declared sqlalchemy base

from handlers import MainHandler, AdminHandler

db_engine = create_engine(options.db_connection_str) # setup db engine for sqlalchemy
db_session = sessionmaker() # setup the session maker for sqlalchemy


class MyApplication(web.Application):
    """ Inhierited tornado.web.Application - stowing some sqlalchemy session information in the application """
    def __init__(self, *args, **kwargs):
        """ setup the session to engine linkage in the initialization """
        self.session = kwargs.pop('session')
        self.session.configure(bind=db_engine)
        super(MyApplication, self).__init__(*args, **kwargs)

    def create_database(self):
        """ this will create a database """
        models_base.metadata.create_all(db_engine)

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
	# SURVEY_DIR_WITH_ENCRYPTED_KEYS=os.path.join(os.path.dirname(__file__), "keys"),
	# PRIVATEKEY=os.path.join(os.path.dirname(__file__), "keys")+'/private_key.bin',
	session=db_session,
	debug=True,
)

# initialisation of the app
application = MyApplication([
	(r'/', MainHandler, dict(db_session=db_session)),
	(r'/admin', AdminHandler, dict(db_session=db_session))
], **settings)


if __name__ == "__main__":
	print("Server running...")
	print(f"localhost:{options.port}")
	print("Press ctrl + c to close")
	application.create_database() # create the database
	application.listen(options.port) # listen on the right port
	ioloop.IOLoop.instance().start() # startup ioloop
