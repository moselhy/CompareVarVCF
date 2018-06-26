
import sys

DVAR = {}
fvar = open(sys.argv[1]+".var")
l = fvar.readline()
while l!= "":
    ll = l.split()
    ident = ll[0]+"_"+ll[1]
    DVAR[ident] = l[:-1]
    l = fvar.readline()
fvar.close()

DVCF = {}
fvcf = open(sys.argv[1]+".vcf")
l = fvcf.readline()
while l!= "":
    ll = l.split()
    q0 = int(ll[4][1:-1].split('/')[0])
    q1 = int(ll[4][1:-1].split('/')[1])
    if q0 >= 5 and q1 < 200:
        ident = ll[0]+"_"+ll[1]
        DVCF[ident] = l[:-1]
    l = fvcf.readline()
fvcf.close()

# true positive and false negative substitution

ftp = open(sys.argv[1]+".tp","w")
ffn = open(sys.argv[1]+".fn","w")
delta = 20
TP = 0
FN = 0
for x in DVAR:
    ns = int(x.split('_')[0])
    ix = int(x.split('_')[1])
    ok = False
    for i in range(ix-delta,ix+delta):
        ident = str(ns)+"_"+str(i)
        if ident in DVCF:
            ok = True
            break
    if ok == True:
        TP = TP+1
        ftp.write(DVAR[x]+"\n")
    else:
        FN = FN+1
        ffn.write(DVAR[x]+"\n")
ftp.close()
ffn.close()

# false positive

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

ff = open(sys.argv[1]+".qlt","w")
ff.write("TP: "+str(TP)+" "+str((TP*100.0)/len(DVAR))+"\n")
ff.write("FN: "+str(FN)+" "+str((FN*100.0)/len(DVAR))+"\n")
ff.write("FP: "+str(FP)+" "+str((FP*100.0)/len(DVAR))+"\n")
ff.write("Len VAR: "+str(len(DVAR))+"\n")
ff.write("Len VCF: "+str(len(DVCF))+"\n")
ff.close()

print "TP",TP, (TP*100.0)/len(DVAR)
print "FN",FN, (FN*100.0)/len(DVAR)
print "FP",FP, (FP*100.0)/len(DVAR)
print "Len VCF", len(DVCF)
print "Len VAR", len(DVAR)

