# evaluate model
import sys
import os
import numpy as np
sys.path.append(os.getcwd()+'/mnlm/engine/')
if len(sys.argv) != 5:
	print 'arguments error!'
	sys.exit()

import proc
from evaluate import *
from utils import stop
lbl = stop.load_model('mnlm/engine/models/lbl.pkl')
mlbl = stop.load_model('mnlm/engine/models/mlbl.pkl')
(z, zt) = proc.process()

# generation
if int(sys.argv[1]):
	print '-----------------------generation----------------------------'
	times = int(sys.argv[1])
	max_bleus = np.zeros((len(zt['tokens']),3))
	ave_bleus = np.zeros((1,3))
	for i in range(times):
		tmp = eval_gen(mlbl, z, zt['tokens'], zt['IM'])
		for j in range(len(zt['tokens'])):
			if tmp[j][0] > max_bleus[j][0]:
				max_bleus[j] = tmp[j]
		print 'round %d: max_bleus=%s' %(i, np.mean(max_bleus, axis=0))
		ave_bleus += np.mean(tmp, axis=0)
	ave_bleus /= times
	print "generation: times=%d, ave_bleus=%s" %(times, ave_bleus)

# retrieval
if int(sys.argv[2]):
	print '----------------------retrieval------------------------------'
	bleus = eval_retr(mlbl, z, zt['tokens'], zt['IM'])
	print "retrieval: bleus=%s" %(np.mean(bleus, axis=0))

# lbl generation
if int(sys.argv[3]):
	print '---------------------lbl generation---------------------------'
	times = int(sys.argv[3])
	max_bleus = np.zeros((len(zt['tokens']), 3))
	ave_bleus = np.zeros((1,3))
	for i in range(times):
		tmp = eval_gen(lbl, z, zt['tokens'])
		for j in range(len(zt['tokens'])):
			if tmp[j][0] > max_bleus[j][0]:
				max_bleus[j] = tmp[j]
		print 'round %d: max_bleus=%s' %(i, np.mean(max_bleus, axis=0))
		ave_bleus += np.mean(tmp, axis=0)
	ave_bleus /= times
	print 'lbl generation: times=%d, ave_bleus=%s' %(times, ave_bleus)

# generation with similar initial
if int(sys.argv[4]):
	print '---------------------generation with similar initial-------------------'
	times = int(sys.argv[4])
	max_bleus = np.zeros((len(zt['tokens']), 3))
	ave_bleus = np.zeros((1,3))
	for i in range(times):
	        tmp = eval_gen(mlbl, z, zt['tokens'], zt['IM'], initial=True)
	        for j in range(len(zt['tokens'])):
	                if tmp[j][0] > max_bleus[j][0]:
	                        max_bleus[j] = tmp[j]
	        print 'round %d: max_bleus=%s' %(i, np.mean(max_bleus, axis=0))
	        ave_bleus += np.mean(tmp, axis=0)
	ave_bleus /= times
	print 'generation with similar initial: times=%d, ave_bleus=%s' %(times, ave_bleus)
