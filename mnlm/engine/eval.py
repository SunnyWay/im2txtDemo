from utils import bleu
from utils import lm_tools
import numpy as np
from utils.similar_init import get_similar_init

def get_bleu(can, ref):
	n1 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=1), n=1)], n=1)
	n2 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=2), n=2)], n=2)
	n3 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=3), n=3)], n=3)
	return [n1, n2, n3]

def eval_gen(net, z, benmarks, IM=None, initial=False, times=1):
	bleu_scores = np.zeros((len(benmarks), 3))
	for j in range(times):
		for i, ref in enumerate(benmarks):
			ref = ref[5:-1]
			#print ' '.join(ref)
			if initial and IM != None:
				init = get_similar_init(net, z, IM[i], k=1, shortlist=25, context=5)[0]
			else:
				init = None

			if IM != None:
				can = lm_tools.sample(net, z['word_dict'], z['index_dict'], num=len(ref), Im=IM[i], initial=init)
				#print ' '.join(can)
			else:
				can = lm_tools.sample(net, z['word_dict'], z['index_dict'], num=len(ref), initial=init)
			tmp = get_bleu(can, ref)
			if tmp[0] > bleu_scores[i][0]:
				bleu_scores[i] = tmp
    	bleu_means = np.mean(bleu_scores, 0)
    	print "round %d: " % j
    	print bleu_means

def eval_retr(net, z, benmarks, IM):
	bleu_scores = np.zeros((len(benmarks), 3))
	for i, im in enumerate(IM):
		nearest, cans = lm_tools.im2txt(net, im, z['word_dict'], z['tokens'], z['IM'], k=5, shortlist=25)
		maxbleu = [0,0,0]
		for can in cans:
			tmp = get_bleu(can, benmarks[i])
			if tmp[0] > maxbleu[0]:
				maxbleu = tmp
		bleu_scores[i] = maxbleu
	bleu_means = np.mean(bleu_scores, 0)
	print bleu_means
		

