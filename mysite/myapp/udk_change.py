#from django.db import models
import mysql.connector
import csv
import sys

config = {
  'user': 'bookparser',
  'password': 'sosnora66',
  'host': 'bookparser.mysql.pythonanywhere-services.com',
  'database': 'bookparser$new ',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute("SELECT id, udk FROM myapp_book")
udks = cursor.fetchall()
for all in udks:
    print all[0], all[1]
    cursor.execute("UPDATE myapp_book SET udk=%s WHERE id=%s", ((all[1][4:], all[0])))
    cnx.commit()
    print all[1][4:]

cursor.close()

cnx.close()