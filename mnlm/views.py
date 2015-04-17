from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render

from models import expr
from models import proc
from models.utils import stop

import random

import sys
sys.path.append("/home/pzy/im2txtDemo/mnlm/models")
(z, zt) = proc.process()
net = stop.load_model('mnlm/models/models/mlbl.pkl')

# Create your views here.
def index(request):
	if 'im_index' in request.POST:
		ret = redirect('description', im_index=int(request.POST['im_index']))
	else:
		ret = redirect('description', im_index=0)
	return ret

def description(request, im_index):
	global z, zt, net
	retr_desc = expr.im2txt(net, z, zt['IM'][int(im_index)], k=3, shortlist=15)
	gen_desc = expr.generate(net, z, im=zt['IM'][int(im_index)]).replace('<end>', '').split(';')
	gen_desc = [de+';' for de in [d.strip() for d in gen_desc] if de]
	im_path = expr.get_im_path([int(im_index)], "/static/iaprtc12/images/")
	ran_im_index = range(len(zt['IM']))
	random.shuffle(ran_im_index)
	ran_im_path = expr.get_im_path(ran_im_index[:9], "/static/iaprtc12/images/")
	return render(request, 'description.html', {
		"retr_desc": retr_desc,
		"gen_desc": gen_desc,
		"im_path": im_path[0],
		"ran_im_dict": zip(ran_im_index[:9], ran_im_path), 
		"cur_index": im_index,
		})

def diffinitresults(request):
	IM_PATH = "/static/iaprtc12/images/"
	BANK_RESULT = "mnlm/models/bank-init-results.txt"
	SIMILAR_RESULT = "mnlm/models/similar-init-results.txt"

	im_path = expr.get_im_path(range(len(zt['IM'])), IM_PATH)
	f = open(BANK_RESULT, "rb")
	bank_results = f.readlines()
	f.close()

	f = open(SIMILAR_RESULT, "rb")
	similar_results = f.readlines()
	f.close()

	table = zip(im_path, bank_results, similar_results)
	print table
	return render(request, 'diffinitresults.html', {
		"table": table
		})
