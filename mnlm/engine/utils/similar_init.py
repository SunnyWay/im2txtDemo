from lm_tools import im2txt

def get_similar_init(net, z, im, k=1, shortlist=15, context=5):
	similar = im2txt(net, im, z['word_dict'],z['tokens'],z['IM'],
		k=k, shortlist=shortlist)
	similar_init = []
	for init in similar:
		if len(init) >= context:
			init = init[:context]
		else:
			init = ['<start>']*context + init
			init = init[-context:]
		similar_init.append(init)
	return similar_init