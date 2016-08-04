# -*- coding: utf-8 -*-
#from django.db import models
import mysql.connector
import csv
import re

config = {
  'user': 'bookparser',
  'password': 'sosnora66',
  'host': 'bookparser.mysql.pythonanywhere-services.com',
  'database': 'bookparser$new ',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

bbk = []

def lev(l):
    if '(' in l:
        l = l[:l.index('(')+1]
    #stop = ['/', ':', '-']
    #for all in stop:
    #    l = l.replace(all, '')
    l = l.split('.')
    s = sum([len(all) for all in l])
    return s, l

def stat(l):
    if l.startswith('-'):
        s = 'vs'
    else:
        s = 'osn'
    return s

def sme(l, code):
    m = re.findall(r"([ ]\d+[.]\d+[.]\d+)|([ ]\d+[.]\d+)", l)
    sm = []
    for all in m:
        for a in all:
            if a != '' and a[1:] != code:
                sm.append(a[1:])
    return sm

def find_parent(code):
    s = 0
    l = lev(code)
    if l == 1:
        s = 'First'
    else:
        s = [item for item in bbk if item['code']==code]
        try:
            s=s[0]['code']
        except:
            pass
    return s

filename = '/home/bookparser/files/bbk_clean.csv'
f = open(filename, 'r')
reader = csv.reader(f)
for row in reader:
    code = row[0]
    text = row[1]
    sm = sme(text, code)
    level = lev(code)[0]
    status = stat(code)
    if status == 'osn':
        parent = find_parent(code)
        x = 0
        while not parent:
            parent = find_parent(code[:-x])
            x +=1
            if x == 25:
                parent = 'Not find'
    else:
        parent = 'other status'
    bbk.append({'code': code, 'text': text, 'sm': sm, 'level': level, 'stat': status, 'parent': parent})
    print code, level, parent, type(parent)
    cursor.execute("SELECT id from myapp_bbk WHERE code = %s", (parent,) )
    p = cursor.fetchall()
    if len(p)>0:
        p = p[0][0]
        print p
        cursor.execute("INSERT INTO myapp_bbk (code, text, sme, level, stat, parent) VALUES (%s, %s, %s, %s, %s, %s)", ((code, text, str(sm), level, status, str(p),)))
    else:
        cursor.execute("INSERT INTO myapp_bbk (code, text, sme, level, stat) VALUES (%s, %s, %s, %s, %s)", ((code, text, str(sm), level, status,)))
    cnx.commit()
f.close()
cursor.close()
for all in bbk:
    print all['stat'], all['code'], " ", all['level'], ' ', all['parent']
    #print all['text']
    #print all['sm']
    #print all['level']
    #print all['stat']
    #print 'parent', all['parent']
print len(bbk)
x = [item for item in bbk if item['parent']==0 or item['parent']==None]
print 'parent', len(x)
for all in x:
    print all['code']


#cursor.execute("SELECT id, udk FROM myapp_book")
#udks = cursor.fetchall()
#for all in udks:
#    print all[0], all[1]
#    new_udk = all[1].replace('[', '')
#    print new_udk
#    cursor.execute("UPDATE myapp_book SET udk=%s WHERE id=%s", ((new_udk, all[0])))
#    cnx.commit()

#cursor.close()

#cnx.close()