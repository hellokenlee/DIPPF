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
	import tkinter.filedialog as tkFileDialog
import PIL
from PIL import Image,ImageTk
from functools import partial
import numpy as np
import os
import sys
import imp

class MainWindow(object):
	"""
	GUI主窗口类:
	Methods:
		loadFunction(self,path):
		createDefaultMenu(self):
		createMenuBar(self):
		draw(self):
	Attributes：
		MainWindow.funcsDict : 在./Functions中搜索到的所有模块，字典对象。比如./Functions/Chapter1/Section1/graying.py -> self.funcDict["Chapter1"]["Section1"]["grayping"]
		MainWindow.pilImage : 当前图片对象，PIL Image对象
		MainWindow.tkImage : 当前图片对象的缩略图，用于显示在主窗口中，ImageTk对象
		MainWindow.imageUndoStack : 图片栈，用于处理撤销，list
		MainWindow.imageRedoStack : 图片栈，用于处理重做，list
		MainWindow.rootTk : 主窗口的Tkinter对象
		MainWindow.menubar : 窗口菜单栏的Tkinter对象
		MainWindow.canvas : 图片显示区域的Tkinter对象
		MainWindow.params : 用于各模块process函数的参数传递,dict
	"""
	#	构造函数
	def __init__(self):
		self.funcsDict = {}
		self.pilImg=None
		self.tkImg=None
		self.imageUndoStack=[]
		self.imageRedoStack=[]
		
		self.params={}
		self.params["image"]=np.array([[[0,0,0]]])
		self.params["mode"]="RGB"

		self.rootTk=Tkinter.Tk()
		self.rootTk.geometry("640x480")
		self.rootTk.title("DIP Tools")

		self.canvas=Tkinter.Canvas(self.rootTk)
		self.canvas.pack(side=Tkinter.TOP,expand=True,fill=Tkinter.BOTH)
		self.menubar=Tkinter.Menu(self.rootTk)
		self.rootTk.config(menu=self.menubar)
		self.createDefaultMenu()

		pass
	#---public:---
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
		fileMenu.add_command(label="Exit",command=self.__exit)
		self.menubar.add_cascade(label="File",menu=fileMenu)

		editMenu=Tkinter.Menu(self.menubar,tearoff=0)
		editMenu.add_command(label="Undo",command=self.undo)
		editMenu.add_command(label="Redo",command=self.redo)
		self.menubar.add_cascade(label="Edit",menu=editMenu)
		pass
	#	撤销
	def undo(self):
		pass
	#	重做
	def redo(self):
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
	#	打开图片的回调函数
	def __imageOpen(self):
		#	弹出文件选择框
		filePath=tkFileDialog.askopenfilename(parent=self.rootTk)
		#	处理取消选择
		if not filePath:
			return
		#	打开图片
		self.pilImg=Image.open(filePath)
		self.params["image"]=np.array(self.pilImg)
		self.params["mode"]=self.pilImg.mode
		print("Open Image:"+filePath+"  "+str(self.pilImg.size[0])+" x "+str(self.pilImg.size[1]))
		#	更新显示的图片
		self.__updateShowingImage()
		pass

	#	保存图片的回调函数
	def __imageSave(self):
		#	弹出文件选择框
		if not self.pilImg:
			print("Image Save: Not Open An Image Yet.")
			return
		filePath=tkFileDialog.asksaveasfilename(parent=self.rootTk)
		if not filePath:
			return
		self.pilImg.save(filePath)
		print("Save Image as: "+filePath)
		pass

	#	更新当前显示的图片
	def __updateShowingImage(self):
		#	获取当前图片
		if not self.pilImg:
			return
		tmp=self.pilImg
		tmp.width=self.pilImg.size[0]
		tmp.height=self.pilImg.size[1]
		#	获取窗口大小
		winWidth=self.rootTk.winfo_width()
		winHeight=self.rootTk.winfo_height()
		print("Current Window size:"+str(winWidth)+" x "+str(winHeight))
		#	检查是否要根据窗口大小裁剪
		if  tmp.height > winHeight or tmp.width > winWidth:
			scale=min(float(winHeight)/float(self.pilImg.height),float(winWidth)/float(self.pilImg.width))
			scaledWidth=int(self.pilImg.width*scale)
			scaledHeight=int(self.pilImg.height*scale)
			print("Image resize to "+str(scaledWidth)+" x "+str(scaledHeight))
			tmp=self.pilImg.resize((scaledWidth,scaledHeight),PIL.Image.ANTIALIAS)
		#	显示在窗口中央
		self.tkImg=ImageTk.PhotoImage(tmp)
		self.canvas.create_image(winWidth/2,winHeight/2,image=self.tkImg)
		pass

	#	退出函数
	def __exit(self):
		print("Exiting...")
		exit()
		pass

	#	处理函数包裹器
	def __buttonFuncWrapper(self,func,params):
		if not self.pilImg:
			return
		func(params)
		self.pilImg=Image.fromarray(params["image"])
		self.__updateShowingImage()
		pass

	#	递归搜索处理函数
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
	
	#	测试处理函数
	def __testRec(self,nowDict):
		for key in nowDict.keys():
			if isinstance(nowDict[key],dict):
				self.__testRec(nowDict[key])
			else:
				nowDict[key].process();

		pass

	#	递归创建处理函数MenuBar
	def __createMenuBarRec(self,nowDict,nowMenu):
		for key in sorted(nowDict.keys()):
			if isinstance(nowDict[key],dict):
				newMenu=Tkinter.Menu(nowMenu,tearoff=0)
				nowMenu.add_cascade(label=key,menu=newMenu)
				self.__createMenuBarRec(nowDict[key],newMenu)
			else:
				nowMenu.add_command(label=key,command=partial(self.__buttonFuncWrapper,nowDict[key].process,self.params))
		
		pass

def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	mw.createMenuBar()
	mw.draw()
	pass


if __name__ == '__main__':
	main()