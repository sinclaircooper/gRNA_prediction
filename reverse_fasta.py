#! /usr/bin/python
import sys

#takes a fasta sequence and reverses it 
#reads from sdtin 

header_list = []
sequence_list = []

for line in sys.stdin:
	if '>' in line:
		header_list.append(line[:-1])
	else:
		header_list.append(line[::-1])

#print header_list
#print sequence_list 

for line in header_list:
	print line
