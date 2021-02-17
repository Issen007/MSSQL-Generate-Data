import pymssql
import argparse
import names
import random
import pandas as pd

cities = ['Stockholm', 'Oslo', 'Paris', 'Copenhagen', 'Tuscon', 'London', 'Toyko', 'Phoenix', 'Frankfurt', 'Helsinki', 'Reykjavik', 'Amsterdam', 'Chicago', 'Sidney', 'Melbourne']


class SqlConnect(object):
    """Connect to you Microsoft SQL Server and can write and read data."""

    def __init__(self, servername, port, database, table, username, password):
        super(SqlConnect, self).__init__()
        self.db = database.lower()
        self.table = table.lower()

        self.conn = pymssql.connect(servername, username, password, self.db)
        self.cursor = self.conn.cursor()

    def read(self, *args, **kwargs):
        ''' Reading all values from your database and tablespace.'''

        print('*' * 10)
        print('Reading data to database {}'.format(self.db))
        print('*' * 10)
        sql_df = pd.read_sql_query('SELECT * FROM {}.dbo.{}'.format(self.db, self.table),self.conn)
        print(sql_df)
        
        self.conn.close()
        return True

    def write(self, *args, **kwargs):
        ''' We will now ask you for a name, age and
            city to be inserted to the database '''

        if a.generate:
            name = str(names.get_first_name())
            age = random.randint(20,75)
            city = random.choice(cities)
        else:
            name = input('What is your name? ')
            age = input('What is your age? ')
            city = input('Where do you live? ')

        print('*' * 10)
        print('Adding ' + name + ' with age ' + str(age) + ' that lives in ' + city)
        print('Writing data to database {}'.format(self.db))
        print('*' * 10)
        query = "INSERT INTO {}(name,age,city) VALUES (%s,%s,%s)".format(self.table)
        self.cursor.execute(query,((name), (age), (city)))
        self.conn.commit()
        return True

    def readwrite(self, *args, **kwargs):
        ''' This will only run write and then read function.'''
        self.write(kwargs)
        self.read(kwargs)

def main():
    sql = SqlConnect(servername = a.servername,
        port = a.port,
        database = a.database,
        table = a.table,
        username = a.username,
        password = a.password)

    if a.writeread:
        sql.readwrite()
    elif a.write:
        sql.write()
    else:
        sql.read()


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='''Test Python Script to Read / Write data to Microsoft SQL Server''',
    )
    g = p.add_mutually_exclusive_group(required = False)
    p.add_argument("--servername", "-S", default='issendb.issen.local', help = "FQDN or IP address to your MS SQL Server, default is issendb.issen.local")
    p.add_argument("--port", "-P", default='1433', help = "Microsoft SQL Server Exposed TCP Port, default is 1433")
    p.add_argument("--database", "-D", default='TestDB', help="Database Name you want to write too, default is TestDB")
    p.add_argument("--table", "-T", default='ReadOnly', help="Table in the Database you want to write to")
    p.add_argument("--username", "-u", help="Username that has access to the database")
    p.add_argument("--password", "-p", help="User password that has access to the database")
    p.add_argument("--generate", "-g", action="store_true", help="Auto Generate Name, Age and City")
    g.add_argument("--write", "-w", action="store_true", help="Do only write data to Database")
    g.add_argument("--read", "-r", action="store_true", help = "Do only read data from Database")
    g.add_argument("--writeread", "-wr", action="store_true", help = "Write data to Database and then read the same data.")
    a = p.parse_args()
    main()
