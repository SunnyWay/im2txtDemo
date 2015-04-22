from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render

from engine import expr
from engine import proc
from engine.utils import stop

from .models  import DiffInitEval

import random
import time

import Image

import h5py

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

	return render(request, 'description.html', {
		"retr_desc": retr_desc,
		"gen_desc": gen_desc,
		"im_path": im_path[0],
		"ran_im_dict": get_rand_ims(), 
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

def uploaddesc(request):
	# save the upload image
	print 'save upload image to /mnlm/static/upload/\n'
	upload_im = request.FILES['upload_im']
	im = Image.open(upload_im)
	fname = get_time_stamp()
	full_name = os.getcwd() + '/mnlm/static/upload/' + fname
	im.save( full_name + '.jpg', "JPEG")

	# save the upload image path to file
	print 'save upload image path to' + fname + '_path.txt\n'
	outfile = open(full_name+'_path.txt', 'wb')
	for i in range(10):
		outfile.write(full_name+'.jpg'+'\n')
	outfile.close()

	# modify feature_config.pbtxt
	print 'modify feature_config.pbtxt\n'
	infile = open(os.getcwd()+'/mnlm/static/upload/feature_config.pbtxt','rb')
	contents = infile.readlines()
	infile.close()
	for index, line in enumerate(contents):
		if line.find('output_file') != -1:
			contents[index] = 'output_file: "' + full_name + '.h5"\n'
			continue
		if line.find('file_pattern') != -1:
			contents[index] = '    file_pattern: "' + full_name + '_path.txt"\n'
			continue
		if line.find('mean_file') != -1:
			contents[index] = '    mean_file: "' + os.getcwd() +'/mnlm/static/upload/pixel_mean.h5"\n'
			continue
	outfile = open(full_name+'_config.pbtxt', 'wb')
	outfile.writelines(contents)
	outfile.close()

	# extract image feature
	print 'extract image feature\n'
	os.system('extract_representation --board=0 --model=' + os.getcwd() + '/mnlm/static/upload/CLS_net_20140621074703.pbtxt --feature-config='+full_name+'_config.pbtxt')

	# read image feature
	print 'read image feature\n'
	im_fea = h5py.File(full_name+'.h5', 'r')['hidden7'].value

	# describe
	print 'get description\n'
	retr_desc = expr.im2txt(net, z, im_fea[0], k=3, shortlist=15)
        gen_desc = expr.generate(net, z, im=im_fea[0]).replace('<end>', '').split(';')
        gen_desc = [de+';' for de in [d.strip() for d in gen_desc] if de]
	
	print 'done\n'
	return render(request, 'description.html', {
		"retr_desc": retr_desc,
		"gen_desc": gen_desc,
		"im_path":  '/static/upload/'+fname + '.jpg',
		"ran_im_dict": get_rand_ims(), 
		"cur_index": 0,
		})


def get_time_stamp():
	prefix = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
	suffix = ('0000'+str(int(random.random()*10000)))[-4:]
	return prefix+suffix

def get_rand_ims():
	ran_im_index = range(len(zt['IM']))
	random.shuffle(ran_im_index)
	ran_im_path = expr.get_im_path(ran_im_index[:9], "/static/iaprtc12/images/")
	return zip(ran_im_index[:9], ran_im_path)
