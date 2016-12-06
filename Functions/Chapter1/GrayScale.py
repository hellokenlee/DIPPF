# -*- coding:utf-8 -*-

# import numpy as np

def process(params):
	img=params["image"]
	for row in range(len(img)):
		for col in range(len(img[0])):
			s=(int(img[row][col][0])+int(img[row][col][0])+int(img[row][col][0]))
			img[row][col][0]=img[row][col][1]=img[row][col][2]=s/3
	# img[:,:,0]=img[:,:,1]=img[:,:,2]=np.sum(img, axis=2)/3
	params["mode"]="L"
	pass
