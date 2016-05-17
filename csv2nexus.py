import csv
import sys
infile = sys.argv[1]

with open(infile) as f:
    reader = csv.reader(f)
    cols = []
    for row in reader:
        cols.append(row)

print "#NEXUS"
print "Begin data;"
print "Dimensions ntax=%i nchar=%i;" % (len(cols)-1, len(cols[0])-1)
print 'Format datatype=Standard missing=- gap=- symbols="01";'
print "Matrix"
for col in cols[1:]: # first line is headers
	species = col[0]
	morph = ''.join(col[1:])
	morph = morph.replace('F', '0')
	morph = morph.replace('T', '1')
	print '%s %s ' % (species, morph)

print ";"
print "End;"		
