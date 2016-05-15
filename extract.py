# encoding: utf-8

import pprint
import urllib
import json
#import yaml

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_groups(source):
	idx_a = 0

	groups = []
	while True:
		# get starting index, break if not
		idx_a = source.find('<h3><span', idx_a)
		if idx_a == -1:
			break
		idx_a = source.find('<table', idx_a)
		idx_b = source.find('</table>', idx_a)
		
		# adiciona
		groups.append(source[idx_a:idx_b])
		
	return groups

def parse_derv(d):
	langs = ['Sanskrit', 'Albanian', 'Avestan', 'English', 'German', 'Gothic', 'Old Norse', 'Latin',
		'Old Church Slavonic', 'Russian', 'Macedonian', 'Lithuanian', 'Kamviri', 'Polish',
		'Czech', 'Pashto', 'Tocharian', 'French', 'Spanish', 'Portuguese', 'Umbrian',
		'Ancient Greek', 'Irish', 'Welsh', 'Hittite', 'Persian', 'Old Armenian', 'Old Prussian',
		'Latvian', 'Gaulish', 'Kurdish', 'Kashmiri', 'Phrygian', 'Luwian', 'Serbo-Croatian',
		'Illyr.', 'Oscan', 'Ossetian', 'Serb.', 'Venetic', 'Lydian', 'Thracian', 'Bulgarian',
		'Crimean Gothic', 'Catalan', 'Breton', 'Waziri', 'Ancient Macedonian', 'Ormuri',
		'Lycian', 'Palaic', 'Old Latin', 'Old East Slavic', 'Italian', 'Eastern Baltic', 'Dutch', 
		'Protoslavonic', 'Baltic', 'Greek', 'Old Slavonic', 'Albania', 'Cornish', 'Kashubian',
		'Silesian', 'Serbian', 'Banuci', 'Scottish Gaelic', 'Old English', 'Old High German', 
		'Old Irish', 'Kurdish/Zazaki', 'Dacian', 'Saka', 'Waneci', 'Wakhi', 'Khosti',
		'Low Saxon', ]
	
	r = None
	for lang in langs:
		if d.startswith(lang + ' '):
			if lang == 'Albania':
				lang = 'Albanian'
			if lang == 'Serb.':
				lang = "Serbian"
			r = lang, d[len(lang)+1:]
			break
			
	if r is None:
		print "!!!", [d], d
		#for i, c in enumerate(d):
		#	print i, [c]
		exit()
	
	return r
	
