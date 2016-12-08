import numpy as np

def process(params):
	images= params["image"];
	maxcol = 0
	HistList = np.zeros (256) 
	img = np.zeros((256,256,3),np.int)
	for row in range(len(images)):
		for  col in range(len(images[0])):
			s = (int(images[row][col][0])+int(images[row][col][1])+int(images[row][col][2]))
			images[row][col][0] =images[row][col][1] =images[row][col][2] = s/3
			HistList[s/3] +=1
	print(images)
	for i in range(256):
		maxcol =  max(HistList[i],maxcol)
	for row in range(256):
		hight = (int)(HistList[row]*(256/maxcol))
		print(HistList[row],maxcol,hight)
		for col in range(256-hight,256):
			img [row][col][0] =128
			img [row][col][1] = 0
			img [row][col][2] = 0
	print(img)
	params["image"] = img 
	params["mode"] = "L"
	pass