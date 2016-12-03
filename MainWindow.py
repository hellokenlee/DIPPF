# -*- coding:utf-8 -*-
__author__="KenLee"
__email__="ken_4000@qq.com"

try:
	#python 2.x
	import Tkinter as Tkinter
	import tkFileDialog
except ImportError:
	#python 3.x
	import tkinter as Tkinter
import PIL
import Image,ImageTk
import os
import sys
import imp

class MainWindow(object):
	"""GUI主窗口类"""
	
	#---public:---
	#	构造函数
	def __init__(self):
		self.funcsDict = {}
		self.rootTk=Tkinter.Tk()
		self.rootTk.title("DIP Tools")
		self.menubar=Tkinter.Menu(self.rootTk)
		self.rootTk.config(menu=self.menubar)
		self.createDefaultMenu()
		pass

	#	加载制定目录下的所有模块
	def loadFunction(self,path):
		self.funcsDict={}
		self.__loadFunctionRec(path,self.funcsDict)
		pass

	#	生成默认菜单(文件，编辑)
	def createDefaultMenu(self):
		fileMenu=Tkinter.Menu(self.menubar,tearoff=0)
		fileMenu.add_command(label="Open",command=self.__imageOpen)
		fileMenu.add_command(label="Save",command=self.__imageSave)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit",command=self.__imageSave)
		self.menubar.add_cascade(label="File",menu=fileMenu)

		editMenu=Tkinter.Menu(self.menubar,tearoff=0)
		editMenu.add_command(label="Undo")
		editMenu.add_command(label="Redo")
		self.menubar.add_cascade(label="Edit",menu=editMenu)
		pass

	#	生成动态菜单
	def createMenuBar(self):
		self.__createMenuBarRec(self.funcsDict,self.menubar)
		pass

	#	GUI主循环
	def draw(self):
		self.rootTk.mainloop()
		pass

	#---private:---
	def __imageOpen(self):
		filePath=tkFileDialog.askopenfilename(parent=self.rootTk)
		print("Open Image:",filePath)
		canvas=Tkinter.Canvas(self.rootTk,width=500,height=500)
		canvas.pack(side=Tkinter.TOP,expand=True,fill=Tkinter.BOTH)
		self.pilImg=Image.open(filePath)
		self.pilImg=self.pilImg.resize((300,300),PIL.Image.ANTIALIAS)
		self.tkImg=ImageTk.PhotoImage(self.pilImg)
		self.img=canvas.create_image(100,80,image=self.tkImg)
		
		pass

	def __imageSave(self):
		print("Image Save pressed")
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
		for key in sorted(nowDict.keys()):
			if isinstance(nowDict[key],dict):
				newMenu=Tkinter.Menu(nowMenu,tearoff=0)
				nowMenu.add_cascade(label=key,menu=newMenu)
				self.__createMenuBarRec(nowDict[key],newMenu)
			else:
				nowMenu.add_command(label=key,command=nowDict[key].process)
		
		pass

def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	mw.createMenuBar()
	mw.draw()
	pass



if __name__ == '__main__':
	main()