def process_group(source):
	idx_a = source.find('</th>')
	idx_a = source.find('</tr>', idx_a)
	
	lex = {}
	
	while True:
		# get starting index, break if not
		idx_a = source.find('<tr>', idx_a)
		if idx_a == -1:
			break
		idx_b = source.find('</tr>', idx_a)
		
		# processa cada entrada
		entrada = source[idx_a:idx_b]
		tds = entrada.split('</td>')
		
		# pega termo em PIE e traducao
		pie_term = strip_tags(tds[0]).replace('\n', '')
		pie_trad = strip_tags(tds[1]).replace('\n', '')
		
		# CORREÇÕES
		tds[2] = tds[2].replace(u'sūnus, soūns', u'sūnus; soūns')
		tds[2] = tds[2].replace('tuwatar, duttariyata', 'tuwatar; duttariyata')
		tds[2] = tds[2].replace('"pula", meaning "bundle"', '"pula" -- meaning "bundle"')
		tds[2] = tds[2].replace('>unkn</span>),', '>unkn</span>);')
		tds[2] = tds[2].replace('>akn</span>),', '>akn</span>);')
		tds[2] = tds[2].replace('na), both meaning "mouth",', 'na); both meaning "mouth";')
		tds[2] = tds[2].replace('(hanu, meaning "jaw"', '(hanu -- meaning "jaw"')
		tds[2] = tds[2].replace('ru, meaning "moustache"', 'ru -- meaning "moustache"')
		tds[2] = tds[2].replace('), meaning "nape,', '); meaning "nape;')
		tds[2] = tds[2].replace('necklace, collar', 'necklace; collar')
		tds[2] = tds[2].replace('(ulna, ell)', '(ulna; ell)')
		tds[2] = tds[2].replace('"elbow, arm, cubit, ell"', '"elbow; arm; cubit; ell"')
		tds[2] = tds[2].replace(u'‎(aleina,', u'‎(aleina;')
		tds[2] = tds[2].replace(', (meaning "cheek")', '; (meaning "cheek")')
		tds[2] = tds[2].replace(', meaning "nail")', '; meaning "nail")')
		tds[2] = tds[2].replace(', meaning "shoulder")', '; meaning "shoulder")')
		tds[2] = tds[2].replace('nail, fingernail', 'nail; fingernail')
		tds[2] = tds[2].replace('>cunr</span>),', '>cunr</span>);')
		tds[2] = tds[2].replace('il</span>), <i class="Armn mention"', 'il</span>); <i class="Armn mention"')
		tds[2] = tds[2].replace('Lithuanian grasa,', 'Lithuanian grasa;')
		tds[2] = tds[2].replace('a</span>), <i class="Deva', 'a</span>); <i class="Deva')
		tds[2] = tds[2].replace('"limit, end"', '"limit; end"')
		tds[2] = tds[2].replace('(spotted, variegated)', '(spotted; variegated)')
		tds[2] = tds[2].replace('(dust, ashes),', '(dust; ashes);')
		tds[2] = tds[2].replace('(vine, grapes)', '(vine; grapes)')
		tds[2] = tds[2].replace('(rubber, gum)', '(rubber; gum)')
		tds[2] = tds[2].replace('>suk</span>),', '>suk</span>);')
		tds[2] = tds[2].replace('modern: kirminas,', 'modern: kirminas;')
		tds[2] = tds[2].replace('Greek aetos,', 'Greek aetos;')
		tds[2] = tds[2].replace('>oror</span>),', '>oror</span>);')
		tds[2] = tds[2].replace('(gander, goose, swan)', ' (gander; goose; swan)')
		tds[2] = tds[2].replace('Avestan udra,', 'Avestan udra;')
		tds[2] = tds[2].replace(u'Albanian shakë, qen,qan', u'Albanian shakë; qen; qan')
		tds[2] = tds[2].replace('Polish drzwi,', 'Polish drzwi;')
		tds[2] = tds[2].replace('English -wich,', 'English -wich;')

		# pega derivados
		tds[2] = tds[2].replace('\n', '')
		derv = tds[2].split(', ')
		derv = [strip_tags(d) for d in derv]
		
		# separa lingua e conteudo nos derivados
		derv = [parse_derv(d) for d in derv]
		
		# adiciona
		lex[pie_term] = {}
		lex[pie_term]['PIE'] = pie_trad
		for d in derv:
			lex[pie_term][d[0]] = d[1]
		
		# adiciona para proximo loop
		idx_a += 1

	return lex

def my_output(lex):
	entries = lex.keys()
	entries.sort()
	
	buf = ''
	for entry in entries:
		buf += '- %s:\n' % (entry[1:])
		
		buf += '\t- PIE: "%s"\n' % (lex[entry]['PIE'])

		del lex[entry]['PIE']
		langs = lex[entry].keys()
		for lang in langs:
			buf += '\t- %s: "%s"\n' % (lang, lex[entry][lang])
		
	print buf.encode('utf-8')
	
def run():
	# read source
	handler = urllib.urlopen('https://en.wiktionary.org/wiki/Appendix:List_of_Proto-Indo-European_nouns')
	source = handler.read()
	handler.close()
	source = source.decode('utf-8')
	
	# extrai grupos de substantivos
	groups = get_groups(source)
	
	# processa
	lex = {}
	for group in groups:
		group_lex = process_group(group)
		lex.update(group_lex)
		
	#print.pprint(lex)
	#print json.dumps(lex, indent=2)
	#import yaml
	#print yaml.dump(lex, encoding=('utf-8'))
	my_output(lex)

if __name__ == "__main__":
	run()