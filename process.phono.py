# encoding: utf-8

import json

IPA_MAP = {
	u'∅'	: None,
	'p'		: "voiceless bilabial stop",
	'b'		: "voiced bilabial stop",
	u'pʰ'	: "aspirated voiceless bilabial stop",
	u'bʱ'	: "aspirated voiced bilabial stop", # glottal sign
	't'		: "voiceless alveolar stop",
	'd'		: "voiced alveolar stop",
	u'dʱ'	: "aspirated alveolar stop", # glottal sign
	'f'		: "voiceless labiodental fricative",
	'v'		: "voiced labiodental fricative",
	u'tʰ'	: "aspirated voiceless alveolar stop",
	u'θ'	: "voiceless dental fricative",
	u'ð'	: "voiced dental fricative",
	'h'		: "voiceless glottal fricative",
	'c'		: "voiceless palatal stop",
	u'ʦ'	: "voiceless alveolar affricate",
	u'ʤ'	: "voiced alveolar affricate",
	'k'		: "voiceless velar stop",
	u'kʰ'	: "aspirated voiceless velar stop",
	'g'		: "voiced velar stop",
	u'ʃ'	: "voiceless palato-alveolar fricative",
	u'ʒ'	: "voiced palato-alveolar fricative",
	's'		: "voiceless alveolar fricative",
	'z'		: "voiced alveolar fricative",
	u'ɕ'	: "voiceless alveolo-palatal fricative",
	'x'		: "voiceless velar fricative",
	u'ʣ'	: "voiced alveolar affricate",
	u'ɦ'	: "voiced glottal fricative",
	u'ʧ'	: "voiceless postalveolar affricate",
	u'ɟ'	: "voiced palatal stop",
	u'gʱ'	: "aspirated voiced velar stop", # glottal sign
	u'kʷ'	: "labialized voiceless velar stop",
	u'hʷ'	: "labialized voiceless glottal fricative",
	'ku'	: "vocalized voiceless velar stop",
	'w'		: "labiovelar approximant",
	u'ʂ'	: "voiceless retroflex fricative",
	'j'		: "palatal approximant",
	'y'		: "close front round vowel",
	u'ʋ'	: "labiodental approximant",
	'm'		: "bilabial nasal",
	'n'		: "alveolar nasal",
	u'ɲ'	: "palatal nasal",
	'l'		: "alveolar lateral approximant",
	'r'		: "alveolar trill",
}

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
			pie = '*%s' % fields[0]
			
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
				row_name = '%s_%s' % (pie, feat[1:]) # remove '+'
				
				# build logical vector
				v = []
				for r in reflexes:
					v.append('FT'[feat in r])
				lv = ','.join(v)
			
				buffer = '%s,%s' % (row_name, lv)
				print buffer.encode('utf-8')

if __name__ == '__main__':
	run()