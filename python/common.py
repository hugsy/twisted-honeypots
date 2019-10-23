from time import strftime
from twisted.python.logfile import LogFile
from twisted.enterprise import adbapi
from twisted.python import log

class PotFactory:
    dbpool = None

    def __init__(self, logfile=None, dburl=None, driver="MySQLdb"):
        self.logfile = logfile
        self.driver = driver # other options ('MySQLdb', 'pymssql', 'psycopg2',)

        if dburl:
            from re import match
            user, passwd, host, port, db = match(r'(.+?)(?::(.+))?@(.+?)(?::(\d+))?/(.+)$', dburl).groups()
            if not user: user = ''
            if not passwd: passwd = ''
            #if not port: port = 3306
            if not port: port = 1433
            if not host: host = '127.0.0.1'
            dbopts = {'user': user, 'passwd': passwd, 'host': host, 'port': int(port), 'db': db,}
            self.dbpool = adbapi.ConnectionPool(self.driver, **dbopts)

    def updatePot(self, login, password, host):
        log.msg('Thank you %s - %s : %s' % (host, login.decode("utf8"), password.decode("utf8")))
        if self.logfile:
            line = "%s : %s : %s : %s\n" % (strftime('%F %T'), host, login.decode("utf8"), password.decode("utf8"))
            open(self.logfile, 'a').write(line)

        if self.dbpool:
            self.dbpool.runQuery('INSERT INTO pot (type, login, password, host) VALUES (%s, %s, %s, %s)', (self.proto, login, password, host))
