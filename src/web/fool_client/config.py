from spyceconf import *

# The root option defines the path from which Spyce requests are processed.
# I.e., when a request for http://yourserver/path/foo.spy arrives,
# Spyce looks for foo.spy in <root>/path/.
root = r'D:\dev\eclipse2\durak_game\spyce-2.1\www\fool_client\www'
# This allows you to import .py modules from the lib directory.
sys.path.append(r'D:\dev\eclipse2\durak_game\spyce-2.1\www\fool_client\lib')

# Some commonly overridden options -- see spyceconf.py from the Spyce
# distribution for details and the full set of options.
debug = False        # True to log more to stderr
port = 8000          # webserver port
indexExtensions = ['spy'] # list of extensions to check if directory requested

# database connection
# Examples:
# db = SqlSoup('postgres://user:pass@localhost/dbname')
# db = SqlSoup('sqlite:///my.db')
# db = SqlSoup('mysql://user:pass@localhost/dbname')
#
# SqlSoup takes the same URLs as an SqlAlchemy Engine.  See 
# http://www.sqlalchemy.org/docs/dbengine.myt#dbengine_establishing
# for more examples.
db = None

# authentication -- see spyceconf.py for how to customize these
login_validator = nevervalidator
login_storage = FileStorage(r'D:\dev\eclipse2\durak_game\spyce-2.1\www\fool_client\login-tokens')
login_render = 'render:login'
loginrequired_render = 'render:login_required'