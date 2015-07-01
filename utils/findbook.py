# -*- coding: utf-8 -*-

#import http.client
import base64
import re
import datetime
import time
import sys
import json
import httplib

login = "libIdType=lib&id=LIBSORO&password=tjfhghl"
conn = httplib.HTTPConnection("library.sogang.ac.kr")
headers = [("HOST", "library.sogang.ac.kr"),
("User-Agent", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.33 Safari/537.31"),
("Connection", "keep-alive"),
("Content-Type", "application/x-www-form-urlencoded")]
conn.request("GET", "/", None, dict(headers))
r1 = conn.getresponse()
#print("result : ", r1.status, r1.reason)
rr = r1.getheaders()[2][1]
rr = rr[0:rr.find(";")]
headers.append(("Cookie", rr))
conn.close()

conn = httplib.HTTPSConnection("library.sogang.ac.kr")
conn.request("POST", "/login", login, dict(headers))
r2 = conn.getresponse()
r2.read()
conn.close()

i=1
bookout = []
list = []
while i<=1:
	conn = httplib.HTTPConnection("library.sogang.ac.kr")
	try:
		conn.request("GET", "/missrepo/list?pn="+str(1)+"&ss=0002",None, dict(headers))
		r1 = conn.getresponse()
	except:
		break
#	print("result : ", r1.status, r1.reason)
	d = r1.read()
	p1 = d.find("<!-- Content List -->")
	p2 = d.find("<!-- Content Paging -->")
	dd = d[p1:p2]
	p3 = p4 = dd.find("<tr>")
	while dd.find("<tr>", p4) != -1:
		p3 = dd.find("<tr>", p4)
		p4 = dd.find("</tr>", p3)
		ddd = dd[p3:p4]
		num = 0
		p5 = ddd.find("\"", ddd.find("a href")+1)
		p6 = ddd.find("\"", p5+1)
		link = ddd[p5+1:p6]
		data = (num, link)
		list.append(data)
	i=i+1

# num: 등록번호
# idnum: 고유번호
# idnum is string ex. 000000114434

fjs=open("../lib/collections/zaddBooks.js","w")
fjs.write("data = [")

def writeJSON(addr, idnum, title, status):
	jsobj = {"addr": "library.sogang.ac.kr"+addr, "idnum": idnum, "title": title, "status": status}
	fjs.write(json.dumps(jsobj, ensure_ascii=False)+", ")

def searchidNum(num, addr, idnum, title):

	conn = httplib.HTTPConnection("library.sogang.ac.kr")
	conn.request("GET", addr , None, dict(headers))
	r1 = conn.getresponse()
#	print("result : ", r1.status, r1.reason)
	d = r1.read()
	p0 = d.find("</thead>")
	try:
		p1 = d.find(str(int(idnum)),p0+1)
	except:
		return
	
	if p1 != -1:
		p2 = d.find("<td>",p1+1)
		p3 = d.find("</td>",p2+1)
		tempStatus = d[p2+4:p3]
		status = re.split(r'[ \r\t\n]+',tempStatus)
		writeJSON(addr, idnum, title, status[1])
		if status[1] == "대출중":
			bookout.append(num)

for i in range(len(list)):
	conn = httplib.HTTPConnection("library.sogang.ac.kr")
	conn.request("GET", list[i][1] ,None, dict(headers))
	r1 = conn.getresponse()
	d = r1.read()
	p1 = d.find("등록번호")
	p2 = d.find("<td>",p1)
	p3 = d.find("</td>",p2+1)
	if p1 != -1:
		idnum = d[p2+4:p3]
		p4 = d.find("<!-- Contnt Detail -->")
		p5 = d.find("<!-- Content Buttons -->")
		detail=d[p4:p5]
		p6 = detail.find("<a href=")
		p7 = detail.find('">',p6+1)
		addr = detail[p6+9:p7]
		p8 = detail.find("</a>")
		title = detail[p7+2:p8]
		searchidNum(num, addr, idnum, title)

fjs.write('{"status":"last"} ];\n')
jscode=" checkedBookNum = " + str(len(bookout)) + "\nfor(var i in data){\nif( data[i].status == \"last\" ) break;\nif(data[i].status == \"대출가능\") { data[i].checked=false; } else { data[i].checked = true; checkedBookNum++; } Books.update(data[i],{$set:{\"status\":data[i],status}},{upsert:true}); }"
fjs.write(jscode)
fjs.close()
