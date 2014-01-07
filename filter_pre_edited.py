#! /usr/bin/python 

import sys 
import re

#reads alignment info from water_to_PreEdited.sh and filters out reads that are a good match to the pre_edited DB


#lists to store things in later 
pipes = []
dna_length = []
headers = []
dna_seq = []
coordinates1 = []
coordinates2 = []
grna = []
gene = []

#pattern for identifying the alignemnt 
pattern =  re.compile(r'\||:|\.')


#read in the alignment output from EMBOSS water
for line in sys.stdin:
	if '#' in line: continue 				#ignore comments in the alignment 
	if pattern.findall(line):
		pipes.append(line.count(':')+line.count('|'))	#identify all matches and count them
	if 'Tb' in line:
		if '#' in line: continue 			#store the portion of the ref seq that matches
		l = line.split()
		dna_length.append(len(l[2]))
		coordinates1.append(l[1])
		gene.append(l[0])
	if 'SEQ' in line:					#store the ID and portion of the query seq that matches
		if '#'  in line:continue
		l = line.split()
		headers.append(l[0])	
		grna.append(l[2])

count_matches = 0
count_reads_that_do_not_match = 0

#collate all the information you have just measured and stored
for p, d,h,c1,g,gene in zip(pipes, dna_length,headers,coordinates1,grna,gene):
	pipes_colons_percent = round(float(p)/float(d)*100, 0)			#calculate the % identity
	if pipes_colons_percent >= 90 and int(d) > 20:				#if the read matches the pre-edited db discard it
		count_matches = count_matches +1 
		print "#%s%s%s%s%s"%(h,d,c1,g,gene)			
	else:
		print "%s \tPC:%s %s %s %s %s"%(h,pipes_colons_percent,c1,d,gene,g)
		count_reads_that_do_not_match = count_reads_that_do_not_match +1




