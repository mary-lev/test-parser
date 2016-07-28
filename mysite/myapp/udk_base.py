import json

udks = {}

filename = '/home/bookparser/files/udks.txt'
with open(filename, 'rb') as f:
    text = f.readlines()
    for row in text:
        row = row.replace('\r\n', '')
        t = row[:4]
        t = t.replace('\t', '')
        print t
        a = row[4:]
        print a
        udks[t] = a

with open('udks.json', 'wb') as f:
    json.dump(udks, f)