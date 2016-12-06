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
		self.rootTk.geometry("640x480")
		self.rootTk.title("DIP Tools")
		self.pilImg=None
		self.tkImg=None
		self.img=None
		self.pilImgPath=[]
		self.canvas=Tkinter.Canvas(self.rootTk)
		self.canvas.pack(side=Tkinter.TOP,expand=True,fill=Tkinter.BOTH)

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
		#	弹出文件选择框
		filePath=tkFileDialog.askopenfilename(parent=self.rootTk)
		#	处理取消选择
		if not filePath:
			return None
		self.pilImgPath.append(filePath)
		#	获取窗口大小
		winWidth=self.rootTk.winfo_width()
		winHeight=self.rootTk.winfo_height()
		print("Current Windwo size:"+str(winWidth)+" x "+str(winHeight))
		#	打开图片
		self.pilImg=Image.open(filePath)
		print("Open Image:"+filePath+"  "+str(self.pilImg.size[0])+" x "+str(self.pilImg.size[1]))
		
		#	对当前窗口不能显示的图片进行缩放
		tmp=self.pilImg
		tmp.width=self.pilImg.size[0]
		tmp.height=self.pilImg.size[1]
		if  tmp.height > winHeight:
			scale=min(float(winHeight)/float(self.pilImg.height),float(winWidth)/float(self.pilImg.width))
			scaledWidth=int(self.pilImg.width*scale)
			scaledHeight=int(self.pilImg.height*scale)
			print("Image resize to "+str(scaledWidth)+" x "+str(scaledHeight))
			tmp=self.pilImg.resize((scaledWidth,scaledHeight),PIL.Image.ANTIALIAS)
		#	显示在窗口中央
		self.tkImg=ImageTk.PhotoImage(tmp)
		self.img=self.canvas.create_image(winWidth/2,winHeight/2,image=self.tkImg)
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
				nowMenu.add_command(label=key,command=partial(nowDict[key].process,self.pilImgPath))
		
		pass

def main():
	mw = MainWindow()
	mw.loadFunction(os.path.join(os.path.abspath('.'),"Functions"))
	mw.createMenuBar()
	mw.draw()
	pass



if __name__ == '__main__':
	main()