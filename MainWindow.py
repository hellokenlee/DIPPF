# -*- coding:utf-8 -*-
__author__="KenLee"
__email__="ken_4000@qq.com"

import Tkinter
import os
import sys
import imp

funcsDict={}
def loadFunctionRec(path,nowDict):
	fileList=os.listdir(path)
	for fileName in fileList:
		filePath=os.path.join(path,fileName)
		if os.path.isdir(filePath):
			#如果是目录
			nowDict[fileName]={}
			loadFunctions(filePath,nowDict[fileName])
		else:
			#如果是文件
			if fileName.endswith('py'):
				moduleName=fileName[0:-3]
				nowDict[fileName[0:-3]]=imp.load_module(moduleName,*imp.find_module(moduleName,[path]))
	pass

def testRec(nowDict):
	if isinstance(nowDict,dict):
		for k in nowDict.keys():
			testRec(nowDict[k])
	else:
		nowDict.test()
	pass

def createMenuBarRec(nowDict,nowMenu):
	if isinstance(nowDict,dict):
		
	pass

def main():

	loadFunctionRec(os.path.join(os.path.abspath('.'),"Functions"),funcsDict)
	testRec(funcsDict)

	rootTk=Tkinter.Tk()
	menubar=Tkinter.Menu(rootTk)
	fileMenu=Tkinter.Menu(menubar,tearoff=0)
	menubar.add_cascade(label="File",menu=fileMenu)

	rootTk.config(menu=menubar)
	rootTk.mainloop()
	pass



if __name__ == '__main__':
	main()