#!/usr/bin/env python

import sys

# Data in .var file
DVAR = {}
fvar = open(sys.argv[1]+".var")
l = fvar.readline()
while l!= "":
    ll = l.split()
    # Get chromosome_position
    ident = ll[0]+"_"+ll[1]
    # Get the whole entry except the last character (new line)
    DVAR[ident] = l[:-1]
    l = fvar.readline()
fvar.close()

# Data in VCF file
DVCF = {}
fvcf = open(sys.argv[1]+".vcf")
l = fvcf.readline()
while l!= "":
    ll = l.split()
    # Get qualities of variant
    q0 = int(ll[4][1:-1].split('/')[0])
    q1 = int(ll[4][1:-1].split('/')[1])
	# If the quality meets threshold, add it to the dataset to compare
    if q0 >= 5 and q1 < 200:
    	# Get chromosome_position
        ident = ll[0]+"_"+ll[1]
        # Get the whole entry except the new line character
        DVCF[ident] = l[:-1]
    l = fvcf.readline()
fvcf.close()

# true positive and false negative substitution
# create output files

ftp = open(sys.argv[1]+".tp","w")
ffn = open(sys.argv[1]+".fn","w")
# Lee-way in variant position
delta = 20
TP = 0
FN = 0
for x in DVAR:
	# Get the chromosome number
    ns = int(x.split('_')[0])
    # Get the variant position
    ix = int(x.split('_')[1])
    ok = False
    # Iterate through other file's variants until a match is found or until lee-way is reached
    for i in range(ix-delta,ix+delta):
        ident = str(ns)+"_"+str(i)
        # If a variant is found in the other file, then stop there
        if ident in DVCF:
            ok = True
            break
    # If variant in that position is found, count a true positive
    if ok == True:
        TP = TP+1
        ftp.write(DVAR[x]+"\n")
    # Otherwise, if no variant is found in the VCF file, count a false negative
    else:
        FN = FN+1
        ffn.write(DVAR[x]+"\n")
ftp.close()
ffn.close()

# false positives
# Do the same as above but vice-versa
ffp = open(sys.argv[1]+".fp","w")
FP = 0
for x in DVCF:
    ns = int(x.split('_')[0])
    ix = int(x.split('_')[1])
    ok = False
    for i in range(ix-delta,ix+delta):
        ident = str(ns)+"_"+str(i)
        if ident in DVAR:
            ok = True
            break
    if ok == False:
        FP = FP+1
        ffp.write(DVCF[x]+"\n")
ffp.close()

# Output results to file
ff = open(sys.argv[1]+".qlt","w")
ff.write("TP: "+str(TP)+" "+str((TP*100.0)/len(DVAR))+"\n")
ff.write("FN: "+str(FN)+" "+str((FN*100.0)/len(DVAR))+"\n")
ff.write("FP: "+str(FP)+" "+str((FP*100.0)/len(DVAR))+"\n")
ff.write("Len VAR: "+str(len(DVAR))+"\n")
ff.write("Len VCF: "+str(len(DVCF))+"\n")
ff.close()

# Output results to console
print("TP",TP, (TP*100.0)/len(DVAR))
print("FN",FN, (FN*100.0)/len(DVAR))
print("FP",FP, (FP*100.0)/len(DVAR))
print("Len VCF", len(DVCF))
print("Len VAR", len(DVAR))

