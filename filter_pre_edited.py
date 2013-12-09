#! /usr/bin/python 

import sys 
#import regex
import re

pipes = []
dna_length = []
headers = []
dna_seq = []
coordinates1 = []
coordinates2 = []
grna = []
gene = []

pattern =  re.compile(r'\||:|\.')

for line in sys.stdin:
	if '#' in line: continue
	if pattern.findall(line):
		pipes.append(line.count(':')+line.count('|'))	
	if 'Tb' in line:
		if '#' in line: continue 
		l = line.split()
		dna_length.append(len(l[2]))
		coordinates1.append(l[1])
		gene.append(l[0])
	if 'SEQ' in line:
		if '#'  in line:continue
		l = line.split()
		headers.append(l[0])	
		grna.append(l[2])
count_matches = 0
count_reads_that_do_not_match = 0

for p, d,h,c1,g,gene in zip(pipes, dna_length,headers,coordinates1,grna,gene):
	pipes_colons_percent = round(float(p)/float(d)*100, 0)
	if pipes_colons_percent >= 90 and int(d) > 20:
		count_matches = count_matches +1 
		print "#%s%s%s%s%s"%(h,d,c1,g,gene)		
		#print "ident: "+str(pipes_colons_percent)	
	else:
		print "%s \tPC:%s %s %s %s %s"%(h,pipes_colons_percent,c1,d,gene,g)
		count_reads_that_do_not_match = count_reads_that_do_not_match +1
		#print "ident: "+str(pipes_colons_percent)
#print "#reads that match target seqs = %s"%(count_matches)
#print "#reads that do not match target seqs = %s"%(count_reads_that_do_not_match)



