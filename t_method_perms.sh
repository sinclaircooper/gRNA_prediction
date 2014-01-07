#!/bin/bash

#shell script that is called by SW_permutations.py 
#does the alignment by calling water 


water -filter yes -bsequence /home/sinclaircooper/grna_extraction/edited_dna_1seq.fa -datafile /home/sinclaircooper/t_shell/t_matrix.txt -gapopen 100 -gapextend 10 -awidth3 200 -aformat pair | tr a-z A-Z | grep -E 'SCORE|READ|EDITED|BRUCEI|SEQ' |grep -v -E '# 1|# 2|/|RUNDATE|REPORT|ALIGNED' |tr -d "#" | awk '{print $1,$2,$3}'

