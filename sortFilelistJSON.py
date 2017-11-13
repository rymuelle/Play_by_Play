#!/usr/bin/python
#coding: utf-8 
import fileListJSON

array = []

def get_week(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 16

for row in fileListJSON.fileListJson:
	parts = row.split(" ")
	#print parts
	for part in parts:
		if "full/" in part:
			number = part.split("/")
			#print part.split("/")
	year = parts[0].split("/")[1]
	print year, number[0]

	number = int(year)*100 + get_week(number[0])
	array.append([row,number])




array.sort(key=lambda x: x[1])

#print array

file  = open("fileListJSON_sorted.py", "w")
file.write("fileListJson = [")
for row in array:
	write_sring = "\"{}\",\n".format(row[0])
	file.write(write_sring)

file.write("]")
file.close()