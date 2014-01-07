#! /usr/bin/python 

#take a read and perform 1000 smith-waterman alignments to test the  significance of a potential gRNA match
#for each read generate a distribution for the randomised alignments, if the real alignment falls outwith this 
#distribution then it is significant and likely to be biologically relevant 

import string
#import sys
import re  
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import itertools
import random
import os,sys
import bisect






#this is a function to shuffle a string 
def Shuffle(string):
	chars  = list(string)
	random.shuffle(chars)
	return ''.join(chars)

#lists to store things later
realALN = []		#list of alignments 
max_perm_score = []	#max score for the randomised alignments
READ_list = []		#list to store the original reads 
scores = []		#to store the 'real' scores 
headers = []		#to store the headers 
perm_scores = []
permALN = []
grna = []

#get the reads (2 lines at a time from sys.stdin) use cat
for line, line2 in itertools.izip_longest(sys.stdin, sys.stdin, fillvalue=''):
	 READ_list.append(line+line2)

#run the first bunch of alignments to get the 'realScores' store the output 
for read in READ_list:
	p1 = subprocess.Popen(["echo",read], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["t_method_perms.sh",read],stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close() 
	output = p2.communicate() 
	realALN.append(output[0])

#this is now the permutation test, take a read and shuffle the sequence send the shuffled seqs to SW_perms.sh get the max score 
	seq  = read.split()
	x=0
	del perm_scores[:]
	while x<1000:
		perm = seq[0]+'_'+str(x)+'\n'+Shuffle(seq[1])
		p3  = subprocess.Popen(["echo",perm], stdout=subprocess.PIPE)
		p4 =  subprocess.Popen(["t_method_perms.sh",perm],stdin=p3.stdout, stdout=subprocess.PIPE)
		p3.stdout.close()
		output2 = p4.communicate()
		#permALN.append(output2[0])		
		p = output2[0].split()
		perm_scores.append(p[1])
		x = x+ 1

#get the scores and the headers from the real alignments 
for line in realALN:
	l = line.split()
	scores.append(l[1])
	headers.append(l[2])
	grna.append(l[7])

#for p in perm_scores:print p 

#print the scores and the headers from the real alignments 
for s,h,ps,g in zip(scores, headers,perm_scores,grna):
	perm_scores = [float(x) for (x) in perm_scores]
	perm_scores.sort()

	index_for_score = bisect.bisect(perm_scores, float(s))
	test_index = float(index_for_score)/1000 
	if test_index<=0.99:
		print "#this alignment is not significant and has a low score %s_%s_%s"%(h,s,str(test_index))
	else:
		print ">%s %s_%s\n%s"%(h,s,str(test_index),g)
