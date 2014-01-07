#! /bin/bash

#this is a script to map to pre-edited mrna
while read line; do read second
    printf "%b\n" "$line" "$second" | reverse_fasta.py|sed '/^$/d' |water -filter yes -bsequence /home/sinclair/grna_extraction/unedited_maxi/unedited_maxiOneseq.fa -datafile /home/sinclair/grna_extraction/matrix.txt -gapopen 100 -gapextend 10 -awidth3 100 -aformat pair -adesshow3  
done < $1



