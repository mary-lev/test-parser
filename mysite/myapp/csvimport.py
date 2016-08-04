# -*- coding: utf-8 -*-
#from django.db import models
import mysql.connector
import csv, sys, re

config = {
  'user': 'bookparser',
  'password': 'sosnora66',
  'host': 'bookparser.mysql.pythonanywhere-services.com',
  'database': 'bookparser$new ',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(buffered=True)
n=0
filename = sys.argv[1]
with open(filename, 'rb') as csvfile:
    tablereader = csv.DictReader(csvfile, delimiter=',')
    for row in tablereader:
        print row['isbn'], row['title']

        #test unique
        cursor.execute("SELECT * from myapp_book WHERE full = %s", (row['text'],) )
        a = cursor.fetchall()
        if len(a) == 0:
            #test null printing
            if not row['printing']:
                exem =0
            else:
                exem = row['printing']

            cursor.execute("INSERT INTO myapp_book "
                "(name, bbk, year, pages, tom, isbn, udk, topics, exem, full) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  ((row['title'], row['bbk'], row['year'],row['page'], row['tom'], row['isbn'],  row['udk'],  row['topics'], exem, row['text'], )))
            book_id = cursor.lastrowid

            #find and count publishers
            if ':' in row['publisher']:
                publishers = row['publisher'].split(':')
                print publishers
                if ';' in row['city']:
                    city = ''
                else:
                    city = row['city']
                for all in publishers:
                    cursor.execute("SELECT id, name FROM myapp_publisher WHERE name = %s", (all,) )
                    two = cursor.fetchone()
                    if two:
                        publisher_id = two[0]
                    else:
                        cursor.execute("INSERT INTO myapp_publisher (name, city) VALUES (%s, %s)", ((all, city)))
                        publisher_id = cursor.lastrowid
                    cursor.execute("INSERT INTO myapp_printings (publisher_id, book_id) VALUES (%s, %s)", ((publisher_id, book_id)))
            else:
                one = (row['publisher'], row['city'])
                cursor.execute("SELECT id, name, city FROM myapp_publisher WHERE name = %s", (row['publisher'],) )
                r = cursor.fetchone()
                if r:
                    publisher_id = r[0]
                    if not r[2]:
                        cursor.execute("UPDATE myapp_publisher SET city=%s WHERE id = %s", (row['city'], publisher_id) )
                else:
                    cursor.execute("INSERT INTO myapp_publisher (name, city) VALUES (%s, %s)", (one))
                    publisher_id = cursor.lastrowid
                cursor.execute("INSERT INTO myapp_printings (publisher_id, book_id) VALUES (%s, %s)", ((publisher_id, book_id)))

            #find author
            if row['author'] != 'None':
                cursor.execute("SELECT id, surname FROM myapp_author WHERE surname=%s", (row['author'],) )
                try:
                    author_id = cursor.fetchone()[0]
                except:
                    cursor.execute("INSERT INTO myapp_author (surname) VALUES (%s)", (row['author'],) )
                    author_id = cursor.lastrowid
                cursor.execute("INSERT INTO myapp_authorship (author_id, book_id) VALUES (%s, %s)", ((author_id, book_id)))


            cnx.commit()
            # find bbk
            b = row['bbk'][7:]
            b = b.split(' + ')
            for all in b:
                s = all
                print s
                cursor.execute("SELECT id FROM myapp_bbk WHERE code = %s", (s,) )
                r = cursor.fetchone()
                s = re.sub('[^0-9.-]','', s)
                while not r:
                    cursor.execute("SELECT id FROM myapp_bbk WHERE code = %s", (s,) )
                    r = cursor.fetchone()
                    s = s[:-1]
                    if len(s)==0:
                        r = 'Not found'
                        n+=1
                print r

        else:
            print 0
cursor.close()

cnx.close()
print n