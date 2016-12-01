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
		self.__loadFunctionRec(path,self.funcsDict)
		pass

	def testFunctions(self):
		self.__testRec(self.funcsDict)
		pass


	def __loadFunctionRec(self,path,nowDict):
		fileList=os.listdir(path)
		for fileName in fileList:
			filePath=os.path.join(path,fileName)
			if os.path.isdir(filePath):
				#如果是目录
				nowDict[fileName]={}
				self.__loadFunctionRec(filePath,nowDict[fileName])
			else:
				#如果是文件
				if fileName.endswith('py'):
					moduleName=fileName[0:-3]
					nowDict[fileName[0:-3]]=[fileName[0:-3],imp.load_module(moduleName,*imp.find_module(moduleName,[path]))]
		pass

	def __testRec(self,nowDict):
		if isinstance(nowDict,dict):
			for k in nowDict.keys():
				self.__testRec(nowDict[k])
		else:
			if nowDict[0][0:4]=="test":
				nowDict[1].process()
		pass

	def __createMenuBarRec(self,nowDict,nowMenu):
		if isinstance(nowDict,dict):
			for key in nowDict.keys():
				newMenu=Tkinter.Menu(nowMenu,tearoff=0)
				nowMenu.add_cascade(label=)
		else:
			nowMenu.add_command(label=nowDict[0],command=nowDict[1])
		pass
		
def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	rootTk=Tkinter.Tk()
	menubar=Tkinter.Menu(rootTk)
	fileMenu=Tkinter.Menu(menubar,tearoff=0)
	fileMenu.add_command(label="Cut")
	subMenu=Tkinter.Menu(fileMenu,tearoff=0)
	fileMenu.add_cascade(label="subMenu",menu=subMenu)
	subMenu.add_command(label="subsubs")
	menubar.add_cascade(label="File",menu=fileMenu)

	rootTk.config(menu=menubar)
	rootTk.mainloop()
	pass



if __name__ == '__main__':
	main()