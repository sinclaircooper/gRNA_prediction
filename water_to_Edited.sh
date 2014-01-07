#!/bin/bash

#smith-waterman alignments for reads to edited maxicircle genes

while read line; do read second
    printf "%b\n" "$line" "$second"|water -filter yes -bsequence /home/sinclaircooper/grna_extraction/edited_dna_1seq.fa -datafile /home/sinclaircooper/t_shell/t_matrix.txt -gapopen 100 -gapextend 10 -awidth3 200 -aformat pair
done < $1 
