import os
import numpy as np
import string
import csv

def get_fileinfo(path):
	
	files=os.listdir(path)
	files = np.asarray(files)
	result = []
	
	
	for idx,val in enumerate(files):
		val = val.replace('.bmp',' ')
		val = val.lstrip('0')
		val = val.strip()
		result.append(int(val))

	print("There are " + str(len(result)) + " frames in target file")
	return result


def csv_write():
	csvfile = open("a.csv","r")
	lines = csvfile.readlines()
	if len(lines) >= 1:
		print("Header exist!")
	else:
		csvfile = open("a.csv","w")
		writer = csv.writer(csvfile)
		writer.writerow(["index","move_limb","COM_pos","COM_dist"])
		print("Header created!")
