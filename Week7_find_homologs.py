#!/usr/bin/env python3
import sys

blastfile = sys.argv[1]
bedfile = sys.argv[2]

# read blast file
hits = []
with open(blastfile) as fin:
    for line in fin: # .readlines() is the default iter method for the open file class
        
        # unpack and convert types of desired columns. This is ugly. We'll revisit later...
        _, sid, pcnt, matchlen, _, _, _, _, sstart, send, _, _, qlen = line.split()
        pcnt = float(pcnt)
        matchlen = int(matchlen)
        sstart = int(sstart)
        send = int(send)
        qlen = int(qlen)
    
        # Keep hits that could be homologs
        if pcnt > 30 and matchlen > 0.9*qlen:
            # We could store matches as a list or tuple.
            # We won't want to modify the elements so a tuple is "safer" in that we then can't modify it by mistake
            hits.append((sid, sstart, send))

# Now read the bed file
feats = []
with open(bedfile) as fin:
    for line in fin:
        bed_sid, bed_start, bed_end, gene, *_ = line.split() # an asterisk before a variable name when unpacking makes that variable store remaining elements
        bed_start = int(bed_start)
        bed_end = int(bed_end)
        
        feats.append((bed_sid, bed_start, bed_end, gene))

# Now we have our two datasets read in, we can loop over them to find matches
homologs = []
for blast_sid, blast_sstart, blast_send in hits: # unpack our blast data
    for bed_sid, bed_start, bed_end, gene in feats:
        # Don't bother checking the rest if the sid doens't match
        if blast_sid != bed_sid:
            continue
        
        # Once we are dealing with features at higher index locations than our hit, go to the next hit (break loop over feats)
        if blast_sstart <= bed_start or blast_send <= bed_start:
            break
        
        # Otherwise, check if the hit is inside the feature
        if (blast_sstart > bed_start
            and blast_sstart <= bed_end
            and blast_send > bed_start
            and blast_send <= bed_end
        ):
            homologs.append(gene)
            break # Each BLAST hit will only be in one feature so move to next hit once you've found it

# Get the unique homologs using a set()
unique_homologs = set(homologs)

print(len(unique_homologs))


