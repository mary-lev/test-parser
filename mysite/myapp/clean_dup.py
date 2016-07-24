import mysql.connector

config = {
  'user': 'bookparser',
  'password': 'sosnora66',
  'host': 'bookparser.mysql.pythonanywhere-services.com',
  'database': 'bookparser$new ',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute("SELECT full FROM myapp_book")
rows = cursor.fetchall()
cursor.close()
for row in rows:
    cursor.execute("SELECT id, full FROM myapp_book WHERE full=%s", (row[0],) )
    c = list(cursor)
    if len(c) == 2:
        cursor.execute("DELETE IGNORE from myapp_book WHERE id=%s", (c[0][0],) )
        print 'Find!', c[0]
        cnx.commit()

cursor.close()

cnx.close()