#!/usr/bin/python



############################################################
#THE IDEA IS TO CALCULATE AND FILTER IF A 'READ' IS GREATER THAN 80% C OR t
#will also filter out any reads that are more than 50% N
###################################################################

import sys 
import re
count_c = 0
count_t = 0

#def str.count(sub[, start[, end]])


header_list = []
seq_list = []

for line in sys.stdin:
	if '>' in line:
		header_list.append(line) 
	else: 
		seq_list.append(line)	



for header, seq in zip(header_list, seq_list):
	n = seq.count('N') 
	c = seq.count('c')
	C = seq.count('C')
	t = seq.count('t')
	T = seq.count('T')
	c_total = c+C
	t_total = t+T
	length = len(seq[:-1])
	c_percent = c_total*1.0/length
	t_percent = t_total*1.0/length
	n_percent = n*1.0/length 
	if c_percent >= 0.8: continue 
	if t_percent >= 0.8: continue
	if n_percent >= 0.1: continue 
	else: print header, seq[:-1] 

