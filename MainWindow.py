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
		self.funcsDict = {}
		pass

	def loadFunction(self,path):
		self.funcsDict={}
		self.__loadFunctionRec(path,self.funcsDict)
		print(self.funcsDict)
		pass

	def testFunctions(self):
		self.__testRec(self.funcsDict)
		pass


	def createMenuBar(self):
		self.rootTk=Tkinter.Tk()
		self.menubar=Tkinter.Menu(self.rootTk)
		self.__createMenuBarRec(self.funcsDict,self.menubar)
		print("done!",self.menubar)
		self.rootTk.config(menu=self.menubar)
		pass

	def show(self):
		self.rootTk.mainloop()
		pass

	def __loadFunctionRec(self,path,nowDict):
		fileList=os.listdir(path)
		for fileName in fileList:
			filePath=os.path.join(path,fileName)
			if os.path.isdir(filePath) and (not filePath.endswith("__")):
				#如果是目录
				nowDict[fileName]={}
				self.__loadFunctionRec(filePath,nowDict[fileName])
			else:
				#如果是文件
				if fileName.endswith('py'):
					moduleName=fileName[0:-3]
					nowDict[moduleName]=imp.load_module(moduleName,*imp.find_module(moduleName,[path]))
		pass

	def __testRec(self,nowDict):
		for key in nowDict.keys():
			if isinstance(nowDict[key],dict):
				self.__testRec(nowDict[key])
			else:
				nowDict[key].process();

		pass

	def __createMenuBarRec(self,nowDict,nowMenu):
		for key in nowDict.keys():
			if isinstance(nowDict[key],dict):
				print(key," is dict")
				newMenu=Tkinter.Menu(nowMenu,tearoff=0)
				nowMenu.add_cascade(label=key,menu=newMenu)
				self.__createMenuBarRec(nowDict[key],newMenu)
			else:
				print(key," is module")
				nowMenu.add_command(label=key,command=nowDict[key].process)
		
		pass

def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	mw.createMenuBar()
	mw.show()
	pass



if __name__ == '__main__':
	main()