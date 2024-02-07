#!/bin/bash

query_file=$1
fna_location=$2
bed_location=$3
match_output_file=$4

ls $bed_location | grep bed | grep -Po "[\w_-]+(?=\.)" | sort -r > filenames.txt
# cat filenames.txt

while read -r filename; do 
	    echo -n "[$(date)] $filename identified gene count: " # [$(date -u)] 
	        
	        variant_outfile="$filenames.txt"

		        tblastn \
				    -query "$query_file" \
				        -subject "$fna_location/$filename.fna" \
					    -outfmt '6 std qlen' \
					        -task tblastn-fast \
						    | awk '$3>30 && $4>0.9*$13' > temp_hits.txt

			    while read -r line; do
				            gene_name=$(echo "$line" | cut -f4)
					           match_start=$(echo "$line" | cut -f2)
						            match_end=$(echo "$line" | cut -f3)

							            while read -r code; do
									                hit_start=$(echo "$code" | cut -f9)
											            hit_end=$(echo "$code" | cut -f10)
												                if (( $hit_start >= $match_start && $hit_end <= $match_end )); then
															                echo "$gene_name"
																	                break
																			            fi
																				            done < temp_hits.txt
																					        done < "$bed_location/$filename.bed" | sort -u > "$variant_outfile"

																						    echo "$(wc -l $variant_outfile). For more details do cat $variant_outfile"
																					    done < "filenames.txt"

																					    # cat $outfile

																					    # clean up
																					    rm temp_hits.txt
																					    rm filenames.txt

