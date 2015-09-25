#coding=utf-8

import B
import os, sys
import json
import re
import subprocess

Root = os.path.abspath(os.path.split(os.path.realpath(__file__))[0]+"/")
CFG = json.loads(open(Root+"/LauncherConfig.json","r").read())


def Start(Prog):
	
	try:
		FilePath = Root+Prog["file"]
		StartPath = Root+"/python27.exe"
	except UnicodeDecodeError:
		FilePath = (Root.decode("GBK")+Prog["file"]).encode("GBK")
		StartPath = (Root.decode("GBK")+"/python27.exe").encode("GBK")
	FilePath = os.path.abspath(FilePath)
	StartPath = os.path.abspath(StartPath)
	if not os.path.isfile(FilePath):
		print FilePath
		print u"该程序文件不存在，请按Enter退出"
		raw_input()
		return 
	print u"启动中。。。。。。。"
	if not (getattr(sys, "getwindowsversion", None)):
		#not a windows
		#print FilePath
		os.system("%s \"%s\""%("python", FilePath))
	
	else:
		#on windows
		subprocess.call("\"%s\" \"%s\""%(StartPath, FilePath))
		
def choo():
	a = 0
	print u"""
	
请注意：如果重启程序多次仍然发现有奇怪的问题，请先尝试运行自动更新升级到最新版再试一次，么么哒

如果不能更新，请尝试着下载最新版喵~在下面可以选择下载最新版~
		
		——也爱你们的喵
	
	"""
	for i in CFG["prog"]:
		a += 1
		print "  %s - %s"%(a, i["name"])
	print u"请输入所需要的软件并按Enter：",
	In = raw_input()
	try:
		Start(CFG["prog"][int(In)-1])
	except IndexError:
		#raise
		print u"输入错误, 请按Enter退出"
		raw_input()
	except :
		print u"有错误发生, 按enter退出"
		raw_input()
		
if __name__ == "__main__":
	choo()
