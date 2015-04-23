# -*- coding: UTF-8 –*-
import sys
sys.path.append("/home/pzy/im2txtDemo/")

import expr, proc
from utils import stop, lm_tools
import time

test_sample_count = 1962

# 初始化，获得tuples和模型
(z, zt) = proc.process()
net = stop.load_model('models/mlbl.pkl')

def cal():
	start = time.time()
	cal_bank_init()
	end = time.time()
	print 'cal_blank_init: %i' % (end-start)
	start = time.time()
	cal_similar_init()
	end = time.time()
	print 'cal_similar_init: %i' % (end-start)

# 计算以 <start> 为上下文，生成的句子
def cal_bank_init():
	global z, zt, net

	li = []
	global test_sample_count
	for i in range(test_sample_count):
		li.append(expr.generate(net, z, im=zt['IM'][i])+'\n')

	output = open('blank-init-results.txt','wb')
	try:
		output.writelines(li)
	finally:
		output.close()

# 计算以与查询图像相似的图像对应的句子开头的几个单词作为上下文，生成句子
def cal_similar_init():
	global z, zt, net
	context = 5

	li = []
	global test_sample_count
	for i in range(test_sample_count):
		similar = get_similar_init(net,z,zt['IM'][i], context=context)[0]
		li.append(' '.join(similar) + ' ' + expr.generate(net, z, im=zt['IM'][i], init=similar)+'\n')
	
	output = open('similar-init-results.txt', 'wb')
	try:
		output.writelines(li)
	finally:
		output.close()

		
if __name__ == '__main__':
	cal()
	print 'done'
