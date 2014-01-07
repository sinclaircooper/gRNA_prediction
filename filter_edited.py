#! /usr/bin/python

#reads alignment output from water_to_Edited.sh and filters out low quality alignments
#the output is a modified gff3 ready for viewing in JBrowse

import sys 
#import regex
import re	
sys.stdout.flush()


pipes = []
dna_length = []
headers = []
coordinates1 = []
grna = []
gene = []
db_seq = []
pipe_col = []

#get the complement
def complement(sequence):
	complement = {'A':'T','C':'G','G':'C','T':'A'}
	return "".join([complement.get(nt.upper(), '') for nt in sequence])

#replace Ts with Us 
def t_2_u(sequence):
	sequence2 = sequence.replace('t', 'u') 
	return sequence2.replace('T','U')	

#function to get the leftmost mapping coordinate and return the corresponding gene 
def lookup(coordinate):							
	if 0 <= coordinate <= 325: g = "Tbrps12ed" 
	elif 325 < coordinate <= 972: g = "Tbnd9ed"
	elif 972 < coordinate <= 1546: g = "Tbnd8ed"
	elif 1546 < coordinate <= 2792: g = "Tbnd7ed"
	elif 2792 < coordinate <= 3257: g = "Tbnd3ed"
	elif 3257 < coordinate <= 4077: g = "Tba6ed"
	elif 4077 < coordinate <= 5185: g = "Tbmurf2ed"
	elif 5185 < coordinate <= 6337: g = "Tbcybed"
	elif 6337 < coordinate <= 6905: g = "Tbcr4ed"
	elif 6905 < coordinate <= 7205: g = "Tbcr3ed"
	elif 7205 < coordinate <= 8175: g = "Tbco3ed"
	elif 8175 < coordinate <= 8853: g = "Tbco2ed"    
	return g

#function to take the leftmost mapping coordinate and return the corresponding coordinte within the 'real gene'
def position(coordinate):
	if 0 <= coordinate <= 325: c = coordinate 
	elif 325 < coordinate <= 972: c = coordinate - 325
	elif 972 < coordinate <= 1546: c = coordinate - 972
	elif 1546 < coordinate <= 2792: c = coordinate - 1546
	elif 2792 < coordinate <= 3257: c = coordinate - 2792
	elif 3257 < coordinate <= 4077: c = coordinate - 3257
	elif 4077 < coordinate <= 5185: c = coordinate - 4077
	elif 5185 < coordinate <= 6337: c = coordinate - 5185
	elif 6337 < coordinate <= 6905: c = coordinate - 6337 
	elif 6905 < coordinate <= 7205: c = coordinate - 6905
	elif 7205 < coordinate <= 8175: c = coordinate - 7205
	elif 8175 < coordinate <= 8853: c = coordinate - 8175
	return c

#caluculate the % pipes and colons - proxy for identity match
def percent(colon, len_seq):
	pc = round(float(colon)/float(len_seq)*100)		 
	return pc

pattern =  re.compile(r'\||:|\.')

#get coordinate 2 for mapping purposes 
def get_C2(c1,len_seq):			
	c2 = c1 + len_seq
	return c2

#pipe in the alignment and split the required lines into lists 
for line in sys.stdin:
	if '#' in line: continue
	if pattern.findall(line):
		pipes.append(line.count(':')+line.count('|'))
		pipe_col.append(line.replace(" ","").strip(),)
	if 'edited' in line:
		#if '#' in line: continue 			 
		l = line.split()				
		dna_length.append(len(l[2]))			#get the length of the seq 
		coordinates1.append(position(int(l[1])))	#get the coordinates and send them to the position function 
		gene.append(lookup(int(l[1])))			#get the coodintes and send them to lookup function 	
		db_seq.append(l[2])	
	if 'SEQ' in line:
		#if '#'  in line:continue
		l = line.split()
		headers.append(l[0])				#get the read header 
		grna.append(l[2])				#get query seq 
count_matches = 0
count_reads_that_do_not_match = 0
pc_pc  = []

#combine all of the lists you  have made and test the alignment for identity
for pipe, d,h,c1,g,gene,db,pc in zip(pipes, dna_length,headers,coordinates1,grna,gene,db_seq,pipe_col):	 
	if percent(pipe,d) > 85 and int(d) > 25:
		if '-' in db+g: print '#'+h+' has gaps in the db/g'
		else:
			count_matches = count_matches +1  			# format the output into modified gff if the match is good 
			print '%s\t.\tmRNA\t%s\t%s\t%s\t.\t.\tID=%s;>Alignment=<Font Face="Courier New">%s mRNA<br>%s<br>%s gRNA<FONT>'%(gene,c1,(get_C2(c1, len(g))),percent(pipe,d),h,t_2_u(db),pc,t_2_u(complement(g)))	
		#print "ident: "+str(pipes_colons_percent)	
	else:
		print "#no_match>%s PC:%s %s %s %s\n#%s"%(h,percent(pipe,d),c1,str(d),gene,g) # otherwise just print some info about the read that failed 
		count_reads_that_do_not_match = count_reads_that_do_not_match +1
		#print "ident: "+str(pipes_colons_percent)

#small summary of matches and non-matches
print "@reads that match target seqs = %s"%(count_matches)
print "@reads that do not match target seqs = %s"%(count_reads_that_do_not_match)
print '@',str(len(pipes)), str(len(headers))


