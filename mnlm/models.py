from django.db import models

class DiffInitEval(models.Model):
	im_index = models.IntegerField(default=0)
	blank = models.IntegerField(default=0)
	similar = models.IntegerField(default=0)
	equ = models.IntegerField(default=0)
	def __unicode__(self):
		return "Image %d" % (self.im_index)