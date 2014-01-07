#!/bin/bash

#smith-waterman alignments to pre-edited maxicircle genes  

while read line; do read second
    printf "%b\n" "$line" "$second"|water -filter yes -bsequence /home/sinclaircooper/grna_extraction/unedited_maxi/unedited_maxiOneseq.fa -datafile /home/sinclaircooper/t_shell/t_matrix.txt -gapopen 100 -gapextend 10 -awidth3 100 -aformat pair 
done < $1 
