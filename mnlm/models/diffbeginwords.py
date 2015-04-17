# -*- coding: UTF-8 –*-
import sys
sys.path.append("/home/p-what/serverCode/im2txtDemo/")

import expr, proc
from utils import stop, lm_tools

test_sample_count = 3 #1962

# 计算以 <start> 为上下文，生成的句子
def cal_bank_init():
	(z, zt) = proc.process()
	net = stop.load_model('models/mlbl.pkl')

	li = []
	global test_sample_count
	for i in range(test_sample_count):
		li.append(expr.generate(net, z, im=zt['IM'][i])+'\n')

	output = open('bank-init-results.txt','wb')
	try:
		output.writelines(li)
	finally:
		output.close()

# 计算以与查询图像相似的图像对应的句子开头的几个单词作为上下文，生成句子
def cal_similar_init():
	(z, zt) = proc.process()
	net = stop.load_model('models/mlbl.pkl')
	context = 5

	li = []
	global test_sample_count
	for i in range(test_sample_count):
		similar = lm_tools.im2txt(net, zt['IM'][i], z['word_dict'], 
			z['tokens'], z['IM'], k=1, shortlist=15)[0]
		if len(similar) >= context:
			similar = similar[:context]
		else:
			similar = ['<start>']*context + similar
			similar = similar[-5:]
		print similar
		li.append(' '.join(similar) + ' ' + expr.generate(net, z, im=zt['IM'][i], init=similar)+'\n')
	
	output = open('similar-init-results.txt', 'wb')
	try:
		output.writelines(li)
	finally:
		output.close()

		
