from utils import bleu
from utils import lm_tools
import numpy as np
from utils.similar_init import get_similar_init

def get_bleu(can, ref):
	n1 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=1), n=1)], n=1)
	n2 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=2), n=2)], n=2)
	n3 = bleu.score_cooked([bleu.cook_test(can, bleu.cook_refs([ref], n=3), n=3)], n=3)
	return [n1, n2, n3]

def eval_gen(net, z, benmarks, IM=None, initial=False):
	bleu_scores = np.zeros((len(benmarks), 3))
	for i, ref in enumerate(benmarks):
		ref = ref[5:-1]	# remove <start> and <end>
		#print ' '.join(ref)
		if initial and IM != None:
			nearest, init = get_similar_init(net, z, IM[i], k=1, shortlist=25, context=5)
			init = init[0]
		else:
			init = None

		if IM != None:
			can = lm_tools.sample(net, z['word_dict'], z['index_dict'], num=len(ref), Im=IM[i], initial=init)
			#print ' '.join(can)
		else:
			can = lm_tools.sample(net, z['word_dict'], z['index_dict'], num=len(ref), initial=init)
		bleu_scores[i] = get_bleu(can, ref)
	return bleu_scores

def eval_retr(net, z, benmarks, IM):
	bleu_scores = np.zeros((len(benmarks), 3))
	for i, im in enumerate(IM):
		nearest, cans = lm_tools.im2txt(net, im, z['word_dict'], z['tokens'], z['IM'], k=20, shortlist=25)
		maxbleu = [0,0,0]
		for can in cans:
			tmp = get_bleu(can, benmarks[i])
			if tmp[0] > maxbleu[0]:
				maxbleu = tmp
		bleu_scores[i] = maxbleu
	return bleu_scores

