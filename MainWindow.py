# -*- coding:utf-8 -*-
__author__="KenLee"
__email__="ken_4000@qq.com"

try:
	#python 2.x
	import Tkinter as Tkinter
except ImportError:
	#python 3.x
	import tkinter as Tkinter
import os
import sys
import imp



class MainWindow(object):
	"""docstring for MainWindow"""
	def __init__(self):
		super(MainWindow, self).__init__()
		self.funcsDict = {}

	def loadFunction(self,path):
		self.funcsDict={}
		self.loadFunctionRec(path,self.funcsDict)
		pass

	def testFunctions(self):
		self.testRec(self.funcsDict)
		pass


	def loadFunctionRec(self,path,nowDict):
		fileList=os.listdir(path)
		for fileName in fileList:
			filePath=os.path.join(path,fileName)
			if os.path.isdir(filePath):
				#如果是目录
				nowDict[fileName]={}
				self.loadFunctionRec(filePath,nowDict[fileName])
			else:
				#如果是文件
				if fileName.endswith('py'):
					moduleName=fileName[0:-3]
					nowDict[fileName[0:-3]]=[fileName[0:-3],imp.load_module(moduleName,*imp.find_module(moduleName,[path]))]
		pass

	def testRec(self,nowDict):
		if isinstance(nowDict,dict):
			for k in nowDict.keys():
				self.testRec(nowDict[k])
		else:
			if nowDict[0][0:4]=="test":
				nowDict[1].process()
		pass

	def createMenuBarRec(self,nowDict,nowMenu):
		if isinstance(nowDict,dict):
			pass
		pass
		




def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	mw.testFunctions()
	print(mw.funcsDict)
	#rootTk=Tkinter.Tk()
	#menubar=Tkinter.Menu(rootTk)
	#fileMenu=Tkinter.Menu(menubar,tearoff=0)
	#menubar.add_cascade(label="File",menu=fileMenu)

	#rootTk.config(menu=menubar)
	#rootTk.mainloop()
	pass



if __name__ == '__main__':
	main()