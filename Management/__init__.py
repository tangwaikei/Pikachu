import pymysql
pymysql.install_as_MySQLdb()
import platform


separator = '\\' if platform.system() == 'Windows' else '/'