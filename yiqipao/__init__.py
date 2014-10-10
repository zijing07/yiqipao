import pymysql
pymysql.install_as_MySQLdb()

import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf-8')

print (sys.getdefaultencoding())
