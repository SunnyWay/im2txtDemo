from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render

from engine import expr
from engine import proc
from engine.utils import stop

from .models  import DiffInitEval

import random

import sys
import os
sys.path.append( os.getcwd() + "/mnlm/engine")
(z, zt) = proc.process()
net = stop.load_model('mnlm/engine/models/mlbl.pkl')

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
	BLANK_RESULT = "mnlm/engine/blank-init-results.txt"
	SIMILAR_RESULT = "mnlm/engine/similar-init-results.txt"

	im_path = expr.get_im_path(range(len(zt['IM'])), IM_PATH)
	f = open(BLANK_RESULT, "rb")
	blank_results = f.readlines()
	f.close()

	f = open(SIMILAR_RESULT, "rb")
	similar_results = f.readlines()
	f.close()

	blank_results = [ l.strip().replace("<end>", "").split(";") for l in blank_results ]
	blank_results = [ [ s.strip() +'.' for s in cap if s.strip() ] for cap in blank_results ]

	similar_results = [ l.strip().replace("<end>", "").split(";") for l in similar_results ]
	similar_results = [ [ s.strip() +'.' for s in cap if s.strip() ] for cap in similar_results ]

	table = zip(im_path, blank_results, similar_results)
	return render(request, 'diffinitresults.html', {
		"table": table,
		})

def evaldiffinit(request):
	IM_PATH = "/static/iaprtc12/images/"
	BLANK_RESULT = "mnlm/engine/blank-init-results.txt"
	SIMILAR_RESULT = "mnlm/engine/similar-init-results.txt"

	index = random.randint(0, len(zt['IM'])-1)
	im_path = expr.get_im_path([index],  IM_PATH)[0]

	f = open(BLANK_RESULT, "rb")
	blank = f.readlines()[index]
	f.close()

	f = open(SIMILAR_RESULT, "rb")
	similar = f.readlines()[index]
	f.close()

	blank = blank.replace('<end>', '').split(';')
	blank = [ s.strip() + '.' for s in blank if s.strip() ]

	similar = similar.replace('<end>', '').split(';')
	similar = [ s.strip() + '.' for s in similar if s.strip() ]

	return render(request, 'evaldiffinit.html', {
		"index": index,
		"im_path": im_path,
		"blank": blank,
		"similar": similar,
		})

def evaldiffinitvote(request, im_index, vote):
	q = DiffInitEval.objects.get(im_index=int(im_index))
	if q :
		if vote == '0':
			q.blank = q.blank + 1
		elif vote == '1':
			q.equ = q.equ + 1
		elif vote == '2':
			q.similar = q.similar + 1
		q.save()
	return redirect('evaldiffinit')
