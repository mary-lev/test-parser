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

name = '/home/bookparser/files/udk_test1.txt'
with open(name, 'r') as f:
    text = f.readlines()

udk = {}
for all in text:
    if '#' not in all and '->' not in all:
        a = all.split(' ')
        if ':' not in all:
            udk[a[0]]=all[len(a[0]):]

cursor.execute("SELECT name, udk FROM myapp_book WHERE id < 300")
c = cursor.fetchall()
res = 0
for all in c:
    print all[1]
    osn = all[1][:all[1].find(':')]
    print osn
    if osn in udk.keys():
        print 'Found!'
    else:
        osn = all[1][:all[1].find('(')]
        print osn
        if osn not in udk.keys():
            osn = all[1][:all[1].find('-')]
            print osn
    try:
        print all[1], udk[osn], all[0]
        res +=1
    except:
        print 'Not found'
print res

