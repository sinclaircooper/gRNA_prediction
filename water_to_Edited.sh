#!/bin/bash

#this is a script for batch processing all of the potential reads from the rua_1 cutting script


FILES=$1/*
for f in $FILES
do
  echo "#doing alignment for $f"
# take action on each file. $f store current file name
  
  cat "$f" | water -filter yes -bsequence /home/sinclair/grna_extraction/edited_mrna.fa -datafile /home/sinclair/grna_extraction/matrix.txt -gapopen 100 -gapextend 3 -awidth3 100 -aformat pair	

done
#run this script on it's own and you will just get the alignments 
#grep 'Score' will return the score 
#grep score and grna?
