# encoding: utf-8

import json

def run():
	# read mapping
	handler = file('ipa.json')
	IPA = json.load(handler)
	handler.close()

	# output header
	print 'context,old_irish,latin,old_english,lithuanian,old_church_slavonic,' \
		'albanian,greek,armenian,hittite,avestan,sanskrit,tocharian_b'
	
	# read data
	header = True
	with open('piephono.txt') as handler:
		for line in handler:
			if header:
				header = False
				continue
			
			# clean line -- not really TSV...
			line = line[:-2]
			line = line.decode("utf-8")
			line = line.replace('\t\t\t', '\t')
			line = line.replace('\t\t', '\t')
			fields = line.split('\t')
			
			# first field is reconstructed PIE
			pie = '%s' % fields[0]
			
			# map ie-languagess reflexes
			reflexes = [IPA[f]['features'] for f in fields[1:]]
			reflexes = [r.split(', ') for r in reflexes]
			
			# collect all distinctive features for this context
			used_feats = [ft for r in reflexes for ft in r] # flatten list
			used_feats = [ft for ft in used_feats if ft] # remove empty, if any
			used_feats = set(used_feats) # unique elements
			
			# output logical vectors for each context/feature in the languages
			for feat in used_feats:
				# build row name
				row_name = '%s.%s' % (pie, feat[1:]) # remove '+'
				
				# build logical vector
				v = []
				for r in reflexes:
					v.append('FT'[feat in r])
				lv = ','.join(v)
				
				buffer = '%s,%s' % (row_name, lv)
				print buffer.encode('utf-8')

if __name__ == '__main__':
	run()